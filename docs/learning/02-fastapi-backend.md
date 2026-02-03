# Learning Module 2: Building the FastAPI Backend

This module covers the design and implementation of our RESTful API using FastAPI.

## Why FastAPI?

FastAPI is a modern, high-performance Python web framework. It was chosen for this project because:

-   **High Performance:** It is one of the fastest Python frameworks available, built on top of Starlette (for the web parts) and Pydantic (for the data parts).
-   **Automatic Docs:** It automatically generates interactive API documentation (Swagger UI and ReDoc). This is a huge time-saver.
-   **Type Hints & Validation:** It uses Python type hints to automatically validate incoming data, reducing bugs.
-   **Dependency Injection:** It has a powerful dependency injection system, which we use to manage database sessions.

## Our API Architecture

Our API is structured into several layers to ensure separation of concerns:

1.  **`main.py`**: The entry point of the application. It initializes the FastAPI app, adds middleware (like CORS), and includes the routers.
2.  **`routers/`**: Each resource (e.g., `samples`, `qc_metrics`) has its own router file. This keeps the code organized.
3.  **`schemas/`**: Pydantic models that define the shape of the data for API requests and responses. This is our API contract.
4.  **`services/`**: The business logic. The routers call service functions to perform the actual work. This keeps the routing layer thin.
5.  **`models/`**: SQLAlchemy ORM models that define the database tables.
6.  **`core/`**: Configuration and database connection management.

## Key Endpoints

-   `POST /samples/`: Create a new sample.
-   `GET /samples/`: Get a list of samples (with filtering and pagination).
-   `GET /samples/{sample_id}`: Get a single sample with its details.
-   `POST /qc_metrics/`: Ingest QC metrics from the pipeline.
