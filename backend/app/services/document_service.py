
from app.database import get_db_connection


def save_document(document_id: str, user_id: int, filename: str):
    connection = get_db_connection()

    try:
        connection.execute(
            """
            INSERT INTO documents (document_id, user_id, filename)
            VALUES (?, ?, ?)
            """,
            (document_id, user_id, filename)
        )

        connection.commit()

    finally:
        connection.close()


def verify_document_owner(document_id: str, user_id: int):
    connection = get_db_connection()

    try:
        document = connection.execute(
            """
            SELECT document_id
            FROM documents
            WHERE document_id = ? AND user_id = ?
            """,
            (document_id, user_id)
        ).fetchone()

        return document is not None

    finally:
        connection.close()
