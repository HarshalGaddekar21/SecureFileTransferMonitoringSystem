import sqlite3

DATABASE = "database/filemonitor.db"


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def get_alerts():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM file_events
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    alerts = []

    for row in rows:

        severity = "Info"
        message = "Normal File Activity"

        # -------------------------------
        # Unauthorized Access
        # -------------------------------
        if row["authorized"] == "No":

            severity = "Critical"
            message = "Unauthorized File Access"

        # -------------------------------
        # Integrity Failure
        # -------------------------------
        elif row["integrity_status"] != "Verified":

            severity = "Critical"
            message = "Integrity Verification Failed"

        # -------------------------------
        # Sensitive File
        # -------------------------------
        elif row["sensitive"] == "Yes":

            severity = "Warning"
            message = "Sensitive File Activity"

        alerts.append({

            "timestamp": row["timestamp"],

            "username": row["username"],

            "event": row["event_type"],

            "file": row["file_name"],

            "severity": severity,

            "message": message

        })

    conn.close()

    return alerts
