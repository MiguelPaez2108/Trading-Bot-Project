"""
Binance WebSocket Feed Implementation
Real-time market data from Binance using WebSocket
"""
import asyncio
import json
from typing import List, Optional
from datetime import datetime
import websockets
import structlog

from src.python.domain.value_objects import Symbol
from src.python.market_data.feeds.base_feed import MarketDataFeed, FeedStatus
from src.python.market_data.normalizer import DataNormalizer

logger = structlog.get_logger(__name__)


class BinanceFeed(MarketDataFeed):
    """
    Binance WebSocket feed implementation.
    Connects to Binance WebSocket streams for real-time market data.
    """
    
    # Binance WebSocket URLs
    TESTNET_WS_URL = "wss://testnet.binance.vision/ws"
    MAINNET_WS_URL = "wss://stream.binance.com:9443/ws"
    
    def __init__(self, testnet: bool = True):
        """
        Initialize Binance feed.
        
        Args:
            testnet: Use testnet if True, mainnet if False
        """
        super().__init__("BINANCE")
        self.testnet = testnet
        self.ws_url = self.TESTNET_WS_URL if testnet else self.MAINNET_WS_URL
        self.websocket: Optional[websockets.WebSocketClientProtocol] = None
        self.listen_task: Optional[asyncio.Task] = None
        self.reconnect_delay = 1  # Start with 1 second
        self.max_reconnect_delay = 60  # Max 60 seconds
        self.normalizer = DataNormalizer()
    
    async def connect(self) -> bool:
        """
        Establish WebSocket connection to Binance.
        
        Returns:
            True if connected successfully
        """
        try:
            self.status = FeedStatus.CONNECTING
            logger.info("connecting_to_binance", testnet=self.testnet)
            
            # Connect to WebSocket
            self.websocket = await websockets.connect(
                self.ws_url,
                ping_interval=20,
                ping_timeout=10,
            )
            
            self.status = FeedStatus.CONNECTED
            self.reconnect_delay = 1  # Reset delay on successful connection
            self.update_heartbeat()
            
            # Start listening for messages
            self.listen_task = asyncio.create_task(self._listen())
            
            logger.info("binance_connected", testnet=self.testnet)
            return True
            
        except Exception as e:
            self.status = FeedStatus.ERROR
            logger.error("binance_connection_error", error=str(e))
            await self._emit_error(e)
            return False
    
    async def disconnect(self) -> None:
        """Close WebSocket connection"""
        logger.info("disconnecting_from_binance")
        
        # Cancel listen task
        if self.listen_task:
            self.listen_task.cancel()
            try:
                await self.listen_task
            except asyncio.CancelledError:
                pass
        
        # Close WebSocket
        if self.websocket:
            await self.websocket.close()
            self.websocket = None
        
        self.status = FeedStatus.DISCONNECTED
        logger.info("binance_disconnected")
    
    async def subscribe(self, symbols: List[Symbol]) -> None:
        """
        Subscribe to kline (candle) streams for symbols.
        
        Args:
            symbols: List of symbols to subscribe to
        """
        if not self.is_connected():
            logger.warning("cannot_subscribe_not_connected")
            return
        
        # Build subscription message
        # Binance format: btcusdt@kline_1m
        streams = []
        for symbol in symbols:
            # Convert BTC/USDT to btcusdt
            binance_symbol = str(symbol).replace("/", "").lower()
            streams.append(f"{binance_symbol}@kline_1m")
            streams.append(f"{binance_symbol}@kline_5m")
            streams.append(f"{binance_symbol}@kline_15m")
            streams.append(f"{binance_symbol}@kline_1h")
        
        subscribe_msg = {
            "method": "SUBSCRIBE",
            "params": streams,
            "id": int(datetime.utcnow().timestamp())
        }
        
        try:
            await self.websocket.send(json.dumps(subscribe_msg))
            self.subscribed_symbols.extend(symbols)
            logger.info("subscribed_to_symbols", symbols=[str(s) for s in symbols])
        except Exception as e:
            logger.error("subscription_error", error=str(e))
            await self._emit_error(e)
    
    async def unsubscribe(self, symbols: List[Symbol]) -> None:
        """
        Unsubscribe from kline streams.
        
        Args:
            symbols: List of symbols to unsubscribe from
        """
        if not self.is_connected():
            return
        
        streams = []
        for symbol in symbols:
            binance_symbol = str(symbol).replace("/", "").lower()
            streams.append(f"{binance_symbol}@kline_1m")
            streams.append(f"{binance_symbol}@kline_5m")
            streams.append(f"{binance_symbol}@kline_15m")
            streams.append(f"{binance_symbol}@kline_1h")
        
        unsubscribe_msg = {
            "method": "UNSUBSCRIBE",
            "params": streams,
            "id": int(datetime.utcnow().timestamp())
        }
        
        try:
            await self.websocket.send(json.dumps(unsubscribe_msg))
            self.subscribed_symbols = [s for s in self.subscribed_symbols if s not in symbols]
            logger.info("unsubscribed_from_symbols", symbols=[str(s) for s in symbols])
        except Exception as e:
            logger.error("unsubscription_error", error=str(e))
    
    async def _listen(self) -> None:
        """
        Listen for WebSocket messages.
        Runs continuously while connected.
        """
        logger.info("binance_listener_started")
        
        try:
            async for message in self.websocket:
                try:
                    data = json.loads(message)
                    await self._handle_message(data)
                    self.update_heartbeat()
                except json.JSONDecodeError as e:
                    logger.error("json_decode_error", error=str(e))
                except Exception as e:
                    logger.error("message_handling_error", error=str(e))
                    
        except websockets.exceptions.ConnectionClosed:
            logger.warning("binance_connection_closed")
            await self._reconnect()
        except asyncio.CancelledError:
            logger.info("binance_listener_cancelled")
        except Exception as e:
            logger.error("binance_listener_error", error=str(e))
            await self._emit_error(e)
            await self._reconnect()
    
    async def _handle_message(self, data: dict) -> None:
        """
        Handle incoming WebSocket message.
        
        Args:
            data: Parsed JSON message
        """
        # Skip subscription confirmations
        if "result" in data or "id" in data:
            return
        
        # Handle kline/candle data
        if "e" in data and data["e"] == "kline":
            await self._handle_kline(data)
    
    async def _handle_kline(self, data: dict) -> None:
        """
        Handle kline (candle) message.
        
        Args:
            data: Kline data from Binance
        """
        try:
            kline = data["k"]
            
            # Convert to internal format
            candle_data = {
                "symbol": kline["s"].replace("USDT", "/USDT"),  # btcusdt -> BTC/USDT
                "interval": kline["i"],
                "timestamp": kline["t"],
                "open": kline["o"],
                "high": kline["h"],
                "low": kline["l"],
                "close": kline["c"],
                "volume": kline["v"],
            }
            
            # Normalize and emit
            candle = self.normalizer.normalize_candle(candle_data, self.exchange_name)
            await self._emit_candle(candle)
            
        except Exception as e:
            logger.error("kline_handling_error", error=str(e), data=data)
    
    async def _reconnect(self) -> None:
        """
        Reconnect with exponential backoff.
        """
        self.status = FeedStatus.RECONNECTING
        
        logger.info("reconnecting_to_binance", delay=self.reconnect_delay)
        await asyncio.sleep(self.reconnect_delay)
        
        # Exponential backoff: 1s, 2s, 4s, 8s, ..., max 60s
        self.reconnect_delay = min(self.reconnect_delay * 2, self.max_reconnect_delay)
        
        # Attempt reconnection
        success = await self.connect()
        
        if success and self.subscribed_symbols:
            # Re-subscribe to previous symbols
            await self.subscribe(self.subscribed_symbols.copy())
