from pydantic import BaseModel


class KLineMARequest(BaseModel):
    start_date: str
    end_date: str
    period: int


class KLineMAResponse(BaseModel):
    date: str
    open: float
    close: float
    high: float
    low: float
    ma: float