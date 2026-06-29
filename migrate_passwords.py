import sqlite3
from werkzeug.security import generate_password_hash

DATABASE = "database/filemonitor.db"

conn = sqlite3.connect(DATABASE)
conn.row_factory = sqlite3.Row

cursor = conn.cursor()

cursor.execute("SELECT id, password FROM users")
users = cursor.fetchall()

updated = 0

for user in users:

    password = user["password"]

    # Skip already hashed passwords
    if password.startswith("scrypt:") or password.startswith("pbkdf2:"):
        continue

    hashed_password = generate_password_hash(password)

    cursor.execute(
        "UPDATE users SET password=? WHERE id=?",
        (hashed_password, user["id"])
    )

    updated += 1

conn.commit()
conn.close()

print("=" * 50)
print("Password migration completed successfully.")
print(f"Users updated: {updated}")
print("=" * 50)
