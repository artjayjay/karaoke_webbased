from fastapi import FastAPI
import socketio
import os
from socket_handlers import SocketHandlers  # Import the SocketHandlers class
from utils.static_files import mount_static_files
from routes import frontend, backend

# Create a FastAPI app
app = FastAPI()

# Create a Socket.IO server
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")

# Mount static files
mount_static_files(app)

# Include frontend and backend routers
app.include_router(backend.router, prefix="/api")
app.include_router(frontend.router)

# # Get the absolute path to the directory containing the Python script
# base_dir = os.path.dirname(os.path.abspath(__file__))

# Register Socket.IO handlers
socket_handlers = SocketHandlers(sio)  # Create an instance of SocketHandlers
socket_handlers.register_handlers()  # Register the handlers

# Attach the Socket.IO server to the FastAPI app
app.mount("/socket.io", socketio.ASGIApp(sio))

# Run the application using uvicorn
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
