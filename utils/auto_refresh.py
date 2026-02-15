"""
Auto-refresh utility for MarketPulse.
Provides configurable auto-refresh functionality with user controls.
"""

import streamlit as st
from datetime import datetime
import time


def setup_auto_refresh(default_interval=300):
    """
    Setup auto-refresh functionality with user controls.

    Args:
        default_interval: Default refresh interval in seconds (default: 300 = 5 minutes)

    Returns:
        tuple: (is_enabled, interval_seconds)
    """
    # Initialize session state
    if 'auto_refresh_enabled' not in st.session_state:
        st.session_state.auto_refresh_enabled = False

    if 'refresh_interval' not in st.session_state:
        st.session_state.refresh_interval = default_interval

    if 'last_refresh' not in st.session_state:
        st.session_state.last_refresh = datetime.now()

    return st.session_state.auto_refresh_enabled, st.session_state.refresh_interval


def render_refresh_controls():
    """
    Render auto-refresh controls in the UI.
    Returns True if refresh should happen.
    """
    col1, col2, col3 = st.sidebar.columns([1, 2, 1])

    with col1:
        # Auto-refresh toggle
        auto_refresh = st.checkbox(
            "🔄",
            value=st.session_state.auto_refresh_enabled,
            help="Enable auto-refresh",
            key="auto_refresh_toggle"
        )
        st.session_state.auto_refresh_enabled = auto_refresh

    with col2:
        if auto_refresh:
            # Refresh interval selector
            interval_options = {
                "1 min": 60,
                "2 min": 120,
                "5 min": 300,
                "10 min": 600,
                "15 min": 900
            }

            selected = st.selectbox(
                "Interval",
                options=list(interval_options.keys()),
                index=2,  # Default to 5 min
                label_visibility="collapsed",
                key="refresh_interval_select"
            )

            st.session_state.refresh_interval = interval_options[selected]

    with col3:
        if auto_refresh:
            # Show countdown
            elapsed = (datetime.now() - st.session_state.last_refresh).total_seconds()
            remaining = max(0, st.session_state.refresh_interval - elapsed)

            if remaining == 0:
                st.session_state.last_refresh = datetime.now()
                return True  # Trigger refresh

            st.caption(f"{int(remaining)}s")

            # Auto-rerun after interval
            time.sleep(min(remaining, 1))
            st.rerun()

    return False


def get_last_refresh_time():
    """Get formatted last refresh time."""
    if 'last_refresh' in st.session_state:
        return st.session_state.last_refresh.strftime("%H:%M:%S")
    return "Never"
