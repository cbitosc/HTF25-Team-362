from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from typing import Optional
import logging

from app.config import settings

logger = logging.getLogger(__name__)


class Database:
    client: Optional[AsyncIOMotorClient] = None # type: ignore
    
    @classmethod
    async def connect_db(cls):
        """Connect to MongoDB database"""
        try:
            cls.client = AsyncIOMotorClient(settings.MONGODB_URL)
            
            # Import models here to avoid circular imports
            from app.models.user_model import User
            from app.models.report_model import HealthReport
            from app.models.healthlog_model import HealthLog
            from app.models.insight_model import HealthInsight
            
            # Initialize beanie with models
            await init_beanie(
                database=cls.client[settings.DATABASE_NAME],
                document_models=[User, HealthReport, HealthLog, HealthInsight]
            )
            
            logger.info("Connected to MongoDB successfully!")
            print(f"Database connected: {settings.DATABASE_NAME}")
            
        except Exception as e:
            logger.error(f"Database connection failed: {str(e)}")
            print(f"Database connection failed: {str(e)}")
            raise e
    
    @classmethod
    async def close_db(cls):
        """Close database connection"""
        if cls.client:
            cls.client.close()
            logger.info("Database connection closed")
            print("Database connection closed")


# Database instance
db = Database()
