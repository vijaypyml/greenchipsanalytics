# MarketPulse 📈

**MarketPulse** is a real-time financial market dashboard built with Streamlit that provides comprehensive visualization and tracking of global financial markets including Indian indices, US markets, commodities, currencies, and cryptocurrencies.

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8%2B-brightgreen)
![License](https://img.shields.io/badge/license-MIT-green)

## ✨ Features

### **Module 1: Global Market Pulse (Command Center)**

- **📊 Comprehensive Market Coverage**: Track 32 markets across 7 asset classes
  - 🇮🇳 **India**: NIFTY 50, SENSEX, BANK NIFTY, INDIA VIX
  - 🇺🇸 **United States**: S&P 500, NASDAQ 100, DOW JONES, VIX
  - 🇪🇺 **Europe**: FTSE 100, DAX, CAC 40, EURO STOXX 50
  - 🌏 **Asia-Pacific**: Nikkei 225, Hang Seng, Shanghai, KOSPI
  - 🟡 **Commodities**: Gold, Silver, Crude WTI, Brent, Natural Gas, Copper
  - 💱 **Forex**: DXY, USD/INR, EUR/USD, GBP/USD, USD/JPY
  - ₿ **Crypto**: BTC, ETH, BNB, SOL

- **🎯 Risk-On/Risk-Off Meter**: Proprietary market regime indicator
  - Synthesizes signals from equities, VIX, crypto, gold, and DXY
  - Real-time regime classification (Risk-On, Neutral, Risk-Off)
  - Interactive gauge with component breakdown
  - Actionable strategy recommendations

- **🔼 Smart Sentiment Signals**: AI-powered technical analysis
  - Multi-factor sentiment scoring (RSI + MACD + Moving Averages)
  - Visual sentiment arrows (🔼 Bullish, 🔽 Bearish, ➡️ Neutral)
  - RSI and volatility metrics on each card
  - 7-day price sparklines

- **📈 NIFTY 50 Market Breadth**: Real-time market health indicators
  - Advance/Decline statistics
  - A/D Ratio with interpretation
  - Average market change
  - Breadth status indicator

- **🔥 NIFTY 50 Heatmap**: Interactive treemap visualization
  - Sector-wise performance
  - Market cap weighted
  - Color-coded by price change

- **🚀 Top Movers**: Real-time tracking of top gainers and losers

- **⏰ Global Market Timings**: Timezone-aware scheduling
  - Shows current status (Open/Closed/Pre-Market/Break)
  - Displays market hours in IST for all global markets
  - Covers India, US, Europe, Japan, Commodities, and Crypto

- **🎨 Professional UI**: Modern, responsive design
  - Dark and Light mode toggle
  - Custom color themes
  - Smooth animations and transitions
  - Mobile-friendly layout

- **🔄 Smart Caching**: Optimized performance
  - 60-second cache for market data
  - Efficient API usage
  - Fast page loads

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository** (or download the ZIP)
   ```bash
   git clone <repository-url>
   cd marketpulse
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - If not, navigate to the URL shown in the terminal

## 📁 Project Structure

```
marketpulse/
├── app.py                      # Main application entry point
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── .gitignore                  # Git ignore rules
│
├── pages/                      # Streamlit pages
│   └── 01_market_pulse.py     # Main dashboard page
│
├── components/                 # Reusable UI components
│   ├── market_card.py         # Market card with sparkline
│   └── heatmap.py             # Treemap heatmap component
│
├── data/                       # Data fetching modules
│   └── fetchers/
│       └── market_data.py     # yfinance data fetchers
│
├── utils/                      # Utility functions
│   ├── formatters.py          # Number/currency formatters
│   ├── market_time.py         # Market schedule logic
│   ├── theme.py               # Theme management
│   └── logger.py              # Logging configuration
│
├── config/                     # Configuration files
│   ├── constants.py           # Market symbols, colors, themes
│   └── settings.py            # App settings
│
├── assets/                     # Static assets
│   └── style.css              # Custom CSS styles
│
└── logs/                       # Application logs (auto-created)
```

## 🔧 Configuration

### Adding New Markets

Edit `config/constants.py` to add new market symbols:

```python
INDICES = {
    "YOUR_CATEGORY": {
        "Market Name": "YAHOO_SYMBOL",
        # Example:
        "FTSE 100": "^FTSE"
    }
}
```

### Customizing Themes

Modify theme colors in `config/constants.py`:

```python
THEMES = {
    "dark": {
        "background": "#0e1117",
        "card_bg": "#1e1e2e",
        # ... more colors
    }
}
```

### Cache Settings

Adjust cache TTL (time-to-live) in `data/fetchers/market_data.py`:

```python
@st.cache_data(ttl=60)  # Cache for 60 seconds
def fetch_market_data(symbol: str):
    # ...
```

## 📊 Data Sources

- **Market Data**: [Yahoo Finance](https://finance.yahoo.com/) via `yfinance` library
- **Real-time Updates**: Data refreshes every 60 seconds (configurable)
- **Historical Data**: 5-day history for sparklines

## 🛠️ Technology Stack

| Technology | Purpose |
|------------|---------|
| **Streamlit** | Web framework and UI |
| **yfinance** | Market data API |
| **Plotly** | Interactive charts and visualizations |
| **Pandas** | Data manipulation |
| **pytz** | Timezone handling |

## 🐛 Troubleshooting

### Common Issues

**1. Data Not Loading**
- Check your internet connection
- Verify Yahoo Finance is accessible
- Check logs in `logs/` directory

**2. Import Errors**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Verify you're using Python 3.8+

**3. Slow Performance**
- Increase cache TTL for less frequent updates
- Reduce the number of markets being tracked

**4. Theme Not Working**
- Clear browser cache
- Check `assets/style.css` exists
- Verify theme configuration in `config/constants.py`

## 📝 Logging

Application logs are stored in `logs/` directory:
- Format: `marketpulse_YYYYMMDD.log`
- Log levels: DEBUG, INFO, WARNING, ERROR
- Console shows WARNING and above
- File logs show DEBUG and above

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2024 GreenGhips

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 🙏 Acknowledgments

- Yahoo Finance for providing free market data API
- Streamlit team for the amazing framework
- All contributors and users of this project

## 📧 Contact & Support

- **Author**: GreenGhips
- **Version**: v1.1.0
- **Issues**: Report bugs via GitHub Issues

---

**Made with ❤️ for market enthusiasts**
