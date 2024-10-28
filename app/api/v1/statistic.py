from fastapi import APIRouter, Depends, HTTPException

from app.schema.v1 import KLineMARequest, KLineMAResponse



router = APIRouter()


router.get("/statistic/ma", response_model=KLineMAResponse)
def get_ma(request: KLineMARequest = Depends()):
    return {
        "date": "2021-01-01",
        "open": 1.0,
        "close": 1.0,
        "high": 1.0,
        "low": 1.0,
        "ma": 1.0,
    }
