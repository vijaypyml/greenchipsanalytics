"""
Technical indicators and sentiment analysis for MarketPulse.
Uses TA-Lib for professional-grade technical analysis.
"""

import pandas as pd
import numpy as np
import ta


def calculate_rsi(df, period=14):
    """
    Calculate Relative Strength Index.

    Args:
        df: DataFrame with 'Close' column
        period: RSI period (default: 14)

    Returns:
        float: RSI value (0-100)
    """
    try:
        rsi_indicator = ta.momentum.RSIIndicator(close=df['Close'], window=period)
        rsi = rsi_indicator.rsi().iloc[-1]
        return rsi if not pd.isna(rsi) else 50.0
    except Exception:
        return 50.0


def calculate_macd(df):
    """
    Calculate MACD and signal line.

    Args:
        df: DataFrame with 'Close' column

    Returns:
        dict: {'macd': float, 'signal': float, 'histogram': float}
    """
    try:
        macd_indicator = ta.trend.MACD(close=df['Close'])
        return {
            'macd': macd_indicator.macd().iloc[-1],
            'signal': macd_indicator.macd_signal().iloc[-1],
            'histogram': macd_indicator.macd_diff().iloc[-1]
        }
    except Exception:
        return {'macd': 0, 'signal': 0, 'histogram': 0}


def calculate_moving_averages(df):
    """
    Calculate key moving averages.

    Args:
        df: DataFrame with 'Close' column

    Returns:
        dict: {'sma_20': float, 'sma_50': float, 'sma_200': float}
    """
    try:
        close = df['Close']
        return {
            'sma_20': ta.trend.SMAIndicator(close, window=20).sma_indicator().iloc[-1] if len(df) >= 20 else close.iloc[-1],
            'sma_50': ta.trend.SMAIndicator(close, window=50).sma_indicator().iloc[-1] if len(df) >= 50 else close.iloc[-1],
            'sma_200': ta.trend.SMAIndicator(close, window=200).sma_indicator().iloc[-1] if len(df) >= 200 else close.iloc[-1]
        }
    except Exception:
        return {'sma_20': 0, 'sma_50': 0, 'sma_200': 0}


def calculate_bollinger_bands(df):
    """
    Calculate Bollinger Bands.

    Args:
        df: DataFrame with 'Close' column

    Returns:
        dict: {'upper': float, 'middle': float, 'lower': float}
    """
    try:
        bb_indicator = ta.volatility.BollingerBands(close=df['Close'])
        return {
            'upper': bb_indicator.bollinger_hband().iloc[-1],
            'middle': bb_indicator.bollinger_mavg().iloc[-1],
            'lower': bb_indicator.bollinger_lband().iloc[-1]
        }
    except Exception:
        return {'upper': 0, 'middle': 0, 'lower': 0}


def calculate_volatility(df):
    """
    Calculate realized volatility (annualized).

    Args:
        df: DataFrame with 'Close' column

    Returns:
        float: Annualized volatility in percentage
    """
    try:
        returns = df['Close'].pct_change().dropna()
        if len(returns) > 0:
            volatility = returns.std() * np.sqrt(252) * 100
            return volatility
        return 0.0
    except Exception:
        return 0.0


def get_sentiment_signal(df, current_price):
    """
    Determine market sentiment based on multiple technical indicators.

    Args:
        df: DataFrame with OHLCV data
        current_price: Current market price

    Returns:
        dict: {
            'sentiment': 'bullish'|'bearish'|'neutral',
            'arrow': '🔼'|'🔽'|'➡️',
            'score': int (-100 to 100),
            'signals': dict of individual signal contributions
        }
    """
    signals = {}
    score = 0

    try:
        # RSI Signal (-30 to +30)
        rsi = calculate_rsi(df)
        signals['rsi'] = rsi
        if rsi < 30:
            score += 30  # Oversold = Bullish
        elif rsi > 70:
            score -= 30  # Overbought = Bearish
        elif rsi < 40:
            score += 15
        elif rsi > 60:
            score -= 15

        # MACD Signal (-20 to +20)
        macd_data = calculate_macd(df)
        signals['macd'] = macd_data
        if macd_data['histogram'] > 0:
            score += 20  # Positive momentum
        else:
            score -= 20  # Negative momentum

        # Moving Average Signal (-30 to +30)
        ma_data = calculate_moving_averages(df)
        signals['moving_averages'] = ma_data

        # Price vs MA20
        if current_price > ma_data['sma_20']:
            score += 15
        else:
            score -= 15

        # MA20 vs MA50 (Golden/Death Cross)
        if len(df) >= 50:
            if ma_data['sma_20'] > ma_data['sma_50']:
                score += 15
            else:
                score -= 15

        # Trend Signal (-20 to +20)
        # Compare current price to price 5 days ago
        if len(df) >= 5:
            price_5d_ago = df['Close'].iloc[-5]
            pct_change_5d = ((current_price - price_5d_ago) / price_5d_ago) * 100

            if pct_change_5d > 2:
                score += 20
            elif pct_change_5d < -2:
                score -= 20
            elif pct_change_5d > 0:
                score += 10
            else:
                score -= 10

    except Exception as e:
        # If calculation fails, return neutral
        score = 0

    # Determine sentiment
    if score > 20:
        sentiment = 'bullish'
        arrow = '🔼'
    elif score < -20:
        sentiment = 'bearish'
        arrow = '🔽'
    else:
        sentiment = 'neutral'
        arrow = '➡️'

    return {
        'sentiment': sentiment,
        'arrow': arrow,
        'score': score,
        'signals': signals,
        'rsi': signals.get('rsi', 50)
    }


def calculate_all_indicators(df):
    """
    Calculate all technical indicators for a given DataFrame.

    Args:
        df: DataFrame with OHLCV data

    Returns:
        dict: Dictionary containing all calculated indicators
    """
    current_price = df['Close'].iloc[-1]

    return {
        'rsi': calculate_rsi(df),
        'macd': calculate_macd(df),
        'moving_averages': calculate_moving_averages(df),
        'bollinger_bands': calculate_bollinger_bands(df),
        'volatility': calculate_volatility(df),
        'sentiment': get_sentiment_signal(df, current_price)
    }
