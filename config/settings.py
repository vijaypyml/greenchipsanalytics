import os
from dotenv import load_dotenv

load_dotenv()

# App Configuration
APP_NAME = "MarketPulse"
Page_Layout = "wide"
REFRESH_INTERVAL = 30  # seconds

# API Configuration (Placeholders)
FRED_API_KEY = os.getenv("FRED_API_KEY")

# Caching
CACHE_TTL = 60  # seconds
