"""
Base Market Data Feed Interface.

Abstract interface for market data feeds.
"""
from abc import ABC, abstractmethod
from typing import Callable, Optional
import logging

from src.python.domain.value_objects.symbol import TradingPair

logger = logging.getLogger(__name__)


class BaseMarketDataFeed(ABC):
    """
    Abstract base class for market data feeds.
    
    All feed implementations must inherit from this class.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Feed name (e.g., 'binance', 'coinbase')."""
        pass
    
    @property
    @abstractmethod
    def is_connected(self) -> bool:
        """Check if feed is connected."""
        pass
    
    @abstractmethod
    async def connect(self) -> None:
        """
        Connect to market data feed.
        
        Should establish WebSocket connections, authenticate, etc.
        """
        pass
    
    @abstractmethod
    async def disconnect(self) -> None:
        """Disconnect from market data feed."""
        pass
    
    @abstractmethod
    async def subscribe_candles(
        self,
        symbol: TradingPair,
        timeframe: str,
        callback: Callable
    ) -> None:
        """
        Subscribe to candle updates.
        
        Args:
            symbol: Trading pair
            timeframe: Timeframe (1m, 5m, 1h, etc.)
            callback: Async function to call with candle data
        """
        pass
    
    @abstractmethod
    async def subscribe_trades(
        self,
        symbol: TradingPair,
        callback: Callable
    ) -> None:
        """
        Subscribe to trade updates.
        
        Args:
            symbol: Trading pair
            callback: Async function to call with trade data
        """
        pass
    
    @abstractmethod
    async def subscribe_orderbook(
        self,
        symbol: TradingPair,
        callback: Callable,
        depth: int = 20
    ) -> None:
        """
        Subscribe to orderbook updates.
        
        Args:
            symbol: Trading pair
            callback: Async function to call with orderbook data
            depth: Orderbook depth
        """
        pass
    
    @abstractmethod
    async def unsubscribe(self, symbol: TradingPair) -> None:
        """
        Unsubscribe from all updates for symbol.
        
        Args:
            symbol: Trading pair
        """
        pass
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.disconnect()
