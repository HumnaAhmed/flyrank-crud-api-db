
import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    return psycopg.connect(DATABASE_URL)


def get_all_tasks():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, title, done FROM tasks ORDER BY id"
            )
            rows = cursor.fetchall()

    return [
        {"id": row[0], "title": row[1], "done": row[2]}
        for row in rows
    ]


def get_task_by_id(task_id):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, title, done FROM tasks WHERE id = %s",
                (task_id,)
            )
            row = cursor.fetchone()

    if row is None:
        return None

    return {"id": row[0], "title": row[1], "done": row[2]}


def create_task(title):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO tasks (title, done)
                VALUES (%s, %s)
                RETURNING id, title, done
                """,
                (title, False)
            )
            row = cursor.fetchone()

    return {"id": row[0], "title": row[1], "done": row[2]}


def update_task(task_id, updates):
    fields = []
    values = []

    for field in ("title", "done"):
        if field in updates:
            fields.append(f"{field} = %s")
            values.append(updates[field])

    if not fields:
        return None

    values.append(task_id)

    query = f"""
        UPDATE tasks
        SET {", ".join(fields)}
        WHERE id = %s
        RETURNING id, title, done
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, tuple(values))
            row = cursor.fetchone()

    if row is None:
        return None

    return {"id": row[0], "title": row[1], "done": row[2]}


def delete_task(task_id):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM tasks WHERE id = %s RETURNING id",
                (task_id,)
            )
            row = cursor.fetchone()

    return row is not None
