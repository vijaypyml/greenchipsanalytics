# Market Constants

# Indices - Organized by Region
INDICES = {
    "INDIA": {
        "NIFTY 50": "^NSEI",
        "SENSEX": "^BSESN",
        "BANK NIFTY": "^NSEBANK",
        "INDIA VIX": "^INDIAVIX"
    },
    "US": {
        "S&P 500": "^GSPC",
        "NASDAQ 100": "^NDX",
        "DOW JONES": "^DJI",
        "VIX": "^VIX"
    },
    "EUROPE": {
        "FTSE 100": "^FTSE",
        "DAX": "^GDAXI",
        "CAC 40": "^FCHI",
        "EURO STOXX 50": "^STOXX50E"
    },
    "ASIA_PACIFIC": {
        "NIKKEI 225": "^N225",
        "HANG SENG": "^HSI",
        "SHANGHAI": "000001.SS",
        "KOSPI": "^KS11"
    },
    "COMMODITIES": {
        "GOLD": "GC=F",
        "SILVER": "SI=F",
        "CRUDE WTI": "CL=F",
        "BRENT CRUDE": "BZ=F",
        "NATURAL GAS": "NG=F",
        "COPPER": "HG=F"
    },
    "FOREX": {
        "DXY": "DX-Y.NYB",
        "USD/INR": "USDINR=X",
        "EUR/USD": "EURUSD=X",
        "GBP/USD": "GBPUSD=X",
        "USD/JPY": "JPY=X"
    },
    "CRYPTO": {
        "BTC/USD": "BTC-USD",
        "ETH/USD": "ETH-USD",
        "BNB/USD": "BNB-USD",
        "SOL/USD": "SOL-USD"
    }
}

# Flattened list for easy iteration
ALL_MARKETS = {
    **INDICES["INDIA"],
    **INDICES["US"],
    **INDICES["EUROPE"],
    **INDICES["ASIA_PACIFIC"],
    **INDICES["COMMODITIES"],
    **INDICES["FOREX"],
    **INDICES["CRYPTO"]
}

# Colors
COLORS = {
    "background": "#0e1117",
    "card_bg": "#1e1e2e",
    "positive": "#00d48a",  # Accent Green
    "negative": "#ff4757",  # Accent Red
    "warning": "#ffa502",
    "text_main": "#ffffff",
    "text_secondary": "#8899aa",
    "border_glow": "rgba(0, 212, 138, 0.3)"
}

# Timeframes
TIMEFRAMES = ["1D", "5D", "1M", "3M", "6M", "1Y", "5Y", "Max"]

# NIFTY 50 Symbols (Yahoo Finance format)
NIFTY_50_SYMBOLS = [
    "ADANIENT.NS", "ADANIPORTS.NS", "APOLLOHOSP.NS", "ASIANPAINT.NS", "AXISBANK.NS",
    "BAJAJ-AUTO.NS", "BAJFINANCE.NS", "BAJAJFINSV.NS", "BPCL.NS", "BHARTIARTL.NS",
    "BRITANNIA.NS", "CIPLA.NS", "COALINDIA.NS", "DIVISLAB.NS", "DRREDDY.NS",
    "EICHERMOT.NS", "GRASIM.NS", "HCLTECH.NS", "HDFCBANK.NS", "HDFCLIFE.NS",
    "HEROMOTOCO.NS", "HINDALCO.NS", "HINDUNILVR.NS", "ICICIBANK.NS", "ITC.NS",
    "INDUSINDBK.NS", "INFY.NS", "JSWSTEEL.NS", "KOTAKBANK.NS", "LTIM.NS",
    "LT.NS", "M&M.NS", "MARUTI.NS", "NTPC.NS", "NESTLEIND.NS",
    "ONGC.NS", "POWERGRID.NS", "RELIANCE.NS", "SBILIFE.NS", "SBIN.NS",
    "SUNPHARMA.NS", "TCS.NS", "TATACONSUM.NS", "TATAMOTORS.NS", "TATASTEEL.NS",
    "TECHM.NS", "TITAN.NS", "ULTRACEMCO.NS", "UPL.NS", "WIPRO.NS"
]

# NIFTY 50 Sector Mapping (Static to avoid API calls)
NIFTY_50_SECTORS = {
    "ADANIENT.NS": "Metals & Mining", "ADANIPORTS.NS": "Infrastructure", "APOLLOHOSP.NS": "Healthcare",
    "ASIANPAINT.NS": "Consumer Durables", "AXISBANK.NS": "Financial Services", "BAJAJ-AUTO.NS": "Automobile",
    "BAJFINANCE.NS": "Financial Services", "BAJAJFINSV.NS": "Financial Services", "BPCL.NS": "Oil, Gas & Consumable Fuels",
    "BHARTIARTL.NS": "Telecommunication", "BRITANNIA.NS": "Fast Moving Consumer Goods", "CIPLA.NS": "Healthcare",
    "COALINDIA.NS": "Oil, Gas & Consumable Fuels", "DIVISLAB.NS": "Healthcare", "DRREDDY.NS": "Healthcare",
    "EICHERMOT.NS": "Automobile", "GRASIM.NS": "Construction Materials", "HCLTECH.NS": "Information Technology",
    "HDFCBANK.NS": "Financial Services", "HDFCLIFE.NS": "Financial Services", "HEROMOTOCO.NS": "Automobile",
    "HINDALCO.NS": "Metals & Mining", "HINDUNILVR.NS": "Fast Moving Consumer Goods", "ICICIBANK.NS": "Financial Services",
    "ITC.NS": "Fast Moving Consumer Goods", "INDUSINDBK.NS": "Financial Services", "INFY.NS": "Information Technology",
    "JSWSTEEL.NS": "Metals & Mining", "KOTAKBANK.NS": "Financial Services", "LTIM.NS": "Information Technology",
    "LT.NS": "Construction", "M&M.NS": "Automobile", "MARUTI.NS": "Automobile",
    "NTPC.NS": "Power", "NESTLEIND.NS": "Fast Moving Consumer Goods", "ONGC.NS": "Oil, Gas & Consumable Fuels",
    "POWERGRID.NS": "Power", "RELIANCE.NS": "Oil, Gas & Consumable Fuels", "SBILIFE.NS": "Financial Services",
    "SBIN.NS": "Financial Services", "SUNPHARMA.NS": "Healthcare", "TCS.NS": "Information Technology",
    "TATACONSUM.NS": "Fast Moving Consumer Goods", "TATAMOTORS.NS": "Automobile", "TATASTEEL.NS": "Metals & Mining",
    "TECHM.NS": "Information Technology", "TITAN.NS": "Consumer Durables", "ULTRACEMCO.NS": "Construction Materials",
    "UPL.NS": "Chemicals", "WIPRO.NS": "Information Technology"
}

# Themes
THEMES = {
    "dark": {
        "background": "#0e1117",
        "card_bg": "#1e1e2e",
        "text_main": "#ffffff",
        "text_secondary": "#8899aa",
        "border": "#2e2e3e",
        "hover": "#3e3e4e"
    },
    "light": {
        "background": "#ffffff",
        "card_bg": "#f0f2f6",
        "text_main": "#000000",
        "text_secondary": "#555555",
        "border": "#d0d4db",
        "hover": "#e0e4eb"
    }
}
