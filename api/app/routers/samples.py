"""
API Router for Sample Management

This router handles all CRUD (Create, Read, Update, Delete) operations
for the Sample resource.

KEY FASTAPI CONCEPTS:
---------------------
- APIRouter: A mini-FastAPI app that can be included in the main app
- Depends: The dependency injection system for providing DB sessions, etc.
- Path parameters: (e.g., /samples/{sample_id}) for fetching a specific resource
- Query parameters: (e.g., /samples?skip=0&limit=10) for pagination
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from .. import schemas
from ..services import sample_service
from ..core.database import get_db

router = APIRouter()


@router.post("/samples/", response_model=schemas.Sample, status_code=201)
def create_sample(sample: schemas.SampleCreate, db: Session = Depends(get_db)):
    """
    Create a new sample.
    
    This endpoint would be called when a new sample arrives at the lab.
    """
    db_sample = sample_service.get_sample_by_external_id(db, external_id=sample.external_id)
    if db_sample:
        raise HTTPException(status_code=400, detail="External ID already registered")
    return sample_service.create_sample(db=db, sample=sample)


@router.get("/samples/", response_model=List[schemas.Sample])
def read_samples(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    patient_id: str = None,
    status: schemas.SampleStatus = None
):
    """
    Retrieve a list of samples with optional filtering and pagination.
    
    This powers the main sample tracking view in the dashboard.
    """
    samples = sample_service.get_samples(db, skip=skip, limit=limit, patient_id=patient_id, status=status)
    return samples


@router.get("/samples/{sample_id}", response_model=schemas.SampleWithDetails)
def read_sample(sample_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single sample by its internal ID, including its QC metrics
    and pipeline run history.
    """
    db_sample = sample_service.get_sample(db, sample_id=sample_id)
    if db_sample is None:
        raise HTTPException(status_code=404, detail="Sample not found")
    return db_sample


@router.patch("/samples/{sample_id}", response_model=schemas.Sample)
def update_sample(sample_id: int, sample: schemas.SampleUpdate, db: Session = Depends(get_db)):
    """
    Update a sample's status or other attributes.
    
    For example, updating the status from 'ANALYSIS' to 'QC_REVIEW'.
    """
    db_sample = sample_service.update_sample(db, sample_id=sample_id, sample_update=sample)
    if db_sample is None:
        raise HTTPException(status_code=404, detail="Sample not found")
    return db_sample
