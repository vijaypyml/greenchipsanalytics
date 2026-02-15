"""
Premium white theme for Green Chips Analytics.
Professional, clean design with a million-dollar feel.
"""

import streamlit as st
import os


def load_premium_theme():
    """
    Loads the premium white theme with sophisticated styling.
    """
    # Premium White Theme Colors
    premium_theme = """
    :root {
        --bg-color: #f8f9fa;
        --bg-gradient: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        --card-bg: #ffffff;
        --card-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        --card-shadow-hover: 0 8px 24px rgba(0, 0, 0, 0.12);
        --text-main: #1a1a1a;
        --text-secondary: #6c757d;
        --text-muted: #adb5bd;
        --border-color: #e9ecef;
        --border-accent: #dee2e6;
        --hover-color: #00d48a;
        --primary-green: #00d48a;
        --primary-red: #ff4757;
        --accent-blue: #4361ee;
        --accent-purple: #7209b7;
        --gradient-green: linear-gradient(135deg, #00d48a 0%, #00a86b 100%);
        --gradient-red: linear-gradient(135deg, #ff4757 0%, #d63031 100%);
    }
    """

    # Get path to CSS file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    css_path = os.path.join(project_root, 'assets', 'style.css')

    try:
        with open(css_path) as f:
            css_content = f.read()
        st.markdown(f'<style>{premium_theme}\n{css_content}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"CSS file not found at {css_path}")
    except Exception as e:
        st.error(f"Error loading CSS: {e}")


def get_current_theme():
    """
    Returns 'light' theme as the app is now white-themed only.

    Returns:
        str: Always returns 'light'
    """
    return 'light'
