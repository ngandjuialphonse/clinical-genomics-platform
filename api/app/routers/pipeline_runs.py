"""
API Router for Pipeline Run Tracking

This router handles the creation and retrieval of pipeline run audit logs.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import schemas
from ..services import pipeline_run_service
from ..core.database import get_db

router = APIRouter()


@router.post("/pipeline_runs/", response_model=schemas.PipelineRun, status_code=201)
def create_pipeline_run(pipeline_run: schemas.PipelineRunCreate, db: Session = Depends(get_db)):
    """
    Create a new pipeline run record.
    
    This would be called at the start of the Nextflow pipeline.
    """
    return pipeline_run_service.create_pipeline_run(db=db, pipeline_run=pipeline_run)


@router.patch("/pipeline_runs/{run_id}", response_model=schemas.PipelineRun)
def update_pipeline_run(run_id: int, run_update: schemas.PipelineRunUpdate, db: Session = Depends(get_db)):
    """
    Update a pipeline run record with completion status.
    
    This would be called at the end of the Nextflow pipeline (onComplete).
    """
    db_run = pipeline_run_service.update_pipeline_run(db, run_id=run_id, run_update=run_update)
    if db_run is None:
        raise HTTPException(status_code=404, detail="Pipeline run not found")
    return db_run


@router.get("/samples/{sample_id}/pipeline_runs/", response_model=List[schemas.PipelineRun])
def read_pipeline_runs_for_sample(sample_id: int, db: Session = Depends(get_db)):
    """
    Retrieve all pipeline run records for a specific sample.
    """
    runs = pipeline_run_service.get_pipeline_runs_for_sample(db, sample_id=sample_id)
    if not runs:
        raise HTTPException(status_code=404, detail="No pipeline runs found for this sample")
    return runs
