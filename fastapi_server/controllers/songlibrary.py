from fastapi import FastAPI, APIRouter, HTTPException, File, UploadFile, Form
from fastapi.responses import JSONResponse
from sqlmodel import SQLModel, Field, select
from models.models import (
    SongLibrary,
    QueueLibrary,
)  # Assuming you have this model defined
from utils.databaseconn import (
    DATABASE_URL,
    AsyncSessionLocal,
)  # Assuming you have this setup
from typing import Optional
import os
import asyncio

# Define the router
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


# Function to fetch songs asynchronously
async def display_songtable(
    column: Optional[str] = None,
    value: Optional[str] = None,
    limit: int = 10,
    offset: int = 0,
):
    async with AsyncSessionLocal() as session:
        # Start with a base query to exclude disabled records
        statement = select(SongLibrary).where(SongLibrary.disabled == False)

        # Apply the filter if column and value are provided
        if column and value:
            if column == "songno":
                condition = SongLibrary.songno == value
            elif column == "songname":
                condition = SongLibrary.songname == value
            elif column == "genre":
                condition = SongLibrary.genre == value
            elif column == "artist":
                condition = SongLibrary.artist == value
            elif column == "album":
                condition = SongLibrary.album == value
            else:
                print(f"Invalid column: {column}")
                return None  # Return None if the column is invalid

            statement = statement.where(condition)

        # Apply pagination (limit and offset)
        statement = statement.limit(limit).offset(offset)

        # Execute the query
        result = await session.execute(statement)  # Fixed: Use execute instead of exec
        songs = result.scalars().all()  # Use scalars() to get model instances

        # Convert songs to a list of dictionaries
        songs_dict = [
            {
                "songno": song.songno,
                "songname": song.songname,
                "genre": song.genre,
                "artist": song.artist,
                "album": song.album,
            }
            for song in songs
        ]
        return songs_dict


# Function to insert a song asynchronously
async def insert_to_songtable(songname, genre, artist, album):
    async with AsyncSessionLocal() as session:
        # Hardcoded song data for testing
        new_song = SongLibrary(
            songname=songname,
            genre=genre,
            artist=artist,
            album=album,
        )

        # Check if there are any disabled records
        statement = select(SongLibrary).where(SongLibrary.disabled == True).limit(1)
        result = await session.execute(statement)  # Fixed: Use execute instead of exec
        disabled_song = (
            result.scalars().first()
        )  # Use scalars() to get the first result

        if disabled_song:
            # Reuse the disabled record by updating it
            disabled_song.songname = new_song.songname
            disabled_song.genre = new_song.genre
            disabled_song.artist = new_song.artist
            disabled_song.album = new_song.album
            disabled_song.disabled = False  # Mark as active
            await session.commit()
            await session.refresh(disabled_song)
            print("Reused disabled record:", disabled_song.songno)
        else:
            # No disabled records, check if the table has reached 9999 active records
            statement = select(SongLibrary).where(SongLibrary.disabled == False)
            result = await session.execute(
                statement
            )  # Fixed: Use execute instead of exec
            active_songs = result.scalars().all()  # Use scalars() to get all results

            if len(active_songs) >= 9999:
                # Table has reached 9999 active records, add to SongLibrary2
                # await insert_song_to_table2(new_song, session)
                print("Full table")
            else:
                # Add the new data to the current table
                # Generate the next available ID
                statement = (
                    select(SongLibrary).order_by(SongLibrary.songno.desc()).limit(1)
                )
                result = await session.execute(
                    statement
                )  # Fixed: Use execute instead of exec
                last_song = (
                    result.scalars().first()
                )  # Use scalars() to get the first result

                if last_song:
                    last_id = int(last_song.songno)
                    new_song.songno = (
                        f"{last_id + 1:04}"  # Format as 4-digit string (e.g., "0001")
                    )
                else:
                    # Table is empty, start from "0001"
                    new_song.songno = "0001"

                session.add(new_song)
                await session.commit()
                await session.refresh(new_song)
                print("Added new record:", new_song.songno)


async def update_song(
    songno: str,
    songname: Optional[str] = None,
    genre: Optional[str] = None,
    artist: Optional[str] = None,
    album: Optional[str] = None,
    disabled: Optional[bool] = None,
):
    async with AsyncSessionLocal() as session:
        # Find the song by ID and ensure it is not disabled
        statement = (
            select(SongLibrary)
            .where(SongLibrary.songno == songno)
            .where(SongLibrary.disabled == False)  # Only fetch active songs
        )
        result = await session.execute(statement)
        song = result.scalars().first()  # Use scalars() to get the first result

        if song:
            # Update only the fields that are provided (not None)
            if songname is not None:
                song.songname = songname
            if genre is not None:
                song.genre = genre
            if artist is not None:
                song.artist = artist
            if album is not None:
                song.album = album
            if disabled is not None:
                song.disabled = disabled

            await session.commit()
            await session.refresh(song)
            print("Updated record:", song.songno)
            return song
        else:
            raise Exception("Song not found")


async def delete_song(songno: str):
    try:
        async with AsyncSessionLocal() as session:
            # Find the song by ID
            statement = select(SongLibrary).where(SongLibrary.songno == songno)
            result = await session.execute(
                statement
            )  # Fixed: Use execute instead of exec
            song = result.scalars().first()  # Use scalars() to get the first result

            if song:
                # Mark the song as disabled
                song.disabled = True
                await session.commit()
                await session.refresh(song)
                print("Disabled record:", song.songno)

                statement = select(QueueLibrary).where(QueueLibrary.songno == songno)
                result = await session.execute(statement)
                queue_entry = result.scalars().first()

                if queue_entry:
                    # Delete the queue entry
                    await session.delete(queue_entry)
                    await session.commit()
                    return JSONResponse(
                        content={"message": "Queue deleted successfully"}
                    )
            else:
                raise Exception("Song not found")

    except Exception as e:
        print("................ ", e)


# Endpoint to display songs
@router.get("/displaysongs/{limit}/{offset}")
async def displaysongs(limit: int, offset: int):
    if offset <= 0:
        offset = 0
    if offset > 0:
        offset = offset - 1
    try:
        songsdata = await display_songtable(limit=limit, offset=offset)
        return JSONResponse(content={"songs": songsdata})
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


async def validate_files(
    file1: Optional[UploadFile] = None, file2: Optional[UploadFile] = None
):
    # If both files are None, skip validation (for /updatesongs)
    if file1 is None and file2 is None:
        return None

    # If only one file is provided, return an error (for /updatesongs)
    if file1 is None or file2 is None:
        return "Both file1 and file2 must be provided if either is provided"

    # Allowed MIME types
    mp4_mime_types = ["video/mp4", "audio/mp4"]  # MP4 video or audio
    wav_mime_type = "audio/wav"  # WAV audio

    # Validate file1
    if file1.size == 0:
        return "file1 is empty"
    if file1.content_type not in mp4_mime_types + [wav_mime_type]:
        return "file1 must be an MP4 video/audio or WAV audio file"
    if not file1.filename.lower().endswith((".mp4", ".wav")):
        return "file1 must have a .mp4 or .wav extension"

    # Validate file2
    if file2.size == 0:
        return "file2 is empty"
    if file1.content_type in mp4_mime_types:
        if file2.content_type != wav_mime_type or not file2.filename.lower().endswith(
            ".wav"
        ):
            return "file2 must be a WAV audio file when file1 is MP4"
    elif file1.content_type == wav_mime_type:
        if (
            file2.content_type not in mp4_mime_types
            or not file2.filename.lower().endswith(".mp4")
        ):
            return "file2 must be an MP4 video/audio file when file1 is WAV"

    return None


@router.post("/insertsongs")
async def insertsongs(
    songname: str = Form(...),
    genre: str = Form(...),
    artist: str = Form(...),
    album: str = Form(...),
    file1: UploadFile = File(...),
    file2: UploadFile = File(...),
):
    validation_result = await validate_files(file1, file2)
    if validation_result:
        return JSONResponse(content={"error": validation_result}, status_code=400)

    try:
        # Insert the song into the database
        await insert_to_songtable(songname, genre, artist, album)

        # Fetch the last inserted song to get the songno
        async with AsyncSessionLocal() as session:
            statement = (
                select(SongLibrary)
                .where(SongLibrary.disabled == False)  # Only consider active songs
                .order_by(SongLibrary.songno.desc())
                .limit(1)
            )
            result = await session.execute(statement)
            last_song = result.scalars().first()

            if last_song:
                songno = last_song.songno
                # Create a directory named after the songno
                song_directory = os.path.join("storage", "files", "songs", songno)
                await asyncio.to_thread(recreate_directory, song_directory)

                # Determine the file types and save them with appropriate names
                file1_extension = (
                    ".mp4"
                    if file1.content_type in ["video/mp4", "audio/mp4"]
                    else ".wav"
                )
                file2_extension = (
                    ".mp4"
                    if file2.content_type in ["video/mp4", "audio/mp4"]
                    else ".wav"
                )

                file1_path = os.path.join(song_directory, f"{songno}{file1_extension}")
                file2_path = os.path.join(song_directory, f"{songno}{file2_extension}")

                await save_uploaded_file_chunked(file1, file1_path)
                await save_uploaded_file_chunked(file2, file2_path)

                return JSONResponse(
                    content={"message": "Song added successfully", "songno": songno}
                )
            else:
                raise HTTPException(
                    status_code=500, detail="Failed to retrieve the last inserted song"
                )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint to update songs
@router.put("/updatesongs")
async def updatesongs(
    songno: str = Form(...),
    songname: str = Form(...),  # Optional
    genre: str = Form(...),  # Optional
    artist: str = Form(...),  # Optional
    album: str = Form(...),  # Optional
    file1: Optional[UploadFile] = File(None),  # Optional
    file2: Optional[UploadFile] = File(None),  # Optional
):
    # Validate the files (if provided)
    validation_result = await validate_files(file1, file2)
    if validation_result:
        return JSONResponse(content={"error": validation_result}, status_code=400)

    try:
        # Update the song details in the database
        await update_song(
            songno=songno, songname=songname, genre=genre, artist=artist, album=album
        )

        # If files are provided, update them
        if file1 and file2:
            # Fetch the song directory
            song_directory = os.path.join("storage", "files", "songs", songno)

            # Recreate the directory (delete if exists, then create)
            await asyncio.to_thread(recreate_directory, song_directory)

            # Determine the file types and save them with appropriate names
            file1_extension = (
                ".mp4" if file1.content_type in ["video/mp4", "audio/mp4"] else ".wav"
            )
            file2_extension = (
                ".mp4" if file2.content_type in ["video/mp4", "audio/mp4"] else ".wav"
            )

            file1_path = os.path.join(song_directory, f"{songno}{file1_extension}")
            file2_path = os.path.join(song_directory, f"{songno}{file2_extension}")

            # Save the files
            await save_uploaded_file_chunked(file1, file1_path)
            await save_uploaded_file_chunked(file2, file2_path)

            return JSONResponse(content={"message": "Song updated successfully"})
        else:
            # No files provided, only update the database
            return JSONResponse(content={"message": "Song updated successfully"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def delete_song_file(song_directory):
    # Delete the song directory and its contents if it exists
    if os.path.exists(song_directory):
        for file in os.listdir(song_directory):
            file_path = os.path.join(song_directory, file)
            os.remove(file_path)
        os.rmdir(song_directory)


# Endpoint to delete songs
@router.delete("/deletesongs/{songno}")
async def deletesongs(songno: str):
    try:
        # Fetch the song directory
        song_directory = os.path.join("storage", "files", "songs", songno)

        # Mark the song as disabled in the database
        await asyncio.to_thread(delete_song_file, song_directory)
        await delete_song(songno)

        return JSONResponse(content={"message": "Song deleted successfully"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
