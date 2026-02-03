"""
Service Layer for Sample Business Logic

This service layer encapsulates the business logic for sample management,
separating it from the API routing layer.

WHY A SERVICE LAYER?
---------------------
-   **Reusability:** Logic can be reused by different parts of the app (e.g., API, background jobs).
-   **Testability:** Business logic can be tested independently of the web framework.
-   **Separation of Concerns:** Keeps the API layer thin and focused on handling HTTP requests.
"""

from sqlalchemy.orm import Session, joinedload
from .. import models, schemas

def get_sample(db: Session, sample_id: int):
    """Get a single sample by ID, with related QC and pipeline runs."""
    return db.query(models.Sample).options(
        joinedload(models.Sample.qc_metrics),
        joinedload(models.Sample.pipeline_runs)
    ).filter(models.Sample.id == sample_id).first()

def get_sample_by_external_id(db: Session, external_id: str):
    """Get a single sample by its external ID."""
    return db.query(models.Sample).filter(models.Sample.external_id == external_id).first()

def get_samples(db: Session, skip: int = 0, limit: int = 100, patient_id: str = None, status: schemas.SampleStatus = None):
    """Get a list of samples with filtering and pagination."""
    query = db.query(models.Sample)
    if patient_id:
        query = query.filter(models.Sample.patient_id == patient_id)
    if status:
        query = query.filter(models.Sample.status == status)
    return query.offset(skip).limit(limit).all()

def create_sample(db: Session, sample: schemas.SampleCreate):
    """Create a new sample record."""
    db_sample = models.Sample(**sample.model_dump())
    db.add(db_sample)
    db.commit()
    db.refresh(db_sample)
    return db_sample

def update_sample(db: Session, sample_id: int, sample_update: schemas.SampleUpdate):
    """Update an existing sample record."""
    db_sample = db.query(models.Sample).filter(models.Sample.id == sample_id).first()
    if not db_sample:
        return None
    
    update_data = sample_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_sample, key, value)
        
    db.commit()
    db.refresh(db_sample)
    return db_sample
