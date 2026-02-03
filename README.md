# Clinical Genomics QC & Monitoring Platform

This repository contains a full-stack, enterprise-grade platform for monitoring and managing clinical genomics data. It is designed to integrate with a bioinformatics pipeline (like the one in the `bioinformatics-platform` repository) to provide a complete end-to-end solution for sample tracking, quality control, and data visualization.

This project demonstrates a full-stack approach to bioinformatics platform engineering, covering:
-   **Backend Development** with FastAPI and PostgreSQL
-   **Frontend Development** with Streamlit
-   **Database Design** with SQLAlchemy ORM
-   **Containerization** with Docker
-   **Infrastructure as Code** with Terraform for AWS deployment
-   **CI/CD** with GitHub Actions

## Features

-   **Sample Tracking:** Real-time view of all samples, their status, and processing history.
-   **QC Dashboard:** Interactive visualization of key quality control metrics.
-   **Audit Trail:** Complete history of all pipeline runs for regulatory compliance.
-   **RESTful API:** A robust API for programmatic access to the platform's data.

## Architecture

![Architecture Diagram](docs/images/architecture.png)  <!-- Placeholder for diagram -->

## Getting Started

### Local Development

1.  **Prerequisites:** Docker and Docker Compose.
2.  **Run:** `docker-compose up --build`
3.  **Access:**
    -   API: `http://localhost:8000/docs`
    -   Dashboard: `http://localhost:8501`

### AWS Deployment

1.  **Prerequisites:** Terraform, AWS CLI.
2.  **Configure AWS Credentials.**
3.  **Deploy:**
    ```bash
    cd terraform/environments/dev
    terraform init
    terraform apply
    ```

## Learning Modules

This project includes a series of learning modules in the `docs/learning` directory to explain the concepts and technologies used:

1.  [Database Schema Design](./docs/learning/01-database-schema.md)
2.  [Building the FastAPI Backend](./docs/learning/02-fastapi-backend.md)
3.  [Creating the Streamlit Dashboard](./docs/learning/03-streamlit-dashboard.md)
4.  [Local Development with Docker Compose](./docs/learning/04-local-development.md)
5.  [AWS Deployment with Terraform](./docs/learning/05-aws-deployment.md)
