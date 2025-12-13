"""
Binance Exchange Adapter.

Specialized adapter for Binance with WebSocket support.
"""
from typing import Optional, Dict, Any, List, Callable
from decimal import Decimal
import logging

from src.python.infrastructure.exchanges.ccxt_wrapper import CCXTWrapper
from src.python.domain.value_objects.symbol import TradingPair
from src.python.infrastructure.config.settings import get_settings

logger = logging.getLogger(__name__)


class BinanceAdapter(CCXTWrapper):
    """
    Binance-specific exchange adapter.
    
    Extends CCXT wrapper with Binance-specific features:
    - WebSocket support
    - Binance-specific order types
    - Futures trading
    """
    
    def __init__(self, testnet: bool = None):
        """
        Initialize Binance adapter.
        
        Args:
            testnet: Use testnet (default: from settings)
        """
        settings = get_settings()
        
        if testnet is None:
            testnet = settings.exchange.binance_testnet
        
        super().__init__(
            exchange_id='binance',
            api_key=settings.exchange.binance_api_key,
            secret_key=settings.exchange.binance_secret_key,
            testnet=testnet,
            rate_limit=settings.exchange.rate_limit_requests_per_minute / 60.0,
            max_retries=3
        )
        
        self.ws_connections: Dict[str, Any] = {}
    
    async def connect(self) -> None:
        """Connect to Binance."""
        await super().connect()
        
        # Set leverage for futures (if needed)
        # await self._set_default_leverage()
    
    async def _set_default_leverage(self, leverage: int = 1) -> None:
        """
        Set default leverage for all symbols.
        
        Args:
            leverage: Leverage multiplier
        """
        try:
            # This is exchange-specific
            if hasattr(self.exchange, 'set_leverage'):
                await self.exchange.set_leverage(leverage)
                logger.info(f"Set default leverage to {leverage}x")
        except Exception as e:
            logger.warning(f"Failed to set leverage: {e}")
    
    # ========================================================================
    # Binance-Specific Features
    # ========================================================================
    
    async def get_funding_rate(self, symbol: TradingPair) -> Dict[str, Any]:
        """
        Get current funding rate (futures only).
        
        Args:
            symbol: Trading pair
        
        Returns:
            Dict with funding rate info
        """
        symbol_str = self._format_symbol(symbol)
        
        funding_rate = await self._retry_request(
            self.exchange.fetch_funding_rate,
            symbol_str
        )
        
        return funding_rate
    
    async def get_mark_price(self, symbol: TradingPair) -> Decimal:
        """
        Get mark price (futures only).
        
        Args:
            symbol: Trading pair
        
        Returns:
            Mark price
        """
        symbol_str = self._format_symbol(symbol)
        
        ticker = await self._retry_request(
            self.exchange.fetch_ticker,
            symbol_str
        )
        
        # Mark price is in 'info' for Binance futures
        mark_price = ticker.get('info', {}).get('markPrice')
        if mark_price:
            return Decimal(str(mark_price))
        
        # Fallback to last price
        return Decimal(str(ticker['last']))
    
    async def get_leverage_brackets(self, symbol: TradingPair) -> List[Dict[str, Any]]:
        """
        Get leverage brackets for symbol.
        
        Args:
            symbol: Trading pair
        
        Returns:
            List of leverage brackets
        """
        symbol_str = self._format_symbol(symbol)
        
        # This requires calling Binance-specific endpoint
        # For now, return default
        return [
            {'bracket': 1, 'initialLeverage': 125, 'notionalCap': 50000},
            {'bracket': 2, 'initialLeverage': 100, 'notionalCap': 250000},
            {'bracket': 3, 'initialLeverage': 50, 'notionalCap': 1000000},
        ]
    
    # ========================================================================
    # WebSocket Support (Placeholder - requires binance-connector-python)
    # ========================================================================
    
    async def subscribe_trades(
        self,
        symbol: TradingPair,
        callback: Callable
    ) -> None:
        """
        Subscribe to trade updates via WebSocket.
        
        Note: Requires binance-connector-python library
        
        Args:
            symbol: Trading pair
            callback: Async function to call with trade data
        """
        # TODO: Implement using binance-connector-python
        # from binance.websocket.spot.websocket_stream import SpotWebsocketStreamClient
        
        logger.warning("WebSocket not yet implemented for Binance")
        raise NotImplementedError("WebSocket support coming soon")
    
    async def subscribe_orderbook(
        self,
        symbol: TradingPair,
        callback: Callable
    ) -> None:
        """Subscribe to orderbook updates via WebSocket."""
        logger.warning("WebSocket not yet implemented for Binance")
        raise NotImplementedError("WebSocket support coming soon")
    
    async def subscribe_user_data(
        self,
        on_order_update: Callable,
        on_position_update: Optional[Callable] = None
    ) -> None:
        """Subscribe to user data updates."""
        logger.warning("WebSocket not yet implemented for Binance")
        raise NotImplementedError("WebSocket support coming soon")
    
    # ========================================================================
    # Utility
    # ========================================================================
    
    def _format_symbol(self, symbol: TradingPair) -> str:
        """
        Format symbol for Binance.
        
        Binance uses 'BTC/USDT' format.
        
        Args:
            symbol: Trading pair
        
        Returns:
            Binance-formatted symbol
        """
        return f"{symbol.base}/{symbol.quote}"


# Global instance
_binance_adapter: Optional[BinanceAdapter] = None


async def get_binance_adapter(testnet: bool = None) -> BinanceAdapter:
    """
    Get global Binance adapter instance.
    
    Args:
        testnet: Use testnet
    
    Returns:
        BinanceAdapter instance
    """
    global _binance_adapter
    
    if _binance_adapter is None:
        _binance_adapter = BinanceAdapter(testnet=testnet)
        await _binance_adapter.connect()
    
    return _binance_adapter


async def close_binance_adapter() -> None:
    """Close global Binance adapter."""
    global _binance_adapter
    
    if _binance_adapter is not None:
        await _binance_adapter.disconnect()
        _binance_adapter = None
