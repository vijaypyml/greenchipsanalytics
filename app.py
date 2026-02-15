import streamlit as st
import os
import sys

# Add project root to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Page Config
st.set_page_config(
    page_title="Green Chips Analytics - Help & Guide",
    page_icon="🟢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import theme utilities
from utils.theme import load_premium_theme

# Sidebar Navigation
st.sidebar.title("🟢 Green Chips Analytics")
st.sidebar.caption("Premium Market Intelligence")

# Load Premium White Theme
load_premium_theme()

st.sidebar.markdown("---")
st.sidebar.subheader("Navigation")
st.sidebar.page_link("pages/01_market_pulse.py", label="📊 Market Pulse Dashboard", icon="🌐")
st.sidebar.page_link("app.py", label="📖 Help & Guide", icon="📚")

st.sidebar.markdown("---")

# Quick Links in Sidebar
st.sidebar.subheader("📚 Quick Guide")
st.sidebar.markdown("""
**Get Started:**
1. [Quick Start](#quick-start)
2. [Feature Overview](#feature-overview)
3. [Usage Workflows](#usage-workflows)
4. [Best Practices](#best-practices)

**Need Help?**
- Check troubleshooting tips below
- Review workflow diagrams
- Explore feature details
""")

st.sidebar.markdown("---")
st.sidebar.caption("v2.0.0 | © 2026 Green Chips Analytics")

# ====================================
# MAIN CONTENT - HELP & GUIDE
# ====================================

# Hero Section
st.markdown("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 60px 40px; border-radius: 20px; margin-bottom: 30px;
            box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);">
    <h1 style="color: white; margin: 0; font-size: 3rem; font-weight: 800;">
        📚 MarketPulse Help & Guide
    </h1>
    <p style="color: rgba(255,255,255,0.9); font-size: 1.3rem; margin: 15px 0 0 0;">
        Your complete guide to mastering market analysis and identifying trading opportunities
    </p>
</div>
""", unsafe_allow_html=True)

# Quick Start Section
st.markdown("<div id='quick-start'></div>", unsafe_allow_html=True)
st.markdown("## 🚀 Quick Start")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 📍 First Time Here?

    **Follow these 3 simple steps:**

    1. **Navigate to Market Pulse**
       👉 Click "Market Pulse Dashboard" in the sidebar

    2. **Select Your Market**
       Choose between 🇮🇳 India (NIFTY 50) or 🇺🇸 USA (S&P 500)

    3. **Explore the Tabs**
       📅 Seasonality → 📊 Market Breadth → 📈 Historical Analysis

    **That's it! You're ready to analyze markets.**
    """)

with col2:
    st.markdown("""
    ### ⚡ Key Features at a Glance

    - **📅 Seasonality Analysis**: Find patterns by month, week, or day
    - **📊 Market Breadth**: Current market health & sector rotation
    - **📈 Historical Trends**: Long-term charts with indicators
    - **🔄 Auto-Refresh**: Stay updated with live data
    - **🏭 Sector Analysis**: Identify sector rotation opportunities
    - **📱 Mobile Optimized**: Access from any device
    """)

# Feature Overview Section
st.markdown("<div id='feature-overview'></div>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("## 🎯 Feature Overview")

# Tab 1: Seasonality
with st.expander("📅 **Tab 1: Seasonality Analysis** - Find Historical Patterns", expanded=True):
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        ### What It Does
        Analyzes **5-15 years** of historical data to reveal seasonal patterns in market performance.

        ### Key Features
        - **Monthly Heatmap**: Visual calendar showing best/worst performing months
        - **Quarterly Breakdown**: Q1-Q4 performance comparison
        - **Deep Dives**: Drill down into weekly, daily, or day-of-week patterns
        - **Index & Sector Analysis**: Analyze any index or individual sector

        ### NEW: Sector Seasonality
        - Select any sector (Banking, IT, Energy, etc.)
        - Click "Analyze" to see seasonal patterns for that sector
        - Identify best months to be invested in specific sectors

        ### Best Used For
        ✅ Planning entry/exit timing based on historical trends
        ✅ Identifying seasonally strong months for trading
        ✅ Comparing current performance to historical norms
        ✅ Sector rotation strategies based on seasonal patterns
        """)

    with col2:
        st.info("""
        **💡 Pro Tip**

        Use the heatmap to spot:
        - Consistently green months = Bullish season
        - Consistently red months = Avoid or hedge
        - Recent divergence from pattern = Opportunity
        """)

        st.success("""
        **🎯 Workflow**

        1. Select index or sector
        2. Set period (5-15 years)
        3. Click "Analyze"
        4. Review heatmap
        5. Drill down for details
        """)

# Tab 2: Market Breadth
with st.expander("📊 **Tab 2: Market Breadth** - Current Market Health"):
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        ### What It Does
        Shows **real-time market strength** by analyzing advancing vs. declining stocks and sectors.

        ### Key Features
        - **A/D Ratio**: Advancing to Declining stocks ratio
        - **Market Breadth Status**: Bullish/Bearish/Neutral classification
        - **Sector Heatmap**: Visual representation of sector performance
        - **Top Movers**: Gainers and losers of the day
        - **NEW: Sector Rotation Map**: Hot/Warm/Cool/Cold sector categorization
        - **Rotation Insights**: Sectors to rotate into/out of

        ### Understanding Indicators

        **A/D Ratio:**
        - > 2.0 = 🚀 Strong Bullish
        - > 1.0 = 📈 Bullish
        - 0.5-1.0 = ➡️ Neutral
        - < 0.5 = 📉 Bearish

        **Sector Rotation:**
        - 🔥 Hot: Strong outperformance - overweight
        - 📈 Warm: Moderate gains - maintain
        - 📉 Cool: Minor weakness - caution
        - ❄️ Cold: Significant weakness - underweight

        ### Best Used For
        ✅ Confirming trend strength before taking positions
        ✅ Detecting divergences (price up, breadth down = warning)
        ✅ Identifying overbought/oversold conditions
        ✅ Sector rotation strategies
        """)

    with col2:
        st.warning("""
        **⚠️ Warning Signal**

        If market hits new highs but A/D ratio is falling = **Bearish Divergence**

        Suggests weakness beneath the surface.
        """)

        st.info("""
        **🔄 Rotation Strategy**

        1. Check Hot sectors
        2. Compare to Warm/Cool
        3. Rotate from Cold to Hot
        4. Monitor weekly changes
        """)

# Tab 3: Historical Analysis
with st.expander("📈 **Tab 3: Historical Analysis** - Long-Term Trends"):
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        ### What It Does
        Displays **1-10 years** of price history with key technical indicators and volatility metrics.

        ### Key Features
        - **Candlestick Chart**: Price action with MA20 and MA50
        - **A/D Line**: Cumulative advance/decline indicator
        - **A/D Ratio**: Daily ratio tracking
        - **VIX**: Volatility index (fear gauge)
        - **Performance Metrics**: Returns, drawdown, volatility

        ### Reading the Charts

        **Moving Averages:**
        - MA20 above MA50 = 📈 Uptrend
        - MA20 below MA50 = 📉 Downtrend
        - Price above both MAs = Strong uptrend

        **A/D Line:**
        - Rising with price = Healthy trend
        - Falling with rising price = Bearish divergence
        - Rising with falling price = Bullish divergence

        **VIX Levels:**
        - < 15 = Low volatility (calm)
        - 15-20 = Moderate volatility
        - 20-30 = High volatility (fear)
        - > 30 = Extreme volatility (panic)

        ### Best Used For
        ✅ Identifying long-term trends and reversals
        ✅ Spotting divergences between price and breadth
        ✅ Timing entries during low volatility periods
        ✅ Avoiding high-risk periods (VIX > 30)
        """)

    with col2:
        st.success("""
        **✅ Bullish Setup**

        - Price > MA20 > MA50
        - A/D Line rising
        - VIX < 20
        - Breadth > 1.5

        = Strong buy signal
        """)

        st.error("""
        **❌ Bearish Setup**

        - Price < MA50
        - A/D Line falling
        - VIX > 25
        - Breadth < 0.75

        = Caution/Exit
        """)

# Usage Workflows Section
st.markdown("<div id='usage-workflows'></div>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("## 🔄 Usage Workflows")

workflow_tab1, workflow_tab2, workflow_tab3 = st.tabs([
    "📊 Day Trading Workflow",
    "📈 Swing Trading Workflow",
    "🎯 Long-Term Investing Workflow"
])

with workflow_tab1:
    st.markdown("""
    ### Day Trading Workflow (Intraday)

    **Morning Routine (Before Market Open):**
    """)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        **Step 1: Check Global Markets**
        - Review overnight moves
        - Check US/Europe close
        - Note any major news
        """)
    with col2:
        st.markdown("""
        **Step 2: Market Breadth**
        - Check A/D Ratio
        - Review sector rotation
        - Identify hot sectors
        """)
    with col3:
        st.markdown("""
        **Step 3: Seasonality**
        - Check today's date pattern
        - Review current month trend
        - Note day-of-week bias
        """)

    st.markdown("""
    **During Market Hours:**
    - ✅ Enable Auto-Refresh (1-2 min intervals)
    - ✅ Monitor Market Breadth tab for shifts
    - ✅ Watch sector rotation for opportunities
    - ✅ Check VIX for volatility spikes

    **End of Day:**
    - 📊 Review Historical tab for trend confirmation
    - 📈 Plan next day's sectors based on rotation
    """)

with workflow_tab2:
    st.markdown("""
    ### Swing Trading Workflow (3-10 days)

    **Weekly Analysis:**
    """)

    st.markdown("""
    ```
    1. SEASONALITY (Tab 1)
       └─> Check current month/week pattern
           └─> Is this a historically strong period?
                ├─> YES: Look for bullish setups
                └─> NO: Be cautious or look for shorts

    2. MARKET BREADTH (Tab 2)
       └─> Check A/D Ratio trend
           └─> Is breadth confirming price action?
                ├─> YES: Trend is healthy, follow it
                └─> NO: Divergence alert, reduce position size

    3. HISTORICAL ANALYSIS (Tab 3)
       └─> Check MA alignment and A/D Line
           └─> Both bullish?
                ├─> YES: Full position size
                └─> NO: Wait for alignment

    4. SECTOR ROTATION (Tab 2)
       └─> Identify Hot/Warm sectors
           └─> Focus trades in these sectors

    5. EXECUTE
       └─> Enter positions in aligned setups
           └─> Set stop loss below MA20
                └─> Target: Next resistance or +5-10%
    ```
    """)

with workflow_tab3:
    st.markdown("""
    ### Long-Term Investing Workflow (Months-Years)

    **Monthly Review Process:**
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **1. Quarterly Assessment**
        - Review Seasonality → Quarterly breakdown
        - Identify best quarters historically
        - Check if current quarter aligns with pattern

        **2. Trend Confirmation**
        - Historical tab → Check MA alignment
        - Price above MA50 for at least 3 months = Uptrend
        - A/D Line rising = Broad participation

        **3. Sector Allocation**
        - Use Seasonality for each sector
        - Rotate into sectors with upcoming strong quarters
        - Reduce exposure to seasonally weak sectors
        """)

    with col2:
        st.markdown("""
        **4. Risk Management**
        - VIX > 30 = Reduce equity allocation
        - VIX < 15 = Full allocation
        - A/D Ratio < 1 for 2+ weeks = Take profits

        **5. Rebalancing Triggers**
        - End of strong seasonal quarter
        - Breadth deterioration (A/D < 0.8)
        - VIX spike above 35
        - Sector rotation from Hot to Cool

        **6. Entry Strategy**
        - Wait for pullback to MA50
        - Ensure breadth is improving
        - Check seasonality is favorable
        - Start position, add on strength
        """)

# Best Practices Section
st.markdown("<div id='best-practices'></div>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("## 💡 Best Practices & Pro Tips")

tips_col1, tips_col2 = st.columns(2)

with tips_col1:
    st.markdown("""
    ### ✅ Do's

    **Analysis:**
    - ✅ Start with Seasonality to understand historical context
    - ✅ Confirm with Market Breadth before taking action
    - ✅ Use Historical tab to identify long-term trends
    - ✅ Cross-reference multiple timeframes
    - ✅ Enable Auto-Refresh during market hours (5min intervals)

    **Trading:**
    - ✅ Follow the breadth (don't fight A/D ratio)
    - ✅ Rotate into Hot sectors, avoid Cold sectors
    - ✅ Wait for seasonal patterns to align with technical setup
    - ✅ Use VIX as risk gauge (reduce size when VIX > 25)
    - ✅ Track divergences between price and A/D Line

    **Risk Management:**
    - ✅ Reduce position size during bearish seasonal periods
    - ✅ Take profits when breadth deteriorates (A/D < 0.8)
    - ✅ Cut exposure by 50% when VIX > 30
    - ✅ Respect MA50 as major support/resistance
    """)

with tips_col2:
    st.markdown("""
    ### ❌ Don'ts

    **Analysis:**
    - ❌ Don't rely on just one indicator
    - ❌ Don't ignore seasonality patterns (they matter!)
    - ❌ Don't trade against strong breadth signals
    - ❌ Don't ignore VIX warnings
    - ❌ Don't use very short periods (< 5 years) for seasonality

    **Trading:**
    - ❌ Don't buy when A/D Ratio < 0.5 (bearish)
    - ❌ Don't ignore sector rotation (sectors lead markets)
    - ❌ Don't trade in historically weak months without confirmation
    - ❌ Don't hold long positions when VIX > 35
    - ❌ Don't fight the trend (follow MA alignment)

    **Risk Management:**
    - ❌ Don't go full allocation in seasonally weak periods
    - ❌ Don't add to losers during breadth deterioration
    - ❌ Don't ignore divergences (price vs breadth)
    - ❌ Don't trade without stop losses
    """)

# Common Scenarios Section
st.markdown("---")
st.markdown("## 🎓 Common Scenarios & How to Interpret")

scenario1, scenario2, scenario3 = st.columns(3)

with scenario1:
    st.success("""
    ### 🟢 Bullish Confirmation

    **Signals:**
    - Seasonally strong month ✅
    - A/D Ratio > 1.5 ✅
    - Price > MA20 > MA50 ✅
    - VIX < 18 ✅
    - Hot sectors expanding ✅

    **Action:**
    → Full position size
    → Favor hot sectors
    → Set stop below MA20
    → Hold through month-end
    """)

with scenario2:
    st.warning("""
    ### 🟡 Mixed Signals

    **Signals:**
    - Seasonally neutral month ⚠️
    - A/D Ratio 0.8-1.2 ⚠️
    - Price choppy around MA50 ⚠️
    - VIX 20-25 ⚠️
    - Sectors rotating quickly ⚠️

    **Action:**
    → Reduced position size (50%)
    → Quick trades only
    → Tight stop losses
    → Wait for clarity
    """)

with scenario3:
    st.error("""
    ### 🔴 Bearish Warning

    **Signals:**
    - Seasonally weak month ❌
    - A/D Ratio < 0.7 ❌
    - Price < MA50 ❌
    - VIX > 25 ❌
    - Cold sectors growing ❌

    **Action:**
    → Reduce to 25% or cash
    → Short hot sectors that turn
    → Hedge portfolio
    → Wait for reversal signals
    """)

# Flowchart Section
st.markdown("---")
st.markdown("## 📊 Visual Decision Flowchart")

st.markdown("### Step-by-Step Analysis Process")

# Step 1
st.markdown("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px; border-radius: 10px; margin: 10px 0; text-align: center;">
    <h3 style="color: white; margin: 0;">🎯 START: Open Market Pulse Dashboard</h3>
</div>
""", unsafe_allow_html=True)

st.markdown("### ↓")

# Step 2 - Seasonality Check
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style="background: #fff3cd; border-left: 5px solid #ffc107;
                padding: 20px; border-radius: 10px; margin: 10px 0;">
        <h4 style="margin: 0 0 10px 0;">📅 STEP 1: Check Seasonality (Tab 1)</h4>
        <p style="margin: 0;"><b>Select index or sector → Click Analyze</b></p>
        <p style="margin: 5px 0 0 0;">Review monthly heatmap for current month</p>
    </div>
    """, unsafe_allow_html=True)

# Decision Point 1
col1, col2, col3 = st.columns(3)
with col1:
    st.success("""
    **✅ Bullish Month**
    (Green in heatmap)

    → Proceed to Step 2
    """)
with col2:
    st.warning("""
    **⚠️ Neutral Month**
    (Mixed pattern)

    → Proceed with caution
    """)
with col3:
    st.error("""
    **❌ Bearish Month**
    (Red in heatmap)

    → Reduce risk / Wait
    """)

st.markdown("### ↓")

# Step 3 - Market Breadth
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style="background: #d1ecf1; border-left: 5px solid #0c5460;
                padding: 20px; border-radius: 10px; margin: 10px 0;">
        <h4 style="margin: 0 0 10px 0;">📊 STEP 2: Check Market Breadth (Tab 2)</h4>
        <p style="margin: 0;"><b>Review A/D Ratio and Sector Rotation</b></p>
        <p style="margin: 5px 0 0 0;">Check if current market health confirms seasonality</p>
    </div>
    """, unsafe_allow_html=True)

# Decision Point 2
col1, col2, col3 = st.columns(3)
with col1:
    st.success("""
    **✅ A/D Ratio > 1.5**
    Strong bullish breadth

    → Proceed to Step 3
    """)
with col2:
    st.warning("""
    **⚠️ A/D Ratio 0.8-1.5**
    Mixed breadth

    → Reduced position size
    """)
with col3:
    st.error("""
    **❌ A/D Ratio < 0.8**
    Weak breadth

    → Avoid / Exit positions
    """)

st.markdown("### ↓")

# Step 4 - Historical Trend
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style="background: #d4edda; border-left: 5px solid #155724;
                padding: 20px; border-radius: 10px; margin: 10px 0;">
        <h4 style="margin: 0 0 10px 0;">📈 STEP 3: Check Historical Trend (Tab 3)</h4>
        <p style="margin: 0;"><b>Analyze MA alignment, A/D Line, and VIX</b></p>
        <p style="margin: 5px 0 0 0;">Confirm trend direction and volatility</p>
    </div>
    """, unsafe_allow_html=True)

# Decision Point 3
col1, col2, col3 = st.columns(3)
with col1:
    st.success("""
    **✅ Bullish Trend**
    - Price > MA20 > MA50
    - A/D Line rising
    - VIX < 20

    → Proceed to Step 4
    """)
with col2:
    st.warning("""
    **⚠️ Mixed Signals**
    - Choppy MAs
    - VIX 20-25

    → Small position only
    """)
with col3:
    st.error("""
    **❌ Bearish Trend**
    - Price < MA50
    - VIX > 25

    → Stay out / Hedge
    """)

st.markdown("### ↓")

# Step 5 - Sector Check
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style="background: #fff3cd; border-left: 5px solid #ffc107;
                padding: 20px; border-radius: 10px; margin: 10px 0;">
        <h4 style="margin: 0 0 10px 0;">🏭 STEP 4: Sector Rotation Check (Tab 2)</h4>
        <p style="margin: 0;"><b>Identify Hot/Warm/Cool/Cold sectors</b></p>
        <p style="margin: 5px 0 0 0;">Focus on sectors showing strength</p>
    </div>
    """, unsafe_allow_html=True)

# Decision Point 4
col1, col2, col3 = st.columns(3)
with col1:
    st.success("""
    **🔥 Hot Sectors Expanding**
    Strong sector leadership

    → FULL POSITION ✅
    """)
with col2:
    st.warning("""
    **📈 Mixed Sector Signals**
    Rotation unclear

    → 50% POSITION ⚠️
    """)
with col3:
    st.error("""
    **❄️ Cold Sectors Dominating**
    Weak leadership

    → AVOID / EXIT ❌
    """)

st.markdown("### ↓")

# Final Actions
st.markdown("### 🎯 Final Action Summary")

action_col1, action_col2, action_col3 = st.columns(3)

with action_col1:
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(0, 212, 138, 0.2) 0%, rgba(0, 212, 138, 0.1) 100%);
                border: 3px solid #00d48a; padding: 25px; border-radius: 15px; height: 100%;">
        <h3 style="color: #00a86b; margin: 0 0 15px 0; text-align: center;">🟢 BULLISH SETUP</h3>
        <p style="margin: 5px 0;"><b>All 4 Steps = Bullish</b></p>
        <hr style="margin: 15px 0;">
        <p style="margin: 5px 0;">✅ Full position size (100%)</p>
        <p style="margin: 5px 0;">✅ Focus on Hot sectors</p>
        <p style="margin: 5px 0;">✅ Set stop below MA20</p>
        <p style="margin: 5px 0;">✅ Enable Auto-Refresh</p>
        <p style="margin: 5px 0;">✅ Hold through month</p>
    </div>
    """, unsafe_allow_html=True)

with action_col2:
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(255, 193, 7, 0.2) 0%, rgba(255, 193, 7, 0.1) 100%);
                border: 3px solid #ffc107; padding: 25px; border-radius: 15px; height: 100%;">
        <h3 style="color: #e9a100; margin: 0 0 15px 0; text-align: center;">🟡 NEUTRAL SETUP</h3>
        <p style="margin: 5px 0;"><b>Mixed signals (2-3 bullish)</b></p>
        <hr style="margin: 15px 0;">
        <p style="margin: 5px 0;">⚠️ Reduced position (25-50%)</p>
        <p style="margin: 5px 0;">⚠️ Quick trades only</p>
        <p style="margin: 5px 0;">⚠️ Tight stop losses</p>
        <p style="margin: 5px 0;">⚠️ Monitor closely</p>
        <p style="margin: 5px 0;">⚠️ Take profits fast</p>
    </div>
    """, unsafe_allow_html=True)

with action_col3:
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(255, 71, 87, 0.2) 0%, rgba(255, 71, 87, 0.1) 100%);
                border: 3px solid #ff4757; padding: 25px; border-radius: 15px; height: 100%;">
        <h3 style="color: #d63031; margin: 0 0 15px 0; text-align: center;">🔴 BEARISH SETUP</h3>
        <p style="margin: 5px 0;"><b>3+ bearish signals</b></p>
        <hr style="margin: 15px 0;">
        <p style="margin: 5px 0;">❌ Exit all positions</p>
        <p style="margin: 5px 0;">❌ Or go to cash</p>
        <p style="margin: 5px 0;">❌ Consider hedging</p>
        <p style="margin: 5px 0;">❌ Wait for reversal</p>
        <p style="margin: 5px 0;">❌ Preserve capital</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Quick Reference Table
st.markdown("### 📋 Quick Reference Table")

st.markdown("""
| Step | Check | Bullish ✅ | Neutral ⚠️ | Bearish ❌ |
|------|-------|-----------|-----------|-----------|
| **1. Seasonality** | Monthly pattern | Green/Positive | Mixed | Red/Negative |
| **2. Breadth** | A/D Ratio | > 1.5 | 0.8-1.5 | < 0.8 |
| **3. Trend** | MA & VIX | Price>MA50, VIX<20 | Choppy, VIX 20-25 | Price<MA50, VIX>25 |
| **4. Sectors** | Rotation Map | Hot expanding | Mixed signals | Cold dominating |
| **→ Action** | Position Size | **100% Full** | **25-50% Reduced** | **0% Cash/Exit** |
""")

# FAQ Section
st.markdown("---")
st.markdown("## ❓ Frequently Asked Questions")

with st.expander("**Q: How often should I check the dashboard?**"):
    st.markdown("""
    **Answer:** Depends on your trading style:

    - **Day Traders**: Every 1-5 minutes (use Auto-Refresh)
    - **Swing Traders**: 2-3 times per day
    - **Investors**: Once per day or weekly

    💡 **Tip**: Enable Auto-Refresh during market hours and set it to match your style.
    """)

with st.expander("**Q: Which tab should I start with?**"):
    st.markdown("""
    **Answer:** Always start with **Seasonality (Tab 1)** to understand the historical context.

    **Recommended Order:**
    1. Seasonality → Understand if timing is favorable
    2. Market Breadth → Check current market health
    3. Historical → Confirm trend direction

    This gives you context → current state → trend confirmation.
    """)

with st.expander("**Q: What if indicators contradict each other?**"):
    st.markdown("""
    **Answer:** Use a weighted approach:

    **Priority Order:**
    1. **Market Breadth (A/D Ratio)** - Most important for current state
    2. **VIX** - Risk gauge, overrides other signals when > 30
    3. **Seasonality** - Context, but can be overridden by breadth
    4. **MA Alignment** - Trend confirmation

    **Rule of Thumb:**
    - 3+ bullish signals = Full position
    - 2 bullish, 2 bearish = Reduced position (50%)
    - 3+ bearish signals = Avoid or exit
    """)

with st.expander("**Q: How do I analyze individual sectors?**"):
    st.markdown("""
    **Answer:** NEW feature in Tab 1 (Seasonality):

    1. Go to **Tab 1: Seasonality**
    2. Select your market (India/USA)
    3. **Use the dropdown** to select a sector (e.g., "🏭 Banking")
    4. Click **"Analyze"** button
    5. View seasonal patterns for that specific sector

    Then check **Tab 2: Market Breadth** to see if that sector is currently Hot/Warm/Cool/Cold.

    **Strategy**: Invest in sectors that are:
    - Entering a seasonally strong period (Tab 1)
    - Currently showing up as Hot or Warm (Tab 2)
    """)

with st.expander("**Q: What does the Sector Rotation Map mean?**"):
    st.markdown("""
    **Answer:** The rotation map in Tab 2 categorizes sectors into 4 zones:

    | Zone | Meaning | Action |
    |------|---------|--------|
    | 🔥 **Hot** | Top 25% performers | Overweight, add positions |
    | 📈 **Warm** | Above average, positive | Maintain, hold positions |
    | 📉 **Cool** | Below average, negative | Reduce, caution |
    | ❄️ **Cold** | Bottom 25% performers | Underweight, avoid |

    **Rotation Strategy:**
    - Move money FROM Cold → Hot sectors
    - Monitor weekly to catch early rotation
    - Hot sectors that turn Cool = Take profits
    """)

# Troubleshooting Section
st.markdown("---")
st.markdown("## 🛠️ Troubleshooting")

trouble_col1, trouble_col2 = st.columns(2)

with trouble_col1:
    st.markdown("""
    ### Common Issues

    **"No data available"**
    - Market may be closed
    - Check market timings (🕒 button)
    - Wait a few minutes and refresh
    - Check internet connection

    **Charts not loading**
    - Clear browser cache (Ctrl+Shift+R)
    - Disable ad blockers temporarily
    - Try different browser (Chrome recommended)

    **Data seems stale**
    - Click manual refresh (🔄 button)
    - Enable Auto-Refresh in sidebar
    - Check "Last refresh" timestamp
    """)

with trouble_col2:
    st.markdown("""
    ### Performance Tips

    **App running slow?**
    - Reduce Auto-Refresh frequency (use 5-10 min)
    - Close unused browser tabs
    - Clear cache periodically
    - Use modern browser (latest Chrome/Edge)

    **Mobile usage**
    - Rotate to landscape for charts
    - Enable full-screen mode
    - Swipe tabs horizontally
    - Use Wi-Fi for better speed

    **Best browser settings**
    - Enable hardware acceleration
    - Allow JavaScript
    - Disable aggressive ad blocking
    """)

# Contact/Support Section
st.markdown("---")
st.markdown("## 📞 Need More Help?")

contact_col1, contact_col2, contact_col3 = st.columns(3)

with contact_col1:
    st.info("""
    ### 📚 Documentation

    - [Quick Start Guide](docs/QUICK_START_GUIDE.md)
    - [Technical Docs](docs/POLISH_AND_OPTIMIZATION.md)
    - Code comments in `/utils`
    """)

with contact_col2:
    st.success("""
    ### 💬 Community

    - Report issues on GitHub
    - Share feedback
    - Request features
    - Contribute improvements
    """)

with contact_col3:
    st.warning("""
    ### ⚡ Quick Actions

    - Press F11 for fullscreen
    - Ctrl+R to refresh
    - Check browser console (F12)
    - Review Streamlit logs
    """)

# Call to Action
st.markdown("---")
st.markdown("""
<div style="background: linear-gradient(135deg, #00d48a 0%, #00a86b 100%);
            padding: 40px; border-radius: 15px; text-align: center;
            box-shadow: 0 8px 30px rgba(0, 212, 138, 0.3);">
    <h2 style="color: white; margin: 0 0 15px 0;">Ready to Start Analyzing? 🚀</h2>
    <p style="color: rgba(255,255,255,0.95); font-size: 1.1rem; margin: 0 0 25px 0;">
        Head over to the Market Pulse dashboard and start uncovering market insights!
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Center the button
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("📊 Go to Market Pulse Dashboard", type="primary", use_container_width=True):
        st.switch_page("pages/01_market_pulse.py")
