"""
Candle Entity - OHLCV data representation.

Path: src/python/domain/entities/candle.py
"""
from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime
from typing import Optional

from src.python.domain.value_objects.symbol import TradingPair


@dataclass
class Candle:
    """
    OHLCV Candle entity.
    
    Represents a single candlestick with OHLCV data.
    """
    # Time and symbol
    time: datetime
    symbol: TradingPair
    timeframe: str
    
    # OHLC prices
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    
    # Volume
    volume: Decimal
    quote_volume: Optional[Decimal] = None
    trades_count: Optional[int] = None
    
    def __post_init__(self):
        """Validate OHLC relationships."""
        # Ensure Decimal types only for non-Decimal inputs
        if not isinstance(self.open, Decimal):
            object.__setattr__(self, 'open', Decimal(str(self.open)))
        if not isinstance(self.high, Decimal):
            object.__setattr__(self, 'high', Decimal(str(self.high)))
        if not isinstance(self.low, Decimal):
            object.__setattr__(self, 'low', Decimal(str(self.low)))
        if not isinstance(self.close, Decimal):
            object.__setattr__(self, 'close', Decimal(str(self.close)))
        if not isinstance(self.volume, Decimal):
            object.__setattr__(self, 'volume', Decimal(str(self.volume)))
        
        # Validate OHLC relationships
        if self.high < self.low:
            raise ValueError(f"High ({self.high}) cannot be less than low ({self.low})")
        if self.high < self.open:
            raise ValueError(f"High ({self.high}) cannot be less than open ({self.open})")
        if self.high < self.close:
            raise ValueError(f"High ({self.high}) cannot be less than close ({self.close})")
        if self.low > self.open:
            raise ValueError(f"Low ({self.low}) cannot be greater than open ({self.open})")
        if self.low > self.close:
            raise ValueError(f"Low ({self.low}) cannot be greater than close ({self.close})")
    
    def is_bullish(self) -> bool:
        """Check if candle is bullish (close > open)."""
        return self.close > self.open
    
    def is_bearish(self) -> bool:
        """Check if candle is bearish (close < open)."""
        return self.close < self.open
    
    def is_doji(self, threshold: Decimal = Decimal('0.001')) -> bool:
        """
        Check if candle is doji (open ≈ close).
        
        Args:
            threshold: Max % difference for doji (default 0.1%)
        """
        body_pct = abs(self.close - self.open) / self.open
        return body_pct < threshold
    
    def body_size(self) -> Decimal:
        """Get candle body size (abs diff between open and close)."""
        return abs(self.close - self.open)
    
    def wick_upper(self) -> Decimal:
        """Get upper wick size."""
        return self.high - max(self.open, self.close)
    
    def wick_lower(self) -> Decimal:
        """Get lower wick size."""
        return min(self.open, self.close) - self.low
    
    def range(self) -> Decimal:
        """Get total candle range (high - low)."""
        return self.high - self.low
    
    def midpoint(self) -> Decimal:
        """Get midpoint of candle."""
        return (self.high + self.low) / Decimal('2')
    
    def typical_price(self) -> Decimal:
        """Get typical price (high + low + close) / 3."""
        return (self.high + self.low + self.close) / Decimal('3')
    
    def __str__(self) -> str:
        """String representation."""
        return (
            f"Candle({self.symbol} {self.timeframe} @ {self.time.isoformat()}: "
            f"O={self.open} H={self.high} L={self.low} C={self.close} V={self.volume})"
        )
    
    def __repr__(self) -> str:
        """Detailed representation."""
        return self.__str__()