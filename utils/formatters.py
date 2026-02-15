"""
Formatting utilities for MarketPulse application.
Provides consistent formatting for currency, percentages, and numbers.
"""


def format_currency(value, currency="$"):
    """
    Formats a number as currency with proper thousand separators.

    Args:
        value: Numeric value to format (can be None)
        currency: Currency symbol (default: "$")

    Returns:
        str: Formatted currency string (e.g., "$1,234.56")

    Examples:
        >>> format_currency(1234.56)
        '$1,234.56'
        >>> format_currency(1234.56, "₹")
        '₹1,234.56'
        >>> format_currency(None)
        '$0.00'
    """
    if value is None:
        return f"{currency}0.00"
    return f"{currency}{value:,.2f}"


def format_percentage(value):
    """
    Formats a number as a percentage with sign.

    Args:
        value: Numeric value to format (can be None)

    Returns:
        str: Formatted percentage string with sign (e.g., "+2.50%" or "-1.23%")

    Examples:
        >>> format_percentage(2.5)
        '+2.50%'
        >>> format_percentage(-1.23)
        '-1.23%'
        >>> format_percentage(None)
        '+0.00%'
    """
    if value is None:
        return "+0.00%"
    return f"{value:+.2f}%"


def format_number(value):
    """
    Formats a number with thousand separators.

    Args:
        value: Numeric value to format (can be None)

    Returns:
        str: Formatted number string (e.g., "1,234.56")

    Examples:
        >>> format_number(1234.56)
        '1,234.56'
        >>> format_number(None)
        '0.00'
    """
    if value is None:
        return "0.00"
    return f"{value:,.2f}"
