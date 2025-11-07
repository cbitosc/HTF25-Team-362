from beanie import Document
from pydantic import Field
from typing import Optional, Dict
from datetime import datetime
from enum import Enum


class ReportType(str, Enum):
    """Types of health reports"""
    LAB_TEST = "lab_test"
    PRESCRIPTION = "prescription"
    XRAY = "xray"
    MRI = "mri"
    CT_SCAN = "ct_scan"
    ULTRASOUND = "ultrasound"
    MEDICAL_CERTIFICATE = "medical_certificate"
    VACCINATION = "vaccination"
    OTHER = "other"


class HealthReport(Document):
    """Health report/document model"""
    
    # Owner Info
    user_id: str = Field(..., index=True)  # Reference to User
    uploaded_by: str  # User ID who uploaded (could be doctor)
    
    # Report Info
    report_type: ReportType
    title: str
    description: Optional[str] = None
    report_date: datetime = Field(default_factory=datetime.utcnow)
    
    # File Info
    file_path: str  # Path to uploaded file
    file_name: str
    file_size: int  # In bytes
    file_type: str  # pdf, jpg, png, etc.
    
    # Medical Data (extracted or manual)
    doctor_name: Optional[str] = None
    hospital_name: Optional[str] = None
    diagnosis: Optional[str] = None
    medications: list[str] = Field(default_factory=list)
    test_results: Optional[Dict] = None  # Key-value pairs of test results
    
    # Access Control
    shared_with_doctors: list[str] = Field(default_factory=list)  # Doctor IDs
    is_sensitive: bool = Field(default=False)
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    tags: list[str] = Field(default_factory=list)
    
    class Settings:
        name = "health_reports"
        indexes = [
            "user_id",
            "report_type",
            "report_date"
        ]
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user123",
                "uploaded_by": "user123",
                "report_type": "lab_test",
                "title": "Blood Test Report",
                "description": "Routine blood work",
                "doctor_name": "Dr. Smith",
                "hospital_name": "City Hospital",
                "test_results": {
                    "Hemoglobin": "14.5 g/dL",
                    "Blood Sugar": "95 mg/dL"
                }
            }
        }
