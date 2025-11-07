from datetime import datetime, timedelta
from fastapi import HTTPException, status
from typing import Optional

from app.models.user_model import User, UserRole
from app.schemas.user_schema import UserRegister, UserLogin, TokenResponse, UserResponse
from app.utils.auth_utils import hash_password, verify_password, create_access_token, create_refresh_token
from app.config import settings


class AuthService:
    """Authentication service for user registration and login"""
    
    @staticmethod
    async def register_user(user_data: UserRegister) -> TokenResponse:
        """Register a new user"""
        
        # Check if user already exists
        existing_user = await User.find_one(User.email == user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Hash password
        hashed_password = hash_password(user_data.password)
        
        # Create user
        user = User(
            email=user_data.email,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
            phone=user_data.phone,
            role=user_data.role,
            is_active=True,
            created_at=datetime.utcnow()
        )
        
        await user.insert()
        
        # Create tokens
        access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email, "role": user.role.value}
        )
        
        refresh_token = create_refresh_token(
            data={"sub": str(user.id)}
        )
        
        # Create user response
        user_response = UserResponse(
            id=str(user.id),
            email=user.email,
            full_name=user.full_name,
            phone=user.phone,
            role=user.role,
            is_active=user.is_active,
            created_at=user.created_at
        )
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user=user_response
        )
    
    
    @staticmethod
    async def login_user(login_data: UserLogin) -> TokenResponse:
        """Login user and return tokens"""
        
        # Find user by email
        user = await User.find_one(User.email == login_data.email)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        # Verify password
        if not verify_password(login_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        # Check if user is active
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is inactive. Please contact support."
            )
        
        # Update last login
        user.last_login = datetime.utcnow()
        await user.save()
        
        # Create tokens
        access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email, "role": user.role.value}
        )
        
        refresh_token = create_refresh_token(
            data={"sub": str(user.id)}
        )
        
        # Create user response
        user_response = UserResponse(
            id=str(user.id),
            email=user.email,
            full_name=user.full_name,
            phone=user.phone,
            role=user.role,
            is_active=user.is_active,
            created_at=user.created_at
        )
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user=user_response
        )
    
    
    @staticmethod
    async def get_user_profile(user_id: str) -> User:
        """Get user profile by ID"""
        user = await User.get(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return user
    
    
    @staticmethod
    async def update_user_profile(user_id: str, update_data: dict) -> User:
        """Update user profile"""
        user = await User.get(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Update fields
        for field, value in update_data.items():
            if value is not None and hasattr(user, field):
                setattr(user, field, value)
        
        user.updated_at = datetime.utcnow()
        await user.save()
        
        return user
    
    
    @staticmethod
    async def create_admin_user():
        """Create admin user if not exists (for initial setup)"""
        admin_email = settings.ADMIN_EMAIL
        
        # Check if admin exists
        existing_admin = await User.find_one(User.email == admin_email)
        
        if not existing_admin:
            admin = User(
                email=admin_email,
                hashed_password=hash_password(settings.ADMIN_PASSWORD),
                full_name="System Administrator",
                role=UserRole.ADMIN,
                is_active=True,
                is_verified=True,
                created_at=datetime.utcnow()
            )
            await admin.insert()
            print(f"✅ Admin user created: {admin_email}")
        else:
            print(f"ℹ️  Admin user already exists: {admin_email}")
