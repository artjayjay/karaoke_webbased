from fastapi import FastAPI, APIRouter, HTTPException, File, UploadFile, Form
from fastapi.responses import JSONResponse
from sqlmodel import SQLModel, Field, select, func
from models.models import SongLibrary, QueueLibrary
from utils.databaseconn import AsyncSessionLocal
from typing import Optional
import os
import asyncio
import math

router = APIRouter()


# Function to fetch songs and queue data with server-side pagination
async def display_songqueue(server_page_size: int = 30, offset: int = 0):
    async with AsyncSessionLocal() as session:
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
            .limit(server_page_size)
            .offset(offset)
        )

        result = await session.execute(statement)
        rows = result.all()

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


# Function to search songs with server-side pagination
async def displaysongtablesearch(
    column: Optional[str] = None,
    value: Optional[str] = None,
    server_page_size: int = 30,
    offset: int = 0,
):
    async with AsyncSessionLocal() as session:
        statement = select(SongLibrary).where(SongLibrary.disabled == False)

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

            statement = statement.where(condition)

        statement = statement.limit(server_page_size).offset(offset)

        result = await session.execute(statement)
        songs = result.scalars().all()

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


# Queue operations (unchanged)
async def insert_to_queuetable(songno: str, singername: str):
    async with AsyncSessionLocal() as session:
        try:
            song_exists = await session.execute(
                select(SongLibrary).where(SongLibrary.songno == songno)
            )
            if not song_exists.scalar():
                raise HTTPException(
                    status_code=404, detail=f"Song with songno {songno} not found"
                )

            statement = (
                select(QueueLibrary).order_by(QueueLibrary.queueno.desc()).limit(1)
            )
            result = await session.execute(statement)
            last_queue_entry = result.scalars().first()

            queuestatus = "on queue"

            if last_queue_entry:
                last_queueno = int(last_queue_entry.queueno)
                new_queueno = f"{last_queueno + 1:04}"
            else:
                new_queueno = "0001"
                queuestatus = "playing"

            new_queue_entry = QueueLibrary(
                queueno=new_queueno,
                songno=songno,
                singername=singername,
                queuestatus=queuestatus,
            )

            session.add(new_queue_entry)
            await session.commit()
            await session.refresh(new_queue_entry)
            return new_queueno

        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


# Endpoint to display songs and queue data with server-side pagination
@router.get("/displaysongqueue/{server_page}/{server_page_size}")
async def displaysongqueue(server_page: int, server_page_size: int):
    try:
        offset = (server_page - 1) * server_page_size
        songqueuedata = await display_songqueue(
            server_page_size=server_page_size, offset=offset
        )
        return JSONResponse(content={"queue": songqueuedata})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint to display songs for queue insert with server-side pagination
@router.get("/displaysongssearch")
async def displaysongssearch(
    searchterm: str, server_page: int = 1, server_page_size: int = 30
):
    try:
        offset = (server_page - 1) * server_page_size

        if searchterm.isdigit():
            songsdata = await displaysongtablesearch(
                column="songno",
                value=searchterm,
                server_page_size=server_page_size,
                offset=offset,
            )
        else:
            columns_to_search = ["songname", "genre", "artist", "album"]
            songsdata = []
            for column in columns_to_search:
                songsdata = await displaysongtablesearch(
                    column=column,
                    value=searchterm,
                    server_page_size=server_page_size,
                    offset=offset,
                )
                if songsdata:
                    break

        return JSONResponse(content={"songs": songsdata})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# All other endpoints remain exactly the same
@router.post("/insertsongqueue")
async def insertsongqueue(
    songno: str = Form(...),
    singername: str = Form(...),
):
    try:
        await insert_to_queuetable(songno, singername)
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
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/updatequeue")
async def updatequeue(
    queueno: str = Form(...),
    singername: str = Form(...),
):
    try:
        async with AsyncSessionLocal() as session:
            statement = select(QueueLibrary).where(QueueLibrary.queueno == queueno)
            result = await session.execute(statement)
            queue_entry = result.scalars().first()

            if queue_entry:
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
async def deletequeue(queueno: str):
    try:
        async with AsyncSessionLocal() as session:
            statement = select(QueueLibrary).where(QueueLibrary.queueno == queueno)
            result = await session.execute(statement)
            queue_entry = result.scalars().first()

            if queue_entry:
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
            statement = (
                select(
                    QueueLibrary.queueno,
                    SongLibrary.songname,
                )
                .join(SongLibrary, SongLibrary.songno == QueueLibrary.songno)
                .where(QueueLibrary.queuestatus == "playing")
            )
            result = await session.execute(statement)
            queue_data = result.first()

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
