# HealthBook — Hospital Appointment & Management System

A web-based hospital appointment booking and clinic management portal built with **Python (Flask)**, **SQLite**, and **Bootstrap 5**. Developed as a SIWES software engineering project.

## Features
* **Patient Portal:** Register, log in, browse specialists across clinical departments, request consultation dates/times, and track appointment statuses (`Pending`, `Approved`, `Cancelled`).
* **Admin Dashboard:** View all patient booking requests in real time, approve or cancel appointments, and add or remove hospital specialists.
* **Pre-Populated Directory:** Includes 20 medical consultants across Cardiology, Neurology, Pediatrics, Orthopedics, Mental Health & Therapy, Physiotherapy, General Medicine, Obstetrics & Gynecology, Surgery, Ophthalmology, ENT, and Dermatology.

## Tech Stack
* **Backend:** Python 3, Flask, SQLite3
* **Frontend:** HTML5, Jinja2, Bootstrap 5.3, Custom CSS

## How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com
   cd healthbook-hospital-system
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   # Windows (PowerShell):
   .venv\Scripts\Activate.ps1
   # macOS / Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the application:**
   ```bash
   python app.py
   ```
   Open your browser and visit `http://127.0.0.1:5000`.

## Demo Credentials
* **Admin Username:** `admin`
* **Admin Password:** `adminpass`
