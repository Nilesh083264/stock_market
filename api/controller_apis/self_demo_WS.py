from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
from services.timers import get_latest_tick

router = APIRouter()

@router.websocket("/ws2")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Client connected")

    try:
        while True:
            await asyncio.sleep(1)
            data = get_latest_tick()
            await websocket.send_json({"data": data})
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print("WebSocket error:", e)