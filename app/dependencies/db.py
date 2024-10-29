import fugledata
import fugledata.models
import requests
import logging
from requests.exceptions import HTTPError, Timeout, RequestException
from app.config.config import settings

logger = logging.getLogger("fuglestat")


def _get_configuration():
    configuration = fugledata.Configuration(
        host=settings.fugledata_base_url
    )
    return configuration

def _get_base_url():
    return settings.fugledata_base_url

def get_klines(symbol: str, start_date: str, end_date: str)->list[fugledata.models.Kline]:
    url = f"{_get_base_url()}/kline"
    params = {
        "symbol": f"eq.{symbol}",
        "dt": [f"lte.{end_date}", f"gte.{start_date}"],
        "order": "dt"
    }
    try:
        response = requests.get(url, timeout=5)
        # Raise an error for bad HTTP responses (4xx and 5xx)
        response.raise_for_status()
    except HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")  # e.g., 404 or 500 errors
    except Timeout as timeout_err:
        logger.error(f"Request timed out: {timeout_err}")
    except RequestException as req_err:
        logger.error(f"An error occurred: {req_err}")
    else:
        # Process the response if no exceptions were raised
        data = response.json()
        return [fugledata.models.Kline.from_dict(item) for item in data]
    
