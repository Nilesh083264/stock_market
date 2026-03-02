from fastapi import  APIRouter
from services.straddle_service import get_straddle_service
from pydantic import BaseModel


router = APIRouter()
class StraddleRequest(BaseModel):
    category: str
    index: str
    expiry: str | None = None
    from_date: str
    to_date: str


@router.post("/api/straddle")
def fetch_straddle(request:StraddleRequest):
    try:
        service = get_straddle_service()
        print(request)
        data = service.fetch_straddle(
            category=request.category,
            index=request.index,
            expiry=request.expiry,
            from_date=request.from_date,
            to_date=request.to_date
        )
        # print("data: ",data , request)
        return {
            "status": "success",
            "data": data
        }

    except Exception as e:
        print("ERROR : ",str(e))
        return {
            "status": "error",
            "message": str(e)
        }

