from typing import Literal
from pydantic import BaseModel


class KLineMAResponse(BaseModel):
    date: str
    ma: float