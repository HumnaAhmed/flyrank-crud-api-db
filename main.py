from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import sqlite3
from pathlib import Path

app = FastAPI()

DB_FILE = Path(__file__).parent / "tasks.db"


class TaskCreate(BaseModel):
    title: str = Field(min_length=1)


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1)
    done: bool | None = None


def get_connection():
    connection = sqlite3.connect(DB_FILE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_connection()

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT 0
        )
        """
    )

    task_count = connection.execute(
        "SELECT COUNT(*) FROM tasks"
    ).fetchone()[0]

    if task_count == 0:
        connection.executemany(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            [
                ("Learn FastAPI", 0),
                ("Build a CRUD API", 0),
                ("Write the README", 1),
            ],
        )

    connection.commit()
    connection.close()


@app.on_event("startup")
def startup():
    initialize_database()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=400,
        content={"error": "Invalid request body"}
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request,
    exc: HTTPException
):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )


@app.get(
    "/",
    description="Show basic information about the Task API."
)
def home():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get(
    "/health",
    description="Check whether the API is running."
)
def health():
    return {
        "status": "ok"
    }


@app.get(
    "/tasks",
    description="Return all tasks."
)
def get_tasks():
    connection = get_connection()

    rows = connection.execute(
        "SELECT id, title, done FROM tasks ORDER BY id"
    ).fetchall()

    connection.close()

    return [
        {
            "id": row["id"],
            "title": row["title"],
            "done": bool(row["done"])
        }
        for row in rows
    ]


@app.get(
    "/tasks/{task_id}",
    description="Return one task by ID."
)
def get_task(task_id: int):
    connection = get_connection()

    row = connection.execute(
        "SELECT id, title, done FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    connection.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    return {
        "id": row["id"],
        "title": row["title"],
        "done": bool(row["done"])
    }


@app.post(
    "/tasks",
    status_code=status.HTTP_201_CREATED,
    description="Create a new task."
)
def create_task(task_data: TaskCreate):
    connection = get_connection()

    cursor = connection.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        (task_data.title, 0)
    )

    connection.commit()

    new_id = cursor.lastrowid

    row = connection.execute(
        "SELECT id, title, done FROM tasks WHERE id = ?",
        (new_id,)
    ).fetchone()

    connection.close()

    return {
        "id": row["id"],
        "title": row["title"],
        "done": bool(row["done"])
    }


@app.put(
    "/tasks/{task_id}",
    description="Update a task by ID."
)
def update_task(task_id: int, task_data: TaskUpdate):
    connection = get_connection()

    row = connection.execute(
        "SELECT id, title, done FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    if row is None:
        connection.close()

        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    updates = task_data.model_dump(
        exclude_unset=True
    )

    if not updates:
        connection.close()

        raise HTTPException(
            status_code=400,
            detail="Update body cannot be empty"
        )

    if "title" in updates and updates["title"] is None:
        connection.close()

        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )

    if "done" in updates and updates["done"] is None:
        connection.close()

        raise HTTPException(
            status_code=400,
            detail="Done must be a boolean"
        )

    if "title" in updates:
        connection.execute(
            "UPDATE tasks SET title = ? WHERE id = ?",
            (updates["title"], task_id)
        )

    if "done" in updates:
        connection.execute(
            "UPDATE tasks SET done = ? WHERE id = ?",
            (int(updates["done"]), task_id)
        )

    connection.commit()

    updated_row = connection.execute(
        "SELECT id, title, done FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    connection.close()

    return {
        "id": updated_row["id"],
        "title": updated_row["title"],
        "done": bool(updated_row["done"])
    }


@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete a task by ID."
)
def delete_task(task_id: int):
    connection = get_connection()

    row = connection.execute(
        "SELECT id FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    if row is None:
        connection.close()

        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    connection.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    connection.commit()
    connection.close()

    return