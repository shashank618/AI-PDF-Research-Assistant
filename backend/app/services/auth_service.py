
from app.database import get_db_connection
from app.services.security import hash_password, verify_password


def register_user(username: str, email: str, password: str):
    connection = get_db_connection()

    try:
        existing_user = connection.execute(
            """
            SELECT id FROM users
            WHERE username = ? OR email = ?
            """,
            (username, email)
        ).fetchone()

        if existing_user:
            raise ValueError("Username or email already registered")

        hashed_password = hash_password(password)

        cursor = connection.execute(
            """
            INSERT INTO users (username, email, hashed_password)
            VALUES (?, ?, ?)
            """,
            (username, email, hashed_password)
        )

        connection.commit()

        return {
            "id": cursor.lastrowid,
            "username": username,
            "email": email,
            "message": "User registered successfully"
        }

    finally:
        connection.close()


def authenticate_user(email: str, password: str):
    connection = get_db_connection()

    try:
        user = connection.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        ).fetchone()

        if not user:
            return None

        if not verify_password(password, user["hashed_password"]):
            return None

        return {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"]
        }

    finally:
        connection.close()
