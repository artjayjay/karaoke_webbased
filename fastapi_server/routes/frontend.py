from fastapi import APIRouter
from views import firstpage, secondpage

router = APIRouter()

router.include_router(firstpage.router)
router.include_router(secondpage.router)