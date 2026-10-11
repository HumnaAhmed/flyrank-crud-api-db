# Task API — SQLite Database

A beginner-friendly CRUD API built with FastAPI and SQLite.

This project is the database version of the Task API from the previous assignment. The API endpoints remain the same, but tasks are now stored permanently in a SQLite database instead of an in-memory Python list.

## Technologies

- Python
- FastAPI
- Uvicorn
- SQLite
- Python `sqlite3`

## Why SQLite?

SQLite was chosen because it is lightweight, requires no separate database server, and stores the database in a single local file.

## Database

The database file is:

```text
tasks.db

```

It is created automatically when the application starts.

The database contains a `tasks` table with:

* `id` — integer primary key
* `title` — text
* `done` — boolean

The three example tasks are inserted only when the table is empty.

## Setup

Create a virtual environment:

```bash
python -m venv .venv

```

Activate it on Windows:

```bash
.venv\Scripts\activate

```

Install dependencies:

```bash
pip install -r requirements.txt

```

## Run

```bash
uvicorn main:app --reload

```

Open:
http://localhost:8000/docs

The SQLite database is created automatically.

## Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/` | API information |
| GET | `/health` | Health check |
| GET | `/tasks` | Return all tasks |
| GET | `/tasks/{task_id}` | Return one task |
| POST | `/tasks` | Create a task |
| PUT | `/tasks/{task_id}` | Update a task |
| DELETE | `/tasks/{task_id}` | Delete a task |

## Example SQL Query

The database was manually inspected using:

```sql
SELECT * FROM tasks WHERE done = 1;

```

This returns only completed tasks.

Other SQL queries tested during the assignment included:

```sql
SELECT * FROM tasks;
SELECT COUNT(*) FROM tasks;
UPDATE tasks SET done = 1;
DELETE FROM tasks WHERE done = 1;

```

## Database Screenshot

<img width="959" height="539" alt="image" src="https://github.com/user-attachments/assets/535caf70-ac0f-4e4c-8de7-06d0e9a5f104" />


## Persistence

Tasks are stored in SQLite, so data survives when the FastAPI server is restarted.

If `tasks.db` does not exist, the application automatically creates the database, creates the `tasks` table, and inserts the three example tasks.

```

Ise save karne ke baad, tum apna **Step 22** aur **Step 23** continue kar sakti ho GitHub par push karne ke liye!

```
