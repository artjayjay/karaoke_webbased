from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Optional
import json
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import asyncio


# Database connection (async)
DATABASE_URL = "sqlite+aiosqlite:///storage/database/karaoke.db"
async_engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)


# Create all tables asynchronously
async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    print("All tables created successfully")


asyncio.run(create_tables())
