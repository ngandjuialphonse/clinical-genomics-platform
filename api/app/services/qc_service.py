"""
Service Layer for QC Metrics Business Logic
"""

from sqlalchemy.orm import Session
from .. import models, schemas
from ..core.config import get_settings

def create_qc_metrics(db: Session, qc_metrics: schemas.QCMetricsCreate):
    """Create a new QC metrics record and perform automated QC check."""
    settings = get_settings()
    
    # Perform automated QC check
    qc_pass, qc_notes = _perform_qc_check(qc_metrics, settings)
    
    db_qc_metrics = models.QCMetrics(
        **qc_metrics.model_dump(),
        qc_pass=qc_pass,
        qc_notes=qc_notes
    )
    db.add(db_qc_metrics)
    db.commit()
    db.refresh(db_qc_metrics)
    return db_qc_metrics

def get_qc_metrics_for_sample(db: Session, sample_id: int):
    """Get all QC metrics for a specific sample."""
    return db.query(models.QCMetrics).filter(models.QCMetrics.sample_id == sample_id).all()

def _perform_qc_check(qc: schemas.QCMetricsCreate, settings: schemas.Settings) -> (bool, str):
    """
    Private function to perform automated QC checks based on thresholds
    defined in the application settings.
    
    Returns a tuple of (qc_pass: bool, qc_notes: str)
    """
    notes = []
    
    if qc.mapping_rate < settings.qc_min_mapping_rate:
        notes.append(f"Mapping rate {qc.mapping_rate:.2f}% is below threshold of {settings.qc_min_mapping_rate}%.")
    
    if qc.duplicate_rate > settings.qc_max_duplicate_rate:
        notes.append(f"Duplicate rate {qc.duplicate_rate:.2f}% is above threshold of {settings.qc_max_duplicate_rate}%.")
        
    if qc.mean_coverage < settings.qc_min_mean_coverage:
        notes.append(f"Mean coverage {qc.mean_coverage:.2f}X is below threshold of {settings.qc_min_mean_coverage}X.")
        
    if qc.q30_percentage < settings.qc_min_q30:
        notes.append(f"Q30 percentage {qc.q30_percentage:.2f}% is below threshold of {settings.qc_min_q30}%.")
        
    if qc.contamination_rate > settings.qc_max_contamination:
        notes.append(f"Contamination rate {qc.contamination_rate:.2f}% is above threshold of {settings.qc_max_contamination}%.")
        
    if not notes:
        return True, "All QC metrics passed."
    else:
        return False, " ".join(notes)


def get_all_qc_metrics(db: Session, skip: int = 0, limit: int = 1000):
    """Get all QC metrics with pagination."""
    return db.query(models.QCMetrics).offset(skip).limit(limit).all()
