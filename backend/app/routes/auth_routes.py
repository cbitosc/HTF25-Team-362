from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict

from app.schemas.user_schema import UserRegister, UserLogin, TokenResponse, UserResponse, UserUpdate
from app.services.auth_service import AuthService
from app.models.user_model import User
from app.utils.role_utils import get_current_user

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister):
    """
    Register a new user
    
    - **email**: Valid email address
    - **password**: Minimum 8 characters
    - **full_name**: User's full name
    - **role**: patient, doctor, or admin (default: patient)
    """
    return await AuthService.register_user(user_data)


@router.post("/login", response_model=TokenResponse)
async def login(login_data: UserLogin):
    """
    Login user and get access token
    
    - **email**: Registered email
    - **password**: User password
    """
    return await AuthService.login_user(login_data)


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """
    Get current user profile
    
    Requires authentication token
    """
    return UserResponse(
        id=str(current_user.id),
        email=current_user.email,
        full_name=current_user.full_name,
        phone=current_user.phone,
        role=current_user.role,
        is_active=current_user.is_active,
        created_at=current_user.created_at
    )


@router.put("/me", response_model=UserResponse)
async def update_profile(
    update_data: UserUpdate,
    current_user: User = Depends(get_current_user)
):
    """
    Update current user profile
    
    Requires authentication token
    """
    updated_user = await AuthService.update_user_profile(
        str(current_user.id),
        update_data.dict(exclude_unset=True)
    )
    
    return UserResponse(
        id=str(updated_user.id),
        email=updated_user.email,
        full_name=updated_user.full_name,
        phone=updated_user.phone,
        role=updated_user.role,
        is_active=updated_user.is_active,
        created_at=updated_user.created_at
    )


@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """
    Logout user (client should delete token)
    
    Requires authentication token
    """
    return {"message": "Successfully logged out"}


@router.get("/verify-token")
async def verify_token(current_user: User = Depends(get_current_user)):
    """
    Verify if token is valid
    
    Requires authentication token
    """
    return {
        "valid": True,
        "user_id": str(current_user.id),
        "email": current_user.email,
        "role": current_user.role
    }
