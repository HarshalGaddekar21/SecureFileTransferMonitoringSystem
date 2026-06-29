import sqlite3

DATABASE = "database/filemonitor.db"


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def get_analytics():

    conn = get_connection()
    cursor = conn.cursor()

    analytics = {}

# ==========================================
# Event Distribution Chart
# ==========================================

def get_event_distribution():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT event_type, COUNT(*) as total
        FROM file_events
        GROUP BY event_type
    """)

    rows = cursor.fetchall()

    conn.close()

    labels = []
    values = []

    for row in rows:
        labels.append(row["event_type"])
        values.append(row["total"])

    return {
        "labels": labels,
        "values": values
    }


# ==========================================
# Top Active Users
# ==========================================

def get_top_users_chart():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT username,
               COUNT(*) AS total
        FROM file_events
        GROUP BY username
        ORDER BY total DESC
        LIMIT 5
    """)

    rows = cursor.fetchall()

    conn.close()

    labels = []
    values = []

    for row in rows:

        labels.append(row["username"])
        values.append(row["total"])

    return {
        "labels": labels,
        "values": values
    }


    # ----------------------------------------
    # Most Active User
    # ----------------------------------------
    cursor.execute("""
        SELECT username, COUNT(*) AS total
        FROM file_events
        GROUP BY username
        ORDER BY total DESC
        LIMIT 1
    """)

    row = cursor.fetchone()

    analytics["top_user"] = row["username"] if row else "N/A"

    # ----------------------------------------
    # Most Accessed File
    # ----------------------------------------
    cursor.execute("""
        SELECT file_name, COUNT(*) AS total
        FROM file_events
        GROUP BY file_name
        ORDER BY total DESC
        LIMIT 1
    """)

    row = cursor.fetchone()

    analytics["top_file"] = row["file_name"] if row else "N/A"

    # ----------------------------------------
    # Sensitive Files
    # ----------------------------------------
    cursor.execute("""
        SELECT COUNT(*)
        FROM file_events
        WHERE sensitive='Yes'
    """)

    analytics["sensitive"] = cursor.fetchone()[0]

    # ----------------------------------------
    # Unauthorized Access
    # ----------------------------------------
    cursor.execute("""
        SELECT COUNT(*)
        FROM file_events
        WHERE authorized='No'
    """)

    analytics["unauthorized"] = cursor.fetchone()[0]

    conn.close()

    return analytics
