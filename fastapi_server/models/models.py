from sqlmodel import SQLModel, Field, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from typing import Optional
import asyncio


# Define the SQLModel for the "songlibrary" table
class SongLibrary(SQLModel, table=True):
    songno: str = Field(primary_key=True)  # Primary key
    songname: str
    genre: str
    artist: str
    album: str
    disabled: bool = Field(default=False)


# Define the SQLModel for the "queuelibrary" table
class QueueLibrary(SQLModel, table=True):
    queueno: str = Field(primary_key=True)  # Primary key
    songno: str
    singername: str
    queuestatus: str


# Define the SQLModel for the "songsettings" table
class SongSettings(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)  # Hidden primary key
    difficulty: str
    showpopupscore: bool = Field(default=False)
    showscore: bool = Field(default=False)
    showsingersname: bool = Field(default=False)
    mainserver: str
    karaokeserver: str
