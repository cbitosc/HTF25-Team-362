from beanie import Document
from pydantic import Field
from typing import Optional, Dict, List
from datetime import datetime


class HealthInsight(Document):
    """AI-generated health insights"""
    
    # Owner Info
    user_id: str = Field(..., index=True)
    patient_name: Optional[str] = None
    
    # Log Selection
    analyzed_log_ids: List[str] = Field(default_factory=list)
    logs_analyzed_count: int = 0
    
    # AI Insights Data
    trends: Optional[Dict] = None
    correlations: Optional[Dict] = None
    recommendations: List[str] = Field(default_factory=list)
    alerts: Optional[Dict] = None
    insights_raw: Optional[str] = None  # Raw AI output
    
    # Analysis Metadata
    analysis_date: datetime = Field(default_factory=datetime.utcnow, index=True)
    data_points_analyzed: int = 0
    ai_model_used: str = "gpt-4o-mini"
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "health_insights"
        indexes = [
            "user_id",
            "analysis_date",
            ("user_id", "analysis_date")  # Compound index
        ]
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user123",
                "patient_name": "John Doe",
                "analyzed_log_ids": ["log1", "log2"],
                "logs_analyzed_count": 2,
                "trends": {"temperature": "Stable"},
                "recommendations": ["Get more rest", "Drink more water"]
            }
        }

