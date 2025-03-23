from fastapi import APIRouter, HTTPException, File, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse
from sqlmodel import select
from models.models import QueueLibrary, SongSettings
from utils.databaseconn import AsyncSessionLocal
import os
import librosa
import numpy as np
from scipy.spatial.distance import cosine
import asyncio

router = APIRouter()


async def getsongplaying():
    """
    Fetch the currently playing song from the queue.
    """
    async with AsyncSessionLocal() as session:
        # Fetch the queue entry using queue status
        queue_statement = select(QueueLibrary).where(
            QueueLibrary.queuestatus == "playing"
        )
        queue_result = await session.execute(queue_statement)
        queue_entry = queue_result.scalars().first()

        if not queue_entry:
            return None, None, None

        return queue_entry.songno, queue_entry.queueno, queue_entry.singername


async def get_song_settings():
    """
    Fetch the current song settings from the database.
    """
    async with AsyncSessionLocal() as session:
        settings_statement = select(SongSettings)
        settings_result = await session.execute(settings_statement)
        settings_entry = settings_result.scalars().first()

        if not settings_entry:
            raise HTTPException(
                status_code=404,
                detail="No SongSettings entry found",
            )

        return settings_entry


def calculate_karaoke_score(original_song_path, user_audio_path):
    original_audio, _ = librosa.load(original_song_path, sr=None, mono=True)
    user_audio, _ = librosa.load(user_audio_path, sr=None, mono=True)

    # Normalize the audio signals
    original_audio = (original_audio - np.mean(original_audio)) / np.std(original_audio)
    user_audio = (user_audio - np.mean(user_audio)) / np.std(user_audio)

    audio1 = original_audio
    audio2 = user_audio

    """
    Compare two audio signals using cosine similarity.
    """
    min_length = min(len(audio1), len(audio2))
    audio1 = audio1[:min_length]
    audio2 = audio2[:min_length]

    # Calculate cosine similarity
    similarity = 1 - cosine(audio1, audio2)
    return abs(similarity) * 100  # Use absolute value


@router.get("/play")
async def play():
    """
    Stream the currently playing song.
    If no song is playing, return a default response.
    """
    songno, queueno, singer = await getsongplaying()

    # If no song is playing, return a default response
    if songno is None or queueno is None:
        return JSONResponse(
            content={"message": "No song is currently playing"},
            status_code=200,
        )

    # Construct the file path dynamically using the songno
    song_directory = os.path.join("storage", "files", "songs", songno)
    file_location = os.path.join(song_directory, f"{songno}.mp4")

    # Check if the file exists
    if not os.path.exists(file_location):
        raise HTTPException(status_code=404, detail="File not found")

    # Stream the file from disk in chunks
    def iterfile():
        with open(file_location, "rb") as buffer:
            while chunk := buffer.read(1024 * 1024):  # Read in chunks of 1MB
                yield chunk

    return StreamingResponse(
        iterfile(),
        media_type="video/mp4",
        headers={"Content-Disposition": f"inline; filename={songno}.mp4"},
    )


@router.post("/result")
async def result(file: UploadFile = File(...)):
    """
    Handle the uploaded user audio, compare it with the original song, and calculate the score.
    Apply settings to determine what to include in the response.
    Delete the current queue entry and update the next song's status to "playing".
    """
    songno, queueno, singer = await getsongplaying()
    settings = await get_song_settings()

    # Validate the uploaded file
    allowed_mime_types = ["audio/wav", "audio/x-wav", "audio/wave"]
    allowed_extensions = [".wav"]

    if file.content_type not in allowed_mime_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Only WAV files are allowed. Received: {file.content_type}",
        )

    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file extension. Only .wav files are allowed. Received: {file_extension}",
        )

    # Save the uploaded file
    save_directory = os.path.join("storage", "files", "temp")
    os.makedirs(save_directory, exist_ok=True)
    user_audio_path = os.path.join(save_directory, f"{queueno}.wav")

    try:
        with open(user_audio_path, "wb") as buffer:
            while chunk := await file.read(1024 * 1024):  # Read in chunks of 1MB
                buffer.write(chunk)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    # Load the original song and user audio
    original_song_path = os.path.join(
        "storage", "files", "songs", songno, f"{songno}.wav"
    )
    if not os.path.exists(original_song_path):
        raise HTTPException(status_code=404, detail="Original song file not found")

    try:

        similarity_percentage = await asyncio.to_thread(
            calculate_karaoke_score, original_song_path, user_audio_path
        )

        # Adjust score based on difficulty
        if settings.difficulty == "easy":
            similarity_percentage = similarity_percentage * 100 + 50
        elif settings.difficulty == "normal":
            similarity_percentage = similarity_percentage * 100 + 20
        elif settings.difficulty == "medium":
            similarity_percentage = similarity_percentage * 100
        elif settings.difficulty == "hard":
            similarity_percentage = similarity_percentage * 50
        elif settings.difficulty == "expert":
            similarity_percentage = similarity_percentage

        # Clamp the score between 0 and 100
        similarity_percentage = max(0, min(100, similarity_percentage))

        # Prepare the response based on settings
        response = {
            "score": (
                float(similarity_percentage) if settings.showscore else "N/A"
            ),  # Convert to native float
            "singersname": (
                singer if settings.showsingersname else "N/A"
            ),  # Replace with actual singer's name if available
        }

        # Delete the current queue entry
        async with AsyncSessionLocal() as session:
            # Fetch the current queue entry
            queue_statement = select(QueueLibrary).where(
                QueueLibrary.queueno == queueno
            )
            queue_result = await session.execute(queue_statement)
            queue_entry = queue_result.scalars().first()

            if queue_entry:
                await session.delete(queue_entry)
                await session.commit()
            else:
                raise HTTPException(status_code=404, detail="Queue entry not found")

            # Fetch the next song in the queue
            next_queue_statement = (
                select(QueueLibrary)
                .where(QueueLibrary.queuestatus == "on queue")
                .order_by(QueueLibrary.queueno.asc())
                .limit(1)
            )
            next_queue_result = await session.execute(next_queue_statement)
            next_queue_entry = next_queue_result.scalars().first()

            # Update the next song's status to "playing"
            if next_queue_entry:
                next_queue_entry.queuestatus = "playing"
                session.add(next_queue_entry)
                await session.commit()
                await session.refresh(next_queue_entry)

        return JSONResponse(content=response)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing audio: {str(e)}")
    finally:
        # Clean up the uploaded file
        if os.path.exists(user_audio_path):
            await asyncio.to_thread(os.remove, user_audio_path)


@router.get("/scorevideo")
async def scorevideo():
    """
    Stream the score video or image based on the settings.
    If showpopupscore is False, return a 404 error.
    """
    settings = await get_song_settings()

    # Check if showpopupscore is enabled
    if not settings.showpopupscore:
        raise HTTPException(
            status_code=404, detail="Score video/image display is disabled in settings"
        )

    # Determine the file path for the score video/image
    scorevid_directory = os.path.join("storage", "files", "settings", "scorevid")
    if not os.path.exists(scorevid_directory):
        raise HTTPException(
            status_code=404, detail="Score video/image directory not found"
        )

    # Check for supported file types
    supported_files = []
    for ext in [".mp4", ".mkv", ".jpg", ".png"]:
        file_path = os.path.join(scorevid_directory, f"scorevid{ext}")
        if os.path.exists(file_path):
            supported_files.append(file_path)

    if not supported_files:
        raise HTTPException(status_code=404, detail="No score video/image file found")

    # Use the first supported file
    file_path = supported_files[0]

    # Determine the media type
    if file_path.endswith(".mp4") or file_path.endswith(".mkv"):
        media_type = "video/mp4"
    elif file_path.endswith(".jpg"):
        media_type = "image/jpeg"
    elif file_path.endswith(".png"):
        media_type = "image/png"
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    # Stream the file from disk in chunks
    def iterfile():
        with open(file_path, "rb") as buffer:
            while chunk := buffer.read(1024 * 1024):  # Read in chunks of 1MB
                yield chunk

    return StreamingResponse(
        iterfile(),
        media_type=media_type,
        headers={
            "Content-Disposition": f"inline; filename=scorevid{os.path.splitext(file_path)[1]}"
        },
    )


@router.get("/applause")
async def applause():
    """
    Stream the applause audio based on the settings.
    If showpopupscore is False, return a 404 error.
    """
    settings = await get_song_settings()

    # Check if showpopupscore is enabled
    if not settings.showpopupscore:
        raise HTTPException(
            status_code=404, detail="Applause audio playback is disabled in settings"
        )

    # Determine the file path for the applause audio
    applause_directory = os.path.join("storage", "files", "settings", "scoreapplause")
    if not os.path.exists(applause_directory):
        raise HTTPException(
            status_code=404, detail="Applause audio directory not found"
        )

    # Check for supported file types
    supported_files = []
    for ext in [".wav"]:
        file_path = os.path.join(applause_directory, f"scoreapplause{ext}")
        if os.path.exists(file_path):
            supported_files.append(file_path)

    if not supported_files:
        raise HTTPException(status_code=404, detail="No applause audio file found")

    # Use the first supported file
    file_path = supported_files[0]

    # Stream the file from disk in chunks
    def iterfile():
        with open(file_path, "rb") as buffer:
            while chunk := buffer.read(1024 * 1024):  # Read in chunks of 1MB
                yield chunk

    return StreamingResponse(
        iterfile(),
        media_type="audio/wav",
        headers={"Content-Disposition": f"inline; filename=scoreapplause.wav"},
    )


@router.get("/settings")
async def get_settings():
    """
    Fetch the current song settings from the database.
    """
    settings = await get_song_settings()
    return JSONResponse(
        content={
            "showpopupscore": settings.showpopupscore,
            "showscore": settings.showscore,
            "showsingersname": settings.showsingersname,
            "mainserver": settings.mainserver,
            "karaokeserver": settings.karaokeserver,
        }
    )


@router.delete("/deletequeue")
async def deletequeue():  # Queue number to identify the entry
    try:
        async with AsyncSessionLocal() as session:
            # Find the queue entry by queueno
            statement = select(QueueLibrary).where(
                QueueLibrary.queuestatus == "playing"
            )
            result = await session.execute(statement)
            queue_entry = result.scalars().first()

            if queue_entry:
                # Delete the queue entry
                await session.delete(queue_entry)
                await session.commit()
                return JSONResponse(content={"message": "Queue deleted successfully"})
            else:
                raise HTTPException(
                    status_code=404,
                    detail=f"Queue entry with queue not found",
                )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
