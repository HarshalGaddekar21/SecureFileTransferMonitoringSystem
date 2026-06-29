import sqlite3
from datetime import datetime

DATABASE = "database/filemonitor.db"


def log_action(username, action, details=""):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO audit_logs(

            timestamp,

            username,

            action,

            details

        )

        VALUES(?,?,?,?)

    """, (

        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

        username,

        action,

        details

    ))

    conn.commit()

    conn.close()


def get_audit_logs():

    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""

        SELECT *

        FROM audit_logs

        ORDER BY id DESC

    """)

    logs = cursor.fetchall()

    conn.close()

    return logs
