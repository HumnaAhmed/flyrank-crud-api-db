CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    done BOOLEAN NOT NULL DEFAULT FALSE
);

INSERT INTO tasks (title, done)
SELECT 'Test Docker Compose app', false
WHERE NOT EXISTS (SELECT 1 FROM tasks WHERE title = 'Test Docker Compose app');