from typing import Literal
from pydantic import BaseModel


class KLineMARequest(BaseModel):
    symbol: str
    start_date: str
    end_date: str
    category: Literal["open", "high", "low", "close"]
    period: int


class KLineMAResponse(BaseModel):
    date: str
    open: float
    close: float
    high: float
    low: float
    ma: float