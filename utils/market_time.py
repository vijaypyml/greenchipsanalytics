import datetime
import pytz
from dataclasses import dataclass
from typing import Dict, List, Optional

# Constants
IST = pytz.timezone('Asia/Kolkata')
UTC = pytz.utc
NY_TZ = pytz.timezone('America/New_York')
LONDON_TZ = pytz.timezone('Europe/London')
TOKYO_TZ = pytz.timezone('Asia/Tokyo')

@dataclass
class MarketSession:
    name: str
    timezone: pytz.timezone
    open_time: datetime.time # Local time
    close_time: datetime.time # Local time
    days: List[int] # 0=Mon, 6=Sun
    has_break: bool = False
    break_start: Optional[datetime.time] = None
    break_end: Optional[datetime.time] = None

class MarketSchedule:
    def __init__(self):
        self.markets = {
            "India (NSE)": MarketSession("India (NSE)", IST, datetime.time(9, 15), datetime.time(15, 30), [0, 1, 2, 3, 4]),
            "USA (NYSE)": MarketSession("USA (NYSE)", NY_TZ, datetime.time(9, 30), datetime.time(16, 0), [0, 1, 2, 3, 4]),
            "Europe (LSE)": MarketSession("Europe (LSE)", LONDON_TZ, datetime.time(8, 0), datetime.time(16, 30), [0, 1, 2, 3, 4]),
            "Japan (Tokyo)": MarketSession("Japan (Tokyo)", TOKYO_TZ, datetime.time(9, 0), datetime.time(15, 0), [0, 1, 2, 3, 4], True, datetime.time(11, 30), datetime.time(12, 30)),
            # Gold (CME) - Simplified to ~23 hours, Sun-Fri. 
            # Note: Handling overnight sessions (cross-day) requires careful logic.
            # CME Globex: Sun 6pm ET to Fri 5pm ET. Daily break 5pm-6pm ET.
            # We treat it as Open if not Sat, and not in daily break.
            "Gold/Commodities": MarketSession("Gold (CME)", NY_TZ, datetime.time(18, 0), datetime.time(17, 0), [0, 1, 2, 3, 4, 6]), 
            "Crypto": MarketSession("Crypto", UTC, datetime.time(0, 0), datetime.time(23, 59, 59), [0, 1, 2, 3, 4, 5, 6])
        }

    def _is_market_open(self, market: MarketSession, local_now: datetime.datetime):
        """Checks if market is open based on local time."""
        current_time = local_now.time()
        weekday = local_now.weekday()

        if weekday not in market.days:
            return False, "Weekend"

        # Crypto is always open
        if market.name == "Crypto":
            return True, "Open"

        # Handle crossing midnight (e.g. Gold starts 18:00 previous day or current day)
        # Simplified CME Logic:
        # If weekday is Sat: Closed.
        # If weekday is Sun: Open if time >= 18:00.
        # If weekday is Fri: Open if time < 17:00.
        # Else (Mon-Thu): Open if time >= 18:00 OR time < 17:00. 
        # (Technically Mon 17:00-18:00 is break)
        if market.name == "Gold (CME)":
            if weekday == 5: # Sat
                return False, "Closed"
            if weekday == 6: # Sun
                return current_time >= market.open_time, "Pre-Open" if current_time < market.open_time else "Open"
            if weekday == 4: # Fri
                return current_time < market.close_time, "Closed" if current_time >= market.close_time else "Open"
            
            # Mon-Thu
            # Break is 17:00 - 18:00
            if current_time >= market.close_time and current_time < market.open_time:
                return False, "Break"
            return True, "Open"

        # Standard Markets (NSE, NYSE, LSE)
        # Check Break
        if market.has_break:
            if market.break_start <= current_time < market.break_end:
                 return False, "Lunch Break"

        if market.open_time <= current_time <= market.close_time:
            return True, "Open"
        
        # Pre-market logic (simple 30 min check)
        # date helper
        dt_open = datetime.datetime.combine(datetime.date.today(), market.open_time)
        dt_current = datetime.datetime.combine(datetime.date.today(), current_time)
        diff = (dt_open - dt_current).total_seconds() / 60
        if 0 < diff <= 60:
            return False, "Pre-Market"

        return False, "Closed"

    def get_market_timings(self):
        """
        Returns status and IST timings for all markets.
        """
        utc_now = datetime.datetime.now(UTC)
        results = []

        for name, market in self.markets.items():
            local_now = utc_now.astimezone(market.timezone)
            is_open, status_text = self._is_market_open(market, local_now)

            # Convert Start/End to IST
            # We take the 'Next' or 'Current' session times. 
            # For simplicity, we show standard Open/Close times in IST for 'Today'
            
            # Create datetime objects for Today in Market TZ
            today = local_now.date() 
            open_dt_local = market.timezone.localize(datetime.datetime.combine(today, market.open_time))
            close_dt_local = market.timezone.localize(datetime.datetime.combine(today, market.close_time))

            # Convert to IST
            open_ist = open_dt_local.astimezone(IST).strftime("%I:%M %p")
            close_ist = close_dt_local.astimezone(IST).strftime("%I:%M %p")

            # Formatting
            color = "green" if is_open else "red"
            if status_text in ["Pre-Market", "Break"]: color = "orange"

            results.append({
                "Market": name,
                "Status": status_text,
                "Color": color,
                "Open (IST)": open_ist,
                "Close (IST)": close_ist,
                "Local Time": local_now.strftime("%I:%M %p")
            })
        
        return results
