from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from typing import List, Optional
from datetime import datetime
import io

from app.models.user_model import User
from app.models.report_model import HealthReport, ReportType
from app.models.healthlog_model import HealthLog
from app.schemas.report_schema import ReportCreate, ReportUpdate, ReportResponse
from app.utils.role_utils import get_current_user
from app.services.file_service import FileService
from app.services.pdf_service import PDFService

router = APIRouter(prefix="/api/reports", tags=["Health Reports"])


@router.post("/upload", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
async def upload_report(
    file: UploadFile = File(...),
    report_type: ReportType = Form(...),
    title: str = Form(...),
    description: Optional[str] = Form(None),
    doctor_name: Optional[str] = Form(None),
    hospital_name: Optional[str] = Form(None),
    diagnosis: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user)
):
    """
    Upload a health report/document
    
    - **file**: Medical report file (PDF, JPG, PNG, DOCX)
    - **report_type**: Type of report (lab_test, prescription, xray, etc.)
    - **title**: Report title
    - **description**: Optional description
    """
    # Upload file
    file_info = await FileService.save_file(file, str(current_user.id))
    
    # Create report document
    report = HealthReport(
        user_id=str(current_user.id),
        uploaded_by=str(current_user.id),
        report_type=report_type,
        title=title,
        description=description,
        file_path=file_info["file_path"],
        file_name=file_info["file_name"],
        file_size=file_info["file_size"],
        file_type=file_info["file_type"],
        doctor_name=doctor_name,
        hospital_name=hospital_name,
        diagnosis=diagnosis,
        report_date=datetime.utcnow(),
        created_at=datetime.utcnow()
    )
    
    await report.insert()
    
    return ReportResponse(
        id=str(report.id),
        user_id=report.user_id,
        report_type=report.report_type,
        title=report.title,
        description=report.description,
        report_date=report.report_date,
        file_name=report.file_name,
        file_type=report.file_type,
        doctor_name=report.doctor_name,
        created_at=report.created_at
    )


@router.get("/export-summary")
async def export_health_summary(
    current_user: User = Depends(get_current_user)
):
    """
    Export complete health summary as PDF
    """
    try:
        # Get user's reports and logs
        reports = await HealthReport.find(
            HealthReport.user_id == str(current_user.id)
        ).sort("-report_date").to_list()
        
        logs = await HealthLog.find(
            HealthLog.user_id == str(current_user.id)
        ).sort("-log_date").limit(30).to_list()
        
        # Generate PDF
        pdf_bytes = PDFService.generate_health_summary(
            user=current_user,
            reports=reports,
            logs=logs
        )
        
        # Return as downloadable file
        filename = f"health_summary_{current_user.full_name.replace(' ', '_')}_{datetime.utcnow().strftime('%Y%m%d')}.pdf"
        
        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
    except Exception as e:
        print(f"Error generating PDF: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate health report: {str(e)}"
        )


@router.get("/", response_model=List[ReportResponse])
async def get_my_reports(
    report_type: Optional[ReportType] = None,
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_user)
):
    """
    Get all reports for current user
    
    - **report_type**: Filter by report type (optional)
    - **skip**: Pagination offset
    - **limit**: Number of results
    """
    query = HealthReport.find(HealthReport.user_id == str(current_user.id))
    
    if report_type:
        query = query.find(HealthReport.report_type == report_type)
    
    reports = await query.sort("-created_at").skip(skip).limit(limit).to_list()
    
    return [
        ReportResponse(
            id=str(report.id),
            user_id=report.user_id,
            report_type=report.report_type,
            title=report.title,
            description=report.description,
            report_date=report.report_date,
            file_name=report.file_name,
            file_type=report.file_type,
            doctor_name=report.doctor_name,
            created_at=report.created_at
        )
        for report in reports
    ]


@router.get("/{report_id}", response_model=ReportResponse)
async def get_report(
    report_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get a specific report by ID"""
    report = await HealthReport.get(report_id)
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    
    # Check if user owns this report
    if report.user_id != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    return ReportResponse(
        id=str(report.id),
        user_id=report.user_id,
        report_type=report.report_type,
        title=report.title,
        description=report.description,
        report_date=report.report_date,
        file_name=report.file_name,
        file_type=report.file_type,
        doctor_name=report.doctor_name,
        created_at=report.created_at
    )


@router.put("/{report_id}", response_model=ReportResponse)
async def update_report(
    report_id: str,
    update_data: ReportUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update report details (not the file)"""
    report = await HealthReport.get(report_id)
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    
    if report.user_id != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Update fields
    update_dict = update_data.dict(exclude_unset=True)
    for field, value in update_dict.items():
        if hasattr(report, field):
            setattr(report, field, value)
    
    report.updated_at = datetime.utcnow()
    await report.save()
    
    return ReportResponse(
        id=str(report.id),
        user_id=report.user_id,
        report_type=report.report_type,
        title=report.title,
        description=report.description,
        report_date=report.report_date,
        file_name=report.file_name,
        file_type=report.file_type,
        doctor_name=report.doctor_name,
        created_at=report.created_at
    )


@router.delete("/{report_id}")
async def delete_report(
    report_id: str,
    current_user: User = Depends(get_current_user)
):
    """Delete a report"""
    report = await HealthReport.get(report_id)
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    
    if report.user_id != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Delete file
    await FileService.delete_file(report.file_path)
    
    # Delete document
    await report.delete()
    
    return {"message": "Report deleted successfully"}
