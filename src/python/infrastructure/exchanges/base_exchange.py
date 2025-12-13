"""
Base Exchange Interface.

Abstract interface that all exchange adapters must implement.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any
from decimal import Decimal
from datetime import datetime

from src.python.domain.entities.order import Order, OrderSide, OrderType, OrderStatus
from src.python.domain.value_objects.symbol import TradingPair


class BaseExchange(ABC):
    """
    Abstract base class for exchange adapters.
    
    All exchange implementations must inherit from this class
    and implement all abstract methods.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Exchange name (e.g., 'binance', 'hyperliquid')."""
        pass
    
    @abstractmethod
    async def connect(self) -> None:
        """
        Initialize connection to exchange.
        
        Should establish WebSocket connections, authenticate, etc.
        """
        pass
    
    @abstractmethod
    async def disconnect(self) -> None:
        """Close all connections to exchange."""
        pass
    
    # ========================================================================
    # Market Data
    # ========================================================================
    
    @abstractmethod
    async def get_ticker(self, symbol: TradingPair) -> Dict[str, Any]:
        """
        Get current ticker for symbol.
        
        Args:
            symbol: Trading pair
        
        Returns:
            Dict with ticker data (last, bid, ask, volume, etc.)
        """
        pass
    
    @abstractmethod
    async def get_orderbook(
        self,
        symbol: TradingPair,
        limit: int = 100
    ) -> Dict[str, Any]:
        """
        Get orderbook for symbol.
        
        Args:
            symbol: Trading pair
            limit: Depth limit
        
        Returns:
            Dict with bids and asks
        """
        pass
    
    @abstractmethod
    async def get_recent_trades(
        self,
        symbol: TradingPair,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get recent trades for symbol.
        
        Args:
            symbol: Trading pair
            limit: Number of trades
        
        Returns:
            List of trade dicts
        """
        pass
    
    # ========================================================================
    # Account
    # ========================================================================
    
    @abstractmethod
    async def get_balance(self) -> Dict[str, Decimal]:
        """
        Get account balances.
        
        Returns:
            Dict of {asset: balance}
        """
        pass
    
    @abstractmethod
    async def get_positions(self) -> List[Dict[str, Any]]:
        """
        Get open positions.
        
        Returns:
            List of position dicts
        """
        pass
    
    # ========================================================================
    # Orders
    # ========================================================================
    
    @abstractmethod
    async def place_order(self, order: Order) -> str:
        """
        Place an order.
        
        Args:
            order: Order entity
        
        Returns:
            Exchange order ID
        
        Raises:
            ExchangeError: If order placement fails
        """
        pass
    
    @abstractmethod
    async def cancel_order(self, order_id: str, symbol: TradingPair) -> bool:
        """
        Cancel an order.
        
        Args:
            order_id: Exchange order ID
            symbol: Trading pair
        
        Returns:
            True if cancelled successfully
        """
        pass
    
    @abstractmethod
    async def get_order(self, order_id: str, symbol: TradingPair) -> Dict[str, Any]:
        """
        Get order details.
        
        Args:
            order_id: Exchange order ID
            symbol: Trading pair
        
        Returns:
            Order details dict
        """
        pass
    
    @abstractmethod
    async def get_open_orders(
        self,
        symbol: Optional[TradingPair] = None
    ) -> List[Dict[str, Any]]:
        """
        Get all open orders.
        
        Args:
            symbol: Optional symbol filter
        
        Returns:
            List of open orders
        """
        pass
    
    # ========================================================================
    # Market Info
    # ========================================================================
    
    @abstractmethod
    async def get_market_info(self, symbol: TradingPair) -> Dict[str, Any]:
        """
        Get market information (precision, limits, etc.).
        
        Args:
            symbol: Trading pair
        
        Returns:
            Market info dict with:
                - price_precision: int
                - size_precision: int
                - min_order_size: Decimal
                - max_order_size: Decimal
                - min_notional: Decimal
        """
        pass
    
    @abstractmethod
    async def has_market(self, symbol: TradingPair) -> bool:
        """
        Check if exchange supports symbol.
        
        Args:
            symbol: Trading pair
        
        Returns:
            True if supported
        """
        pass
    
    # ========================================================================
    # WebSocket
    # ========================================================================
    
    @abstractmethod
    async def subscribe_trades(
        self,
        symbol: TradingPair,
        callback: callable
    ) -> None:
        """
        Subscribe to trade updates via WebSocket.
        
        Args:
            symbol: Trading pair
            callback: Async function to call with trade data
        """
        pass
    
    @abstractmethod
    async def subscribe_orderbook(
        self,
        symbol: TradingPair,
        callback: callable
    ) -> None:
        """
        Subscribe to orderbook updates via WebSocket.
        
        Args:
            symbol: Trading pair
            callback: Async function to call with orderbook data
        """
        pass
    
    @abstractmethod
    async def subscribe_user_data(
        self,
        on_order_update: callable,
        on_position_update: Optional[callable] = None
    ) -> None:
        """
        Subscribe to user data updates (orders, positions).
        
        Args:
            on_order_update: Callback for order updates
            on_position_update: Optional callback for position updates
        """
        pass
    
    # ========================================================================
    # Utility
    # ========================================================================
    
    @abstractmethod
    async def health_check(self) -> bool:
        """
        Check if exchange connection is healthy.
        
        Returns:
            True if healthy
        """
        pass
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.disconnect()
