from werkzeug.security import check_password_hash

import sqlite3

DATABASE = "database/filemonitor.db"


def authenticate(username, password):

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM users
        WHERE username=?
          AND status='Active'
    """, (username,))

    user = cursor.fetchone()

    conn.close()

    if user is None:
        return None

    if check_password_hash(user["password"], password):
        return user

    return None
