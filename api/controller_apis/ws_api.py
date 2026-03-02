from fastapi import APIRouter, WebSocket, WebSocketDisconnect,Request
from services.ws_manager import manager

router = APIRouter()


@router.websocket("/ws/ticks")
async def websocket_endpoint(websocket: WebSocket):
    # data = await websocket.receive_json()
    # print("ALL DATA ..",data)
    await manager.connect(websocket)

    try:
        while True:
            await websocket.receive_text()  # Keep connection alive

    except WebSocketDisconnect:
        manager.disconnect(websocket)
