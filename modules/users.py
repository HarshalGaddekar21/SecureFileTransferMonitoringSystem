from werkzeug.security import generate_password_hash

import sqlite3

DATABASE = "database/filemonitor.db"


# ----------------------------------------
# Get all users
# ----------------------------------------

def get_all_users():

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM users
        ORDER BY id
    """)

    users = cursor.fetchall()

    conn.close()

    return users


# ----------------------------------------
# Add new user
# ----------------------------------------

def add_user(username,
             password,
             full_name,
             role,
             status="Active"):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    hashed_password = generate_password_hash(password)

    cursor.execute("""

        INSERT INTO users(

            username,

            password,

            full_name,

            role,

            status

        )

        VALUES(?,?,?,?,?)

    """, (

        username,

        hashed_password,

        full_name,

        role,

        status

    ))

    conn.commit()

    conn.close()


# ----------------------------------------
# Get one user by ID
# ----------------------------------------

def get_user(user_id):

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM users
        WHERE id=?
    """, (user_id,))

    user = cursor.fetchone()

    conn.close()

    return user


# ----------------------------------------
# Update user
# ----------------------------------------

def update_user(user_id,
                username,
                password,
                full_name,
                role,
                status):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    hashed_password = generate_password_hash(password)

    cursor.execute("""

        UPDATE users

        SET

            username=?,

            password=?,

            full_name=?,

            role=?,

            status=?

        WHERE id=?

    """, (

        username,

        hashed_password,

        full_name,

        role,

        status,

        user_id

    ))

    conn.commit()

    conn.close()


# ----------------------------------------
# Delete User
# ----------------------------------------

def delete_user(user_id):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM users WHERE id=?",
        (user_id,)
    )

    conn.commit()
    conn.close()


# ----------------------------------------
# Count Administrators
# ----------------------------------------

def count_admins():

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""

        SELECT COUNT(*)

        FROM users

        WHERE role='Administrator'

    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total


# ----------------------------------------
# Get User By Username
# ----------------------------------------

def get_user_by_username(username):

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""

        SELECT *

        FROM users

        WHERE username=?

    """, (username,))

    user = cursor.fetchone()

    conn.close()

    return user

# ----------------------------------------
# Change Password
# ----------------------------------------

def change_password(user_id, new_password):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""

        UPDATE users

        SET password=?

        WHERE id=?

    """, (

        generate_password_hash(new_password),

        user_id

    ))

    conn.commit()

    conn.close()




