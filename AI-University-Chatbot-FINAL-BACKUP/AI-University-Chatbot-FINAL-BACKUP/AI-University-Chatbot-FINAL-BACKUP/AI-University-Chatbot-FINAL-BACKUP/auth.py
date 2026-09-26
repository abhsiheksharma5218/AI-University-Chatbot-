import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE_NAME = "chatbot.db"


def create_users_table():

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'student',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def register_user(name, email, password, role="student"):

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    hashed_password = generate_password_hash(password)

    try:

        cursor.execute("""
            INSERT INTO users (name, email, password, role)
            VALUES (?, ?, ?, ?)
        """, (name, email, hashed_password, role))

        connection.commit()

        return True, "User registered successfully."

    except sqlite3.IntegrityError:

        return False, "Email already exists."

    finally:

        connection.close()


def login_user(email, password):

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, email, password, role
        FROM users
        WHERE email = ?
    """, (email,))

    user = cursor.fetchone()

    connection.close()

    if user and check_password_hash(user[3], password):

        return {
            "id": user[0],
            "name": user[1],
            "email": user[2],
            "role": user[4]
        }

    return None