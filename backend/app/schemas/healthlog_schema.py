from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.models.healthlog_model import SymptomSeverity, MoodType


class HealthLogCreate(BaseModel):
    """Schema for creating health log"""
    log_date: Optional[datetime] = None
    
    # Patient and Doctor Info
    patient_name: Optional[str] = None
    doctor_name: Optional[str] = None
    
    # Vitals
    temperature: Optional[float] = Field(None, ge=35.0, le=45.0)
    blood_pressure_systolic: Optional[int] = Field(None, ge=50, le=250)
    blood_pressure_diastolic: Optional[int] = Field(None, ge=30, le=150)
    heart_rate: Optional[int] = Field(None, ge=30, le=220)
    oxygen_saturation: Optional[float] = Field(None, ge=0, le=100)
    weight: Optional[float] = Field(None, ge=10, le=300)
    blood_sugar: Optional[float] = Field(None, ge=0, le=600)
    
    # Symptoms
    has_fever: bool = False
    has_cough: bool = False
    has_headache: bool = False
    has_fatigue: bool = False
    has_body_pain: bool = False
    has_nausea: bool = False
    
    pain_level: SymptomSeverity = SymptomSeverity.NONE
    symptom_severity: SymptomSeverity = SymptomSeverity.NONE
    
    # Mental Health
    mood: MoodType = MoodType.OKAY
    stress_level: int = Field(5, ge=1, le=10)
    anxiety_level: int = Field(5, ge=1, le=10)
    
    # Lifestyle
    sleep_hours: Optional[float] = Field(None, ge=0, le=24)
    sleep_quality: int = Field(5, ge=1, le=10)
    water_intake: Optional[float] = Field(None, ge=0, le=20)
    exercise_minutes: Optional[int] = Field(None, ge=0, le=1440)
    
    medications_taken: List[str] = Field(default_factory=list)
    notes: Optional[str] = None
    symptoms_description: Optional[str] = None


class HealthLogUpdate(BaseModel):
    """Schema for updating health log"""
    temperature: Optional[float] = None
    mood: Optional[MoodType] = None
    sleep_hours: Optional[float] = None
    notes: Optional[str] = None


class HealthLogResponse(BaseModel):
    """Schema for health log response"""
    id: str
    user_id: str
    log_date: datetime
    patient_name: Optional[str] = None
    doctor_name: Optional[str] = None
    temperature: Optional[float] = None
    blood_pressure_systolic: Optional[int] = None
    blood_pressure_diastolic: Optional[int] = None
    has_fever: bool = False
    has_cough: bool = False
    has_headache: bool = False
    has_fatigue: bool = False
    has_body_pain: bool = False
    has_nausea: bool = False
    mood: MoodType
    pain_level: SymptomSeverity
    sleep_hours: Optional[float] = None
    sleep_quality: int
    stress_level: int
    anxiety_level: int
    notes: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
