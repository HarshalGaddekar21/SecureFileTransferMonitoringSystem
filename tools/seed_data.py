import sqlite3
import random
import hashlib
from datetime import datetime, timedelta

# ============================================
# Database Configuration
# ============================================

DATABASE = "database/filemonitor.db"

# ============================================
# Connect to Database
# ============================================

conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

# ============================================
# Sample Data
# ============================================

users = [
    "kali",
    "root",
    "admin",
    "harshal",
    "developer",
    "guest"
]

processes = [
    "python3",
    "nano",
    "vim",
    "cp",
    "mv",
    "rm",
    "gedit",
    "code"
]

files = [
    "salary.xlsx",
    "employees.csv",
    "config.json",
    "report.pdf",
    "database.db",
    "project.py",
    "backup.zip",
    "passwords.txt",
    "invoice.docx",
    "notes.txt",
    "presentation.pptx",
    "accounts.xlsx",
    "photo.jpg",
    "archive.tar.gz",
    "server.log"
]

folders = [
    "/home/kali/Documents/",
    "/home/kali/Desktop/",
    "/home/kali/Downloads/",
    "/home/kali/Projects/",
    "/home/kali/SecureFiles/",
    "/etc/",
    "/var/log/",
    "/tmp/"
]

event_types = [
    "Created",
    "Modified",
    "Deleted",
    "Moved"
]

integrity_status = [
    "Verified",
    "Modified"
]

sensitive_status = [
    "Yes",
    "No"
]

authorization_status = [
    "Yes",
    "No"
]

event_status = [
    "Success",
    "Warning",
    "Blocked"
]

# ============================================
# Generate Random SHA256 Hash
# ============================================

def random_hash():

    random_text = str(random.random())

    return hashlib.sha256(random_text.encode()).hexdigest()

# ============================================
# Generate Random Timestamp
# ============================================

def random_timestamp():

    days = random.randint(0, 30)

    seconds = random.randint(0, 86400)

    dt = datetime.now() - timedelta(days=days, seconds=seconds)

    return dt.strftime("%Y-%m-%d %H:%M:%S")

# ============================================
# Generate Demo Records
# ============================================

records = []

TOTAL_RECORDS = 100

for i in range(TOTAL_RECORDS):

    event = random.choice(event_types)

    file_name = random.choice(files)

    source_folder = random.choice(folders)

    source_path = source_folder + file_name

    # If event is "Moved", choose a different destination
    if event == "Moved":

        destination_folder = random.choice(folders)

        while destination_folder == source_folder:

            destination_folder = random.choice(folders)

        destination_path = destination_folder + file_name

    else:

        destination_path = ""

    username = random.choice(users)

    process_name = random.choice(processes)

    hash_before = random_hash()

    # Modified files usually have different hashes
    if event == "Modified":

        hash_after = random_hash()

        integrity = "Modified"

    else:

        hash_after = hash_before

        integrity = "Verified"

    sensitive = random.choices(

        ["Yes", "No"],

        weights=[25, 75]

    )[0]

    authorized = random.choices(

        ["Yes", "No"],

        weights=[80, 20]

    )[0]

    # Status depends on authorization
    if authorized == "No":

        status = "Blocked"

    else:

        status = random.choice(

            ["Success", "Warning"]

        )

    timestamp = random_timestamp()

    records.append(

        (

            timestamp,

            event,

            file_name,

            source_path,

            destination_path,

            username,

            process_name,

            hash_before,

            hash_after,

            integrity,

            sensitive,

            authorized,

            status

        )

    )

# ============================================
# Optional: Clear Existing Demo Data
# ============================================

print("Removing existing records...")

cursor.execute("DELETE FROM file_events")

conn.commit()

# ============================================
# Insert Generated Records
# ============================================

print(f"Inserting {TOTAL_RECORDS} demo records...")

cursor.executemany(
    """
    INSERT INTO file_events
    (
        timestamp,
        event_type,
        file_name,
        source_path,
        destination_path,
        username,
        process_name,
        hash_before,
        hash_after,
        integrity_status,
        sensitive,
        authorized,
        status
    )
    VALUES
    (
        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
    )
    """,
    records
)

conn.commit()

print("===================================")
print("Database seeded successfully!")
print(f"Total records inserted: {TOTAL_RECORDS}")
print("===================================")

conn.close()
