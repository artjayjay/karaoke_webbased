from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("firstpage/index.html", {"request": request})

@router.get("/head", response_class=HTMLResponse)
async def head(request: Request):
    return templates.TemplateResponse("head/index.html", {"request": request})