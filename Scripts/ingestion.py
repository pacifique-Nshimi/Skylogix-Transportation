import requests
import logging
from typing import Dict, Any
from .config import WEATHER_API_BASE_URL, WEATHER_API_KEY

logger = logging.getLogger(__name__)

def fetch_raw_weather(city: str, country: str) -> Dict[str, Any]:
    """Extracts raw data from the OpenWeather API."""
    if not WEATHER_API_KEY:
        raise RuntimeError("WEATHER_API_KEY is not set")

    params = {
        "q": f"{city},{country}",
        "appid": WEATHER_API_KEY,
        "units": "metric",
    }

    resp = requests.get(WEATHER_API_BASE_URL, params=params, timeout=10)
    
    if resp.status_code != 200:
        logger.error("API Error [%s]: %s", resp.status_code, resp.text)
        resp.raise_for_status()

    return resp.json()