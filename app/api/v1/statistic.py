from fastapi import APIRouter, Depends, HTTPException
import requests
from typing import Literal
import numpy as np
import logging
from datetime import datetime, timedelta
from app.dependencies.db import get_klines
from app.schema.v1 import KLineMAResponse
import fugledata
import talib
from fugledata.rest import ApiException


router = APIRouter()
logger = logging.getLogger("fuglestat")


@router.get("/statistic/ma", response_model=list[KLineMAResponse])
def get_moving_average(
    symbol: str,
    start_date: str,
    end_date: str,
    category: Literal["open", "high", "low", "close"],
    period: int
):
    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        # Calculate start date considering the period for moving average
        start_date_for_data = start_date - timedelta(days=2 * period)
        kline_data = get_klines(
            symbol,
            start_date_for_data.strftime("%Y-%m-%d"),
            end_date.strftime("%Y-%m-%d")
        )

        # Filter the data for the requested date range and calculate moving average
        trading_days = sorted([kline.dt for kline in kline_data if start_date <= kline.dt <= end_date])
        n_trading_days = len(trading_days)
        prices = [getattr(k, category) for k in kline_data]
        prices = np.array(prices, dtype=float)
        ma = talib.SMA(prices, period)
        ma = ma.tolist()
        # Prepare the response
        return [KLineMAResponse(date=dt.strftime("%Y-%m-%d"), ma=m) for dt, m in zip(trading_days ,ma[-n_trading_days:])]
        
    except ApiException as api_err:
        logger.error(f"ApiException: {api_err}")
        raise HTTPException(
            status_code=500, detail="Error connecting to the data service."
        )
    except ValueError as e:
        logger.error(f"ValueError: {e}")
        raise HTTPException(status_code=422, detail=f"Invalid input: {str(e)}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"RequestException: {req_err}")
        raise HTTPException(
            status_code=500, detail="Error connecting to the data service."
        )
    except Exception as e:
        logger.error(f"Unhandled Exception: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")