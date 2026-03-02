from fastapi import APIRouter
from api.controller_apis.UI_API import router as UI_api
from api.controller_apis.historical_data_API import router as historical_data_api
from api.controller_apis.ws_api import router as ws_api
from api.controller_apis.demo import router as ws_ap
from api.controller_apis.self_demo_WS import router as self_demo_WS

router = APIRouter()


router.include_router(UI_api)
router.include_router(ws_api)
router.include_router(ws_ap)
router.include_router(self_demo_WS)
router.include_router(historical_data_api)
