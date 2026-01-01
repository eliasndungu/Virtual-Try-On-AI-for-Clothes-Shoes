"""Database service for managing database operations."""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator

from ..core.config import settings
from ..models.database import Base


class DatabaseService:
    """Service for database operations."""
    
    def __init__(self):
        self.engine = create_async_engine(
            settings.DATABASE_URL,
            echo=False,
            future=True
        )
        
        self.async_session_maker = sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
    
    async def init_db(self):
        """Initialize database tables."""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get database session."""
        async with self.async_session_maker() as session:
            try:
                yield session
            finally:
                await session.close()


db_service = DatabaseService()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting database session."""
    async for session in db_service.get_session():
        yield session
