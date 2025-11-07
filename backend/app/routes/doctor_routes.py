from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.models.user_model import User, UserRole
from app.models.report_model import HealthReport
from app.models.healthlog_model import HealthLog
from app.utils.role_utils import get_current_user, require_role

router = APIRouter(prefix="/api/doctor", tags=["Doctor"])


@router.get("/patients", response_model=List[dict])
async def get_my_patients(
    current_user: User = Depends(require_role([UserRole.DOCTOR]))
):
    """
    Get list of patients assigned to current doctor
    """
    # Get users where assigned_doctor_id matches current doctor
    patients = await User.find(
        User.assigned_doctor_id == str(current_user.id),
        User.role == UserRole.PATIENT
    ).to_list()
    
    return [
        {
            "id": str(patient.id),
            "full_name": patient.full_name,
            "email": patient.email,
            "phone": patient.phone,
            "blood_group": patient.blood_group,
            "created_at": patient.created_at
        }
        for patient in patients
    ]


@router.get("/patient/{patient_id}/reports")
async def get_patient_reports(
    patient_id: str,
    current_user: User = Depends(require_role([UserRole.DOCTOR]))
):
    """
    Get all reports for a specific patient (doctor access)
    """
    # Verify patient is assigned to this doctor
    patient = await User.get(patient_id)
    
    if not patient or patient.assigned_doctor_id != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this patient's records"
        )
    
    reports = await HealthReport.find(
        HealthReport.user_id == patient_id
    ).sort("-created_at").to_list()
    
    return reports


@router.get("/patient/{patient_id}/logs")
async def get_patient_logs(
    patient_id: str,
    limit: int = 30,
    current_user: User = Depends(require_role([UserRole.DOCTOR]))
):
    """
    Get health logs for a specific patient (doctor access)
    """
    patient = await User.get(patient_id)
    
    if not patient or patient.assigned_doctor_id != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this patient's records"
        )
    
    logs = await HealthLog.find(
        HealthLog.user_id == patient_id
    ).sort("-log_date").limit(limit).to_list()
    
    return logs
