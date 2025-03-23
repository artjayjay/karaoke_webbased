from fastapi import APIRouter

from controllers import songlibrary, songqueue, songsettings, karaokeplayer

router = APIRouter()

router.include_router(songlibrary.router, prefix="/songlibrary")
router.include_router(songqueue.router, prefix="/songqueue")
router.include_router(songsettings.router, prefix="/songsettings")
router.include_router(karaokeplayer.router, prefix="/karaokeplayer")
