from datetime import datetime, timezone
from typing import Any, Dict
from pymongo import UpdateOne
from .config import PROVIDER_NAME

def transform_weather_data(raw: Dict[str, Any], city: str, country: str) -> Dict[str, Any]:
    """Normalizes raw API JSON into our internal schema."""
    
    dt_unix = raw.get("dt")
    observed_at = (
        datetime.fromtimestamp(dt_unix, tz=timezone.utc) 
        if dt_unix else datetime.now(timezone.utc)
    )

    # Extract nested fields safely
    main = raw.get("main", {})
    wind = raw.get("wind", {})
    weather_list = raw.get("weather", [])
    first_weather = weather_list[0] if weather_list else {}

    return {
        "city": city,
        "country": country,
        "provider": PROVIDER_NAME,
        "observed_at": observed_at,
        "coordinates": {
            "lat": raw.get("coord", {}).get("lat"),
            "lon": raw.get("coord", {}).get("lon"),
        },
        "metrics": {
            "temp_c": main.get("temp"),
            "feels_like_c": main.get("feels_like"),
            "pressure_hpa": main.get("pressure"),
            "humidity_pct": main.get("humidity"),
            "wind_speed_ms": wind.get("speed"),
            "rain_1h_mm": raw.get("rain", {}).get("1h", 0.0),
        },
        "conditions": {
            "main": first_weather.get("main"),
            "description": first_weather.get("description"),
        }
    }

def create_upsert_op(normalized_doc: Dict[str, Any]) -> UpdateOne:
    """Wraps normalized data into a MongoDB UpdateOne operation."""
    now = datetime.now(timezone.utc)
    
    filter_doc = {
        "provider": normalized_doc["provider"],
        "city": normalized_doc["city"],
        "observed_at": normalized_doc["observed_at"],
    }

    normalized_doc["updatedAt"] = now
    
    return UpdateOne(
        filter_doc, 
        {
            "$set": normalized_doc,
            "$setOnInsert": {"createdAt": now}
        }, 
        upsert=True
    )