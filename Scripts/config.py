import os
from dotenv import load_dotenv

# Load variables from .env into the environment
load_dotenv()

# API Configuration
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
WEATHER_API_BASE_URL = os.getenv("WEATHER_API_BASE_URL")

# Database Configuration
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
MONGODB_DB = os.getenv("MONGODB_DB", "weather_db")
MONGODB_COLLECTION = os.getenv("MONGODB_COLLECTION", "weather_raw")

# Application Constants
PROVIDER_NAME = os.getenv("PROVIDER_NAME", "OpenWeather")

# List of cities to track (Can also be moved to a JSON file or DB)
CITIES = [
    {"name": "London", "country": "GB"},
    {"name": "New York", "country": "US"},
    {"name": "Tokyo", "country": "JP"},
    {"name": "Lagos", "country": "NG"},
]