import os
import uuid
from datetime import datetime
from fastapi import UploadFile, HTTPException, status
from typing import Optional
import aiofiles

from app.config import settings


class FileService:
    """Service for handling file uploads and management"""
    
    ALLOWED_EXTENSIONS = settings.ALLOWED_EXTENSIONS.split(',')
    MAX_FILE_SIZE = settings.MAX_FILE_SIZE
    UPLOAD_DIR = settings.UPLOAD_DIR
    
    @staticmethod
    def _ensure_upload_dir():
        """Ensure upload directory exists"""
        os.makedirs(FileService.UPLOAD_DIR, exist_ok=True)
    
    @staticmethod
    def _get_file_extension(filename: str) -> str:
        """Get file extension"""
        return filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    
    @staticmethod
    def _validate_file(file: UploadFile) -> bool:
        """Validate file type and size"""
        # Check extension
        ext = FileService._get_file_extension(file.filename)
        if ext not in FileService.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File type not allowed. Allowed types: {FileService.ALLOWED_EXTENSIONS}"
            )
        
        return True
    
    @staticmethod
    async def save_file(file: UploadFile, user_id: str) -> dict:
        """Save uploaded file and return file info"""
        try:
            # Ensure directory exists
            FileService._ensure_upload_dir()
            
            # Validate file
            FileService._validate_file(file)
            
            # Generate unique filename
            ext = FileService._get_file_extension(file.filename)
            unique_filename = f"{user_id}_{uuid.uuid4().hex[:8]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
            file_path = os.path.join(FileService.UPLOAD_DIR, unique_filename)
            
            # Read file content
            content = await file.read()
            file_size = len(content)
            
            # Check file size
            if file_size > FileService.MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"File too large. Max size: {FileService.MAX_FILE_SIZE / (1024*1024):.1f}MB"
                )
            
            # Save file
            async with aiofiles.open(file_path, 'wb') as f:
                await f.write(content)
            
            return {
                "file_path": file_path,
                "file_name": file.filename,
                "unique_filename": unique_filename,
                "file_size": file_size,
                "file_type": ext
            }
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error uploading file: {str(e)}"
            )
    
    @staticmethod
    async def delete_file(file_path: str) -> bool:
        """Delete a file"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error deleting file: {str(e)}"
            )
    
    @staticmethod
    def get_file_path(filename: str) -> str:
        """Get full file path"""
        return os.path.join(FileService.UPLOAD_DIR, filename)
