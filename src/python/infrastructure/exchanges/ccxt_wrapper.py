"""
CCXT Wrapper with retry logic and error handling.

Wraps CCXT library with institutional-grade error handling.
"""
import ccxt.async_support as ccxt
import asyncio
from typing import Optional, Dict, Any, List
from decimal import Decimal
import logging
from datetime import datetime

from src.python.infrastructure.exchanges.base_exchange import BaseExchange
from src.python.infrastructure.exchanges.exceptions import (
    ExchangeError,
    RateLimitError,
    AuthenticationError,
    InsufficientBalanceError,
    InvalidOrderError,
    OrderNotFoundError,
    MarketNotFoundError,
    NetworkError,
    ExchangeMaintenanceError
)
from src.python.infrastructure.exchanges.rate_limiter import TokenBucketRateLimiter
from src.python.domain.entities.order import Order, OrderSide, OrderType, OrderStatus
from src.python.domain.value_objects.symbol import TradingPair

logger = logging.getLogger(__name__)


class CCXTWrapper(BaseExchange):
    """
    CCXT wrapper with retry logic and error handling.
    
    Features:
    - Exponential backoff retry
    - Rate limiting
    - Error mapping to domain exceptions
    - Connection management
    """
    
    def __init__(
        self,
        exchange_id: str,
        api_key: str,
        secret_key: str,
        testnet: bool = True,
        rate_limit: float = 10.0,
        max_retries: int = 3
    ):
        """
        Initialize CCXT wrapper.
        
        Args:
            exchange_id: Exchange ID (e.g., 'binance')
            api_key: API key
            secret_key: Secret key
            testnet: Use testnet
            rate_limit: Requests per second
            max_retries: Max retry attempts
        """
        self.exchange_id = exchange_id
        self.api_key = api_key
        self.secret_key = secret_key
        self.testnet = testnet
        self.max_retries = max_retries
        
        # Rate limiter
        self.rate_limiter = TokenBucketRateLimiter(
            rate=rate_limit,
            capacity=rate_limit * 2
        )
        
        # CCXT exchange instance
        self.exchange: Optional[ccxt.Exchange] = None
        
        # Market info cache
        self._markets: Optional[Dict] = None
    
    @property
    def name(self) -> str:
        """Exchange name."""
        return self.exchange_id
    
    async def connect(self) -> None:
        """Initialize CCXT exchange."""
        try:
            # Create exchange instance
            exchange_class = getattr(ccxt, self.exchange_id)
            
            config = {
                'apiKey': self.api_key,
                'secret': self.secret_key,
                'enableRateLimit': False,  # We handle rate limiting
                'options': {
                    'defaultType': 'future',  # For futures trading
                }
            }
            
            # Testnet configuration
            if self.testnet:
                if self.exchange_id == 'binance':
                    config['urls'] = {
                        'api': {
                            'public': 'https://testnet.binancefuture.com',
                            'private': 'https://testnet.binancefuture.com',
                        }
                    }
            
            self.exchange = exchange_class(config)
            
            # Load markets
            await self._load_markets()
            
            logger.info(f"Connected to {self.exchange_id} ({'testnet' if self.testnet else 'live'})")
            
        except Exception as e:
            logger.error(f"Failed to connect to {self.exchange_id}: {e}")
            raise ExchangeError(f"Connection failed: {e}")
    
    async def disconnect(self) -> None:
        """Close exchange connection."""
        if self.exchange:
            await self.exchange.close()
            logger.info(f"Disconnected from {self.exchange_id}")
    
    async def _load_markets(self) -> None:
        """Load and cache market information."""
        try:
            self._markets = await self._retry_request(
                self.exchange.load_markets
            )
        except Exception as e:
            logger.error(f"Failed to load markets: {e}")
            raise
    
    async def _retry_request(self, func, *args, **kwargs) -> Any:
        """
        Execute request with exponential backoff retry.
        
        Args:
            func: Async function to call
            *args: Function arguments
            **kwargs: Function keyword arguments
        
        Returns:
            Function result
        
        Raises:
            ExchangeError: If all retries fail
        """
        last_exception = None
        
        for attempt in range(self.max_retries):
            try:
                # Rate limiting
                await self.rate_limiter.acquire()
                
                # Execute request
                result = await func(*args, **kwargs)
                return result
                
            except ccxt.RateLimitExceeded as e:
                last_exception = e
                wait_time = 2 ** attempt  # Exponential backoff
                logger.warning(f"Rate limit exceeded, waiting {wait_time}s (attempt {attempt + 1}/{self.max_retries})")
                await asyncio.sleep(wait_time)
                
            except ccxt.NetworkError as e:
                last_exception = e
                wait_time = 2 ** attempt
                logger.warning(f"Network error, retrying in {wait_time}s (attempt {attempt + 1}/{self.max_retries})")
                await asyncio.sleep(wait_time)
                
            except ccxt.ExchangeNotAvailable as e:
                last_exception = e
                wait_time = 5 ** attempt
                logger.warning(f"Exchange unavailable, retrying in {wait_time}s (attempt {attempt + 1}/{self.max_retries})")
                await asyncio.sleep(wait_time)
                
            except Exception as e:
                # Don't retry on other errors
                self._handle_exception(e)
        
        # All retries failed
        self._handle_exception(last_exception)
    
    def _handle_exception(self, e: Exception) -> None:
        """
        Map CCXT exceptions to domain exceptions.
        
        Args:
            e: CCXT exception
        
        Raises:
            Appropriate domain exception
        """
        if isinstance(e, ccxt.AuthenticationError):
            raise AuthenticationError(str(e))
        elif isinstance(e, ccxt.InsufficientFunds):
            raise InsufficientBalanceError(str(e))
        elif isinstance(e, ccxt.InvalidOrder):
            raise InvalidOrderError(str(e))
        elif isinstance(e, ccxt.OrderNotFound):
            raise OrderNotFoundError(str(e))
        elif isinstance(e, ccxt.BadSymbol):
            raise MarketNotFoundError(str(e))
        elif isinstance(e, ccxt.RateLimitExceeded):
            raise RateLimitError(str(e))
        elif isinstance(e, ccxt.NetworkError):
            raise NetworkError(str(e))
        elif isinstance(e, ccxt.ExchangeNotAvailable):
            raise ExchangeMaintenanceError(str(e))
        else:
            raise ExchangeError(str(e))
    
    # ========================================================================
    # Market Data
    # ========================================================================
    
    async def get_ticker(self, symbol: TradingPair) -> Dict[str, Any]:
        """Get current ticker."""
        symbol_str = self._format_symbol(symbol)
        ticker = await self._retry_request(
            self.exchange.fetch_ticker,
            symbol_str
        )
        return ticker
    
    async def get_orderbook(
        self,
        symbol: TradingPair,
        limit: int = 100
    ) -> Dict[str, Any]:
        """Get orderbook."""
        symbol_str = self._format_symbol(symbol)
        orderbook = await self._retry_request(
            self.exchange.fetch_order_book,
            symbol_str,
            limit
        )
        return orderbook
    
    async def get_recent_trades(
        self,
        symbol: TradingPair,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get recent trades."""
        symbol_str = self._format_symbol(symbol)
        trades = await self._retry_request(
            self.exchange.fetch_trades,
            symbol_str,
            limit=limit
        )
        return trades
    
    # ========================================================================
    # Account
    # ========================================================================
    
    async def get_balance(self) -> Dict[str, Decimal]:
        """Get account balances."""
        balance = await self._retry_request(
            self.exchange.fetch_balance
        )
        
        # Convert to Decimal
        result = {}
        for asset, amounts in balance.get('total', {}).items():
            if amounts and float(amounts) > 0:
                result[asset] = Decimal(str(amounts))
        
        return result
    
    async def get_positions(self) -> List[Dict[str, Any]]:
        """Get open positions."""
        positions = await self._retry_request(
            self.exchange.fetch_positions
        )
        
        # Filter only open positions
        return [p for p in positions if float(p.get('contracts', 0)) > 0]
    
    # ========================================================================
    # Orders
    # ========================================================================
    
    async def place_order(self, order: Order) -> str:
        """Place an order."""
        symbol_str = self._format_symbol(order.symbol)
        
        # Map order type
        order_type = 'market' if order.order_type == OrderType.MARKET else 'limit'
        side = 'buy' if order.side == OrderSide.BUY else 'sell'
        
        # Prepare params
        params = {}
        if order.order_type == OrderType.STOP_LOSS:
            params['stopPrice'] = float(order.stop_price)
        
        # Place order
        result = await self._retry_request(
            self.exchange.create_order,
            symbol_str,
            order_type,
            side,
            float(order.size),
            float(order.price) if order.price else None,
            params
        )
        
        return result['id']
    
    async def cancel_order(self, order_id: str, symbol: TradingPair) -> bool:
        """Cancel an order."""
        symbol_str = self._format_symbol(symbol)
        
        try:
            await self._retry_request(
                self.exchange.cancel_order,
                order_id,
                symbol_str
            )
            return True
        except OrderNotFoundError:
            return False
    
    async def get_order(self, order_id: str, symbol: TradingPair) -> Dict[str, Any]:
        """Get order details."""
        symbol_str = self._format_symbol(symbol)
        order = await self._retry_request(
            self.exchange.fetch_order,
            order_id,
            symbol_str
        )
        return order
    
    async def get_open_orders(
        self,
        symbol: Optional[TradingPair] = None
    ) -> List[Dict[str, Any]]:
        """Get all open orders."""
        symbol_str = self._format_symbol(symbol) if symbol else None
        orders = await self._retry_request(
            self.exchange.fetch_open_orders,
            symbol_str
        )
        return orders
    
    # ========================================================================
    # Market Info
    # ========================================================================
    
    async def get_market_info(self, symbol: TradingPair) -> Dict[str, Any]:
        """Get market information."""
        symbol_str = self._format_symbol(symbol)
        
        if not self._markets:
            await self._load_markets()
        
        market = self._markets.get(symbol_str)
        if not market:
            raise MarketNotFoundError(f"Market {symbol_str} not found")
        
        return {
            'price_precision': market['precision']['price'],
            'size_precision': market['precision']['amount'],
            'min_order_size': Decimal(str(market['limits']['amount']['min'])),
            'max_order_size': Decimal(str(market['limits']['amount']['max'])),
            'min_notional': Decimal(str(market['limits']['cost']['min'])),
        }
    
    async def has_market(self, symbol: TradingPair) -> bool:
        """Check if exchange supports symbol."""
        symbol_str = self._format_symbol(symbol)
        
        if not self._markets:
            await self._load_markets()
        
        return symbol_str in self._markets
    
    # ========================================================================
    # WebSocket (Not implemented in base CCXT)
    # ========================================================================
    
    async def subscribe_trades(self, symbol: TradingPair, callback: callable) -> None:
        """Subscribe to trade updates."""
        raise NotImplementedError("WebSocket not implemented in base CCXT wrapper")
    
    async def subscribe_orderbook(self, symbol: TradingPair, callback: callable) -> None:
        """Subscribe to orderbook updates."""
        raise NotImplementedError("WebSocket not implemented in base CCXT wrapper")
    
    async def subscribe_user_data(
        self,
        on_order_update: callable,
        on_position_update: Optional[callable] = None
    ) -> None:
        """Subscribe to user data updates."""
        raise NotImplementedError("WebSocket not implemented in base CCXT wrapper")
    
    # ========================================================================
    # Utility
    # ========================================================================
    
    async def health_check(self) -> bool:
        """Check if exchange connection is healthy."""
        try:
            await self._retry_request(self.exchange.fetch_time)
            return True
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False
    
    def _format_symbol(self, symbol: TradingPair) -> str:
        """
        Format symbol for exchange.
        
        Args:
            symbol: Trading pair
        
        Returns:
            Exchange-formatted symbol (e.g., 'BTC/USDT')
        """
        return f"{symbol.base}/{symbol.quote}"
