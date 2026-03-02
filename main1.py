from fastapi import FastAPI
from api.routes import router as api_router
from services.ticker_manager import ticker_manager

app = FastAPI()
app.include_router(api_router)


@app.on_event("startup")
def start_ticker():
    ticker_manager.start()


@app.on_event("shutdown")
def stop_ticker():
    ticker_manager.stop()