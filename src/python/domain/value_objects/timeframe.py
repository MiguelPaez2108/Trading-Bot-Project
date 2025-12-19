"""
Timeframe Value Object.

Path: src/python/domain/value_objects/timeframe.py
"""
from enum import Enum
from datetime import timedelta


class Timeframe(str, Enum):
    """
    Supported timeframes for trading.
    
    String enum for easy serialization.
    """
    # Minutes
    ONE_MINUTE = "1m"
    THREE_MINUTES = "3m"
    FIVE_MINUTES = "5m"
    FIFTEEN_MINUTES = "15m"
    THIRTY_MINUTES = "30m"
    
    # Hours
    ONE_HOUR = "1h"
    TWO_HOURS = "2h"
    FOUR_HOURS = "4h"
    SIX_HOURS = "6h"
    EIGHT_HOURS = "8h"
    TWELVE_HOURS = "12h"
    
    # Days
    ONE_DAY = "1d"
    THREE_DAYS = "3d"
    
    # Weeks
    ONE_WEEK = "1w"
    
    def to_timedelta(self) -> timedelta:
        """
        Convert timeframe to timedelta.
        
        Returns:
            timedelta representing the interval
        
        Example:
            >>> Timeframe.ONE_HOUR.to_timedelta()
            timedelta(hours=1)
        """
        mapping = {
            "1m": timedelta(minutes=1),
            "3m": timedelta(minutes=3),
            "5m": timedelta(minutes=5),
            "15m": timedelta(minutes=15),
            "30m": timedelta(minutes=30),
            "1h": timedelta(hours=1),
            "2h": timedelta(hours=2),
            "4h": timedelta(hours=4),
            "6h": timedelta(hours=6),
            "8h": timedelta(hours=8),
            "12h": timedelta(hours=12),
            "1d": timedelta(days=1),
            "3d": timedelta(days=3),
            "1w": timedelta(weeks=1),
        }
        return mapping[self.value]
    
    def to_seconds(self) -> int:
        """
        Convert timeframe to seconds.
        
        Returns:
            Number of seconds in interval
        """
        return int(self.to_timedelta().total_seconds())
    
    def to_minutes(self) -> int:
        """Convert timeframe to minutes."""
        return int(self.to_seconds() / 60)
    
    @classmethod
    def from_string(cls, timeframe: str) -> "Timeframe":
        """
        Create Timeframe from string.
        
        Args:
            timeframe: Timeframe string (e.g., '1h', '5m')
        
        Returns:
            Timeframe enum
        
        Raises:
            ValueError: If timeframe not supported
        
        Example:
            >>> tf = Timeframe.from_string("1h")
            >>> print(tf)
            1h
        """
        timeframe = timeframe.lower()
        
        for tf in cls:
            if tf.value == timeframe:
                return tf
        
        raise ValueError(f"Unsupported timeframe: {timeframe}")
    
    def is_intraday(self) -> bool:
        """Check if timeframe is intraday (< 1 day)."""
        return self.to_seconds() < 86400  # 24 hours
    
    def __str__(self) -> str:
        """String representation."""
        return self.value