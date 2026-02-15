"""
Error handling utilities for MarketPulse.
Provides graceful error handling and user-friendly messages.
"""

import streamlit as st
import functools
import logging
from typing import Callable, Any, Optional


# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def safe_data_fetch(
    fallback_value: Any = None,
    error_message: str = "Failed to load data",
    show_error: bool = True
):
    """
    Decorator for safe data fetching with graceful error handling.

    Args:
        fallback_value: Value to return on error
        error_message: User-friendly error message
        show_error: Whether to show error in UI

    Returns:
        Decorated function with error handling
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ConnectionError as e:
                logger.error(f"Connection error in {func.__name__}: {e}")
                if show_error:
                    st.error(f"🌐 {error_message} - Connection issue. Please check your internet.")
                return fallback_value
            except TimeoutError as e:
                logger.error(f"Timeout in {func.__name__}: {e}")
                if show_error:
                    st.warning(f"⏱️ {error_message} - Request timed out. Trying again...")
                return fallback_value
            except ValueError as e:
                logger.error(f"Data validation error in {func.__name__}: {e}")
                if show_error:
                    st.warning(f"📊 {error_message} - Invalid data received.")
                return fallback_value
            except Exception as e:
                logger.error(f"Unexpected error in {func.__name__}: {e}")
                if show_error:
                    st.error(f"❌ {error_message} - {str(e)[:100]}")
                return fallback_value

        return wrapper
    return decorator


def handle_empty_data(data, data_name: str = "Data", show_warning: bool = True):
    """
    Check if data is empty and show appropriate message.

    Args:
        data: Data to check (DataFrame, dict, list, etc.)
        data_name: Name of the data for error message
        show_warning: Whether to show warning in UI

    Returns:
        bool: True if data is valid, False if empty
    """
    import pandas as pd

    is_empty = False

    if data is None:
        is_empty = True
    elif isinstance(data, pd.DataFrame) and data.empty:
        is_empty = True
    elif isinstance(data, (list, dict)) and len(data) == 0:
        is_empty = True

    if is_empty and show_warning:
        st.info(f"ℹ️ {data_name} is currently unavailable. Data may be updating or market is closed.")

    return not is_empty


def show_loading_fallback(message: str = "Loading..."):
    """
    Show a loading placeholder.

    Args:
        message: Loading message to display
    """
    st.info(f"⏳ {message}")


def retry_on_failure(func: Callable, retries: int = 3, delay: float = 1.0):
    """
    Retry a function on failure.

    Args:
        func: Function to retry
        retries: Number of retries
        delay: Delay between retries in seconds

    Returns:
        Function result or None on failure
    """
    import time

    for attempt in range(retries):
        try:
            return func()
        except Exception as e:
            logger.warning(f"Attempt {attempt + 1}/{retries} failed: {e}")
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                logger.error(f"All {retries} attempts failed")
                return None


class ErrorBoundary:
    """
    Context manager for error boundaries in Streamlit components.
    """

    def __init__(self, component_name: str, fallback_ui: Optional[Callable] = None):
        self.component_name = component_name
        self.fallback_ui = fallback_ui

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            logger.error(f"Error in {self.component_name}: {exc_val}")
            st.error(f"❌ Error loading {self.component_name}")

            if self.fallback_ui:
                self.fallback_ui()

            return True  # Suppress exception
        return False
