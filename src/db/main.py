from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from src.config import Config
from sqlmodel import SQLModel, create_engine
from src.campaingns.models import Campaign
from typing import AsyncGenerator


async_engine = create_async_engine(url=Config.DATABASE_URL, echo=True)


async def init_db():
    """create db connection"""
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    Session = async_sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with Session() as session:
        yield session
