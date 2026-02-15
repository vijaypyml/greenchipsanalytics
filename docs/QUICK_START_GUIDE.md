# MarketPulse - Quick Start Guide

Welcome to MarketPulse! This guide will help you get started with the newly polished and optimized features.

## 🚀 Getting Started

### Running the Application

```bash
cd "d:\Vijay GCP\marketpulse"
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

---

## 🎛️ Using Auto-Refresh

### Step 1: Open the Sidebar
Click the `>` arrow in the top-left corner to open the sidebar (if not already open)

### Step 2: Enable Auto-Refresh
1. Look for the **⚙️ Settings** section in the sidebar
2. Check the **🔄** checkbox to enable auto-refresh
3. A dropdown menu will appear

### Step 3: Select Refresh Interval
Choose your preferred refresh interval:
- **1 min** - For active trading (data updates every minute)
- **2 min** - For frequent monitoring
- **5 min** - Recommended for general use (default)
- **10 min** - For casual viewing
- **15 min** - For long-term monitoring

### Step 4: Monitor Status
- Watch the countdown timer showing seconds until next refresh
- Check "Last refresh" timestamp to see when data was last updated

### Manual Refresh
You can always manually refresh by clicking the **🔄** button in the top-right corner

---

## 📊 Navigating the Dashboard

### Global Market Overview
**Location**: Top section (always visible)

Shows:
- Market status indicators (🟢 Open, 🔴 Closed, 🟠 Pre-Market)
- Global markets across 7 tabs:
  - 🇮🇳 India (NIFTY, SENSEX, etc.)
  - 🇺🇸 US (S&P 500, NASDAQ, DOW)
  - 🇪🇺 Europe (DAX, FTSE, CAC)
  - 🌏 Asia-Pacific (Nikkei, Hang Seng, etc.)
  - 🟡 Commodities (Gold, Oil, Silver)
  - 💱 Forex (USD/INR, EUR/USD, etc.)
  - ₿ Crypto (Bitcoin, Ethereum)

### Market Selection
**Location**: Below global overview, before deep analysis

1. Use the dropdown to select your market:
   - 🇮🇳 India (NIFTY 50)
   - 🇺🇸 USA (S&P 500)

2. The info box shows selected index details

### Deep Analysis Tabs

#### 📅 Tab 1: Seasonality (Default)
**Best for**: Finding seasonal patterns and trading edges

Features:
- Monthly performance heatmap (10-year history)
- Best/worst performing months
- Quarterly performance breakdown
- Deep dive options:
  - 📊 Weekly (Week 1-5 analysis)
  - 📅 Daily (Day 1-31 analysis)
  - 📆 Day-of-Week (Mon-Fri patterns)

**How to use**:
1. Adjust the year slider (5-15 years, default 10)
2. Identify best/worst months from the heatmap
3. Click drill-down views for granular analysis
4. Select specific months for weekly/daily patterns

#### 📊 Tab 2: Market Breadth
**Best for**: Understanding market strength

Features:
- Advancing vs Declining stocks
- A/D Ratio with visual indicator
- Market breadth status (Bullish/Bearish)
- Market heatmap by sector
- Top gainers and losers

**How to use**:
1. Check the A/D Ratio metric (>1 = Bullish)
2. Review the breadth status card
3. Explore the heatmap for sector rotation
4. Monitor top movers tables

#### 📈 Tab 3: Historical Analysis
**Best for**: Long-term trend analysis

Features:
- Candlestick chart with moving averages (MA20, MA50)
- A/D Line indicator (TradingView style)
- A/D Ratio indicator
- VIX volatility indicator
- Performance metrics

**How to use**:
1. Adjust year slider (1-10 years, default 5)
2. Analyze price trends and moving averages
3. Check A/D indicators for divergences
4. Monitor VIX for volatility spikes
5. Review performance metrics at bottom

#### 🏭 Tab 4: Sector Analysis
**Best for**: Sector rotation strategies

Features:
- Sector performance overview
- Rotation map (Hot/Warm/Cool/Cold)
- Sector performance comparison chart
- Detailed sector metrics table
- Rotation strategy insights

**How to use**:
1. Check advancing vs declining sectors
2. Identify hot sectors (strong outperformance)
3. Review rotation map for positioning
4. Use strategy insights for allocation decisions

---

## 📱 Mobile Usage

### Accessing on Mobile
1. Open your mobile browser
2. Navigate to your app's URL
3. The interface automatically adapts to mobile

### Mobile-Optimized Features
- **Single column layout**: All cards stack vertically
- **Touch-friendly tabs**: Swipe through tabs horizontally
- **Larger buttons**: Easy to tap (44px minimum)
- **Responsive charts**: Pinch to zoom, swipe to pan
- **Horizontal scroll**: Tables scroll smoothly

### Tips for Mobile
- Use landscape mode for better chart viewing
- Enable full-screen mode in browser
- Bookmark for quick access
- Use auto-refresh to save manual refreshes

---

## 🛡️ Error Handling

### What Happens on Error?
The app gracefully handles errors:
- **Network issues**: Shows "Connection issue" message
- **Timeouts**: Displays "Request timed out" warning
- **Invalid data**: Shows "Invalid data received" message
- **Empty data**: Info message about unavailable data

### What You Should Do
1. **Check your internet connection**
2. **Wait a moment and try manual refresh**
3. **Check market status** (markets might be closed)
4. **Try a different market** if one isn't working

### Data Unavailable?
Common reasons:
- Market is closed (check market timings)
- API rate limits reached (wait a few minutes)
- Temporary network issues (refresh after a moment)
- Data provider maintenance (try later)

---

## ⚡ Performance Tips

### For Best Performance

1. **Enable Auto-Refresh**
   - Prevents manual cache clearing
   - Optimizes data fetching schedule

2. **Choose Appropriate Intervals**
   - Shorter intervals = More API calls = Slower
   - Longer intervals = Fewer calls = Faster

3. **Close Unused Tabs**
   - Only active tab fetches data
   - Switching tabs triggers new data fetch

4. **Clear Cache Periodically**
   - Use manual refresh button
   - Helps if data seems stale

5. **Use Modern Browser**
   - Chrome, Firefox, Edge, Safari
   - Enable hardware acceleration
   - Keep browser updated

### Keyboard Shortcuts
- `Ctrl + R` / `Cmd + R` - Refresh page
- `Ctrl + Shift + R` / `Cmd + Shift + R` - Hard refresh
- `F11` - Full screen mode
- `Esc` - Exit dialogs/modals

---

## 🎨 Customization

### Market Timings
Click the **🕒** button in top-right to:
- View global market timings in IST
- Check market status (Open/Closed)
- See local times for each market

### Changing Default Market
The app defaults to India (NIFTY 50). To change:
1. Use the market selector dropdown
2. Your selection persists for the session

### Adjusting Chart Periods
- **Seasonality**: 5-15 years slider
- **Historical**: 1-10 years slider
- Both default to optimal values

---

## 📊 Understanding Indicators

### A/D (Advance/Decline) Line
**What it shows**: Cumulative difference between advancing and declining stocks

**How to read**:
- Rising A/D Line = Market breadth improving
- Falling A/D Line = Market breadth weakening
- Divergence from price = Potential reversal

### A/D Ratio
**What it shows**: Ratio of advancing to declining stocks

**How to read**:
- Ratio > 2.0 = Strong bullish sentiment
- Ratio > 1.0 = Bullish (more advancing)
- Ratio < 1.0 = Bearish (more declining)
- Ratio < 0.5 = Strong bearish sentiment

### VIX (Volatility Index)
**What it shows**: Expected market volatility

**How to read**:
- VIX < 15 = Low volatility (calm market)
- VIX 15-20 = Moderate volatility
- VIX > 20 = High volatility (fearful market)
- VIX > 30 = Extreme volatility (panic)

### Market Breadth Status
**Categories**:
- 🚀 **Strong Bullish**: A/D Ratio > 2 (100% strength)
- 📈 **Bullish**: A/D Ratio > 1 (75% strength)
- ➡️ **Neutral**: A/D Ratio 0.5-1 (50% strength)
- 📉 **Bearish**: A/D Ratio < 0.5 (25% strength)

---

## 🔍 Troubleshooting

### App Not Loading?
1. Check if Streamlit server is running
2. Verify URL is correct (`http://localhost:8501`)
3. Try different port: `streamlit run app.py --server.port 8502`
4. Clear browser cache

### Data Not Showing?
1. Check internet connection
2. Verify market is open (check timings)
3. Try manual refresh (🔄 button)
4. Check browser console (F12) for errors

### Charts Not Rendering?
1. Enable JavaScript in browser
2. Disable ad blockers temporarily
3. Update browser to latest version
4. Try incognito/private mode

### Auto-Refresh Not Working?
1. Ensure checkbox is enabled in sidebar
2. Check if countdown timer is running
3. Verify interval is selected
4. Try disabling/re-enabling

### Mobile Display Issues?
1. Rotate to landscape mode
2. Clear mobile browser cache
3. Enable desktop site mode temporarily
4. Try different mobile browser

---

## 💡 Pro Tips

### Trading Strategy
1. **Morning**: Check seasonality for today's date
2. **Pre-Market**: Review global markets overview
3. **Market Open**: Monitor market breadth indicators
4. **Intraday**: Watch sector rotation (every 30-60 min)
5. **End of Day**: Review historical charts for trends

### Research Workflow
1. Start with **Seasonality** to identify patterns
2. Check **Market Breadth** for current strength
3. Analyze **Historical** charts for trends
4. Review **Sector Analysis** for rotation opportunities

### Best Practices
- ✅ Enable auto-refresh during market hours
- ✅ Check VIX before major trades
- ✅ Monitor A/D Line for divergences
- ✅ Use sector rotation for allocation
- ✅ Compare across multiple markets
- ❌ Don't ignore market breadth warnings
- ❌ Don't trade against strong VIX signals
- ❌ Don't ignore seasonal patterns

---

## 📞 Getting Help

### Resources
1. **Documentation**: Check `/docs` folder
2. **Code Comments**: Review inline comments
3. **Browser Console**: F12 → Console for errors
4. **Streamlit Logs**: Terminal where app is running

### Common Questions

**Q: Why is data delayed?**
A: Free data sources may have 15-minute delays. Auto-refresh helps minimize staleness.

**Q: Can I add more markets?**
A: Yes! Edit `config/markets.py` to add new markets.

**Q: How do I export data?**
A: Currently not supported. Coming in future versions.

**Q: Is historical data adjusted?**
A: Yes, data is adjusted for splits and dividends.

**Q: Can I customize refresh intervals?**
A: Yes! Edit `utils/auto_refresh.py` to add custom intervals.

---

## 🎯 Next Steps

### Learn More
- Read [POLISH_AND_OPTIMIZATION.md](./POLISH_AND_OPTIMIZATION.md) for technical details
- Explore code in `/utils` for understanding implementations
- Review `/config` for customization options

### Contribute
- Report bugs or issues
- Suggest new features
- Improve documentation

---

**Happy Trading! 📈**

*Last Updated: 2026-02-15*
*Version: 1.0*
