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

router = APIRouter()


# Function to fetch songs and queue data asynchronously
async def display_songqueue(
    limit: int = 10,
    offset: int = 0,
):
    async with AsyncSessionLocal() as session:
        # Join SongLibrary and QueueLibrary tables
        statement = (
            select(
                QueueLibrary.queueno,
                SongLibrary.songname,
                SongLibrary.genre,
                SongLibrary.artist,
                SongLibrary.album,
                QueueLibrary.singername,
            )
            .join(SongLibrary, SongLibrary.songno == QueueLibrary.songno)
            .where(SongLibrary.disabled == False)
            .limit(limit)
            .offset(offset)
        )

        # Execute the query
        result = await session.execute(statement)
        rows = result.all()

        # Convert rows to a list of dictionaries
        queue_data = [
            {
                "queueno": row.queueno,
                "songname": row.songname,
                "genre": row.genre,
                "artist": row.artist,
                "album": row.album,
                "singername": row.singername,
            }
            for row in rows
        ]
        return queue_data


async def displaysongtablesearch(
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


async def insert_to_queuetable(songno: str, singername: str):
    """
    Inserts a new entry into the QueueLibrary table.

    Args:
        songno (str): The song number (songno) to be added to the queue.
        singername (str): The name of the singer for the queue entry.

    Returns:
        str: The queueno of the newly inserted queue entry.

    Raises:
        HTTPException: If the song does not exist in the SongLibrary table.
    """
    async with AsyncSessionLocal() as session:
        try:
            # Check if the song exists in the SongLibrary table
            song_exists = await session.execute(
                select(SongLibrary).where(SongLibrary.songno == songno)
            )
            if not song_exists.scalar():
                raise HTTPException(
                    status_code=404, detail=f"Song with songno {songno} not found"
                )

            # Fetch the last queue entry to determine the next queueno
            statement = (
                select(QueueLibrary).order_by(QueueLibrary.queueno.desc()).limit(1)
            )
            result = await session.execute(statement)
            last_queue_entry = result.scalars().first()

            queuestatus = "on queue"

            if last_queue_entry:
                # Increment the last queueno by 1
                last_queueno = int(last_queue_entry.queueno)
                new_queueno = (
                    f"{last_queueno + 1:04}"  # Format as 4-digit string (e.g., "0001")
                )
            else:
                # If no queue entries exist, start from "0001"
                new_queueno = "0001"
                queuestatus = "playing"

            # Create a new queue entry
            new_queue_entry = QueueLibrary(
                queueno=new_queueno,
                songno=songno,
                singername=singername,
                queuestatus=queuestatus,
            )

            # Add the new queue entry to the session and commit
            session.add(new_queue_entry)
            await session.commit()
            await session.refresh(new_queue_entry)
            print("Added new record:", new_queue_entry.queueno)
            return new_queue_entry.queueno  # Return the new queueno

        except HTTPException as e:
            raise e  # Re-raise HTTPException to propagate the error
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


# Endpoint to display songs and queue data
@router.get("/displaysongqueue/{limit}/{offset}")
async def displaysongqueue(limit: int, offset: int):
    if offset <= 0:
        offset = 0
    if offset > 0:
        offset = offset - 1
    try:
        songqueuedata = await display_songqueue(limit=limit, offset=offset)
        return JSONResponse(content={"queue": songqueuedata})
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint to display songs for queue insert
@router.get("/displaysongssearch")
async def displaysongssearch(
    searchterm: str,  # No default value here
    limit: int = 10,
    offset: int = 0,
):

    if offset <= 0:
        offset = 0
    if offset > 0:
        offset = offset - 1

    try:
        # Determine which column to search based on the input
        if searchterm.isdigit():
            # If the input is numeric, search in the songno column (unique)
            column = "songno"
            songsdata = await displaysongtablesearch(
                column=column, value=searchterm, limit=limit, offset=offset
            )
        else:
            # If the input is non-numeric, search in the following order:
            # 1. songname
            # 2. genre
            # 3. artist
            # 4. album
            columns_to_search = ["songname", "genre", "artist", "album"]
            songsdata = []

            for column in columns_to_search:
                songsdata = await displaysongtablesearch(
                    column=column, value=searchterm, limit=limit, offset=offset
                )
                if songsdata:
                    break  # Stop searching if results are found

        # Return an empty list if no songs are found
        if not songsdata:
            songsdata = []

        return JSONResponse(content={"songs": songsdata})
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/insertsongqueue")
async def insertsongqueue(
    songno: str = Form(...),
    singername: str = Form(...),
):
    try:
        # Insert the song into the database
        await insert_to_queuetable(songno, singername)

        # Fetch the last inserted song to get the queueno
        async with AsyncSessionLocal() as session:
            statement = (
                select(QueueLibrary).order_by(QueueLibrary.queueno.desc()).limit(1)
            )
            result = await session.execute(statement)
            last_queue_entry = result.scalars().first()

            if last_queue_entry:
                return JSONResponse(
                    content={"message": "Song Queue added successfully"}
                )
            else:
                raise HTTPException(
                    status_code=500, detail="Failed to retrieve the last inserted song"
                )
    except Exception as e:
        print("................ ", e)
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/updatequeue")
async def updatequeue(
    queueno: str = Form(...),  # Queue number to identify the entry
    singername: str = Form(...),  # New singer name to update
):
    try:
        async with AsyncSessionLocal() as session:
            # Find the queue entry by queueno
            statement = select(QueueLibrary).where(QueueLibrary.queueno == queueno)
            result = await session.execute(statement)
            queue_entry = result.scalars().first()

            if queue_entry:
                # Update the singername
                queue_entry.singername = singername
                await session.commit()
                await session.refresh(queue_entry)
                return JSONResponse(content={"message": "Queue updated successfully"})
            else:
                raise HTTPException(
                    status_code=404,
                    detail=f"Queue entry with queueno {queueno} not found",
                )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/deletequeue/{queueno}")
async def deletequeue(queueno: str):  # Queue number to identify the entry
    try:
        async with AsyncSessionLocal() as session:
            # Find the queue entry by queueno
            statement = select(QueueLibrary).where(QueueLibrary.queueno == queueno)
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
                    detail=f"Queue entry with queueno {queueno} not found",
                )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/displayplayingcurrentsong")
async def displayplayingcurrentsong():
    try:
        async with AsyncSessionLocal() as session:
            # Join QueueLibrary with SongLibrary to get the songname
            statement = (
                select(
                    QueueLibrary.queueno,
                    SongLibrary.songname,
                )
                .join(SongLibrary, SongLibrary.songno == QueueLibrary.songno)
                .where(QueueLibrary.queuestatus == "playing")
            )
            result = await session.execute(statement)
            queue_data = result.first()  # Use first() to get the first row

            if queue_data:
                return JSONResponse(
                    content={
                        "queueno": queue_data.queueno,
                        "songname": queue_data.songname,
                    }
                )
            else:
                return JSONResponse(
                    content={
                        "queueno": "none",
                        "songname": "none",
                    }
                )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
