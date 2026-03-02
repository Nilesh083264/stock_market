from fastapi import FastAPI, HTTPException, Depends
import uvicorn
from api.routes import router as api_routers
from core.config import settings
from services.ticker_manager import ticker_manager
from contextlib import asynccontextmanager
import asyncio

from services.timers import start_producer



@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Starting ticker...")
    asyncio.create_task(start_producer())
    loop = asyncio.get_running_loop()
    ticker_manager.start(loop)

    yield  # App runs here

    print("Shutting down ticker...")
    ticker_manager.stop()

app = FastAPI(lifespan=lifespan)
app.include_router(api_routers)


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT)
