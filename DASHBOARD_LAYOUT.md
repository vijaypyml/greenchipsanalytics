# MarketPulse Dashboard Layout Documentation

## 📐 **New Layout Structure**

### **Overview**
The dashboard uses a **2-column layout** for the main command center, with detailed analysis sections below.

---

## 🎨 **Layout Breakdown**

### **Top Section: 2-Column Design**

```
+------------------------+--------------------------------------------+
|                        |                                            |
|  📊 MARKET             |  📈 MARKET OVERVIEW                        |
|  COMMAND CENTER        |  (Tabs for each asset class)              |
|                        |                                            |
|  • Risk-On/Off Meter   |  Tabs:                                     |
|  • Gauge Chart         |  🇮🇳 India | 🇺🇸 US | 🇪🇺 Europe |      |
|  • Score: -100 to +100 |  🌏 Asia-Pac | 🟡 Commod | 💱 Forex |    |
|  • Regime Status       |  ₿ Crypto                                  |
|  • Component Breakdown |                                            |
|                        |  Each tab shows:                           |
|                        |  - Market cards with prices                |
|  (Narrow column:       |  - Sentiment arrows                        |
|   1 part width)        |  - RSI & Volatility                        |
|                        |  - 7-day sparklines                        |
|                        |                                            |
|                        |  (Wide column: 2.5 parts width)            |
+------------------------+--------------------------------------------+
```

**Column Ratio**: 1 : 2.5 (Left narrower, Right wider)

---

### **Bottom Sections: Full Width**

```
+---------------------------------------------------------------+
| 📈 NIFTY 50 MARKET BREADTH                                    |
| • Advancing/Declining stocks                                  |
| • A/D Ratio                                                   |
| • Average Change                                              |
| • Breadth Status                                              |
+---------------------------------------------------------------+

+---------------------------------------------------------------+
| 🔥 MARKET HEATMAP (NIFTY 50)                                  |
| • Interactive treemap                                         |
| • Sector-wise performance                                     |
| • Color-coded by change                                       |
+---------------------------------------------------------------+

+---------------------------------------------------------------+
| 🚀 TOP MOVERS (NIFTY 50)                                      |
| • Top 5 Gainers                                               |
| • Top 5 Losers                                                |
+---------------------------------------------------------------+
```

---

## 🎯 **Left Column: Market Command Center**

### **Purpose**
Single-source-of-truth for overall market sentiment.

### **Components**
1. **Risk-On/Risk-Off Gauge**
   - Visual meter showing market regime
   - Score from -100 (Strong Risk-Off) to +100 (Strong Risk-On)

2. **Regime Classification**
   - 🟢 Risk-On (> +30)
   - 🟡 Neutral (-30 to +30)
   - 🔴 Risk-Off (< -30)

3. **Interactive Elements**
   - "📊 View Component Breakdown" expander
   - "ℹ️ How to Interpret" guide

### **Logic**
```
Score Calculation:
├─ Equities (40%): SPX, NSEI, FTSE, Nikkei
├─ VIX (20%): Inverted (VIX up = Risk-Off)
├─ Crypto (15%): BTC, ETH
├─ Gold (10%): Slightly inverted (safe haven)
└─ DXY (15%): Inverted (Dollar up = Risk-Off)

Final Score = Sum of all contributions × 3
```

---

## 📊 **Right Column: Market Overview**

### **Tab Structure**

| Tab | Markets | Count |
|-----|---------|-------|
| 🇮🇳 **India** | NIFTY 50, SENSEX, BANK NIFTY, INDIA VIX | 4 |
| 🇺🇸 **US** | S&P 500, NASDAQ 100, DOW JONES, VIX | 4 |
| 🇪🇺 **Europe** | FTSE 100, DAX, CAC 40, EURO STOXX 50 | 4 |
| 🌏 **Asia-Pac** | Nikkei 225, Hang Seng, Shanghai, KOSPI | 4 |
| 🟡 **Commod** | Gold, Silver, WTI, Brent, Nat Gas, Copper | 6 |
| 💱 **Forex** | DXY, USD/INR, EUR/USD, GBP/USD, USD/JPY | 5 |
| ₿ **Crypto** | BTC, ETH, BNB, SOL | 4 |

**Total Markets**: 31 markets across 7 asset classes

### **Each Market Card Shows**
- **Name**: Market identifier
- **Price**: Current price with smart currency (₹/$)
- **Change**: Percentage and absolute change
- **Sentiment Arrow**: 🔼 Bullish | ➡️ Neutral | 🔽 Bearish
- **RSI**: 14-period RSI (color-coded)
- **Volatility**: Annualized volatility %
- **Sparkline**: 7-day price mini-chart

---

## 🎨 **Design Benefits**

### **1. Space Efficiency**
- Risk meter always visible on left
- Market overview organized in tabs (less scrolling)
- All critical info above the fold

### **2. Better Information Architecture**
- Command center (regime) separated from market details
- Easy to scan one market at a time via tabs
- Related markets grouped together

### **3. User Experience**
- **Glance**: Check risk meter for overall sentiment
- **Detail**: Click tab for specific region/asset class
- **Analysis**: Scroll down for NIFTY 50 deep dive

---

## 📱 **Responsive Behavior**

### **Desktop (> 1200px)**
- 2-column layout works perfectly
- All tabs visible
- Gauge chart full size

### **Tablet (768px - 1200px)**
- Columns stack vertically
- Risk meter on top
- Market overview below with tabs

### **Mobile (< 768px)**
- Single column
- Vertical scroll
- Tabs still functional

---

## 🔧 **Technical Implementation**

### **Streamlit Code Structure**

```python
# Main 2-column layout
main_col1, main_col2 = st.columns([1, 2.5])

# LEFT COLUMN
with main_col1:
    render_risk_meter(risk_markets)

# RIGHT COLUMN
with main_col2:
    # 7 tabs for asset classes
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([...])

    with tab1:
        render_compact_group("India", INDICES["INDIA"])

    # ... repeat for other tabs
```

---

## 💡 **Key Differences from Old Layout**

### **Before**
```
[Risk Meter] (Full width, separate section)
[India] [US] [Europe] [Asia-Pac] (4 columns)
[Commodities] [Forex] [Crypto] (3 columns)
[Market Breadth]
[Heatmap]
[Top Movers]
```

### **After**
```
[Risk Meter (Left) | Market Tabs (Right)] (2 columns)
[Market Breadth]
[Heatmap]
[Top Movers]
```

**Benefits**:
- ✅ Less vertical scrolling
- ✅ Risk meter always visible
- ✅ Organized by asset class (tabs)
- ✅ More screen real estate for gauge
- ✅ Cleaner, more professional look

---

## 🎯 **Usage Guide**

### **For Quick Market Check**
1. Open dashboard
2. Check **Risk-On/Off Meter** (left side)
3. If interested in specific region → Click relevant tab (right side)

### **For Deep Analysis**
1. Check overall regime (Risk meter)
2. Review your focus markets in tabs
3. Scroll down for NIFTY 50 breadth
4. Check heatmap for sector rotation
5. View top movers for opportunities

---

## 📝 **Future Enhancements**

Potential improvements:
1. **Customizable tabs**: Let users choose which asset classes to show
2. **Tab order**: Drag-and-drop to reorder tabs
3. **Favorites**: Pin favorite markets to a "Favorites" tab
4. **Comparison mode**: Side-by-side comparison of 2 markets
5. **Alerts**: Highlight tabs when major moves happen

---

**Last Updated**: Module 1 Integration
**Version**: 2.0.0
**Layout**: 2-Column with Tabs
