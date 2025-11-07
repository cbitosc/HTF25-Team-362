from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from datetime import datetime, timedelta

from app.models.user_model import User
from app.models.healthlog_model import HealthLog
from app.schemas.healthlog_schema import HealthLogCreate, HealthLogUpdate, HealthLogResponse
from app.utils.role_utils import get_current_user

router = APIRouter(prefix="/api/logs", tags=["Health Logs"])


@router.post("/", response_model=HealthLogResponse, status_code=status.HTTP_201_CREATED)
async def create_health_log(
    log_data: HealthLogCreate,
    current_user: User = Depends(get_current_user)
):
    """
    Create a new health log entry
    
    Track daily symptoms, vitals, mood, and lifestyle
    """
    # Use current time for log_date (allow multiple logs per day)
    log_date = log_data.log_date or datetime.utcnow()
    
    try:
        # Create log
        health_log = HealthLog(
            user_id=str(current_user.id),
            log_date=log_date,
            **log_data.dict(exclude={'log_date'}),
            created_at=datetime.utcnow()
        )
        
        await health_log.insert()
    except Exception as e:
        print(f"Error creating log: {e}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Failed to create log: {str(e)}"
        )
    
    return HealthLogResponse(
        id=str(health_log.id),
        user_id=health_log.user_id,
        log_date=health_log.log_date,
        patient_name=health_log.patient_name,
        doctor_name=health_log.doctor_name,
        temperature=health_log.temperature,
        blood_pressure_systolic=health_log.blood_pressure_systolic,
        blood_pressure_diastolic=health_log.blood_pressure_diastolic,
        has_fever=health_log.has_fever,
        has_cough=health_log.has_cough,
        has_headache=health_log.has_headache,
        has_fatigue=health_log.has_fatigue,
        has_body_pain=health_log.has_body_pain,
        has_nausea=health_log.has_nausea,
        mood=health_log.mood,
        pain_level=health_log.pain_level,
        sleep_hours=health_log.sleep_hours,
        sleep_quality=health_log.sleep_quality,
        stress_level=health_log.stress_level,
        anxiety_level=health_log.anxiety_level,
        notes=health_log.notes,
        created_at=health_log.created_at
    )


@router.get("/", response_model=List[HealthLogResponse])
async def get_my_logs(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user)
):
    """
    Get health logs for current user
    
    - **start_date**: Filter from this date
    - **end_date**: Filter until this date
    - **skip**: Pagination offset
    - **limit**: Number of results (max 100)
    """
    query = HealthLog.find(HealthLog.user_id == str(current_user.id))
    
    if start_date:
        query = query.find(HealthLog.log_date >= start_date)
    
    if end_date:
        query = query.find(HealthLog.log_date <= end_date)
    
    logs = await query.sort("-log_date").skip(skip).limit(limit).to_list()
    
    return [
        HealthLogResponse(
            id=str(log.id),
            user_id=log.user_id,
            log_date=log.log_date,
            patient_name=log.patient_name,
            doctor_name=log.doctor_name,
            temperature=log.temperature,
            blood_pressure_systolic=log.blood_pressure_systolic,
            blood_pressure_diastolic=log.blood_pressure_diastolic,
            has_fever=log.has_fever,
            has_cough=log.has_cough,
            has_headache=log.has_headache,
            has_fatigue=log.has_fatigue,
            has_body_pain=log.has_body_pain,
            has_nausea=log.has_nausea,
            mood=log.mood,
            pain_level=log.pain_level,
            sleep_hours=log.sleep_hours,
            sleep_quality=log.sleep_quality,
            stress_level=log.stress_level,
            anxiety_level=log.anxiety_level,
            notes=log.notes,
            created_at=log.created_at
        )
        for log in logs
    ]


@router.get("/today", response_model=HealthLogResponse)
async def get_today_log(current_user: User = Depends(get_current_user)):
    """Get today's health log"""
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)
    
    log = await HealthLog.find_one(
        HealthLog.user_id == str(current_user.id),
        HealthLog.log_date >= today_start,
        HealthLog.log_date < today_end
    )
    
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No log entry for today"
        )
    
    return HealthLogResponse(
        id=str(log.id),
        user_id=log.user_id,
        log_date=log.log_date,
        temperature=log.temperature,
        mood=log.mood,
        sleep_hours=log.sleep_hours,
        has_fever=log.has_fever,
        has_headache=log.has_headache,
        created_at=log.created_at
    )


@router.get("/{log_id}", response_model=HealthLogResponse)
async def get_log(
    log_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get a specific health log by ID"""
    log = await HealthLog.get(log_id)
    
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Log not found"
        )
    
    if log.user_id != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    return HealthLogResponse(
        id=str(log.id),
        user_id=log.user_id,
        log_date=log.log_date,
        temperature=log.temperature,
        mood=log.mood,
        sleep_hours=log.sleep_hours,
        has_fever=log.has_fever,
        has_headache=log.has_headache,
        created_at=log.created_at
    )


@router.put("/{log_id}", response_model=HealthLogResponse)
async def update_log(
    log_id: str,
    update_data: HealthLogUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update a health log entry"""
    log = await HealthLog.get(log_id)
    
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Log not found"
        )
    
    if log.user_id != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Update fields
    update_dict = update_data.dict(exclude_unset=True)
    for field, value in update_dict.items():
        if hasattr(log, field):
            setattr(log, field, value)
    
    log.updated_at = datetime.utcnow()
    await log.save()
    
    return HealthLogResponse(
        id=str(log.id),
        user_id=log.user_id,
        log_date=log.log_date,
        temperature=log.temperature,
        mood=log.mood,
        sleep_hours=log.sleep_hours,
        has_fever=log.has_fever,
        has_headache=log.has_headache,
        created_at=log.created_at
    )


@router.delete("/{log_id}")
async def delete_log(
    log_id: str,
    current_user: User = Depends(get_current_user)
):
    """Delete a health log entry"""
    log = await HealthLog.get(log_id)
    
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Log not found"
        )
    
    if log.user_id != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    await log.delete()
    
    return {"message": "Log deleted successfully"}
