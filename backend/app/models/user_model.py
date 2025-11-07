from beanie import Document
from pydantic import EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    """User role types"""
    PATIENT = "patient"
    DOCTOR = "doctor"
    ADMIN = "admin"


class User(Document):
    """User model for authentication and profile"""
    
    # Basic Info
    email: EmailStr = Field(..., unique=True, index=True)
    hashed_password: str
    full_name: str
    phone: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    gender: Optional[str] = None
    
    # Role & Permissions
    role: UserRole = Field(default=UserRole.PATIENT)
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)
    
    # Medical Info (for patients)
    blood_group: Optional[str] = None
    allergies: List[str] = Field(default_factory=list)
    chronic_conditions: List[str] = Field(default_factory=list)
    emergency_contact: Optional[str] = None
    
    # Doctor Info (for doctors)
    specialization: Optional[str] = None
    license_number: Optional[str] = None
    hospital_affiliation: Optional[str] = None
    
    # Doctor-Patient Relationship
    assigned_doctor_id: Optional[str] = None  # For patients
    patients_list: List[str] = Field(default_factory=list)  # For doctors
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None
    
    class Settings:
        name = "users"
        indexes = [
            "email",
            "role",
            "is_active"
        ]
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "patient@example.com",
                "full_name": "John Doe",
                "phone": "+91-9876543210",
                "role": "patient",
                "blood_group": "O+",
                "allergies": ["Penicillin"],
                "chronic_conditions": ["Diabetes Type 2"]
            }
        }
