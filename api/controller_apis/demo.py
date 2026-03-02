from fastapi import APIRouter
from services.straddle_service import get_straddle_service
from services.ws_manager import manager
from pydantic import BaseModel

router = APIRouter()

class StraddleRequest(BaseModel):
    category: str
    index: str
    expiry: str | None = None
    from_date: str
    to_date: str


@router.post("/api1/straddle")
async def fetch_straddle(request: StraddleRequest):

    try:
        service = get_straddle_service()

        data = service.fetch_straddle(
            category=request.category,
            index=request.index,
            expiry=request.expiry,
            from_date=request.from_date,
            to_date=request.to_date
        )

        response_payload = {
            "type": "straddle",
            "status": "success",
            "data": data
        }

        # 🔥 Broadcast to WebSocket clients
        if manager.active_connections:
            await manager.broadcast(response_payload)

        return response_payload

    except Exception as e:

        error_payload = {
            "type": "straddle",
            "status": "error",
            "message": str(e)
        }

        if manager.active_connections:
            await manager.broadcast(error_payload)

        return error_payload