"""
Market configuration for multi-market support.
Centralizes all market-specific settings for India, USA, and future markets.
"""

MARKETS = {
    "INDIA": {
        "name": "India",
        "flag": "🇮🇳",
        "currency": "₹",
        "currency_name": "INR",
        "main_index": {
            "name": "NIFTY 50",
            "symbol": "^NSEI",
            "constituents_count": 50
        },
        "alternative_indices": {
            "SENSEX": "^BSESN",
            "NIFTY Bank": "^NSEBANK"
        },
        "sectors": {
            "Bank": "^NSEBANK",
            "IT": "^CNXIT",
            "Pharma": "^CNXPHARMA",
            "Auto": "^CNXAUTO",
            "FMCG": "^CNXFMCG",
            "Metal": "^CNXMETAL",
            "Financial Services": "^CNXFINANCE",
            "Energy": "^CNXENERGY",
            "Realty": "^CNXREALTY",
            "Media": "^CNXMEDIA",
            "Healthcare": "^CNXHEALTHCARE"
        },
        "vix_symbol": "^INDIAVIX",
        "vix_name": "NIFTY VIX"
    },
    "USA": {
        "name": "USA",
        "flag": "🇺🇸",
        "currency": "$",
        "currency_name": "USD",
        "main_index": {
            "name": "S&P 500",
            "symbol": "^GSPC",
            "constituents_count": 500
        },
        "alternative_indices": {
            "NASDAQ": "^IXIC",
            "DOW": "^DJI",
            "Russell 2000": "^RUT"
        },
        "sectors": {
            "Technology": "XLK",           # Technology Select Sector SPDR ETF
            "Financials": "XLF",           # Financial Select Sector SPDR ETF
            "Healthcare": "XLV",           # Health Care Select Sector SPDR ETF
            "Energy": "XLE",               # Energy Select Sector SPDR ETF
            "Consumer Discretionary": "XLY",  # Consumer Discretionary SPDR ETF
            "Consumer Staples": "XLP",     # Consumer Staples Select Sector SPDR ETF
            "Industrials": "XLI",          # Industrial Select Sector SPDR ETF
            "Materials": "XLB",            # Materials Select Sector SPDR ETF
            "Utilities": "XLU",            # Utilities Select Sector SPDR ETF
            "Real Estate": "XLRE",         # Real Estate Select Sector SPDR ETF
            "Communication": "XLC"         # Communication Services SPDR ETF
        },
        "vix_symbol": "^VIX",
        "vix_name": "CBOE VIX"
    }
}


def get_market_config(market_id):
    """
    Get configuration for a specific market.

    Args:
        market_id: Market identifier (e.g., "INDIA", "USA")

    Returns:
        dict: Market configuration
    """
    return MARKETS.get(market_id, MARKETS["INDIA"])


def get_available_markets():
    """
    Get list of available markets with display names.

    Returns:
        list: List of tuples (market_id, display_name)
    """
    return [(key, f"{config['flag']} {config['name']}") for key, config in MARKETS.items()]


def format_currency(value, market_config):
    """
    Format currency value based on market configuration.

    Args:
        value: Numeric value to format
        market_config: Market configuration dict

    Returns:
        str: Formatted currency string
    """
    currency = market_config.get("currency", "$")
    if abs(value) >= 1e9:
        return f"{currency}{value/1e9:.2f}B"
    elif abs(value) >= 1e6:
        return f"{currency}{value/1e6:.2f}M"
    elif abs(value) >= 1e3:
        return f"{currency}{value/1e3:.2f}K"
    else:
        return f"{currency}{value:.2f}"
