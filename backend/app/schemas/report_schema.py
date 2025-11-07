from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from datetime import datetime
from app.models.report_model import ReportType


class ReportCreate(BaseModel):
    """Schema for creating health report"""
    report_type: ReportType
    title: str
    description: Optional[str] = None
    report_date: Optional[datetime] = None
    doctor_name: Optional[str] = None
    hospital_name: Optional[str] = None
    diagnosis: Optional[str] = None
    medications: List[str] = Field(default_factory=list)
    test_results: Optional[Dict] = None
    is_sensitive: bool = False
    tags: List[str] = Field(default_factory=list)


class ReportUpdate(BaseModel):
    """Schema for updating health report"""
    title: Optional[str] = None
    description: Optional[str] = None
    doctor_name: Optional[str] = None
    hospital_name: Optional[str] = None
    diagnosis: Optional[str] = None
    medications: Optional[List[str]] = None
    test_results: Optional[Dict] = None
    tags: Optional[List[str]] = None


class ReportResponse(BaseModel):
    """Schema for report response"""
    id: str
    user_id: str
    report_type: ReportType
    title: str
    description: Optional[str]
    report_date: datetime
    file_name: str
    file_type: str
    doctor_name: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True
