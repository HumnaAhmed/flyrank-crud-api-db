```markdown
# FlyRank CRUD API with PostgreSQL & Docker (BE-04)

## Architecture Overview
This project is a RESTful API built with **FastAPI**, containerized using **Docker**, and connected to a **PostgreSQL** database. 
- The application and database run in separate Docker containers managed by **Docker Compose**.
- The containers communicate securely over a shared internal Docker network.
- Healthchecks and `depends_on` configurations ensure the FastAPI application only boots after the PostgreSQL database is fully initialized and ready to accept connections.

## Database Integration
To fulfill the core architectural goal of this assignment, the data storage mechanism was completely refactored to use PostgreSQL instead of SQLite/in-memory lists. 
- The `psycopg` connection and SQL queries were integrated directly into the FastAPI route handlers in `main.py`.
- Database initialization is handled automatically on the first boot via an `init.sql` script mounted to the container.

## Data Persistence Verification
Data persistence is achieved using **Docker Volumes** (`postgres_data` mapped to `/var/lib/postgresql/data`). Persistence was actively tested and proven using the following methodology:
1. Started the stack using `docker compose up -d`.
2. Created new tasks via `POST /tasks` and verified their existence in the database.
3. Completely destroyed the running containers using `docker compose down`.
4. Restarted the stack using `docker compose up -d`.
5. Executed a `GET /tasks` request. The previously created rows were still present and retrieved successfully, proving the data survives container restarts and destruction.

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

## How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd <your-repo-folder>

```

2. **Configure Environment:**
Create a `.env` file in the root directory based on the provided example:
```bash
cp .env.example .env

```


3. **Launch the Stack:**
Build and start the application and database containers:
```bash
docker compose up --build -d

```


4. **Access the API:**
* Interactive API Documentation (Swagger UI): `http://localhost:8000/docs`
* API endpoints are available at `http://localhost:8000/tasks`



```