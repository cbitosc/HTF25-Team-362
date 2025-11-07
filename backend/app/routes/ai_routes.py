from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Dict, Optional

from app.models.user_model import User
from app.models.healthlog_model import HealthLog
from app.models.insight_model import HealthInsight
from app.utils.role_utils import get_current_user
from app.services.ai_service import AIService
from datetime import datetime

router = APIRouter(prefix="/api/ai", tags=["AI Insights"])


class SymptomRequest(BaseModel):
    symptom: str
    severity: str = "mild"


class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[List[Dict]] = None


class SelectedLogsRequest(BaseModel):
    log_ids: List[str]
    patient_name: Optional[str] = None


@router.post("/analyze-selected")
async def analyze_selected_logs(
    request: SelectedLogsRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Analyze selected health logs
    
    - **log_ids**: List of log IDs to analyze
    - **patient_name**: Optional patient name to include in analysis
    """
    # Get selected logs
    logs = []
    for log_id in request.log_ids:
        log = await HealthLog.find_one(
            HealthLog.id == log_id,
            HealthLog.user_id == str(current_user.id)
        )
        if log:
            logs.append(log)
    
    if not logs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No logs found with the provided IDs"
        )
    
    # Generate insights
    insights = await AIService.analyze_health_trends(current_user, logs)
    
    return {
        "patient_name": request.patient_name or current_user.full_name,
        "logs_analyzed": len(logs),
        "selected_logs": [log_id for log_id in request.log_ids],
        **insights
    }


@router.get("/insights")
async def get_health_insights(
    days: int = 30,
    current_user: User = Depends(get_current_user)
):
    """
    Get AI-powered health insights based on recent health logs
    
    - **days**: Number of days to analyze (default: 30)
    """
    # Get recent logs
    logs = await HealthLog.find(
        HealthLog.user_id == str(current_user.id)
    ).sort("-log_date").limit(days).to_list()
    
    if not logs:
        return {
            "message": "No health data available. Start logging your daily health to get insights!",
            "logs_count": 0
        }
    
    # Generate insights
    insights = await AIService.analyze_health_trends(current_user, logs)
    
    return {
        "user_name": current_user.full_name,
        "logs_analyzed": len(logs),
        "analysis_period_days": days,
        **insights
    }


@router.post("/symptom-advice")
async def get_symptom_advice(
    request: SymptomRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Get AI advice for a specific symptom
    
    - **symptom**: The symptom you're experiencing (e.g., "headache", "fever")
    - **severity**: mild, moderate, or severe
    """
    advice = await AIService.get_symptom_advice(
        symptom=request.symptom,
        severity=request.severity
    )
    
    return advice


@router.post("/chat")
async def chat_with_assistant(
    request: ChatRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Chat with AI health assistant
    
    - **message**: Your question or message
    - **conversation_history**: Previous messages (optional)
    """
    response = await AIService.chat_with_health_assistant(
        user=current_user,
        message=request.message,
        conversation_history=request.conversation_history
    )
    
    return response


@router.get("/sleep-analysis")
async def analyze_sleep_patterns(
    current_user: User = Depends(get_current_user)
):
    """Analyze sleep patterns and provide recommendations"""
    
    # Get logs with sleep data
    logs = await HealthLog.find(
        HealthLog.user_id == str(current_user.id),
        HealthLog.sleep_hours != None
    ).sort("-log_date").limit(30).to_list()
    
    if not logs:
        return {"message": "No sleep data available"}
    
    # Calculate averages
    avg_sleep = sum(log.sleep_hours for log in logs) / len(logs)
    avg_quality = sum(log.sleep_quality for log in logs) / len(logs)
    
    return {
        "average_sleep_hours": round(avg_sleep, 1),
        "average_sleep_quality": round(avg_quality, 1),
        "total_nights_tracked": len(logs),
        "recommendation": "Adults should aim for 7-9 hours of quality sleep per night." if avg_sleep < 7 else "Your sleep duration looks good!",
        "insights": f"You're averaging {avg_sleep:.1f} hours of sleep with a quality rating of {avg_quality:.1f}/10."
    }


@router.get("/saved-insights")
async def get_saved_insights(current_user: User = Depends(get_current_user)):
    """Get saved insights for current user"""
    insights = await HealthInsight.find(
        HealthInsight.user_id == str(current_user.id)
    ).sort("-analysis_date").to_list()
    
    return {
        "insights": [{
            "id": str(insight.id),
            "patient_name": insight.patient_name,
            "analyzed_log_ids": insight.analyzed_log_ids,
            "logs_analyzed_count": insight.logs_analyzed_count,
            "analysis_date": insight.analysis_date,
            "trends": insight.trends,
            "correlations": insight.correlations,
            "recommendations": insight.recommendations,
            "alerts": insight.alerts,
            "insights_raw": insight.insights_raw,
            "data_points_analyzed": insight.data_points_analyzed
        } for insight in insights]
    }


@router.post("/save-insight")
async def save_insight(
    request: Dict,
    current_user: User = Depends(get_current_user)
):
    """Save AI-generated insight to database"""
    import json as json_lib
    
    try:
        insights = request.get('insights', {})
        
        # Extract data from request
        insight = HealthInsight(
            user_id=str(current_user.id),
            patient_name=request.get('patient_name', current_user.full_name),
            analyzed_log_ids=request.get('log_ids', []),
            logs_analyzed_count=request.get('logs_analyzed', 0),
            insights_raw=request.get('insights_raw', str(request.get('insights', ''))),
            trends=insights.get('trends') if isinstance(insights, dict) else None,
            correlations=insights.get('correlations') if isinstance(insights, dict) else None,
            recommendations=insights.get('recommendations', []) if isinstance(insights, dict) else [],
            alerts=insights.get('alerts') if isinstance(insights, dict) else None,
            data_points_analyzed=request.get('data_points_analyzed', 0),
            ai_model_used="gpt-4o-mini",
            analysis_date=datetime.utcnow(),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        await insight.insert()
        
        return {
            "message": "Insight saved successfully",
            "insight_id": str(insight.id)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to save insight: {str(e)}"
        )


@router.delete("/saved-insights/{insight_id}")
async def delete_saved_insight(
    insight_id: str,
    current_user: User = Depends(get_current_user)
):
    """Delete a saved AI insight"""
    try:
        insight = await HealthInsight.get(insight_id)
        
        if not insight:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Insight not found"
            )
        
        if insight.user_id != str(current_user.id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        await insight.delete()
        
        return {"message": "Insight deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete insight: {str(e)}"
        )
