"""
Abstract Market Data Feed Interface
Base class for all exchange feed implementations
"""
from abc import ABC, abstractmethod
from enum import Enum
from typing import Callable, List, Optional
from datetime import datetime
import structlog

from src.python.domain.value_objects import Symbol

logger = structlog.get_logger(__name__)


class FeedStatus(Enum):
    """Feed connection status"""
    DISCONNECTED = "DISCONNECTED"
    CONNECTING = "CONNECTING"
    CONNECTED = "CONNECTED"
    RECONNECTING = "RECONNECTING"
    ERROR = "ERROR"


class MarketDataFeed(ABC):
    """
    Abstract base class for market data feeds.
    Implementations should handle WebSocket connections to exchanges.
    """
    
    def __init__(self, exchange_name: str):
        """
        Initialize feed.
        
        Args:
            exchange_name: Name of the exchange (e.g., "BINANCE")
        """
        self.exchange_name = exchange_name
        self.status = FeedStatus.DISCONNECTED
        self.subscribed_symbols: List[Symbol] = []
        self.last_heartbeat: Optional[datetime] = None
        
        # Callbacks
        self._on_candle_callback: Optional[Callable] = None
        self._on_trade_callback: Optional[Callable] = None
        self._on_orderbook_callback: Optional[Callable] = None
        self._on_error_callback: Optional[Callable] = None
    
    @abstractmethod
    async def connect(self) -> bool:
        """
        Establish connection to exchange.
        
        Returns:
            True if connected successfully
        """
        pass
    
    @abstractmethod
    async def disconnect(self) -> None:
        """Close connection to exchange"""
        pass
    
    @abstractmethod
    async def subscribe(self, symbols: List[Symbol]) -> None:
        """
        Subscribe to market data for symbols.
        
        Args:
            symbols: List of symbols to subscribe to
        """
        pass
    
    @abstractmethod
    async def unsubscribe(self, symbols: List[Symbol]) -> None:
        """
        Unsubscribe from market data for symbols.
        
        Args:
            symbols: List of symbols to unsubscribe from
        """
        pass
    
    def get_status(self) -> FeedStatus:
        """Get current connection status"""
        return self.status
    
    def is_connected(self) -> bool:
        """Check if feed is connected"""
        return self.status == FeedStatus.CONNECTED
    
    def set_on_candle(self, callback: Callable) -> None:
        """Set callback for candle updates"""
        self._on_candle_callback = callback
    
    def set_on_trade(self, callback: Callable) -> None:
        """Set callback for trade updates"""
        self._on_trade_callback = callback
    
    def set_on_orderbook(self, callback: Callable) -> None:
        """Set callback for orderbook updates"""
        self._on_orderbook_callback = callback
    
    def set_on_error(self, callback: Callable) -> None:
        """Set callback for errors"""
        self._on_error_callback = callback
    
    async def _emit_candle(self, candle_data: dict) -> None:
        """Emit candle event"""
        if self._on_candle_callback:
            await self._on_candle_callback(candle_data)
    
    async def _emit_trade(self, trade_data: dict) -> None:
        """Emit trade event"""
        if self._on_trade_callback:
            await self._on_trade_callback(trade_data)
    
    async def _emit_orderbook(self, orderbook_data: dict) -> None:
        """Emit orderbook event"""
        if self._on_orderbook_callback:
            await self._on_orderbook_callback(orderbook_data)
    
    async def _emit_error(self, error: Exception) -> None:
        """Emit error event"""
        logger.error("feed_error", exchange=self.exchange_name, error=str(error))
        if self._on_error_callback:
            await self._on_error_callback(error)
    
    def update_heartbeat(self) -> None:
        """Update last heartbeat timestamp"""
        self.last_heartbeat = datetime.utcnow()
    
    def is_heartbeat_alive(self, timeout_seconds: int = 60) -> bool:
        """
        Check if heartbeat is alive.
        
        Args:
            timeout_seconds: Timeout in seconds
        
        Returns:
            True if heartbeat is recent
        """
        if not self.last_heartbeat:
            return False
        
        elapsed = (datetime.utcnow() - self.last_heartbeat).total_seconds()
        return elapsed < timeout_seconds
