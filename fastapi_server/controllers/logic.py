from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from starlette.responses import StreamingResponse
import os
from utils.databaseconn import read_data, write_data

router = APIRouter()


# Initialize JSON file with empty data if it doesn't exist
async def initialize_data():
    if not await read_data():
        await write_data({"users": []})


initialize_data()


@router.get("/greet/{name}")
async def greet(name: str):
    print("User clicked the button from the client side")
    return f"Hello, {name} from Python!"


@router.get("/getviddata")
async def getviddata():
    mp4_file_path = "api/viddata"
    print("User trigger the function from the client side")
    return JSONResponse(content={"video_path": mp4_file_path})


# File download endpoint with streaming
@router.get("/viddata")
async def download_file():
    file_location = f"storage/files/songs/test_song/test_song_karaoke_vid.mp4"
    if not os.path.exists(file_location):
        raise HTTPException(status_code=404, detail="File not found")

    # Stream the file from disk in chunks
    def iterfile():
        with open(file_location, "rb") as buffer:
            while chunk := buffer.read(1024 * 1024):  # Read in chunks of 1MB
                yield chunk

    return StreamingResponse(
        iterfile(),
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": f"attachment; filename=test_song_karaoke_vid.mp4"
        },
    )
