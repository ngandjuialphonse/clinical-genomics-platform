"""
Service Layer for Pipeline Run Business Logic
"""

from sqlalchemy.orm import Session
from .. import models, schemas

def create_pipeline_run(db: Session, pipeline_run: schemas.PipelineRunCreate):
    """Create a new pipeline run record."""
    db_run = models.PipelineRun(**pipeline_run.model_dump())
    db.add(db_run)
    db.commit()
    db.refresh(db_run)
    return db_run

def update_pipeline_run(db: Session, run_id: int, run_update: schemas.PipelineRunUpdate):
    """Update a pipeline run with completion status."""
    db_run = db.query(models.PipelineRun).filter(models.PipelineRun.id == run_id).first()
    if not db_run:
        return None
    
    update_data = run_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_run, key, value)
        
    db.commit()
    db.refresh(db_run)
    return db_run

def get_pipeline_runs_for_sample(db: Session, sample_id: int):
    """Get all pipeline runs for a specific sample."""
    return db.query(models.PipelineRun).filter(models.PipelineRun.sample_id == sample_id).all()
