from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import psycopg
import os

load_dotenv(override=True)
app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")


class TaskCreate(BaseModel):
    title: str = Field(min_length=1)


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1)
    done: bool | None = None


def get_connection():
    return psycopg.connect(DATABASE_URL)


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


@app.get("/", description="Show basic information about the Task API.")
def home():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health", description="Check whether the API is running.")
def health():
    return {"status": "ok"}


@app.get("/tasks", description="Return all tasks.")
def get_tasks():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, title, done FROM tasks ORDER BY id"
            )
            rows = cursor.fetchall()

    return [
        {
            "id": row[0],
            "title": row[1],
            "done": row[2]
        }
        for row in rows
    ]


@app.get("/tasks/{task_id}", description="Return one task by ID.")
def get_task(task_id: int):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, title, done FROM tasks WHERE id = %s",
                (task_id,)
            )
            row = cursor.fetchone()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    return {
        "id": row[0],
        "title": row[1],
        "done": row[2]
    }


@app.post(
    "/tasks",
    status_code=status.HTTP_201_CREATED,
    description="Create a new task."
)
def create_task(task_data: TaskCreate):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO tasks (title, done)
                VALUES (%s, %s)
                RETURNING id, title, done
                """,
                (task_data.title, False)
            )
            row = cursor.fetchone()

    return {
        "id": row[0],
        "title": row[1],
        "done": row[2]
    }


@app.put("/tasks/{task_id}", description="Update a task by ID.")
def update_task(task_id: int, task_data: TaskUpdate):
    updates = task_data.model_dump(exclude_unset=True)

    if not updates:
        raise HTTPException(
            status_code=400,
            detail="Update body cannot be empty"
        )

    if "title" in updates and updates["title"] is None:
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )

    if "done" in updates and updates["done"] is None:
        raise HTTPException(
            status_code=400,
            detail="Done must be a boolean"
        )

    with get_connection() as connection:
        with connection.cursor() as cursor:

            cursor.execute(
                "SELECT id FROM tasks WHERE id = %s",
                (task_id,)
            )

            if cursor.fetchone() is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"Task {task_id} not found"
                )

            if "title" in updates and "done" in updates:
                cursor.execute(
                    """
                    UPDATE tasks
                    SET title = %s, done = %s
                    WHERE id = %s
                    RETURNING id, title, done
                    """,
                    (
                        updates["title"],
                        updates["done"],
                        task_id
                    )
                )

            elif "title" in updates:
                cursor.execute(
                    """
                    UPDATE tasks
                    SET title = %s
                    WHERE id = %s
                    RETURNING id, title, done
                    """,
                    (
                        updates["title"],
                        task_id
                    )
                )

            else:
                cursor.execute(
                    """
                    UPDATE tasks
                    SET done = %s
                    WHERE id = %s
                    RETURNING id, title, done
                    """,
                    (
                        updates["done"],
                        task_id
                    )
                )

            row = cursor.fetchone()

    return {
        "id": row[0],
        "title": row[1],
        "done": row[2]
    }


@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete a task by ID."
)
def delete_task(task_id: int):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM tasks WHERE id = %s RETURNING id",
                (task_id,)
            )

            row = cursor.fetchone()

            if row is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"Task {task_id} not found"
                )

    return