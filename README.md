# Task API — Dockerized PostgreSQL Stack

## Overview

A RESTful Task Management API built with FastAPI and PostgreSQL. The application and database run together using Docker Compose.

This project demonstrates CRUD operations, database persistence, repository-based data access, and containerization.

## Tech Stack

- Python 3.12
- FastAPI
- PostgreSQL 16
- Psycopg
- Docker
- Docker Compose
- Pydantic

## Project Structure

```text
flyrank-crud-api-db/
│
├── main.py
├── repository.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── init.sql
├── .env.example
├── .gitignore
└── README.md
```

## Architecture

The application uses a simple layered structure:

- **API Layer:** FastAPI routes handle incoming HTTP requests.
- **Repository Layer:** `repository.py` handles PostgreSQL database operations.
- **Database Layer:** PostgreSQL stores task records persistently.
- **Containerization:** Docker Compose runs the FastAPI application and PostgreSQL database together.

The API routes and response structure were kept unchanged while database access was moved into the repository module and PostgreSQL was used for persistent storage.

## Database Schema

The `tasks` table contains:

| Column | Type | Description |
|---|---|---|
| id | SERIAL PRIMARY KEY | Unique task ID |
| title | TEXT | Task title |
| done | BOOLEAN | Task completion status |

The database uses a Docker named volume named `postgres_data` to preserve data across container recreation.

## Environment Configuration

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://taskuser:taskpassword@db:5432/taskdb
```

The `.env` file is excluded from Git.

Use `.env.example` as the configuration template.

## Run the Application

Make sure Docker Desktop is running.

Start the complete application and database stack with:

```bash
docker compose up --build
```

Run in detached mode:

```bash
docker compose up -d --build
```

Check container status:

```bash
docker compose ps
```

API documentation:

http://localhost:8000/docs

Stop containers without deleting the database volume:

```bash
docker compose down
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API information |
| GET | `/health` | Health check |
| GET | `/tasks` | Retrieve all tasks |
| GET | `/tasks/{task_id}` | Retrieve one task |
| POST | `/tasks` | Create a task |
| PUT | `/tasks/{task_id}` | Update a task |
| DELETE | `/tasks/{task_id}` | Delete a task |

## Persistence Verification

Persistence was tested by:

1. Creating task records in PostgreSQL.
2. Restarting the FastAPI application container.
3. Restarting the PostgreSQL container.
4. Running `docker compose down` without deleting the volume.
5. Recreating the application and database containers using `docker compose up -d --build`.
6. Retrieving the previously created task records through the API.

The records remained available after container recreation, confirming that the PostgreSQL Docker volume preserved the database data.

## Assignment Completion

Implemented:

- PostgreSQL running inside Docker.
- Persistent named Docker volume.
- Environment-based database connection configuration.
- `.env` excluded from Git and `.env.example` provided.
- SQL initialization script.
- PostgreSQL repository module.
- FastAPI application container.
- Docker Compose configuration for the complete stack.
- CRUD operations and persistence verification.
