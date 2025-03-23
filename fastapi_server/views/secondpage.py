from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/karaokeplayer", response_class=HTMLResponse)
async def karaokeplayer(request: Request):
    return templates.TemplateResponse("secondpage/index.html", {"request": request})