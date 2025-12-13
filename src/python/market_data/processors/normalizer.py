"""
Market Data Normalizer.

Normalizes market data from different exchanges to common format.
"""
from typing import Dict, Any
from decimal import Decimal
from datetime import datetime
import logging

from src.python.domain.entities.candle import Candle
from src.python.domain.value_objects.symbol import TradingPair

logger = logging.getLogger(__name__)


class MarketDataNormalizer:
    """
    Normalizes market data from different exchanges.
    
    Converts exchange-specific formats to domain entities.
    """
    
    def normalize_candle(
        self,
        raw_data: Dict[str, Any],
        symbol: TradingPair,
        timeframe: str,
        source: str = "unknown"
    ) -> Candle:
        """
        Normalize candle data.
        
        Args:
            raw_data: Raw candle data from exchange
            symbol: Trading pair
            timeframe: Timeframe
            source: Data source (exchange name)
        
        Returns:
            Normalized Candle entity
        """
        # Different exchanges have different formats
        if source == "binance":
            return self._normalize_binance_candle(raw_data, symbol, timeframe)
        elif source == "ccxt":
            return self._normalize_ccxt_candle(raw_data, symbol, timeframe)
        else:
            # Generic format
            return self._normalize_generic_candle(raw_data, symbol, timeframe)
    
    def _normalize_binance_candle(
        self,
        data: Dict[str, Any],
        symbol: TradingPair,
        timeframe: str
    ) -> Candle:
        """
        Normalize Binance candle format.
        
        Binance format:
        {
            't': timestamp,
            'o': open,
            'h': high,
            'l': low,
            'c': close,
            'v': volume,
            'q': quote_volume,
            'n': trades_count
        }
        """
        return Candle(
            time=datetime.fromtimestamp(data['t'] / 1000),
            symbol=symbol,
            timeframe=timeframe,
            open=Decimal(str(data['o'])),
            high=Decimal(str(data['h'])),
            low=Decimal(str(data['l'])),
            close=Decimal(str(data['c'])),
            volume=Decimal(str(data['v'])),
            quote_volume=Decimal(str(data.get('q', 0))),
            trades_count=data.get('n', 0)
        )
    
    def _normalize_ccxt_candle(
        self,
        data: list,
        symbol: TradingPair,
        timeframe: str
    ) -> Candle:
        """
        Normalize CCXT candle format.
        
        CCXT format: [timestamp, open, high, low, close, volume]
        """
        return Candle(
            time=datetime.fromtimestamp(data[0] / 1000),
            symbol=symbol,
            timeframe=timeframe,
            open=Decimal(str(data[1])),
            high=Decimal(str(data[2])),
            low=Decimal(str(data[3])),
            close=Decimal(str(data[4])),
            volume=Decimal(str(data[5])),
            quote_volume=None,
            trades_count=None
        )
    
    def _normalize_generic_candle(
        self,
        data: Dict[str, Any],
        symbol: TradingPair,
        timeframe: str
    ) -> Candle:
        """Normalize generic candle format."""
        return Candle(
            time=self._parse_timestamp(data.get('time', data.get('timestamp'))),
            symbol=symbol,
            timeframe=timeframe,
            open=Decimal(str(data['open'])),
            high=Decimal(str(data['high'])),
            low=Decimal(str(data['low'])),
            close=Decimal(str(data['close'])),
            volume=Decimal(str(data['volume'])),
            quote_volume=Decimal(str(data.get('quote_volume', 0))) if data.get('quote_volume') else None,
            trades_count=data.get('trades_count')
        )
    
    def _parse_timestamp(self, ts: Any) -> datetime:
        """Parse timestamp to datetime."""
        if isinstance(ts, datetime):
            return ts
        elif isinstance(ts, (int, float)):
            # Assume milliseconds if > 1e10
            if ts > 1e10:
                return datetime.fromtimestamp(ts / 1000)
            return datetime.fromtimestamp(ts)
        elif isinstance(ts, str):
            return datetime.fromisoformat(ts)
        else:
            raise ValueError(f"Cannot parse timestamp: {ts}")
