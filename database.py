import sqlite3
import os

# ==========================================
# Secure File Transfer Monitoring System
# Database Initialization
# ==========================================

os.makedirs("database", exist_ok=True)

conn = sqlite3.connect("database/filemonitor.db")
cursor = conn.cursor()

# ======================================================
# File Events Table
# ======================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS file_events(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    timestamp TEXT,

    event_type TEXT,

    file_name TEXT,

    source_path TEXT,

    destination_path TEXT,

    username TEXT,

    process_name TEXT,

    hash_before TEXT,

    hash_after TEXT,

    integrity_status TEXT,

    sensitive TEXT,

    authorized TEXT,

    status TEXT
)
""")

# ======================================================
# Users Table
# ======================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT UNIQUE NOT NULL,

    password TEXT NOT NULL,

    full_name TEXT,

    role TEXT NOT NULL,

    status TEXT DEFAULT 'Active',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")



# ---------------------------------------
# Audit Logs
# ---------------------------------------

cursor.execute("""

CREATE TABLE IF NOT EXISTS audit_logs(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    timestamp TEXT,

    username TEXT,

    action TEXT,

    details TEXT

)

""")




# ======================================================
# Default Administrator
# ======================================================

cursor.execute("""
SELECT COUNT(*)
FROM users
WHERE username='admin'
""")

exists = cursor.fetchone()[0]

if exists == 0:

    cursor.execute("""
    INSERT INTO users
    (
        username,
        password,
        full_name,
        role,
        status
    )
    VALUES
    (
        'admin',
        'admin123',
        'System Administrator',
        'Administrator',
        'Active'
    )
    """)

conn.commit()
conn.close()

print("Database initialized successfully.")
print("Default Administrator")
print("Username : admin")
print("Password : admin123")
