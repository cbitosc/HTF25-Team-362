from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER
from datetime import datetime
from typing import List
import io

from app.models.user_model import User
from app.models.report_model import HealthReport
from app.models.healthlog_model import HealthLog


class PDFService:
    """Service for generating PDF health summaries"""
    
    @staticmethod
    def generate_health_summary(user: User, reports: List[HealthReport], logs: List[HealthLog]) -> bytes:
        """Generate comprehensive health summary PDF"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=24, 
                                     textColor=colors.HexColor('#2C3E50'), alignment=TA_CENTER, spaceAfter=30)
        heading_style = ParagraphStyle('CustomHeading', parent=styles['Heading2'], fontSize=16,
                                       textColor=colors.HexColor('#34495E'), spaceAfter=12)
        
        elements.append(Paragraph("Personal Health Record Summary", title_style))
        elements.append(Spacer(1, 0.3*inch))
        
        elements.append(Paragraph("Patient Information", heading_style))
        patient_data = [
            ['Full Name:', user.full_name or 'N/A'],
            ['Email:', user.email or 'N/A'],
            ['Phone:', user.phone or 'N/A'],
            ['Blood Group:', user.blood_group or 'N/A'],
            ['Date of Birth:', user.date_of_birth.strftime('%Y-%m-%d') if user.date_of_birth else 'N/A'],
            ['Report Generated:', datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')]
        ]
        
        patient_table = Table(patient_data, colWidths=[2*inch, 4*inch])
        patient_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ECF0F1')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        elements.append(patient_table)
        elements.append(Spacer(1, 0.3*inch))
        
        if reports:
            elements.append(Paragraph(f"Health Reports ({len(reports)})", heading_style))
            report_data = [['Date', 'Type', 'Title']]
            for report in reports[:10]:
                report_data.append([
                    report.report_date.strftime('%Y-%m-%d') if report.report_date else 'N/A',
                    report.report_type.value.replace('_', ' ').title() if report.report_type else 'N/A',
                    report.title[:30] if report.title else 'N/A'
                ])
            report_table = Table(report_data, colWidths=[2*inch, 2*inch, 3*inch])
            report_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
            ]))
            elements.append(report_table)
            elements.append(Spacer(1, 0.3*inch))
        
        if logs:
            elements.append(Paragraph(f"Health Logs ({len(logs)} entries)", heading_style))
            log_data = [['Date', 'Temperature', 'BP', 'Mood']]
            for log in logs[:15]:
                bp = f"{log.blood_pressure_systolic}/{log.blood_pressure_diastolic}" if log.blood_pressure_systolic else 'N/A'
                temp = f"{log.temperature:.1f}°C" if log.temperature else 'N/A'
                log_data.append([
                    log.log_date.strftime('%Y-%m-%d') if log.log_date else 'N/A',
                    temp,
                    bp,
                    log.mood.value if log.mood else 'N/A'
                ])
            log_table = Table(log_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1*inch])
            log_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2ECC71')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
            ]))
            elements.append(log_table)
        
        elements.append(Spacer(1, 0.3*inch))
        footer = Paragraph("<i>This is a confidential medical document. Handle with care.</i>", styles['Normal'])
        elements.append(footer)
        
        doc.build(elements)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes

