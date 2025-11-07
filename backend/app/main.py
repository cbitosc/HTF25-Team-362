from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import uvicorn

from app.config import settings
from app.database.db import db
from app.services.auth_service import AuthService

# Import all routes
from app.routes.auth_routes import router as auth_router
from app.routes.report_routes import router as report_router
from app.routes.healthlog_routes import router as healthlog_router
from app.routes.doctor_routes import router as doctor_router
from app.routes.ai_routes import router as ai_router


# Lifespan context manager for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("=" * 50)
    print("Starting Personal Health Record System...")
    print("=" * 50)
    
    # Connect to database
    await db.connect_db()
    
    # Create admin user if not exists
    try:
        await AuthService.create_admin_user()
    except Exception as e:
        print(f"Warning: Error creating admin user: {e}")
    
    print("=" * 50)
    print("Application started successfully!")
    print(f"API Docs: http://{settings.HOST}:{settings.PORT}/docs")
    print(f"Health Check: http://{settings.HOST}:{settings.PORT}/health")
    print("=" * 50)
    
    yield
    
    # Shutdown
    print("\n" + "=" * 50)
    print("Shutting down application...")
    print("=" * 50)
    await db.close_db()
    print("Shutdown complete")


# Initialize FastAPI app with lifespan
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    Personal Health Record Management System with AI Insights
    
    ## Features
    * 🔐 User Authentication & Authorization
    * 📊 Health Logs Tracking
    * 📄 Medical Reports Management
    * 🤖 AI-Powered Health Insights
    * 👨‍⚕️ Doctor-Patient Access Control
    * 📥 Export Health Summary as PDF
    
    ## Authentication
    Use the 🔒 Authorize button to add your JWT token.
    """,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include all routers
app.include_router(auth_router)
app.include_router(report_router)
app.include_router(healthlog_router)
app.include_router(doctor_router)
app.include_router(ai_router)


@app.get("/", tags=["Root"])
def root():
    """Welcome endpoint with API information"""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "status": "running",
        "documentation": {
            "swagger_ui": "/docs",
            "redoc": "/redoc"
        },
        "endpoints": {
            "authentication": "/api/auth",
            "health_reports": "/api/reports",
            "health_logs": "/api/logs",
            "doctor_access": "/api/doctor",
            "ai_insights": "/api/ai"
        },
        "quick_start": {
            "1": "Register: POST /api/auth/register",
            "2": "Login: POST /api/auth/login",
            "3": "Get Token: Copy access_token from login response",
            "4": "Authorize: Click 🔒 button and paste token",
            "5": "Start using API endpoints!"
        }
    }


@app.get("/health", tags=["Health Check"])
async def health_check():
    """Health check endpoint to verify API and database status"""
    db_status = "connected" if db.client is not None else "disconnected"
    
    return {
        "status": "healthy",
        "database": db_status,
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": "development" if settings.DEBUG else "production"
    }


@app.get("/stats", tags=["Statistics"])
async def get_stats():
    """Get API statistics"""
    from app.models.user_model import User
    from app.models.report_model import HealthReport
    from app.models.healthlog_model import HealthLog
    
    try:
        total_users = await User.count()
        total_reports = await HealthReport.count()
        total_logs = await HealthLog.count()
        
        return {
            "total_users": total_users,
            "total_health_reports": total_reports,
            "total_health_logs": total_logs,
            "api_version": settings.APP_VERSION
        }
    except Exception as e:
        return {
            "error": "Database not connected",
            "message": str(e)
        }


@app.get("/test-users", tags=["Debug"])
async def test_users():
    """Test endpoint to check users in database"""
    from app.models.user_model import User
    try:
        users = await User.find_all().to_list()
        return {
            "users": [{"email": u.email, "full_name": u.full_name, "role": u.role.value} for u in users]
        }
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
