import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import time
import os
import sys

# Add project root to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

# Page Config (Must be first Streamlit command)
st.set_page_config(
    page_title="Market Pulse | Green Chips Analytics",
    page_icon="../assets/favcon.png",
    layout="wide",
    initial_sidebar_state="expanded"
)



# Import components and data fetchers
from data.fetchers.market_data import fetch_market_data, get_market_status, fetch_nifty_50_data
from data.fetchers.multi_market_data import fetch_index_constituents, fetch_market_index_history, get_market_vix_data
from config.constants import INDICES, TIMEFRAMES
from config.markets import MARKETS, get_market_config
from components.market_card import render_market_card
from components.heatmap import render_heatmap
from components.risk_meter import render_risk_meter
from utils.market_time import MarketSchedule
from utils.theme import load_premium_theme
from utils.auto_refresh import setup_auto_refresh, render_refresh_controls, get_last_refresh_time
from utils.error_handler import safe_data_fetch, handle_empty_data, ErrorBoundary
from utils.ui import render_sidebar_header, render_sidebar_navigation

# Load Premium White Theme
try:
    load_premium_theme()
except Exception as e:
    st.error(f"Error loading CSS: {e}")

# Setup Auto-Refresh
setup_auto_refresh(default_interval=300)  # 5 minutes default

# Sidebar: Auto-Refresh Controls
with st.sidebar:
    render_sidebar_header()
    render_sidebar_navigation()
    
    st.markdown("### ⚙️ Settings")

    # Auto-refresh controls
    should_refresh = render_refresh_controls()
    if should_refresh:
        st.cache_data.clear()
        st.rerun()

    st.markdown("---")

    # Performance Stats
    st.markdown("### 📊 Performance")
    if 'last_refresh' in st.session_state:
        st.caption(f"Last refresh: {get_last_refresh_time()}")

    # Cache info
    st.caption("💾 Data caching enabled")

    st.markdown("---")
    
    # Logo in Sidebar Bottom? Or Top?
    # Navigation is handled by multipage app structure usually.
    # Let's add the logo ID at the top if possible, but st.sidebar is sequential.
    # The user manual had it at the top. 
    # Let's put it in the "About" section or just clean up.
    
    # About
    st.markdown("### ℹ️ About")
    
    st.caption("**Green Chips**")
        
    st.caption("Real-time market intelligence.")
    st.caption("Version 1.0")

# Cached data fetching functions for performance
@st.cache_data(ttl=300, show_spinner=False)  # Cache for 5 minutes
@safe_data_fetch(fallback_value={}, error_message="Failed to fetch market data", show_error=False)
def fetch_market_data_cached(symbol):
    """Cached version of fetch_market_data with error handling."""
    return fetch_market_data(symbol)

@st.cache_data(ttl=300, show_spinner=False)
@safe_data_fetch(fallback_value=pd.DataFrame(), error_message="Failed to fetch index constituents", show_error=False)
def fetch_index_constituents_cached(market_id, limit=None):
    """Cached version of fetch_index_constituents with error handling."""
    return fetch_index_constituents(market_id, limit)

@st.cache_data(ttl=600, show_spinner=False)  # Cache for 10 minutes (less volatile)
@safe_data_fetch(fallback_value=pd.DataFrame(), error_message="Failed to fetch historical data", show_error=False)
def fetch_market_index_history_cached(market_id, period_years=5):
    """Cached version of fetch_market_index_history with error handling."""
    return fetch_market_index_history(market_id, period_years)

@st.cache_data(ttl=600, show_spinner=False)  # Cache for 10 minutes
@safe_data_fetch(fallback_value=pd.DataFrame(), error_message="Failed to fetch symbol data", show_error=False)
def fetch_symbol_history_cached(symbol, period_years=5):
    """Cached version of fetch_symbol_history for any symbol (index or sector)."""
    from data.fetchers.multi_market_data import fetch_symbol_history
    return fetch_symbol_history(symbol, period_years)

@st.cache_data(ttl=600, show_spinner=False)
@safe_data_fetch(fallback_value=pd.DataFrame(), error_message="Failed to fetch VIX data", show_error=False)
def get_market_vix_data_cached(market_id, period_years=5):
    """Cached version of get_market_vix_data with error handling."""
    return get_market_vix_data(market_id, period_years)

@st.cache_data(ttl=300, show_spinner=False)
@safe_data_fetch(fallback_value={}, error_message="Failed to fetch sector performance", show_error=False)
def fetch_sector_performance_cached(market_id):
    """Cached version of fetch_sector_performance with error handling."""
    from data.fetchers.multi_market_data import fetch_sector_performance
    return fetch_sector_performance(market_id)

# Page Title and Header (Ultra-Compact)
logo_path = os.path.join(project_root, "assets", "greenchips_logo.jpeg")
col_header, col_notify = st.columns([10, 1])
with col_header:
    # Function to load image as base64
    def get_img_as_base64(file_path):
        import base64
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()

    if os.path.exists(logo_path):
        img_base64 = get_img_as_base64(logo_path)
        img_html = f'<img src="data:image/jpeg;base64,{img_base64}" style="width: 40px; height: 40px; border-radius: 50%; object-fit: cover; vertical-align: middle; margin-right: 10px;">'
    else:
        img_html = '<span style="font-size: 30px; vertical-align: middle; margin-right: 10px;">🟢</span>'

    st.markdown(f"""
        <div style="display: flex; align-items: center;">
            {img_html}
            <h3 style="margin: 0; padding: 0; font-size: 1.2rem; display: inline-block; vertical-align: middle;">Green Chips Analytics</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.caption("Real-time global market intelligence")

with col_notify:
    # Notification Icon for Market Timings
    if st.button("🕒", help="Market Timings (IST)"):
        st.session_state['show_timings'] = not st.session_state.get('show_timings', False)

# Market Schedule Logic
schedule = MarketSchedule()
timings = schedule.get_market_timings()

# Show Timings Dialog/Expander if toggled
if st.session_state.get('show_timings', False):
    with st.expander("🌍 Global Market Timings (IST)", expanded=True):
        st.markdown("### Market Status & Hours")
        
        # Create a clean table
        timing_data = pd.DataFrame(timings)
        
        # Style the dataframe
        def color_status(val):
            color = 'red'
            if val == 'Open': color = 'green'
            elif val == 'Pre-Market': color = 'orange'
            return f'color: {color}; font-weight: bold'

        st.dataframe(
            timing_data[['Market', 'Status', 'Open (IST)', 'Close (IST)', 'Local Time']].style.applymap(color_status, subset=['Status']),
            hide_index=True,
            use_container_width=True
        )

# Top Bar: Status & Refresh (Compact)
col1, col2 = st.columns([4, 1])
with col1:
    # Quick Status Strip
    status_html_parts = []
    for item in timings:
        if item['Market'] in ["India (NSE)", "USA (NYSE)", "Gold (CME)"]:
            icon = "🟢" if item['Status'] == "Open" else "🔴"
            if item['Status'] in ["Pre-Market", "Break"]: icon = "🟠"
            status_html_parts.append(f"{icon} {item['Market']}: {item['Status']}")

    status_html = " &nbsp;|&nbsp; ".join(status_html_parts)
    st.markdown(f"<small>{status_html}</small>", unsafe_allow_html=True)

with col2:
    col_btn, col_time = st.columns([1, 2])
    with col_btn:
        if st.button("🔄", help="Refresh Data"):
            st.cache_data.clear()
            st.session_state.last_refresh = datetime.now()
            st.rerun()
    with col_time:
        st.caption(f"Updated: {get_last_refresh_time()}")

# Main Layout: 2-Column Design (Command Center Left, Market Overview Right)
main_col1, main_col2 = st.columns([1, 2.5])  # 1:2.5 ratio (left narrower, right wider)

# LEFT COLUMN: Market Command Center (Risk-On/Risk-Off Meter)
with main_col1:
    st.markdown("<p style='font-size: 0.85rem; font-weight: 700; margin: 0; color: #6c757d;'>📊 MARKET COMMAND CENTER</p>", unsafe_allow_html=True)

    # Fetch key markets for risk calculation
    with st.spinner("Calculating..."):
        risk_markets = {}
        key_symbols = ['^GSPC', '^NSEI', '^VIX', 'BTC-USD', 'GC=F', 'DX-Y.NYB', '^FTSE', '^N225']

        for symbol in key_symbols:
            try:
                data = fetch_market_data_cached(symbol)
                if data:
                    risk_markets[symbol] = data
            except Exception as e:
                continue

        # Render the Risk-On/Risk-Off meter
        if risk_markets:
            render_risk_meter(risk_markets)
        else:
            st.warning("Unable to calculate market regime.")

# RIGHT COLUMN: Market Overview (Tabbed - Ultra-Compact)
with main_col2:
    st.markdown("<p style='font-size: 0.85rem; font-weight: 700; margin: 0; color: #6c757d;'>📈 MARKET OVERVIEW</p>", unsafe_allow_html=True)

    # Helper to render markets in a compact grid (2 columns for cleaner layout)
    def render_compact_group(title, markets_dict):
        """Render markets in a 2-column grid for compact display"""
        market_items = list(markets_dict.items())

        # Create 2-column layout for markets
        for i in range(0, len(market_items), 2):
            cols = st.columns(2)

            # First column
            if i < len(market_items):
                name, symbol = market_items[i]
                with cols[0]:
                    data = fetch_market_data_cached(symbol)
                    if data:
                        data['name'] = name
                        render_market_card(data)
                    else:
                        st.error(f"{name}")

            # Second column
            if i + 1 < len(market_items):
                name, symbol = market_items[i + 1]
                with cols[1]:
                    data = fetch_market_data_cached(symbol)
                    if data:
                        data['name'] = name
                        render_market_card(data)
                    else:
                        st.error(f"{name}")

    # Create 7 tabs for different asset classes
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "🇮🇳 India",
        "🇺🇸 US",
        "🇪🇺 Europe",
        "🌏 Asia-Pac",
        "🟡 Commod",
        "💱 Forex",
        "₿ Crypto"
    ])

    # Tab 1: India Markets
    with tab1:
        render_compact_group("India", INDICES["INDIA"])

    # Tab 2: US Markets
    with tab2:
        render_compact_group("US", INDICES["US"])

    # Tab 3: European Markets
    with tab3:
        render_compact_group("Europe", INDICES["EUROPE"])

    # Tab 4: Asia-Pacific Markets
    with tab4:
        render_compact_group("Asia-Pacific", INDICES["ASIA_PACIFIC"])

    # Tab 5: Commodities
    with tab5:
        render_compact_group("Commodities", INDICES["COMMODITIES"])

    # Tab 6: Forex
    with tab6:
        render_compact_group("Forex", INDICES["FOREX"])

    # Tab 7: Crypto
    with tab7:
        render_compact_group("Crypto", INDICES["CRYPTO"])

st.markdown("<br>", unsafe_allow_html=True)

# Market Selector Section (placed before Index Analysis)
st.markdown("---")
st.markdown("### 🌍 Select Market for Deep Analysis")

col_selector, col_info = st.columns([3, 7])

with col_selector:
    selected_market = st.selectbox(
        "Choose market to analyze",
        options=list(MARKETS.keys()),
        format_func=lambda x: f"{MARKETS[x]['flag']} {MARKETS[x]['name']}",
        key="market_selector"
    )
    # Get market configuration
    market_config = get_market_config(selected_market)

with col_info:
    st.info(f"📊 You're now analyzing **{market_config['main_index']['name']}** with {market_config['main_index']['constituents_count']} constituents. Currency: {market_config['currency']}")

st.markdown("<br>", unsafe_allow_html=True)

# Fetch index data for selected market
index_name = market_config['main_index']['name']
with st.spinner(f"Fetching {index_name} data..."):
    index_data = fetch_index_constituents_cached(selected_market, limit=100 if selected_market == "USA" else None)

# Validate data
if not handle_empty_data(index_data, data_name=f"{index_name} data", show_warning=False):
    st.warning(f"⚠️ {index_name} data is currently unavailable. Please try refreshing.")

# Dynamic Analysis Section Title
st.markdown(f"#### 📈 {index_name} Analysis")

tab1, tab2, tab3 = st.tabs(["📅 Seasonality", "📊 Market Breadth", "📈 Historical Analysis"])

# Tab 2: Market Breadth
with tab2:
    with ErrorBoundary("Market Breadth"):
        st.markdown("##### Market Breadth Indicators")

        if not index_data.empty:
            # Calculate breadth metrics
            advancing = (index_data['Change %'] > 0).sum()
            declining = (index_data['Change %'] < 0).sum()
            unchanged = (index_data['Change %'] == 0).sum()
            ad_ratio = advancing / declining if declining > 0 else advancing

            # Display metrics
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    "Advancing",
                    advancing,
                    delta=f"{advancing/50*100:.0f}% of stocks",
                    delta_color="normal"
                )

            with col2:
                st.metric(
                    "Declining",
                    declining,
                    delta=f"{declining/50*100:.0f}% of stocks",
                    delta_color="inverse"
                )

            with col3:
                st.metric(
                    "A/D Ratio",
                    f"{ad_ratio:.2f}",
                    delta="Bullish" if ad_ratio > 1 else "Bearish"
                )

            with col4:
                avg_change = index_data['Change %'].mean()
                st.metric(
                    "Avg Change",
                    f"{avg_change:+.2f}%",
                    delta="Positive breadth" if avg_change > 0 else "Negative breadth"
                )

            # Market breadth interpretation with enhanced visuals
            if ad_ratio > 2:
                breadth_status = "Strong Bullish"
                breadth_icon = "🚀"
                breadth_color = "#00d48a"
                gradient_start = "rgba(0, 212, 138, 0.2)"
                gradient_end = "rgba(0, 212, 138, 0.05)"
                progress_width = "100%"
            elif ad_ratio > 1:
                breadth_status = "Bullish"
                breadth_icon = "📈"
                breadth_color = "#00d48a"
                gradient_start = "rgba(0, 212, 138, 0.15)"
                gradient_end = "rgba(0, 212, 138, 0.03)"
                progress_width = "75%"
            elif ad_ratio > 0.5:
                breadth_status = "Neutral"
                breadth_icon = "➡️"
                breadth_color = "#ffa502"
                gradient_start = "rgba(255, 165, 2, 0.15)"
                gradient_end = "rgba(255, 165, 2, 0.03)"
                progress_width = "50%"
            else:
                breadth_status = "Bearish"
                breadth_icon = "📉"
                breadth_color = "#ff4757"
                gradient_start = "rgba(255, 71, 87, 0.15)"
                gradient_end = "rgba(255, 71, 87, 0.03)"
                progress_width = "25%"

            st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, {gradient_start} 0%, {gradient_end} 100%), #ffffff;
            border-radius: 16px;
            padding: 24px 28px;
            margin-top: 20px;
            border: 2px solid {breadth_color}30;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08), 0 1px 3px rgba(0, 0, 0, 0.05);
            position: relative;
            overflow: hidden;
        ">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px;">
                <div style="display: flex; align-items: center; gap: 14px;">
                    <div style="
                        background: linear-gradient(135deg, {breadth_color}20 0%, {breadth_color}10 100%);
                        border-radius: 12px;
                        padding: 12px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                    ">
                        <span style="font-size: 2.2rem;">{breadth_icon}</span>
                    </div>
                    <div>
                        <h3 style="color: {breadth_color}; margin: 0; font-size: 1.65rem; font-weight: 700; letter-spacing: -0.02em;">{breadth_status}</h3>
                        <p style="color: #6c757d; font-size: 0.9rem; margin: 4px 0 0 0; font-weight: 500;">Market Breadth Signal</p>
                    </div>
                </div>
                <div style="text-align: right;">
                    <p style="color: {breadth_color}; font-size: 2.2rem; font-weight: 800; margin: 0; letter-spacing: -0.03em;">{ad_ratio:.2f}</p>
                    <p style="color: #adb5bd; font-size: 0.8rem; margin: 2px 0 0 0; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">A/D Ratio</p>
                </div>
            </div>
            <div style="
                width: 100%;
                height: 10px;
                background: linear-gradient(90deg, #e9ecef 0%, #f1f3f5 100%);
                border-radius: 12px;
                overflow: hidden;
                margin-top: 14px;
                box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.06);
            ">
                <div style="
                    width: {progress_width};
                    height: 100%;
                    background: linear-gradient(90deg, {breadth_color} 0%, {breadth_color}dd 100%);
                    border-radius: 12px;
                    transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
                    box-shadow: 0 0 12px {breadth_color}60;
                "></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        else:
            st.info("Market breadth data unavailable")

        st.markdown("<br>", unsafe_allow_html=True)

        # Heatmap Section
        st.markdown("##### 🔥 Market Heatmap")

        if not index_data.empty:
            # Validate data has required columns before rendering
            required_cols = ['Symbol', 'Change %', 'Market Cap', 'Sector', 'Price']
            missing_cols = [col for col in required_cols if col not in index_data.columns]

            if missing_cols:
                st.error(f"⚠️ Market data is incomplete. Missing: {', '.join(missing_cols)}")
                st.info("💡 This usually indicates a data fetch issue. Try refreshing the page.")
            else:
                render_heatmap(index_data, currency=market_config['currency'], index_name=index_name)
        else:
            st.error(f"❌ Failed to load {index_name} data for heatmap")
            st.info("💡 Possible reasons:\n- Market is currently closed\n- Data provider (Yahoo Finance) is temporarily unavailable\n- Network connectivity issue\n\n**Try:** Refresh the page or check back when the market is open.")

        st.markdown("<br>", unsafe_allow_html=True)

        # Top Movers (Real Data)
        st.markdown("##### 🚀 Top Movers")
        col_g, col_l = st.columns(2)

        if not index_data.empty:
            # Sort by Change %
            df_sorted = index_data.sort_values(by="Change %", ascending=False)

            top_gainers = df_sorted.head(5)[['Symbol', 'Price', 'Change %', 'Volume']]
            top_losers = df_sorted.tail(5).sort_values(by="Change %", ascending=True)[['Symbol', 'Price', 'Change %', 'Volume']]

            with col_g:
                st.markdown("###### Top Gainers")
                st.dataframe(
                    top_gainers.style.format({"Price": "{:.2f}", "Change %": "{:+.2f}%", "Volume": "{:,}"}),
                    hide_index=True,
                    use_container_width=True
                )

            with col_l:
                st.markdown("###### Top Losers")
                st.dataframe(
                    top_losers.style.format({"Price": "{:.2f}", "Change %": "{:+.2f}%", "Volume": "{:,}"}),
                    hide_index=True,
                    use_container_width=True
                )
        else:
            st.info("No data available for Top Movers")

        # Sector Analysis Section
        st.markdown("---")
        st.markdown("##### 🏭 Sector Rotation & Performance")
        st.caption("Identify leading and lagging sectors for rotation strategies")

        # Fetch sector performance data with caching and error handling
        with st.spinner("Fetching sector data..."):
            sector_data = fetch_sector_performance_cached(selected_market)

        if sector_data:
            # Create DataFrame for easier manipulation
            sectors_df = pd.DataFrame([
                {
                    'Sector': name,
                    'Price': data['price'],
                    'Change %': data['change_pct']
                }
                for name, data in sector_data.items()
            ])

            # Sort by performance
            sectors_df = sectors_df.sort_values('Change %', ascending=False)

            # Sector Performance Overview
            st.markdown("##### 📊 Sector Performance Overview")

            col1, col2, col3, col4 = st.columns(4)

            advancing_sectors = (sectors_df['Change %'] > 0).sum()
            declining_sectors = (sectors_df['Change %'] < 0).sum()
            total_sectors = len(sectors_df)
            avg_sector_change = sectors_df['Change %'].mean()

            with col1:
                st.metric(
                    "Advancing Sectors",
                    advancing_sectors,
                    delta=f"{advancing_sectors/total_sectors*100:.0f}% of sectors"
                )

            with col2:
                st.metric(
                    "Declining Sectors",
                    declining_sectors,
                    delta=f"{declining_sectors/total_sectors*100:.0f}% of sectors",
                    delta_color="inverse"
                )

            with col3:
                st.metric(
                    "Avg Sector Change",
                    f"{avg_sector_change:+.2f}%",
                    delta="Sector strength"
                )

            with col4:
                best_sector = sectors_df.iloc[0]
                st.metric(
                    "Leader",
                    best_sector['Sector'][:12] + "..." if len(best_sector['Sector']) > 12 else best_sector['Sector'],
                    delta=f"{best_sector['Change %']:+.2f}%"
                )

            # Sector Rotation Analysis
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("##### 🔄 Sector Rotation Map")

            # Categorize sectors
            strong_threshold = sectors_df['Change %'].quantile(0.75)
            weak_threshold = sectors_df['Change %'].quantile(0.25)

            hot_sectors = sectors_df[sectors_df['Change %'] >= strong_threshold]
            warm_sectors = sectors_df[(sectors_df['Change %'] < strong_threshold) & (sectors_df['Change %'] > 0)]
            cool_sectors = sectors_df[(sectors_df['Change %'] <= 0) & (sectors_df['Change %'] > weak_threshold)]
            cold_sectors = sectors_df[sectors_df['Change %'] <= weak_threshold]

            col_hot, col_warm, col_cool, col_cold = st.columns(4)

            with col_hot:
                st.markdown("""
                <div style="background: linear-gradient(135deg, rgba(0, 212, 138, 0.15) 0%, rgba(0, 212, 138, 0.05) 100%);
                            border-left: 4px solid #00d48a; padding: 15px; border-radius: 8px; height: 200px;">
                    <p style="margin: 0; font-size: 0.75rem; color: #6c757d; font-weight: 600;">🔥 HOT SECTORS</p>
                    <p style="margin: 5px 0 10px 0; font-size: 0.85rem; color: #00d48a; font-weight: 700;">Strong Outperformance</p>
                """, unsafe_allow_html=True)
                for _, sector in hot_sectors.iterrows():
                    st.markdown(f"<p style='margin: 3px 0; font-size: 0.75rem;'>• {sector['Sector'][:15]}: <span style='color: #00d48a; font-weight: 600;'>{sector['Change %']:+.1f}%</span></p>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            with col_warm:
                st.markdown("""
                <div style="background: linear-gradient(135deg, rgba(0, 212, 138, 0.08) 0%, rgba(0, 212, 138, 0.02) 100%);
                            border-left: 4px solid #51cf66; padding: 15px; border-radius: 8px; height: 200px;">
                    <p style="margin: 0; font-size: 0.75rem; color: #6c757d; font-weight: 600;">📈 WARM SECTORS</p>
                    <p style="margin: 5px 0 10px 0; font-size: 0.85rem; color: #51cf66; font-weight: 700;">Moderate Gains</p>
                """, unsafe_allow_html=True)
                for _, sector in warm_sectors.iterrows():
                    st.markdown(f"<p style='margin: 3px 0; font-size: 0.75rem;'>• {sector['Sector'][:15]}: <span style='color: #51cf66; font-weight: 600;'>{sector['Change %']:+.1f}%</span></p>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            with col_cool:
                st.markdown("""
                <div style="background: linear-gradient(135deg, rgba(255, 71, 87, 0.08) 0%, rgba(255, 71, 87, 0.02) 100%);
                            border-left: 4px solid #ff6b81; padding: 15px; border-radius: 8px; height: 200px;">
                    <p style="margin: 0; font-size: 0.75rem; color: #6c757d; font-weight: 600;">📉 COOL SECTORS</p>
                    <p style="margin: 5px 0 10px 0; font-size: 0.85rem; color: #ff6b81; font-weight: 700;">Minor Weakness</p>
                """, unsafe_allow_html=True)
                for _, sector in cool_sectors.iterrows():
                    st.markdown(f"<p style='margin: 3px 0; font-size: 0.75rem;'>• {sector['Sector'][:15]}: <span style='color: #ff6b81; font-weight: 600;'>{sector['Change %']:+.1f}%</span></p>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            with col_cold:
                st.markdown("""
                <div style="background: linear-gradient(135deg, rgba(255, 71, 87, 0.15) 0%, rgba(255, 71, 87, 0.05) 100%);
                            border-left: 4px solid #ff4757; padding: 15px; border-radius: 8px; height: 200px;">
                    <p style="margin: 0; font-size: 0.75rem; color: #6c757d; font-weight: 600;">❄️ COLD SECTORS</p>
                    <p style="margin: 5px 0 10px 0; font-size: 0.85rem; color: #ff4757; font-weight: 700;">Significant Weakness</p>
                """, unsafe_allow_html=True)
                for _, sector in cold_sectors.iterrows():
                    st.markdown(f"<p style='margin: 3px 0; font-size: 0.75rem;'>• {sector['Sector'][:15]}: <span style='color: #ff4757; font-weight: 600;'>{sector['Change %']:+.1f}%</span></p>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            # Sector Performance Chart
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("##### 📊 Sector Performance Comparison")

            fig_sectors = go.Figure()

            colors = ['#00d48a' if x > 0 else '#ff4757' for x in sectors_df['Change %']]

            fig_sectors.add_trace(go.Bar(
                y=sectors_df['Sector'],
                x=sectors_df['Change %'],
                orientation='h',
                marker_color=colors,
                text=sectors_df['Change %'].apply(lambda x: f'{x:+.2f}%'),
                textposition='outside',
                hovertemplate='<b>%{y}</b><br>Change: %{x:+.2f}%<extra></extra>'
            ))

            fig_sectors.update_layout(
                title='Today\'s Sector Performance Ranking',
                xaxis_title='Change %',
                yaxis_title='',
                template='plotly_white',
                height=max(400, len(sectors_df) * 30),
                showlegend=False,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Inter, sans-serif"),
                yaxis=dict(autorange="reversed")
            )

            st.plotly_chart(fig_sectors, use_container_width=True)

            # Sector Strength Table
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("##### 📈 Detailed Sector Metrics")

            # Add relative strength score (normalized)
            sectors_df['Strength Score'] = ((sectors_df['Change %'] - sectors_df['Change %'].min()) /
                                             (sectors_df['Change %'].max() - sectors_df['Change %'].min()) * 100).round(0)

            def color_performance(val):
                if val > 1:
                    return 'background-color: #d4edda; color: #155724; font-weight: 600;'
                elif val > 0:
                    return 'background-color: #d1ecf1; color: #0c5460; font-weight: 600;'
                elif val > -1:
                    return 'background-color: #fff3cd; color: #856404; font-weight: 600;'
                else:
                    return 'background-color: #f8d7da; color: #721c24; font-weight: 600;'

            styled_sectors = sectors_df[['Sector', 'Change %', 'Strength Score']].style.format({
                'Change %': '{:+.2f}%',
                'Strength Score': '{:.0f}'
            }).applymap(color_performance, subset=['Change %'])

            st.dataframe(styled_sectors, hide_index=True, use_container_width=True)

            # Sector Rotation Strategy Insights
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("##### 💡 Rotation Strategy Insights")

            best_3 = sectors_df.head(3)
            worst_3 = sectors_df.tail(3)

            col_insights1, col_insights2 = st.columns(2)

            with col_insights1:
                st.markdown("""
                <div style="background: linear-gradient(135deg, rgba(0, 212, 138, 0.1) 0%, rgba(0, 212, 138, 0.05) 100%);
                            border-left: 4px solid #00d48a; padding: 20px; border-radius: 10px;">
                    <p style="margin: 0 0 10px 0; font-size: 0.75rem; color: #6c757d; font-weight: 600;">🎯 ROTATION INTO</p>
                    <p style="margin: 0 0 15px 0; font-size: 0.95rem; font-weight: 700; color: #00d48a;">Top Performing Sectors</p>
                """, unsafe_allow_html=True)
                for idx, row in best_3.iterrows():
                    st.markdown(f"<p style='margin: 5px 0; font-size: 0.85rem;'><b>{row['Sector']}</b>: {row['Change %']:+.2f}%</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='margin-top: 15px; font-size: 0.75rem; color: #6c757d;'>💡 Avg: {best_3['Change %'].mean():+.2f}% | Consider overweight</p>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            with col_insights2:
                st.markdown("""
                <div style="background: linear-gradient(135deg, rgba(255, 71, 87, 0.1) 0%, rgba(255, 71, 87, 0.05) 100%);
                            border-left: 4px solid #ff4757; padding: 20px; border-radius: 10px;">
                    <p style="margin: 0 0 10px 0; font-size: 0.75rem; color: #6c757d; font-weight: 600;">⚠️ ROTATION OUT OF</p>
                    <p style="margin: 0 0 15px 0; font-size: 0.95rem; font-weight: 700; color: #ff4757;">Underperforming Sectors</p>
                """, unsafe_allow_html=True)
                for idx, row in worst_3.iterrows():
                    st.markdown(f"<p style='margin: 5px 0; font-size: 0.85rem;'><b>{row['Sector']}</b>: {row['Change %']:+.2f}%</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='margin-top: 15px; font-size: 0.75rem; color: #6c757d;'>⚠️ Avg: {worst_3['Change %'].mean():+.2f}% | Consider underweight</p>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

        else:
            st.warning("No sector data available for the selected market")

# Tab 3: Historical Analysis
with tab3:
    with ErrorBoundary("Historical Analysis"):
        st.markdown("##### NIFTY 50 Historical Performance")

        # Year selector
        import yfinance as yf
        import plotly.graph_objects as go
        from datetime import datetime, timedelta

        col1, col2 = st.columns([4, 1])
        with col1:
            years = st.slider(
                "Select number of years for historical analysis",
                min_value=1,
                max_value=10,
                value=5,
                step=1,
                help="Drag to select the number of years of historical data to analyze"
            )
        with col2:
            st.metric("Period", f"{years}Y", delta=None)

        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=years * 365)

        with st.spinner("Fetching historical data..."):
            try:
                # Fetch historical data for selected market with ErrorBoundary
                hist_data = fetch_market_index_history_cached(selected_market, period_years=years)

                if not hist_data.empty:
                    # Calculate moving averages
                    hist_data['MA20'] = hist_data['Close'].rolling(window=20).mean()
                    hist_data['MA50'] = hist_data['Close'].rolling(window=50).mean()

                    # Create candlestick chart with moving averages
                    fig = go.Figure()

                    # Add candlestick
                    fig.add_trace(go.Candlestick(
                        x=hist_data.index,
                        open=hist_data['Open'],
                        high=hist_data['High'],
                        low=hist_data['Low'],
                        close=hist_data['Close'],
                        name='NIFTY 50',
                        increasing_line_color='#00d48a',
                        decreasing_line_color='#ff4757'
                    ))

                    # Add moving averages
                    fig.add_trace(go.Scatter(
                        x=hist_data.index,
                        y=hist_data['MA20'],
                        mode='lines',
                        name='MA 20',
                        line=dict(color='#4361ee', width=1.5)
                    ))

                    fig.add_trace(go.Scatter(
                        x=hist_data.index,
                        y=hist_data['MA50'],
                        mode='lines',
                        name='MA 50',
                        line=dict(color='#7209b7', width=1.5)
                    ))

                    # Update layout
                    fig.update_layout(
                        title=f'{index_name} - {years} Year Chart',
                        yaxis_title='Price (₹)',
                        xaxis_title='Date',
                        template='plotly_white',
                        height=500,
                        hovermode='x unified',
                        xaxis_rangeslider_visible=False,
                        font=dict(family="Inter, sans-serif"),
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                    )

                    st.plotly_chart(fig, use_container_width=True)

                    # Calculate daily A/D values
                    hist_data['Daily_Change'] = hist_data['Close'] - hist_data['Open']
                    hist_data['Is_Advancing'] = (hist_data['Daily_Change'] > 0).astype(int)
                    hist_data['Is_Declining'] = (hist_data['Daily_Change'] < 0).astype(int)

                    # Calculate cumulative A/D Line (Volume-weighted)
                    hist_data['AD_Value'] = hist_data['Volume'] * np.where(
                        hist_data['Daily_Change'] > 0, 1,
                        np.where(hist_data['Daily_Change'] < 0, -1, 0)
                    )
                    hist_data['AD_Line'] = hist_data['AD_Value'].cumsum()

                    # Calculate rolling A/D Ratio (20-day window)
                    hist_data['Advancing_20D'] = hist_data['Is_Advancing'].rolling(window=20).sum()
                    hist_data['Declining_20D'] = hist_data['Is_Declining'].rolling(window=20).sum()
                    hist_data['AD_Ratio_20D'] = hist_data['Advancing_20D'] / hist_data['Declining_20D'].replace(0, 1)

                    # Normalize A/D Line for better visualization
                    ad_normalized = (hist_data['AD_Line'] - hist_data['AD_Line'].min()) / (hist_data['AD_Line'].max() - hist_data['AD_Line'].min()) * 100

                    # A/D Line Indicator Chart
                    fig_ad_line = go.Figure()

                    fig_ad_line.add_trace(go.Scatter(
                        x=hist_data.index,
                        y=ad_normalized,
                        mode='lines',
                        name='A/D Line',
                        line=dict(color='#4361ee', width=2),
                        fill='tozeroy',
                        fillcolor='rgba(67, 97, 238, 0.1)'
                    ))

                    fig_ad_line.add_hline(
                        y=50,
                        line_dash="dash",
                        line_color="#adb5bd",
                        annotation_text="Neutral",
                        annotation_position="right"
                    )

                    fig_ad_line.update_layout(
                        yaxis_title='A/D Line',
                        xaxis_title='',
                        template='plotly_white',
                        height=150,
                        hovermode='x unified',
                        font=dict(family="Inter, sans-serif", size=10),
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        showlegend=False,
                        margin=dict(t=10, l=50, r=20, b=30),
                        xaxis=dict(showticklabels=False)
                    )

                    st.plotly_chart(fig_ad_line, use_container_width=True)

                    # A/D Ratio Indicator Chart
                    fig_ad_ratio = go.Figure()

                    fig_ad_ratio.add_trace(go.Scatter(
                        x=hist_data.index,
                        y=hist_data['AD_Ratio_20D'],
                        mode='lines',
                        name='A/D Ratio',
                        line=dict(color='#00d48a', width=2)
                    ))

                    fig_ad_ratio.add_hline(y=1.0, line_dash="dash", line_color="#adb5bd", annotation_text="1.0", annotation_position="right")
                    fig_ad_ratio.add_hline(y=2.0, line_dash="dot", line_color="#00d48a", annotation_text="2.0", annotation_position="right", annotation_font_size=9)
                    fig_ad_ratio.add_hline(y=0.5, line_dash="dot", line_color="#ff4757", annotation_text="0.5", annotation_position="right", annotation_font_size=9)

                    fig_ad_ratio.update_layout(
                        yaxis_title='A/D Ratio',
                        xaxis_title='',
                        template='plotly_white',
                        height=150,
                        hovermode='x unified',
                        font=dict(family="Inter, sans-serif", size=10),
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        showlegend=False,
                        margin=dict(t=10, l=50, r=20, b=30),
                        xaxis=dict(showticklabels=False)
                    )

                    st.plotly_chart(fig_ad_ratio, use_container_width=True)

                    # VIX Indicator Chart (Market-specific)
                    try:
                        vix_name = market_config.get('vix_name', 'VIX')
                        vix_data = get_market_vix_data_cached(selected_market, period_years=years)

                        if not vix_data.empty:
                            fig_vix = go.Figure()

                            fig_vix.add_trace(go.Scatter(
                                x=vix_data.index,
                                y=vix_data['Close'],
                                mode='lines',
                                name=vix_name,
                                line=dict(color='#ff4757', width=2),
                                fill='tozeroy',
                                fillcolor='rgba(255, 71, 87, 0.1)'
                            ))

                            # VIX reference levels
                            fig_vix.add_hline(y=20, line_dash="dash", line_color="#ffa502", annotation_text="High Volatility (20)", annotation_position="right", annotation_font_size=9)
                            fig_vix.add_hline(y=15, line_dash="dot", line_color="#adb5bd", annotation_text="Moderate (15)", annotation_position="right", annotation_font_size=9)

                            fig_vix.update_layout(
                                yaxis_title=vix_name,
                                xaxis_title='Date',
                                template='plotly_white',
                                height=150,
                                hovermode='x unified',
                                font=dict(family="Inter, sans-serif", size=10),
                                paper_bgcolor='rgba(0,0,0,0)',
                                plot_bgcolor='rgba(0,0,0,0)',
                                showlegend=False,
                                margin=dict(t=10, l=50, r=20, b=40)
                            )

                            st.plotly_chart(fig_vix, use_container_width=True)
                    except Exception as e:
                        st.warning(f"Could not load NIFTY VIX data: {e}")

                    # Performance Metrics (moved to end)
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("###### Performance Metrics")

                    start_price = hist_data['Close'].iloc[0]
                    end_price = hist_data['Close'].iloc[-1]
                    change = end_price - start_price
                    change_pct = (change / start_price) * 100

                    high = hist_data['High'].max()
                    low = hist_data['Low'].min()
                    avg_volume = hist_data['Volume'].mean()

                    col1, col2, col3, col4 = st.columns(4)

                    with col1:
                        st.metric(
                            "Period Return",
                            f"{change_pct:+.2f}%",
                            delta=f"₹{change:+.2f}"
                        )

                    with col2:
                        st.metric(
                            "Period High",
                            f"₹{high:.2f}",
                            delta=f"{((high - end_price) / end_price * 100):+.2f}% from current"
                        )

                    with col3:
                        st.metric(
                            "Period Low",
                            f"₹{low:.2f}",
                            delta=f"{((end_price - low) / low * 100):+.2f}% from current"
                        )

                    with col4:
                        st.metric(
                            "Avg Daily Volume",
                            f"{avg_volume/1e7:.2f}M",
                            delta="shares"
                        )

                    # Summary metrics
                    st.markdown("<br>", unsafe_allow_html=True)
                    col1, col2, col3 = st.columns(3)

                    total_advancing = hist_data['Is_Advancing'].sum()
                    total_declining = hist_data['Is_Declining'].sum()
                    current_ad_ratio = hist_data['AD_Ratio_20D'].iloc[-1] if not pd.isna(hist_data['AD_Ratio_20D'].iloc[-1]) else 0

                    with col1:
                        st.metric(
                            "Total Advancing Days",
                            f"{total_advancing}",
                            delta=f"{total_advancing/(total_advancing+total_declining)*100:.1f}% of days"
                        )

                    with col2:
                        st.metric(
                            "Total Declining Days",
                            f"{total_declining}",
                            delta=f"{total_declining/(total_advancing+total_declining)*100:.1f}% of days"
                        )

                    with col3:
                        ad_status = "Bullish" if current_ad_ratio > 1 else "Bearish"
                        st.metric(
                            "Current A/D Ratio (20D)",
                            f"{current_ad_ratio:.2f}",
                            delta=ad_status
                        )

                else:
                    st.error("No historical data available")

            except Exception as e:
                st.error(f"Error fetching historical data: {e}")

# Tab 1: Seasonality Analysis
with tab1:
    with ErrorBoundary("Seasonality Analysis"):
        st.markdown("##### 📅 Seasonal Patterns & Trading Edge")
        st.caption("Discover which months historically favor bulls or bears")

        # Index/Sector Selection
        st.markdown("---")
        col_selector, col_button = st.columns([3, 1])

        with col_selector:
            # Build options based on selected market
            market_config = get_market_config(selected_market)

            # Create dropdown options
            options = []
            option_symbols = {}  # Map display name to symbol

            # Add main index first
            main_index_name = f"📊 {market_config['main_index']['name']}"
            options.append(main_index_name)
            option_symbols[main_index_name] = market_config['main_index']['symbol']

            # Add sectors
            for sector_name, sector_symbol in market_config.get('sectors', {}).items():
                display_name = f"🏭 {sector_name}"
                options.append(display_name)
                option_symbols[display_name] = sector_symbol

            # Index/Sector selector
            selected_option = st.selectbox(
                "Select Index or Sector for Seasonality Analysis",
                options=options,
                index=0,  # Default to main index
                help="Choose an index or sector to analyze seasonal patterns"
            )

            # Get the symbol for the selected option
            selected_symbol = option_symbols[selected_option]
            selected_display_name = selected_option.replace("📊 ", "").replace("🏭 ", "")

        with col_button:
            st.markdown("<br>", unsafe_allow_html=True)  # Add spacing
            analyze_clicked = st.button("🔍 Analyze", type="primary", use_container_width=True)

        # Year range selector
        col1, col2 = st.columns([4, 1])
        with col1:
            season_years = st.slider(
                "Select number of years for seasonality analysis",
                min_value=5,
                max_value=15,
                value=10,
                step=1,
                help="Analyze seasonal patterns over the selected time period"
            )
        with col2:
            st.metric("Period", f"{season_years}Y", delta=None)

        # Initialize session state for analysis trigger
        if 'season_analyzed' not in st.session_state:
            st.session_state.season_analyzed = True  # Auto-analyze on first load

        # Update session state on button click
        if analyze_clicked:
            st.session_state.season_analyzed = True
            st.cache_data.clear()  # Clear cache to fetch fresh data

        # Only run analysis if button was clicked or first load
        if st.session_state.get('season_analyzed', False):
            # Fetch historical data for seasonality
            with st.spinner(f"Calculating seasonal patterns for {selected_display_name}..."):
                try:
                    # Use cached fetch for selected symbol (index or sector)
                    season_data = fetch_symbol_history_cached(selected_symbol, period_years=season_years)

                    if not season_data.empty:
                        # Calculate monthly returns
                        season_data['Year'] = season_data.index.year
                        season_data['Month'] = season_data.index.month
                        season_data['Month_Name'] = season_data.index.strftime('%b')
    
                        # Group by year and month to get monthly returns
                        monthly_returns = []
                        for year in season_data['Year'].unique():
                            for month in range(1, 13):
                                month_data = season_data[(season_data['Year'] == year) & (season_data['Month'] == month)]
                                if len(month_data) > 0:
                                    month_return = ((month_data['Close'].iloc[-1] - month_data['Close'].iloc[0]) / month_data['Close'].iloc[0]) * 100
                                    monthly_returns.append({
                                        'Year': year,
                                        'Month': month,
                                        'Month_Name': month_data['Month_Name'].iloc[0],
                                        'Return': month_return
                                    })
    
                        df_monthly = pd.DataFrame(monthly_returns)
    
                        # Create pivot table for heatmap
                        pivot_data = df_monthly.pivot(index='Year', columns='Month_Name', values='Return')
    
                        # Reorder columns to calendar order
                        month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                        pivot_data = pivot_data.reindex(columns=[m for m in month_order if m in pivot_data.columns])
    
                        # Create layout: Heatmap (70%) and Stats (30%)
                        col_heat, col_stats = st.columns([7, 3])
    
                        with col_heat:
                            # Monthly Performance Heatmap
                            import plotly.express as px
    
                            fig_heatmap = px.imshow(
                                pivot_data,
                                labels=dict(x="Month", y="Year", color="Return %"),
                                x=pivot_data.columns,
                                y=pivot_data.index,
                                color_continuous_scale=[
                                    [0.0, '#d63031'],    # Deep Red
                                    [0.3, '#ff4757'],    # Red
                                    [0.5, '#f1f3f5'],    # Light Grey
                                    [0.7, '#00d48a'],    # Green
                                    [1.0, '#00a86b']     # Deep Green
                                ],
                                color_continuous_midpoint=0,
                                aspect="auto"
                            )
    
                            fig_heatmap.update_layout(
                                title='Monthly Performance Heatmap (%)',
                                height=400,
                                font=dict(family="Inter, sans-serif"),
                                paper_bgcolor='rgba(0,0,0,0)',
                                plot_bgcolor='rgba(0,0,0,0)',
                                coloraxis_colorbar=dict(
                                    title="Return %",
                                    thickness=15,
                                    len=0.7
                                )
                            )
    
                            fig_heatmap.update_traces(
                                text=np.round(pivot_data.values, 1),
                                texttemplate='%{text}%',
                                textfont={"size": 10}
                            )
    
                            st.plotly_chart(fig_heatmap, use_container_width=True)
    
                        with col_stats:
                            # Month Statistics Table
                            st.markdown("**Month Stats**")
    
                            month_stats = []
                            for month_name in month_order:
                                if month_name in df_monthly['Month_Name'].values:
                                    month_returns = df_monthly[df_monthly['Month_Name'] == month_name]['Return']
                                    pos_count = (month_returns > 0).sum()
                                    neg_count = (month_returns < 0).sum()
                                    total_count = len(month_returns)
                                    win_rate = (pos_count / total_count * 100) if total_count > 0 else 0
                                    avg_return = month_returns.mean()
    
                                    month_stats.append({
                                        'Month': month_name,
                                        'Pos': pos_count,
                                        'Neg': neg_count,
                                        'Win%': win_rate,
                                        'Avg%': avg_return
                                    })
    
                            df_stats = pd.DataFrame(month_stats)
    
                            # Style the stats table
                            def color_win_rate(val):
                                if val >= 70:
                                    return 'background-color: #d4edda; color: #155724'
                                elif val >= 50:
                                    return 'background-color: #fff3cd; color: #856404'
                                else:
                                    return 'background-color: #f8d7da; color: #721c24'
    
                            styled_stats = df_stats.style.format({
                                'Win%': '{:.0f}%',
                                'Avg%': '{:+.1f}%'
                            }).applymap(color_win_rate, subset=['Win%'])
    
                            st.dataframe(styled_stats, hide_index=True, use_container_width=True, height=460)
    
                        # Key Insights Section
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.markdown("##### 💡 Key Insights")
    
                        # Calculate insights
                        best_months = df_stats.nlargest(3, 'Win%')[['Month', 'Win%', 'Avg%']]
                        worst_months = df_stats.nsmallest(3, 'Win%')[['Month', 'Win%', 'Avg%']]
                        highest_avg = df_stats.nlargest(1, 'Avg%')[['Month', 'Avg%']].iloc[0]
                        current_month_name = datetime.now().strftime('%b')
                        current_month_stats = df_stats[df_stats['Month'] == current_month_name]
    
                        col1, col2, col3 = st.columns(3)
    
                        with col1:
                            st.markdown(f"""
                            <div style="background: linear-gradient(135deg, rgba(0, 212, 138, 0.1) 0%, rgba(0, 212, 138, 0.05) 100%);
                                        border-left: 4px solid #00d48a; padding: 15px; border-radius: 8px;">
                                <p style="margin: 0; font-size: 0.75rem; color: #6c757d; font-weight: 600;">BEST MONTHS</p>
                                <p style="margin: 5px 0 0 0; font-size: 1.1rem; font-weight: 700; color: #00d48a;">
                                    {', '.join(best_months['Month'].tolist())}
                                </p>
                                <p style="margin: 5px 0 0 0; font-size: 0.8rem; color: #6c757d;">
                                    Win Rate: {best_months['Win%'].iloc[0]:.0f}%
                                </p>
                            </div>
                            """, unsafe_allow_html=True)
    
                        with col2:
                            st.markdown(f"""
                            <div style="background: linear-gradient(135deg, rgba(255, 71, 87, 0.1) 0%, rgba(255, 71, 87, 0.05) 100%);
                                        border-left: 4px solid #ff4757; padding: 15px; border-radius: 8px;">
                                <p style="margin: 0; font-size: 0.75rem; color: #6c757d; font-weight: 600;">WEAKEST MONTHS</p>
                                <p style="margin: 5px 0 0 0; font-size: 1.1rem; font-weight: 700; color: #ff4757;">
                                    {', '.join(worst_months['Month'].tolist())}
                                </p>
                                <p style="margin: 5px 0 0 0; font-size: 0.8rem; color: #6c757d;">
                                    Win Rate: {worst_months['Win%'].iloc[0]:.0f}%
                                </p>
                            </div>
                            """, unsafe_allow_html=True)
    
                        with col3:
                            if not current_month_stats.empty:
                                current_win = current_month_stats['Win%'].iloc[0]
                                current_avg = current_month_stats['Avg%'].iloc[0]
                                color = '#00d48a' if current_win >= 50 else '#ff4757'
                                st.markdown(f"""
                                <div style="background: linear-gradient(135deg, rgba(67, 97, 238, 0.1) 0%, rgba(67, 97, 238, 0.05) 100%);
                                            border-left: 4px solid #4361ee; padding: 15px; border-radius: 8px;">
                                    <p style="margin: 0; font-size: 0.75rem; color: #6c757d; font-weight: 600;">CURRENT MONTH</p>
                                    <p style="margin: 5px 0 0 0; font-size: 1.1rem; font-weight: 700; color: #4361ee;">
                                        {current_month_name}
                                    </p>
                                    <p style="margin: 5px 0 0 0; font-size: 0.8rem; color: {color};">
                                        Win Rate: {current_win:.0f}% | Avg: {current_avg:+.1f}%
                                    </p>
                                </div>
                                """, unsafe_allow_html=True)
    
                        # Quarterly Performance
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.markdown("##### 📈 Quarterly Performance")
    
                        df_monthly['Quarter'] = df_monthly['Month'].apply(lambda x: f'Q{(x-1)//3 + 1}')
                        quarterly_stats = df_monthly.groupby('Quarter').agg({
                            'Return': ['mean', lambda x: (x > 0).sum() / len(x) * 100]
                        }).round(2)
                        quarterly_stats.columns = ['Avg Return %', 'Win Rate %']
                        quarterly_stats = quarterly_stats.reindex(['Q1', 'Q2', 'Q3', 'Q4'])
    
                        col1, col2, col3, col4 = st.columns(4)
                        quarters = [col1, col2, col3, col4]
    
                        for idx, (quarter, row) in enumerate(quarterly_stats.iterrows()):
                            with quarters[idx]:
                                color = '#00d48a' if row['Avg Return %'] > 0 else '#ff4757'
                                st.metric(
                                    quarter,
                                    f"{row['Avg Return %']:+.1f}%",
                                    delta=f"Win Rate: {row['Win Rate %']:.0f}%"
                                )
    
                        # Deep Dive: Granular Seasonality Analysis
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.markdown("---")
                        st.markdown("#### 🔍 Deep Dive: Granular Seasonality")
                        st.caption("Drill down into weekly, daily, or day-of-week patterns")
    
                        # Drill-down view selector
                        col_view, col_month = st.columns([3, 2])
    
                        with col_view:
                            drill_view = st.radio(
                                "Select Drill-Down View:",
                                ["📊 Weekly (Week 1-5)", "📅 Daily (Day 1-31)", "📆 Day-of-Week (Mon-Fri)"],
                                horizontal=True,
                                label_visibility="collapsed"
                            )
    
                        # Weekly Seasonality (Week 1-5)
                        if drill_view == "📊 Weekly (Week 1-5)":
                            with col_month:
                                selected_month = st.selectbox(
                                    "Select Month",
                                    month_order,
                                    index=datetime.now().month - 1
                                )
    
                            st.markdown(f"**Weekly Performance Analysis - {selected_month}**")
    
                            # Calculate week-of-month for each date
                            season_data_copy = season_data.copy()
                            season_data_copy['Date'] = season_data_copy.index
                            season_data_copy['Year'] = season_data_copy['Date'].dt.year
                            season_data_copy['Month'] = season_data_copy['Date'].dt.month
                            season_data_copy['Month_Name'] = season_data_copy['Date'].dt.strftime('%b')
                            season_data_copy['Day'] = season_data_copy['Date'].dt.day
    
                            # Calculate week of month (1-5)
                            season_data_copy['Week_of_Month'] = ((season_data_copy['Day'] - 1) // 7) + 1
                            season_data_copy['Week_of_Month'] = season_data_copy['Week_of_Month'].clip(1, 5)
    
                            # Filter for selected month
                            month_num = month_order.index(selected_month) + 1
                            month_data = season_data_copy[season_data_copy['Month'] == month_num].copy()
    
                            if len(month_data) > 0:
                                # Calculate weekly returns
                                weekly_returns = []
                                for year in month_data['Year'].unique():
                                    for week in range(1, 6):
                                        week_data = month_data[(month_data['Year'] == year) & (month_data['Week_of_Month'] == week)]
                                        if len(week_data) > 1:
                                            week_return = ((week_data['Close'].iloc[-1] - week_data['Close'].iloc[0]) / week_data['Close'].iloc[0]) * 100
                                            weekly_returns.append({
                                                'Year': year,
                                                'Week': f'Week {week}',
                                                'Return': week_return
                                            })
    
                                df_weekly = pd.DataFrame(weekly_returns)
    
                                if not df_weekly.empty:
                                    # Create pivot for heatmap
                                    pivot_weekly = df_weekly.pivot(index='Year', columns='Week', values='Return')
                                    pivot_weekly = pivot_weekly.reindex(columns=[f'Week {i}' for i in range(1, 6)])
    
                                    # Layout: Heatmap (70%) and Stats (30%)
                                    col_heat_week, col_stats_week = st.columns([7, 3])
    
                                    with col_heat_week:
                                        # Weekly heatmap
                                        fig_weekly = px.imshow(
                                            pivot_weekly,
                                            labels=dict(x="Week", y="Year", color="Return %"),
                                            x=pivot_weekly.columns,
                                            y=pivot_weekly.index,
                                            color_continuous_scale=[
                                                [0.0, '#d63031'],
                                                [0.3, '#ff4757'],
                                                [0.5, '#f1f3f5'],
                                                [0.7, '#00d48a'],
                                                [1.0, '#00a86b']
                                            ],
                                            color_continuous_midpoint=0,
                                            aspect="auto"
                                        )
    
                                        fig_weekly.update_layout(
                                            title=f'{selected_month} - Weekly Performance Heatmap',
                                            height=350,
                                            font=dict(family="Inter, sans-serif", size=11),
                                            paper_bgcolor='rgba(0,0,0,0)',
                                            plot_bgcolor='rgba(0,0,0,0)',
                                            coloraxis_colorbar=dict(title="Return %", thickness=12, len=0.7)
                                        )
    
                                        fig_weekly.update_traces(
                                            text=np.round(pivot_weekly.values, 1),
                                            texttemplate='%{text}%',
                                            textfont={"size": 9}
                                        )
    
                                        st.plotly_chart(fig_weekly, use_container_width=True)
    
                                    with col_stats_week:
                                        # Week statistics
                                        st.markdown("**Week Stats**")
    
                                        week_stats = []
                                        for week in [f'Week {i}' for i in range(1, 6)]:
                                            if week in df_weekly['Week'].values:
                                                week_returns = df_weekly[df_weekly['Week'] == week]['Return']
                                                pos = (week_returns > 0).sum()
                                                neg = (week_returns < 0).sum()
                                                total = len(week_returns)
                                                win_rate = (pos / total * 100) if total > 0 else 0
                                                avg_return = week_returns.mean()
    
                                                week_stats.append({
                                                    'Week': week,
                                                    'Pos': pos,
                                                    'Neg': neg,
                                                    'Win%': win_rate,
                                                    'Avg%': avg_return
                                                })
    
                                        df_week_stats = pd.DataFrame(week_stats)
    
                                        styled_week_stats = df_week_stats.style.format({
                                            'Win%': '{:.0f}%',
                                            'Avg%': '{:+.1f}%'
                                        }).applymap(
                                            lambda val: (
                                                'background-color: #d4edda; color: #155724' if val >= 70 else
                                                'background-color: #fff3cd; color: #856404' if val >= 50 else
                                                'background-color: #f8d7da; color: #721c24'
                                            ),
                                            subset=['Win%']
                                        )
    
                                        st.dataframe(styled_week_stats, hide_index=True, use_container_width=True, height=220)
    
                                        # Best week insight
                                        best_week = df_week_stats.loc[df_week_stats['Win%'].idxmax()]
                                        st.markdown(f"""
                                        <div style="margin-top: 10px; padding: 10px; background: linear-gradient(135deg, rgba(0, 212, 138, 0.1) 0%, rgba(0, 212, 138, 0.05) 100%);
                                                    border-left: 3px solid #00d48a; border-radius: 5px;">
                                            <p style="margin: 0; font-size: 0.7rem; color: #6c757d; font-weight: 600;">BEST WEEK</p>
                                            <p style="margin: 3px 0 0 0; font-size: 0.95rem; font-weight: 700; color: #00d48a;">{best_week['Week']}</p>
                                            <p style="margin: 2px 0 0 0; font-size: 0.75rem; color: #6c757d;">
                                                {best_week['Win%']:.0f}% Win | {best_week['Avg%']:+.1f}% Avg
                                            </p>
                                        </div>
                                        """, unsafe_allow_html=True)
                                else:
                                    st.info(f"Not enough data for {selected_month} weekly analysis")
                            else:
                                st.info(f"No data available for {selected_month}")
    
                        # Daily Seasonality (Day 1-31)
                        elif drill_view == "📅 Daily (Day 1-31)":
                            with col_month:
                                selected_month = st.selectbox(
                                    "Select Month",
                                    month_order,
                                    index=datetime.now().month - 1,
                                    key="daily_month"
                                )
    
                            st.markdown(f"**Daily Performance Analysis - {selected_month}**")
    
                            # Calculate daily returns for selected month
                            month_num = month_order.index(selected_month) + 1
                            season_data_daily = season_data.copy()
                            season_data_daily['Year'] = season_data_daily.index.year
                            season_data_daily['Month'] = season_data_daily.index.month
                            season_data_daily['Day'] = season_data_daily.index.day
    
                            month_daily_data = season_data_daily[season_data_daily['Month'] == month_num].copy()
    
                            if len(month_daily_data) > 0:
                                # Calculate daily returns
                                month_daily_data['Daily_Return'] = month_daily_data['Close'].pct_change() * 100
    
                                daily_returns = []
                                for day in range(1, 32):
                                    day_data = month_daily_data[month_daily_data['Day'] == day]
                                    if len(day_data) > 0:
                                        for _, row in day_data.iterrows():
                                            if not pd.isna(row['Daily_Return']):
                                                daily_returns.append({
                                                    'Year': row['Year'],
                                                    'Day': day,
                                                    'Return': row['Daily_Return']
                                                })
    
                                df_daily = pd.DataFrame(daily_returns)
    
                                if not df_daily.empty:
                                    # Create pivot for heatmap
                                    pivot_daily = df_daily.pivot_table(index='Year', columns='Day', values='Return', aggfunc='mean')
    
                                    # Layout
                                    col_heat_day, col_stats_day = st.columns([7, 3])
    
                                    with col_heat_day:
                                        fig_daily = px.imshow(
                                            pivot_daily,
                                            labels=dict(x="Day", y="Year", color="Return %"),
                                            x=pivot_daily.columns,
                                            y=pivot_daily.index,
                                            color_continuous_scale=[
                                                [0.0, '#d63031'],
                                                [0.3, '#ff4757'],
                                                [0.5, '#f1f3f5'],
                                                [0.7, '#00d48a'],
                                                [1.0, '#00a86b']
                                            ],
                                            color_continuous_midpoint=0,
                                            aspect="auto"
                                        )
    
                                        fig_daily.update_layout(
                                            title=f'{selected_month} - Daily Performance Heatmap',
                                            height=350,
                                            font=dict(family="Inter, sans-serif", size=10),
                                            paper_bgcolor='rgba(0,0,0,0)',
                                            plot_bgcolor='rgba(0,0,0,0)',
                                            coloraxis_colorbar=dict(title="Return %", thickness=12, len=0.7)
                                        )
    
                                        fig_daily.update_traces(
                                            text=np.round(pivot_daily.values, 1),
                                            texttemplate='%{text}%',
                                            textfont={"size": 7}
                                        )
    
                                        st.plotly_chart(fig_daily, use_container_width=True)
    
                                    with col_stats_day:
                                        # Day statistics summary
                                        st.markdown("**Day Stats (Top 10)**")
    
                                        day_stats = df_daily.groupby('Day').agg({
                                            'Return': ['mean', lambda x: (x > 0).sum() / len(x) * 100, 'count']
                                        }).round(2)
                                        day_stats.columns = ['Avg%', 'Win%', 'Count']
                                        day_stats = day_stats[day_stats['Count'] >= 3]  # Filter days with at least 3 data points
                                        day_stats = day_stats.sort_values('Avg%', ascending=False).head(10)
    
                                        st.dataframe(
                                            day_stats.style.format({'Avg%': '{:+.1f}%', 'Win%': '{:.0f}%'}),
                                            use_container_width=True,
                                            height=400
                                        )
                                else:
                                    st.info(f"Not enough data for {selected_month} daily analysis")
                            else:
                                st.info(f"No data available for {selected_month}")
    
                        # Day-of-Week Analysis
                        elif drill_view == "📆 Day-of-Week (Mon-Fri)":
                            st.markdown("**Day-of-Week Performance Analysis**")
    
                            # Calculate day of week returns
                            season_data_dow = season_data.copy()
                            season_data_dow['DayOfWeek'] = season_data_dow.index.day_name()
                            season_data_dow['Daily_Return'] = season_data_dow['Close'].pct_change() * 100
    
                            # Filter out weekends (if any)
                            weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
                            season_data_dow = season_data_dow[season_data_dow['DayOfWeek'].isin(weekdays)]
    
                            if not season_data_dow.empty:
                                # Calculate statistics by day of week
                                dow_stats = season_data_dow.groupby('DayOfWeek').agg({
                                    'Daily_Return': ['mean', lambda x: (x > 0).sum() / len(x) * 100, 'count']
                                }).round(2)
                                dow_stats.columns = ['Avg Return %', 'Win Rate %', 'Count']
    
                                # Reorder by weekday
                                dow_stats = dow_stats.reindex(weekdays)
    
                                # Display metrics
                                st.markdown("##### Performance by Day of Week")
                                cols = st.columns(5)
    
                                day_abbr = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
                                for idx, (day, abbr) in enumerate(zip(weekdays, day_abbr)):
                                    with cols[idx]:
                                        if day in dow_stats.index:
                                            avg_ret = dow_stats.loc[day, 'Avg Return %']
                                            win_rate = dow_stats.loc[day, 'Win Rate %']
    
                                            st.metric(
                                                abbr,
                                                f"{avg_ret:+.2f}%",
                                                delta=f"{win_rate:.0f}% WR"
                                            )
    
                                # Visualization
                                st.markdown("<br>", unsafe_allow_html=True)
    
                                col_chart_dow, col_insights_dow = st.columns([6, 4])
    
                                with col_chart_dow:
                                    # Bar chart
                                    fig_dow = go.Figure()
    
                                    colors = ['#00d48a' if x > 0 else '#ff4757' for x in dow_stats['Avg Return %']]
    
                                    fig_dow.add_trace(go.Bar(
                                        x=day_abbr,
                                        y=dow_stats['Avg Return %'],
                                        marker_color=colors,
                                        text=dow_stats['Avg Return %'].apply(lambda x: f'{x:+.2f}%'),
                                        textposition='outside'
                                    ))
    
                                    fig_dow.update_layout(
                                        title='Average Return by Day of Week',
                                        yaxis_title='Average Return %',
                                        template='plotly_white',
                                        height=300,
                                        showlegend=False,
                                        paper_bgcolor='rgba(0,0,0,0)',
                                        plot_bgcolor='rgba(0,0,0,0)',
                                        font=dict(family="Inter, sans-serif")
                                    )
    
                                    st.plotly_chart(fig_dow, use_container_width=True)
    
                                with col_insights_dow:
                                    st.markdown("**Key Insights**")
    
                                    best_day = dow_stats['Avg Return %'].idxmax()
                                    worst_day = dow_stats['Avg Return %'].idxmin()
                                    best_wr_day = dow_stats['Win Rate %'].idxmax()
    
                                    st.markdown(f"""
                                    <div style="padding: 12px; background: linear-gradient(135deg, rgba(0, 212, 138, 0.1) 0%, rgba(0, 212, 138, 0.05) 100%);
                                                border-left: 3px solid #00d48a; border-radius: 6px; margin-bottom: 10px;">
                                        <p style="margin: 0; font-size: 0.7rem; color: #6c757d; font-weight: 600;">BEST DAY</p>
                                        <p style="margin: 3px 0 0 0; font-size: 1rem; font-weight: 700; color: #00d48a;">{best_day}</p>
                                        <p style="margin: 2px 0 0 0; font-size: 0.75rem; color: #6c757d;">
                                            Avg: {dow_stats.loc[best_day, 'Avg Return %']:+.2f}%
                                        </p>
                                    </div>
    
                                    <div style="padding: 12px; background: linear-gradient(135deg, rgba(255, 71, 87, 0.1) 0%, rgba(255, 71, 87, 0.05) 100%);
                                                border-left: 3px solid #ff4757; border-radius: 6px; margin-bottom: 10px;">
                                        <p style="margin: 0; font-size: 0.7rem; color: #6c757d; font-weight: 600;">WEAKEST DAY</p>
                                        <p style="margin: 3px 0 0 0; font-size: 1rem; font-weight: 700; color: #ff4757;">{worst_day}</p>
                                        <p style="margin: 2px 0 0 0; font-size: 0.75rem; color: #6c757d;">
                                            Avg: {dow_stats.loc[worst_day, 'Avg Return %']:+.2f}%
                                        </p>
                                    </div>
    
                                    <div style="padding: 12px; background: linear-gradient(135deg, rgba(67, 97, 238, 0.1) 0%, rgba(67, 97, 238, 0.05) 100%);
                                                border-left: 3px solid #4361ee; border-radius: 6px;">
                                        <p style="margin: 0; font-size: 0.7rem; color: #6c757d; font-weight: 600;">HIGHEST WIN RATE</p>
                                        <p style="margin: 3px 0 0 0; font-size: 1rem; font-weight: 700; color: #4361ee;">{best_wr_day}</p>
                                        <p style="margin: 2px 0 0 0; font-size: 0.75rem; color: #6c757d;">
                                            Win Rate: {dow_stats.loc[best_wr_day, 'Win Rate %']:.0f}%
                                        </p>
                                    </div>
                                    """, unsafe_allow_html=True)
    
                                # Detailed table
                                st.markdown("<br>", unsafe_allow_html=True)
                                st.markdown("**Detailed Statistics**")
                                st.dataframe(
                                    dow_stats.style.format({
                                        'Avg Return %': '{:+.2f}%',
                                        'Win Rate %': '{:.1f}%',
                                        'Count': '{:.0f}'
                                    }),
                                    use_container_width=True
                                )
    
                    else:
                        st.error("No historical data available for seasonality analysis")

                except Exception as e:
                    st.error(f"Error calculating seasonality: {e}")

