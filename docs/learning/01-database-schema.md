# Learning Module 1: Database Schema Design

This module explains the design of the PostgreSQL database schema, which is the foundation of our platform.

## Why a Relational Database?

In bioinformatics, we deal with massive, unstructured files (FASTQ, BAM). So why use a structured, relational database like PostgreSQL?

-   **Metadata Management:** We don't store the 100GB BAM file in the database. We store the *metadata* about it: the sample ID, the pipeline version, the QC metrics, and a pointer (S3 path) to the file itself.
-   **Queryability:** You can't efficiently ask 10,000 BAM files, "Which samples have a mapping rate below 95%?" But you can ask a SQL database this question in milliseconds.
-   **Audit & Compliance:** For clinical applications (CAP/CLIA), you need a bulletproof audit trail. A relational database with transactions provides this.

## Our Schema: The Four Core Tables

Our schema is designed around the typical workflow of a clinical genomics lab:

1.  **`samples`**: The central table. Every biological sample gets a record here. It tracks the sample's journey from `RECEIVED` to `COMPLETE`.
2.  **`sequencing_runs`**: Tracks instrument-level data. This helps detect if a specific sequencing machine is performing poorly.
3.  **`qc_metrics`**: Stores the quality control data extracted from the bioinformatics pipeline. This is where we store metrics like mapping rate, coverage, and contamination.
4.  **`pipeline_runs`**: An audit log of every time the Nextflow pipeline is run. This is critical for reproducibility and regulatory compliance.

## SQLAlchemy ORM

We use **SQLAlchemy**, a Python Object-Relational Mapper (ORM), to interact with the database. Instead of writing raw SQL, we define Python classes (our `models`) that map to the database tables.

**Why use an ORM?**
-   **Productivity:** It's faster to write Python than complex SQL.
-   **Database Agnostic:** We could switch from PostgreSQL to MySQL with minimal code changes.
-   **Security:** It helps prevent SQL injection attacks.
