from fastapi import APIRouter, Depends, HTTPException
import requests
import logging
from datetime import datetime, timedelta
from app.dependencies.db import get_klines
from app.schema.v1 import KLineMARequest, KLineMAResponse
import fugledata
from fugledata.rest import ApiException


router = APIRouter()
logger = logging.getLogger("fuglestat")


@router.get("/statistic/ma", response_model=KLineMAResponse)
def get_moving_average(request: KLineMARequest):
    try:
        start_date = datetime.strptime(request.start_date, "%Y-%m-%d").date() - timedelta(days=2 * request.period)
        start_date = start_date.strftime("%Y-%m-%d")
        kline_data = get_klines(
            request.symbol, start_date, request.end_date
        )
        # Calculate the moving average
    except ApiException as api_err:
        logger.error(f"ApiException: {api_err}")
        return HTTPException(
            status_code=500, detail="Error connecting to the date service."
        )
    except ValueError as e:
        logger.error(f"ValueError: {e}")
        return HTTPException(status_code=422, detail=f"Invalid input: {str(e)}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"RequestException: {req_err}")
        return HTTPException(
            status_code=500, detail="Error connecting to the date service."
        )
    except Exception as e:
        logger.error(f"Unhandled Exception: {e}")
        return HTTPException(status_code=500, detail="Internal Server Error")

