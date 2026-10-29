
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

import repository

app = FastAPI()


class TaskCreate(BaseModel):
    title: str = Field(min_length=1)


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1)
    done: bool | None = None


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
    return repository.get_all_tasks()


@app.get("/tasks/{task_id}", description="Return one task by ID.")
def get_task(task_id: int):
    task = repository.get_task_by_id(task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    return task


@app.post(
    "/tasks",
    status_code=status.HTTP_201_CREATED,
    description="Create a new task."
)
def create_task(task_data: TaskCreate):
    return repository.create_task(task_data.title)


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

    task = repository.update_task(task_id, updates)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    return task


@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete a task by ID."
)
def delete_task(task_id: int):
    deleted = repository.delete_task(task_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    return
