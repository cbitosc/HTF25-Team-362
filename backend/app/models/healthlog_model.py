from beanie import Document
from pydantic import Field
from typing import Optional, Dict
from datetime import datetime
from enum import Enum


class SymptomSeverity(str, Enum):
    """Severity levels for symptoms"""
    NONE = "none"
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"
    CRITICAL = "critical"


class MoodType(str, Enum):
    """Mood types"""
    EXCELLENT = "excellent"
    GOOD = "good"
    OKAY = "okay"
    LOW = "low"
    DEPRESSED = "depressed"


class HealthLog(Document):
    """Daily health log/symptom tracker"""
    
    # Owner Info
    user_id: str = Field(..., index=True)
    log_date: datetime = Field(default_factory=datetime.utcnow, index=True)
    
    # Patient and Doctor Info
    patient_name: Optional[str] = None
    doctor_name: Optional[str] = None
    
    # Vital Signs
    temperature: Optional[float] = None  # In Celsius
    blood_pressure_systolic: Optional[int] = None
    blood_pressure_diastolic: Optional[int] = None
    heart_rate: Optional[int] = None  # BPM
    oxygen_saturation: Optional[float] = None  # SpO2 percentage
    weight: Optional[float] = None  # In kg
    blood_sugar: Optional[float] = None  # mg/dL
    
    # Symptoms
    has_fever: bool = Field(default=False)
    has_cough: bool = Field(default=False)
    has_headache: bool = Field(default=False)
    has_fatigue: bool = Field(default=False)
    has_body_pain: bool = Field(default=False)
    has_nausea: bool = Field(default=False)
    
    # Symptom Severity
    pain_level: SymptomSeverity = Field(default=SymptomSeverity.NONE)
    symptom_severity: SymptomSeverity = Field(default=SymptomSeverity.NONE)
    
    # Mental Health
    mood: MoodType = Field(default=MoodType.OKAY)
    stress_level: int = Field(default=5, ge=1, le=10)  # 1-10 scale
    anxiety_level: int = Field(default=5, ge=1, le=10)
    
    # Lifestyle
    sleep_hours: Optional[float] = None
    sleep_quality: int = Field(default=5, ge=1, le=10)
    water_intake: Optional[float] = None  # In liters
    exercise_minutes: Optional[int] = None
    
    # Medications Taken
    medications_taken: list[str] = Field(default_factory=list)
    
    # Notes
    notes: Optional[str] = None
    symptoms_description: Optional[str] = None
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "health_logs"
        indexes = [
            "user_id",
            "log_date",
            ("user_id", "log_date")  # Compound index
        ]
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user123",
                "temperature": 98.6,
                "blood_pressure_systolic": 120,
                "blood_pressure_diastolic": 80,
                "heart_rate": 72,
                "has_headache": True,
                "pain_level": "mild",
                "mood": "good",
                "sleep_hours": 7.5,
                "water_intake": 2.5,
                "notes": "Feeling better today"
            }
        }
