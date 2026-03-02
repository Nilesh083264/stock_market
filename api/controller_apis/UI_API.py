import fastapi
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from constants.constant import BASE_DIR



router = fastapi.APIRouter()
STATIC_DIR = BASE_DIR / "static"
router.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@router.get("/")
def home():
    return FileResponse(Path("static/ind.html"))
    # return FileResponse(Path("static/test_ws.html"))
