"""
Application Configuration

This module uses Pydantic's BaseSettings to manage configuration.
Settings are loaded from environment variables, with sensible defaults
for local development.

WHY PYDANTIC SETTINGS?
----------------------
1. Type validation: Ensures config values are the correct type
2. Environment variables: Automatically reads from env vars
3. .env file support: Can load from .env files in development
4. Documentation: Settings are self-documenting with type hints
"""

import os
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    In production, these are set via:
    - Docker environment variables
    - Kubernetes ConfigMaps/Secrets
    - AWS Parameter Store or Secrets Manager
    """
    
    # Application
    app_name: str = "Clinical Genomics QC Platform"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Database
    database_url: str = "postgresql://postgres:postgres@localhost:5432/clinical_genomics"
    
    # API
    api_prefix: str = "/api/v1"
    
    # CORS (Cross-Origin Resource Sharing)
    # In production, restrict this to your frontend domain
    cors_origins: list = ["http://localhost:8501", "http://localhost:3000"]
    
    # QC Thresholds - These define pass/fail criteria
    # These values are typical for clinical-grade sequencing
    qc_min_mapping_rate: float = 95.0  # Minimum mapping rate (%)
    qc_max_duplicate_rate: float = 30.0  # Maximum duplicate rate (%)
    qc_min_mean_coverage: float = 30.0  # Minimum mean coverage (X)
    qc_min_q30: float = 80.0  # Minimum Q30 percentage
    qc_max_contamination: float = 1.0  # Maximum contamination rate (%)
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    The @lru_cache decorator ensures we only create one Settings
    instance, which is reused for all requests. This is more
    efficient than creating a new instance for each request.
    """
    return Settings()
