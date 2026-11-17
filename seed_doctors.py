import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "hospital.db")

DOCTORS = [
    # Cardiology
    (
        "Adebayo Ogunlesi",
        "Cardiology",
        "Consultant Cardiologist with 14 years of experience in hypertension management, heart failure care, echocardiography, and preventive cardiovascular screening.",
        "Mon,Wed,Fri",
    ),
    (
        "Ngozi Okafor-Eze",
        "Cardiology",
        "Interventional Cardiologist specializing in cardiac arrhythmias, ECG diagnostics, lipid disorders, and post-cardiac event rehabilitation.",
        "Tue,Thu",
    ),
    # Neurology
    (
        "Ibrahim Danjuma",
        "Neurology",
        "Consultant Neurologist focused on stroke recovery, chronic migraine treatment, epilepsy management, and neuromuscular disorders.",
        "Mon,Wed",
    ),
    (
        "Funmilayo Adeyemi",
        "Neurology",
        "Clinical Neurologist specializing in neurodegenerative conditions, peripheral neuropathy, sleep disorders, and EEG evaluations.",
        "Tue,Thu,Fri",
    ),
    # Pediatrics
    (
        "Chidinma Nwosu",
        "Pediatrics",
        "Consultant Pediatrician dedicated to infant wellness, childhood immunization schedules, developmental monitoring, and acute pediatric care.",
        "Mon,Tue,Thu,Fri",
    ),
    (
        "Tunde Bakare",
        "Pediatrics",
        "Pediatric Specialist with expertise in childhood asthma, nutritional counseling, neonatal follow-ups, and infectious disease prevention.",
        "Wed,Sat",
    ),
    # Orthopedics
    (
        "Emeka Obi-Nwankwo",
        "Orthopedics",
        "Consultant Orthopedic Surgeon specializing in fracture management, joint replacement consultations, arthritis care, and sports injuries.",
        "Mon,Thu",
    ),
    (
        "Zainab Abubakar",
        "Orthopedics",
        "Orthopedic & Trauma Specialist focusing on spine health, ligament reconstruction, back pain therapy, and post-surgical mobility recovery.",
        "Tue,Fri",
    ),
    # Psychiatry & Mental Health Therapy
    (
        "Bimpe Akinwumi",
        "Mental Health & Therapy",
        "Clinical Psychologist & Licensed Therapist offering evidence-based cognitive behavioral therapy (CBT), stress management, trauma recovery, and counseling.",
        "Mon,Wed,Fri",
    ),
    (
        "Halima Abdullahi",
        "Psychiatry",
        "Consultant Psychiatrist specializing in mood disorders, anxiety management, sleep therapy, and holistic mental health evaluations.",
        "Tue,Thu",
    ),
    # Physiotherapy & Rehabilitation
    (
        "Kayode Adeniyi",
        "Physiotherapy",
        "Senior Physiotherapist & Rehabilitation Specialist focused on post-operative recovery, stroke mobility therapy, sports injury rehab, and chronic back pain.",
        "Mon,Tue,Thu,Sat",
    ),
    # General & Family Medicine
    (
        "Oluwaseun Babalola",
        "General Medicine",
        "Senior Medical Officer providing comprehensive primary care, routine health checkups, diabetes management, and chronic illness monitoring.",
        "Mon,Tue,Wed,Thu,Fri",
    ),
    (
        "Hauwa Suleiman",
        "Family Medicine",
        "Consultant Family Physician focused on holistic preventive medicine, malaria and typhoid care, lifestyle counseling, and family wellness.",
        "Tue,Thu,Sat",
    ),
    # Obstetrics & Gynecology
    (
        "Kemi Alabi-Balogun",
        "Obstetrics & Gynecology",
        "Consultant Obstetrician & Gynecologist specializing in antenatal care, high-risk pregnancy monitoring, maternal wellness, and fertility consultations.",
        "Mon,Wed,Fri",
    ),
    (
        "Amaka Uche-Chukwu",
        "Obstetrics & Gynecology",
        "Women's Health Specialist experienced in reproductive health screenings, fibroid management, family planning, and postnatal care.",
        "Tue,Thu",
    ),
    # Surgery & Emergency Care
    (
        "Segun Fashola",
        "General Surgery",
        "Consultant General Surgeon skilled in minimally invasive laparoscopic procedures, hernia repairs, appendectomies, and surgical consultations.",
        "Mon,Wed",
    ),
    (
        "Yakubu Musa",
        "Emergency Medicine",
        "Emergency & Trauma Physician leading rapid triage, acute medical stabilization, wound care, and urgent inpatient referrals.",
        "Mon,Tue,Wed,Thu,Fri,Sat",
    ),
    # Ophthalmology & ENT
    (
        "Bukola Onabanjo",
        "Ophthalmology",
        "Consultant Ophthalmologist specializing in comprehensive eye exams, glaucoma screening, cataract evaluations, and vision correction.",
        "Tue,Thu",
    ),
    (
        "Nnamdi Azikiwe-Ojo",
        "ENT (Ear, Nose & Throat)",
        "Otolaryngologist treating sinusitis, hearing loss, tonsillitis, allergic rhinitis, and voice or throat conditions.",
        "Wed,Fri",
    ),
    # Dermatology & Diagnostics
    (
        "Folake Soyinka",
        "Dermatology",
        "Consultant Dermatologist specializing in clinical skin conditions, eczema, acne therapy, fungal infections, and allergic skin reactions.",
        "Mon,Thu",
    ),
]


def seed():
    if not os.path.exists(DB_PATH):
        print(
            "Error: hospital.db not found. Run 'python app.py' once first to create the database."
        )
        return

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Clear old sample doctors so there are no duplicates or broken bios
    cur.execute("DELETE FROM doctors")

    cur.executemany(
        "INSERT INTO doctors (name, department, bio, available_days) VALUES (?, ?, ?, ?)",
        DOCTORS,
    )
    conn.commit()
    conn.close()
    print(f"Successfully added {len(DOCTORS)} medical practitioners to hospital.db!")


if __name__ == "__main__":
    seed()
