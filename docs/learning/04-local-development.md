# Learning Module 4: Local Development with Docker Compose

This module explains how we set up a local development environment using Docker Compose.

## Why Docker Compose?

Our platform consists of three services: a PostgreSQL database, a FastAPI backend, and a Streamlit dashboard. Docker Compose allows us to define and run this multi-container application with a single command.

**Benefits:**
-   **Reproducible Environment:** Guarantees that every developer has the exact same setup.
-   **Isolation:** The services run in isolated containers, so they don't interfere with other projects on your machine.
-   **Easy to Use:** `docker-compose up` is all you need to start the entire platform.

## Our `docker-compose.yml`

Our Docker Compose file defines three services:

1.  **`db`**: Runs the official `postgres:13-alpine` image. It uses a volume (`postgres_data`) to persist the database data.
2.  **`api`**: Builds the FastAPI backend from its `Dockerfile`. It uses a volume to mount the local code into the container, so changes are reflected instantly (hot-reloading).
3.  **`dashboard`**: Builds the Streamlit dashboard from its `Dockerfile`. It also uses a volume for hot-reloading.

**Key Concepts:**
-   **`depends_on`**: Ensures that the `api` service waits for the `db` service to be healthy before starting.
-   **`environment`**: Used to pass environment variables (like the `DATABASE_URL`) to the containers.
-   **`volumes`**: Mounts local directories into the containers for live code reloading.

