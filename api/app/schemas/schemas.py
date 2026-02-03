"""
Clinical Genomics Platform - Pydantic Schemas

This module defines the Pydantic models for API data validation.
These schemas are used for:
1.  Request body validation (e.g., when creating a new sample)
2.  Response serialization (e.g., when returning a list of samples)
3.  API documentation (FastAPI automatically generates OpenAPI docs from these)

WHY SEPARATE SCHEMAS FROM MODELS?
---------------------------------
-   **Security:** Prevents accidentally exposing sensitive model fields (like passwords)
-   **Clarity:** Defines a clear API contract, separate from the database structure
-   **Flexibility:** Allows the API shape to evolve independently of the database
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from ..models.models import SampleStatus, RunStatus

# --- Base Schemas ---
# These are the common fields shared across create/update/read schemas

class SampleBase(BaseModel):
    external_id: str = Field(..., description="The ID from the submitting institution")
    patient_id: str = Field(..., description="De-identified patient identifier")
    sample_type: str = Field(..., description="Type of biological material (e.g., blood, tissue)")
    collection_date: Optional[datetime] = None
    metadata: Optional[dict] = None

class SequencingRunBase(BaseModel):
    run_id: str = Field(..., description="Unique identifier for the sequencing run")
    instrument_id: str
    instrument_type: str
    flowcell_id: Optional[str] = None
    run_date: datetime
    cluster_density: Optional[float] = None
    cluster_passing_filter: Optional[float] = None
    q30_percentage: Optional[float] = None
    total_reads: Optional[float] = None
    error_rate: Optional[float] = None

class QCMetricsBase(BaseModel):
    sample_id: int
    sequencing_run_id: Optional[int] = None
    total_reads: float
    mapped_reads: float
    mapping_rate: float
    duplicate_rate: Optional[float] = None
    mean_coverage: Optional[float] = None
    median_coverage: Optional[float] = None
    uniformity: Optional[float] = None
    q30_percentage: Optional[float] = None
    mean_base_quality: Optional[float] = None
    gc_content: Optional[float] = None
    contamination_rate: Optional[float] = None
    rrna_rate: Optional[float] = None
    exonic_rate: Optional[float] = None
    intronic_rate: Optional[float] = None
    intergenic_rate: Optional[float] = None

class PipelineRunBase(BaseModel):
    sample_id: int
    pipeline_name: str
    pipeline_version: str
    nextflow_version: Optional[str] = None
    run_name: Optional[str] = None
    work_dir: Optional[str] = None
    output_dir: Optional[str] = None
    started_at: datetime
    git_commit: Optional[str] = None

# --- Create Schemas ---
# Used for creating new records (POST requests)

class SampleCreate(SampleBase):
    pass

class SequencingRunCreate(SequencingRunBase):
    pass

class QCMetricsCreate(QCMetricsBase):
    pass

class PipelineRunCreate(PipelineRunBase):
    pass

# --- Update Schemas ---
# Used for updating existing records (PUT/PATCH requests)
# All fields are optional

class SampleUpdate(BaseModel):
    external_id: Optional[str] = None
    patient_id: Optional[str] = None
    sample_type: Optional[str] = None
    collection_date: Optional[datetime] = None
    status: Optional[SampleStatus] = None
    metadata: Optional[dict] = None

class PipelineRunUpdate(BaseModel):
    completed_at: Optional[datetime] = None
    duration_minutes: Optional[float] = None
    status: Optional[RunStatus] = None
    exit_code: Optional[int] = None
    error_message: Optional[str] = None
    cpu_hours: Optional[float] = None
    memory_gb_hours: Optional[float] = None
    cost_estimate: Optional[float] = None

# --- Read Schemas (for API Responses) ---
# These include fields from the database model (like id, created_at)

class Sample(SampleBase):
    id: int
    received_date: datetime
    status: SampleStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Pydantic v2, formerly orm_mode

class SequencingRun(SequencingRunBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class QCMetrics(QCMetricsBase):
    id: int
    qc_pass: Optional[bool] = None
    qc_notes: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class PipelineRun(PipelineRunBase):
    id: int
    completed_at: Optional[datetime] = None
    duration_minutes: Optional[float] = None
    status: RunStatus
    exit_code: Optional[int] = None
    error_message: Optional[str] = None
    cpu_hours: Optional[float] = None
    memory_gb_hours: Optional[float] = None
    cost_estimate: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True

# --- Schemas with Relationships (for nested responses) ---

class SampleWithDetails(Sample):
    qc_metrics: List[QCMetrics] = []
    pipeline_runs: List[PipelineRun] = []

    class Config:
        from_attributes = True
