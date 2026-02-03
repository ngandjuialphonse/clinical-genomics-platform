"""
Clinical Genomics Platform - Database Models

This module defines the SQLAlchemy ORM models for the clinical genomics platform.
These models represent the core entities in a clinical genomics laboratory:

1. Sample - A biological sample (e.g., blood, tissue) from a patient
2. SequencingRun - A single run on a sequencing instrument (e.g., Illumina NovaSeq)
3. QCMetrics - Quality control metrics extracted from the bioinformatics pipeline
4. PipelineRun - A record of each pipeline execution for audit purposes

WHY THIS DESIGN?
----------------
In clinical genomics, traceability is paramount. Every sample must be trackable
from collection to final report. This schema enables:
- Full audit trail of all pipeline executions
- Historical QC trending to detect instrument drift
- Sample-to-report lineage for regulatory compliance (CAP/CLIA)
"""

from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import (
    Column, Integer, String, Float, DateTime, ForeignKey, 
    Text, Enum, Boolean, JSON, Index
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class SampleStatus(str, PyEnum):
    """
    Sample lifecycle states in a clinical lab.
    
    RECEIVED: Sample arrived at the lab
    EXTRACTED: DNA/RNA extraction complete
    SEQUENCING: Currently on the sequencer
    ANALYSIS: Bioinformatics pipeline running
    QC_REVIEW: Awaiting QC review by lab director
    COMPLETE: Analysis complete, ready for reporting
    FAILED: Sample failed QC or processing
    """
    RECEIVED = "received"
    EXTRACTED = "extracted"
    SEQUENCING = "sequencing"
    ANALYSIS = "analysis"
    QC_REVIEW = "qc_review"
    COMPLETE = "complete"
    FAILED = "failed"


class RunStatus(str, PyEnum):
    """Pipeline run status for tracking execution state."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class Sample(Base):
    """
    Represents a biological sample in the clinical genomics workflow.
    
    This is the central entity - everything else relates back to a sample.
    In a real clinical lab, this would link to the Laboratory Information
    Management System (LIMS).
    
    Attributes:
        sample_id: Internal unique identifier (auto-generated)
        external_id: The ID used by the submitting institution (e.g., hospital)
        patient_id: De-identified patient identifier (HIPAA compliant)
        sample_type: Type of biological material (blood, tissue, etc.)
        collection_date: When the sample was collected from the patient
        received_date: When the sample arrived at the lab
        status: Current state in the processing workflow
    """
    __tablename__ = "samples"
    
    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String(100), unique=True, nullable=False, index=True)
    patient_id = Column(String(100), nullable=False, index=True)
    sample_type = Column(String(50), nullable=False)  # blood, tissue, saliva, etc.
    collection_date = Column(DateTime, nullable=True)
    received_date = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum(SampleStatus), default=SampleStatus.RECEIVED)
    metadata = Column(JSON, nullable=True)  # Flexible field for additional data
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    qc_metrics = relationship("QCMetrics", back_populates="sample")
    pipeline_runs = relationship("PipelineRun", back_populates="sample")
    
    # Index for common queries
    __table_args__ = (
        Index('idx_sample_status_date', 'status', 'received_date'),
    )


class SequencingRun(Base):
    """
    Represents a single sequencing run on an instrument.
    
    One sequencing run can contain multiple samples (multiplexing).
    This table tracks instrument-level metrics that affect all samples
    on that run.
    
    WHY TRACK THIS?
    ---------------
    Instrument performance can drift over time. By tracking run-level
    metrics, we can detect when a sequencer needs maintenance before
    it affects sample quality.
    """
    __tablename__ = "sequencing_runs"
    
    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(String(100), unique=True, nullable=False, index=True)
    instrument_id = Column(String(50), nullable=False)
    instrument_type = Column(String(50), nullable=False)  # NovaSeq, NextSeq, etc.
    flowcell_id = Column(String(50), nullable=True)
    run_date = Column(DateTime, nullable=False)
    
    # Run-level QC metrics
    cluster_density = Column(Float, nullable=True)  # clusters/mm²
    cluster_passing_filter = Column(Float, nullable=True)  # percentage
    q30_percentage = Column(Float, nullable=True)  # % bases >= Q30
    total_reads = Column(Float, nullable=True)  # in millions
    error_rate = Column(Float, nullable=True)  # percentage
    
    status = Column(String(20), default="completed")
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    qc_metrics = relationship("QCMetrics", back_populates="sequencing_run")


class QCMetrics(Base):
    """
    Quality Control metrics for a sample from the bioinformatics pipeline.
    
    These metrics are extracted from tools like FastQC, MultiQC, Picard,
    and samtools. They determine whether a sample passes or fails QC.
    
    KEY METRICS EXPLAINED:
    ----------------------
    - total_reads: Number of sequencing reads (should match expected depth)
    - mapped_reads: Reads that aligned to the reference genome
    - mapping_rate: mapped_reads / total_reads (typically >95% is good)
    - duplicate_rate: PCR duplicates (high = library prep issue)
    - mean_coverage: Average sequencing depth across target regions
    - uniformity: How evenly distributed the coverage is
    - contamination_rate: Cross-sample contamination (should be <1%)
    """
    __tablename__ = "qc_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    sample_id = Column(Integer, ForeignKey("samples.id"), nullable=False)
    sequencing_run_id = Column(Integer, ForeignKey("sequencing_runs.id"), nullable=True)
    
    # Read-level metrics
    total_reads = Column(Float, nullable=False)  # in millions
    mapped_reads = Column(Float, nullable=False)  # in millions
    mapping_rate = Column(Float, nullable=False)  # percentage
    duplicate_rate = Column(Float, nullable=True)  # percentage
    
    # Coverage metrics
    mean_coverage = Column(Float, nullable=True)
    median_coverage = Column(Float, nullable=True)
    uniformity = Column(Float, nullable=True)  # % bases at >0.2x mean coverage
    
    # Quality metrics
    q30_percentage = Column(Float, nullable=True)
    mean_base_quality = Column(Float, nullable=True)
    gc_content = Column(Float, nullable=True)
    
    # Contamination
    contamination_rate = Column(Float, nullable=True)
    
    # QC Decision
    qc_pass = Column(Boolean, nullable=True)
    qc_notes = Column(Text, nullable=True)
    
    # For RNA-Seq specific metrics
    rrna_rate = Column(Float, nullable=True)  # ribosomal RNA contamination
    exonic_rate = Column(Float, nullable=True)  # % reads in exons
    intronic_rate = Column(Float, nullable=True)
    intergenic_rate = Column(Float, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    sample = relationship("Sample", back_populates="qc_metrics")
    sequencing_run = relationship("SequencingRun", back_populates="qc_metrics")
    
    __table_args__ = (
        Index('idx_qc_sample_date', 'sample_id', 'created_at'),
    )


class PipelineRun(Base):
    """
    Audit log for pipeline executions.
    
    Every time the Nextflow pipeline runs, we record:
    - Which sample was processed
    - Which version of the pipeline was used
    - How long it took
    - Whether it succeeded or failed
    
    WHY THIS MATTERS FOR CLINICAL:
    ------------------------------
    Regulatory bodies (CAP, CLIA, FDA) require complete traceability.
    If a patient's result is questioned, we must be able to show exactly
    which software version produced that result.
    """
    __tablename__ = "pipeline_runs"
    
    id = Column(Integer, primary_key=True, index=True)
    sample_id = Column(Integer, ForeignKey("samples.id"), nullable=False)
    
    # Pipeline identification
    pipeline_name = Column(String(100), nullable=False)
    pipeline_version = Column(String(50), nullable=False)
    nextflow_version = Column(String(50), nullable=True)
    
    # Execution details
    run_name = Column(String(100), nullable=True)  # Nextflow run name
    work_dir = Column(String(500), nullable=True)  # S3 path to work directory
    output_dir = Column(String(500), nullable=True)  # S3 path to results
    
    # Timing
    started_at = Column(DateTime, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    duration_minutes = Column(Float, nullable=True)
    
    # Status
    status = Column(Enum(RunStatus), default=RunStatus.PENDING)
    exit_code = Column(Integer, nullable=True)
    error_message = Column(Text, nullable=True)
    
    # Resource usage
    cpu_hours = Column(Float, nullable=True)
    memory_gb_hours = Column(Float, nullable=True)
    cost_estimate = Column(Float, nullable=True)  # Estimated AWS cost
    
    # Git commit for reproducibility
    git_commit = Column(String(40), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    sample = relationship("Sample", back_populates="pipeline_runs")
    
    __table_args__ = (
        Index('idx_pipeline_status_date', 'status', 'started_at'),
    )
