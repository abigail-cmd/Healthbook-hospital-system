from flask import Flask, render_template, request, redirect, url_for, flash, session, g
import sqlite3
import os
from datetime import datetime


# Default admin:
# username: admin
# password: adminpass
# 
# 
# (Use admin to add doctors and approve appointments.)

# === CONFIG ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "hospital.db")

app = Flask(__name__)
app.secret_key = "replace_this_with_a_strong_secret"  # change for production

# === DB UTIL ===
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop("db", None)
    
    if db is not None:
        db.close()

def init_db():
    db = sqlite3.connect(DB_PATH)
    cur = db.cursor()
    # Users: simple users table, role = 'admin' or 'patient'
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'patient',
        full_name TEXT
    );

    CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        department TEXT NOT NULL,
        bio TEXT,
        available_days TEXT  -- comma separated like "Mon,Tue,Wed"
    );

    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER NOT NULL,
        doctor_id INTEGER NOT NULL,
        appointment_date TEXT NOT NULL, -- ISO date 'YYYY-MM-DD'
        appointment_time TEXT NOT NULL, -- 'HH:MM'
        reason TEXT,
        status TEXT NOT NULL DEFAULT 'Pending', -- Pending, Approved, Cancelled
        created_at TEXT,
        FOREIGN KEY(patient_id) REFERENCES users(id),
        FOREIGN KEY(doctor_id) REFERENCES doctors(id)
    );
    """)
    # Create a default admin user (for demo)
    try:
        cur.execute("INSERT INTO users (username, password, role, full_name) VALUES (?, ?, ?, ?)",
                    ("admin", "adminpass", "admin", "Administrator"))
    except sqlite3.IntegrityError:
        pass
    db.commit()
    db.close()

# Initialize DB if missing
if not os.path.exists(DB_PATH):
    init_db()

# === HELPERS ===
def current_user():
    uid = session.get("user_id")
    if not uid:
        return None
    db = get_db()
    return db.execute("SELECT * FROM users WHERE id = ?", (uid,)).fetchone()

def login_required(f):
    from functools import wraps
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please log in first", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def wrapper(*args, **kwargs):
        user = current_user()
        if not user or user["role"] != "admin":
            flash("Admin access required", "danger")
            return redirect(url_for("index"))
        return f(*args, **kwargs)
    return wrapper

# === ROUTES ===

@app.route("/")
def index():
    db = get_db()
    doctors = db.execute("SELECT * FROM doctors ORDER BY department, name").fetchall()
    return render_template("index.html", doctors=doctors, user=current_user())

# Registration (patient)
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()
        full_name = request.form.get("full_name") or ""
        if not username or not password:
            flash("username and password are required", "warning")
            return redirect(url_for("register"))
        db = get_db()
        try:
            db.execute("INSERT INTO users (username, password, role, full_name) VALUES (?, ?, 'patient', ?)",
                       (username, password, full_name))
            db.commit()
            flash("Registration successful. Log in now.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Username already taken", "danger")
            return redirect(url_for("register"))
    return render_template("register.html", user=current_user())

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ? AND password = ?",
                          (username, password)).fetchone()
        if user:
            session["user_id"] = user["id"]
            flash("Logged in successfully", "success")
            return redirect(url_for("index"))
        else:
            flash("Invalid credentials", "danger")
            return redirect(url_for("login"))
    return render_template("login.html", user=current_user())

# Logout
@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out", "info")
    return redirect(url_for("index"))

# View doctor list and book
@app.route("/doctors")
def doctors():
    db = get_db()
    doctors = db.execute("SELECT * FROM doctors ORDER BY department, name").fetchall()
    return render_template("doctors.html", doctors=doctors, user=current_user())

# Book appointment (patient)
@app.route("/book/<int:doctor_id>", methods=["GET", "POST"])
@login_required
def book(doctor_id):
    db = get_db()
    doctor = db.execute("SELECT * FROM doctors WHERE id = ?", (doctor_id,)).fetchone()
    if not doctor:
        flash("Doctor not found", "danger")
        return redirect(url_for("doctors"))

    if request.method == "POST":
        date = request.form["date"]  # expected YYYY-MM-DD
        time = request.form["time"]  # expected HH:MM
        reason = request.form.get("reason", "")
        # basic validation
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            flash("Invalid date format", "warning")
            return redirect(url_for("book", doctor_id=doctor_id))
        patient = current_user()
        db.execute("""INSERT INTO appointments
                      (patient_id, doctor_id, appointment_date, appointment_time, reason, status, created_at)
                      VALUES (?, ?, ?, ?, ?, 'Pending', ?)""",
                   (patient["id"], doctor_id, date, time, reason, datetime.utcnow().isoformat()))
        db.commit()
        flash("Appointment requested — waiting for approval", "success")
        return redirect(url_for("my_appointments"))
    return render_template("book.html", doctor=doctor, user=current_user())

# Patient's own appointments
@app.route("/my-appointments")
@login_required
def my_appointments():
    user = current_user()
    db = get_db()
    rows = db.execute("""SELECT a.*, d.name as doctor_name, d.department
                         FROM appointments a JOIN doctors d ON a.doctor_id=d.id
                         WHERE a.patient_id = ?
                         ORDER BY a.appointment_date DESC, a.appointment_time DESC""",
                      (user["id"],)).fetchall()
    return render_template("my_appointments.html", appointments=rows, user=user)

# Admin dashboard
@app.route("/admin")
@admin_required
def admin_dashboard():
    db = get_db()
    appointments = db.execute("""SELECT a.*, u.full_name as patient_name, d.name as doctor_name
                                 FROM appointments a
                                 JOIN users u ON a.patient_id=u.id
                                 JOIN doctors d ON a.doctor_id=d.id
                                 ORDER BY a.status, a.appointment_date DESC""").fetchall()
    return render_template("dashboard.html", appointments=appointments, user=current_user())

# Admin add doctor
@app.route("/admin/doctors", methods=["GET", "POST"])
@admin_required
def manage_doctors():
    db = get_db()
    if request.method == "POST":
        name = request.form["name"].strip()
        dept = request.form["department"].strip()
        bio = request.form.get("bio", "")
        days = request.form.get("available_days", "")
        if not name or not dept:
            flash("Name and department required", "warning")
            return redirect(url_for("manage_doctors"))
        db.execute("INSERT INTO doctors (name, department, bio, available_days) VALUES (?, ?, ?, ?)",
                   (name, dept, bio, days))
        db.commit()
        flash("Doctor added", "success")
        return redirect(url_for("manage_doctors"))
    doctors = db.execute("SELECT * FROM doctors ORDER BY department, name").fetchall()
    return render_template("manage_doctors.html", doctors=doctors, user=current_user())

# Admin approve / cancel appointment
@app.route("/admin/appointment/<int:appt_id>/action/<action>")
@admin_required
def appointment_action(appt_id, action):
    db = get_db()
    if action not in ("approve", "cancel"):
        flash("Invalid action", "danger")
        return redirect(url_for("admin_dashboard"))
    new_status = "Approved" if action == "approve" else "Cancelled"
    db.execute("UPDATE appointments SET status = ? WHERE id = ?", (new_status, appt_id))
    db.commit()
    flash(f"Appointment {new_status}", "success")
    return redirect(url_for("admin_dashboard"))

# Simple edit/delete for admin doctors (optional)
@app.route("/admin/doctor/<int:id>/delete")
@admin_required
def delete_doctor(id):
    db = get_db()
    db.execute("DELETE FROM doctors WHERE id = ?", (id,))
    db.commit()
    flash("Doctor removed", "info")
    return redirect(url_for("manage_doctors"))

# Run
if __name__ == "__main__":
    app.run(debug=True)
