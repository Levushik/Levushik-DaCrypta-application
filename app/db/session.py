"""
Basic SQLAlchemy engine and session definition
"""

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import settings

engine = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URI), pool_pre_ping=True)
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False,
                                  expire_on_commit=False, bind=engine)


async def get_db() -> AsyncSession:
    """
    AsyncSession generator
    """
    async with SessionLocal() as db:
        await db.begin()
        yield db
