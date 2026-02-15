import streamlit as st
import os

def render_sidebar_header():
    """Renders the sidebar header with logo and title."""
    # Custom CSS for Round Logo
    st.markdown("""
    <style>
        [data-testid="stSidebar"] img {
            border-radius: 50%;
            object-fit: cover;
        }
    </style>
    """, unsafe_allow_html=True)

    # Sidebar Header
    col_logo, col_title = st.sidebar.columns([1, 4])
    
    # Construct path relative to this file
    # utils/ui.py -> project_root/utils/ui.py
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    logo_path = os.path.join(project_root, "assets", "greenchips_logo.jpeg")

    with col_logo:
        if os.path.exists(logo_path):
            st.image(logo_path, use_container_width=True)
        else:
            st.warning("Logo not found")

    with col_title:
        st.markdown("<h2 style='margin: 0; padding: 0;'>Green Chips</h2>", unsafe_allow_html=True)
        
    st.sidebar.caption("Premium Market Intelligence")
    st.sidebar.markdown("---")

def render_sidebar_navigation():
    """Renders the sidebar navigation links."""
    st.sidebar.subheader("Navigation")
    
    # Navigation Links
    # Note: Paths are relative to the main application entry point (app.py)
    st.sidebar.page_link("app.py", label="📖 Help & Guide", icon="📚")
    st.sidebar.page_link("pages/01_market_pulse.py", label="📊 Market Pulse", icon="🌐")
    
    st.sidebar.markdown("---")
