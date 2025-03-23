from fastapi import FastAPI, APIRouter, HTTPException, File, UploadFile, Form
from fastapi.responses import JSONResponse
from sqlmodel import SQLModel, Field, select
from models.models import (
    SongLibrary,
    QueueLibrary,
    SongSettings,
)  # Assuming you have this model defined
from utils.databaseconn import (
    DATABASE_URL,
    AsyncSessionLocal,
)  # Assuming you have this setup
from typing import Optional
import os
import asyncio

router = APIRouter()


# Function to create a directory if it doesn't exist
def recreate_directory(directory: str):
    """
    Deletes the directory (if it exists) and recreates it.
    """
    # Delete the directory if it exists
    if os.path.exists(directory):
        for root, dirs, files in os.walk(directory, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                os.rmdir(os.path.join(root, dir))
        os.rmdir(directory)
        print(f"Deleted folder: {directory}")

    # Create the directory
    os.makedirs(directory, exist_ok=True)
    print(f"Created folder: {directory}")


# Function to save uploaded files in chunks
async def save_uploaded_file_chunked(file: UploadFile, destination: str):
    with open(destination, "wb") as buffer:
        while chunk := await file.read(1024 * 1024):  # Read in chunks of 1MB
            buffer.write(chunk)


@router.get("/displaysettings")
async def displaysettings():
    try:
        async with AsyncSessionLocal() as session:
            # Fetch the first (or only) SongSettings entry
            statement = select(SongSettings)
            result = await session.execute(statement)
            settings_entry = result.scalars().first()

            # If no entry exists, create a new one with default values
            if not settings_entry:
                settings_entry = SongSettings(
                    difficulty="easy",  # Default values
                    showpopupscore=True,
                    showscore=True,
                    showsingersname=True,
                    mainserver="defaultmainserver",
                    karaokeserver="defaultkaraokeserver",
                )
                session.add(settings_entry)
                await session.commit()
                await session.refresh(settings_entry)

            # Return the settings entry as a JSON response
            return JSONResponse(
                content={
                    "difficulty": settings_entry.difficulty,
                    "showpopupscore": settings_entry.showpopupscore,
                    "showscore": settings_entry.showscore,
                    "showsingersname": settings_entry.showsingersname,
                    "mainserver": settings_entry.mainserver,
                    "karaokeserver": settings_entry.karaokeserver,
                }
            )

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/updatesettings")
async def updatesettings(
    difficulty: Optional[str] = Form(None),
    showpopupscore: Optional[str] = Form(None),
    showscore: Optional[str] = Form(None),
    showsingersname: Optional[str] = Form(None),
    scorevidid: Optional[UploadFile] = File(None),
    scoreapplauseid: Optional[UploadFile] = File(None),
    mainserver: Optional[str] = Form(None),
    karaokeserver: Optional[str] = Form(None),
):
    try:
        async with AsyncSessionLocal() as session:
            # Fetch the first (or only) SongSettings entry
            statement = select(SongSettings)
            result = await session.execute(statement)
            settings_entry = result.scalars().first()

            # If no entry exists, create a new one
            if not settings_entry:
                settings_entry = SongSettings(
                    difficulty="easy",  # Default values
                    showpopupscore=True,
                    showscore=True,
                    showsingersname=True,
                    mainserver="defaultmainserver",
                    karaokeserver="defaultkaraokeserver",
                )
                session.add(settings_entry)
                await session.commit()

            # Update only the fields that are provided in the request
            if difficulty is not None:
                settings_entry.difficulty = difficulty

            # Convert string values to boolean
            if showpopupscore is not None:
                settings_entry.showpopupscore = showpopupscore.lower() == "true"
            if showscore is not None:
                settings_entry.showscore = showscore.lower() == "true"
            if showsingersname is not None:
                settings_entry.showsingersname = showsingersname.lower() == "true"
            if mainserver is not None:
                settings_entry.mainserver = mainserver
            if karaokeserver is not None:
                settings_entry.karaokeserver = karaokeserver

            # Commit the changes to the database
            await session.commit()
            await session.refresh(settings_entry)

            # Handle file uploads (scorevidid and scoreapplauseid)
            if scorevidid:
                # Check if the file is either a video or an image
                if not (
                    scorevidid.content_type.startswith("video/")
                    or scorevidid.content_type.startswith("image/")
                ):
                    raise HTTPException(
                        status_code=400,
                        detail="scorevidid must be a video file or an image file (e.g., for background)",
                    )

                scorevid_directory = os.path.join(
                    "storage", "files", "settings", "scorevid"
                )
                await asyncio.to_thread(recreate_directory, scorevid_directory)

                # Determine the file extension based on content type
                if scorevidid.content_type.startswith("video/"):
                    file_extension = (
                        ".mp4" if scorevidid.content_type == "video/mp4" else ".mkv"
                    )
                elif scorevidid.content_type.startswith("image/"):
                    file_extension = (
                        ".jpg" if scorevidid.content_type == "image/jpeg" else ".png"
                    )

                # Construct the file path
                file_path = os.path.join(
                    scorevid_directory, f"scorevid{file_extension}"
                )

                # Save the file
                await save_uploaded_file_chunked(scorevidid, file_path)

            if scoreapplauseid:
                if scoreapplauseid.content_type != "audio/wav":
                    raise HTTPException(
                        status_code=400,
                        detail="scoreapplauseid must be a .wav file",
                    )

                scoreapplause_directory = os.path.join(
                    "storage", "files", "settings", "scoreapplause"
                )
                await asyncio.to_thread(recreate_directory, scoreapplause_directory)

                file_extension = ".wav"
                file_path = os.path.join(
                    scoreapplause_directory, f"scoreapplause{file_extension}"
                )
                await save_uploaded_file_chunked(scoreapplauseid, file_path)

            return JSONResponse(
                content={"message": "SongSettings updated successfully"}
            )

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
