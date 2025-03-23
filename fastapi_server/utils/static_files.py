from fastapi.staticfiles import StaticFiles

def mount_static_files(app):
    """
    Mount static files to the FastAPI app.
    """
    app.mount("/static", StaticFiles(directory="static"), name="static")