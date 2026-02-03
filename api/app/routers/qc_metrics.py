"""
API Router for QC Metrics

This router handles the ingestion and retrieval of QC metrics from the
bioinformatics pipeline.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import schemas
from ..services import qc_service
from ..core.database import get_db

router = APIRouter()


@router.post("/qc_metrics/", response_model=schemas.QCMetrics, status_code=201)
def create_qc_metrics(qc_metrics: schemas.QCMetricsCreate, db: Session = Depends(get_db)):
    """
    Create a new QC metrics record.
    
    This endpoint would be called by a post-processing script at the end
    of the Nextflow pipeline.
    """
    return qc_service.create_qc_metrics(db=db, qc_metrics=qc_metrics)


@router.get("/samples/{sample_id}/qc_metrics/", response_model=List[schemas.QCMetrics])
def read_qc_metrics_for_sample(sample_id: int, db: Session = Depends(get_db)):
    """
    Retrieve all QC metrics records for a specific sample.
    """
    qc_metrics = qc_service.get_qc_metrics_for_sample(db, sample_id=sample_id)
    if not qc_metrics:
        raise HTTPException(status_code=404, detail="No QC metrics found for this sample")
    return qc_metrics


@router.get("/qc_metrics/all/", response_model=List[schemas.QCMetrics])
def read_all_qc_metrics(db: Session = Depends(get_db), skip: int = 0, limit: int = 1000):
    """
    Retrieve all QC metrics records.
    """
    return qc_service.get_all_qc_metrics(db, skip=skip, limit=limit)
