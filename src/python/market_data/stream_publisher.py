"""
Redis Streams Publisher
Publishes market data to Redis Streams for real-time consumption
"""
import asyncio
from typing import Any, Dict, Optional
import msgpack
import redis.asyncio as aioredis
import structlog

from src.python.domain.entities import Candle
from src.python.infrastructure.config.settings import get_settings

logger = structlog.get_logger(__name__)


class RedisStreamsPublisher:
    """
    Publishes market data to Redis Streams.
    Uses msgpack for efficient serialization.
    """
    
    def __init__(self):
        """Initialize Redis Streams publisher"""
        settings = get_settings()
        self.redis_url = settings.redis_streams_url
        self.redis: Optional[aioredis.Redis] = None
        self.buffer: Dict[str, list] = {}
        self.buffer_size = 10  # Batch size
        self.flush_task: Optional[asyncio.Task] = None
        self.is_running = False
    
    async def connect(self) -> bool:
        """
        Connect to Redis.
        
        Returns:
            True if connected successfully
        """
        try:
            self.redis = await aioredis.from_url(
                self.redis_url,
                encoding="utf-8",
                decode_responses=False,  # We use msgpack
            )
            
            # Test connection
            await self.redis.ping()
            
            logger.info("redis_streams_connected")
            return True
            
        except Exception as e:
            logger.error("redis_connection_error", error=str(e))
            return False
    
    async def disconnect(self) -> None:
        """Disconnect from Redis"""
        if self.redis:
            await self.redis.close()
            self.redis = None
        logger.info("redis_streams_disconnected")
    
    async def publish_candle(self, candle: Candle) -> None:
        """
        Publish candle to Redis Stream.
        
        Args:
            candle: Candle entity to publish
        
        Stream format: market_data:{symbol}:candles:{timeframe}
        Example: market_data:BTC/USDT:candles:1m
        """
        if not self.redis:
            logger.warning("redis_not_connected")
            return
        
        try:
            # Build stream key
            stream_key = f"market_data:{candle.symbol}:candles:{candle.timeframe}"
            
            # Serialize candle data with msgpack
            candle_dict = {
                "symbol": str(candle.symbol),
                "timeframe": str(candle.timeframe),
                "timestamp": int(candle.timestamp.timestamp() * 1000),
                "open": float(candle.open.value),
                "high": float(candle.high.value),
                "low": float(candle.low.value),
                "close": float(candle.close.value),
                "volume": float(candle.volume.value),
                "exchange": candle.exchange,
            }
            
            packed_data = msgpack.packb(candle_dict)
            
            # Publish to stream
            await self.redis.xadd(
                stream_key,
                {"data": packed_data},
                maxlen=10000,  # Keep last 10K candles
                approximate=True,
            )
            
            logger.debug(
                "candle_published",
                symbol=str(candle.symbol),
                timeframe=str(candle.timeframe)
            )
            
        except Exception as e:
            logger.error("candle_publish_error", error=str(e))
    
    async def publish_trade(self, trade_data: Dict[str, Any]) -> None:
        """
        Publish trade to Redis Stream.
        
        Args:
            trade_data: Normalized trade data
        
        Stream format: market_data:{symbol}:trades
        """
        if not self.redis:
            return
        
        try:
            stream_key = f"market_data:{trade_data['symbol']}:trades"
            
            # Serialize with msgpack
            trade_dict = {
                "symbol": str(trade_data["symbol"]),
                "price": float(trade_data["price"].value),
                "quantity": float(trade_data["quantity"].value),
                "side": trade_data["side"],
                "timestamp": int(trade_data["timestamp"].timestamp() * 1000),
                "exchange": trade_data["exchange"],
                "trade_id": trade_data.get("trade_id"),
                "is_buyer_maker": trade_data.get("is_buyer_maker", False),
            }
            
            packed_data = msgpack.packb(trade_dict)
            
            await self.redis.xadd(
                stream_key,
                {"data": packed_data},
                maxlen=50000,  # Keep last 50K trades
                approximate=True,
            )
            
            logger.debug("trade_published", symbol=str(trade_data["symbol"]))
            
        except Exception as e:
            logger.error("trade_publish_error", error=str(e))
    
    async def publish_orderbook(self, orderbook_data: Dict[str, Any]) -> None:
        """
        Publish orderbook snapshot to Redis Stream.
        
        Args:
            orderbook_data: Orderbook data
        
        Stream format: market_data:{symbol}:orderbook
        """
        if not self.redis:
            return
        
        try:
            stream_key = f"market_data:{orderbook_data['symbol']}:orderbook"
            
            packed_data = msgpack.packb(orderbook_data)
            
            await self.redis.xadd(
                stream_key,
                {"data": packed_data},
                maxlen=1000,  # Keep last 1K snapshots
                approximate=True,
            )
            
            logger.debug("orderbook_published", symbol=orderbook_data["symbol"])
            
        except Exception as e:
            logger.error("orderbook_publish_error", error=str(e))
    
    async def get_latest_candles(
        self,
        symbol: str,
        timeframe: str,
        count: int = 100
    ) -> list:
        """
        Get latest candles from Redis Stream.
        
        Args:
            symbol: Trading symbol
            timeframe: Timeframe (e.g., "1m", "1h")
            count: Number of candles to retrieve
        
        Returns:
            List of candle dicts
        """
        if not self.redis:
            return []
        
        try:
            stream_key = f"market_data:{symbol}:candles:{timeframe}"
            
            # Read from stream
            messages = await self.redis.xrevrange(
                stream_key,
                count=count
            )
            
            candles = []
            for msg_id, msg_data in messages:
                packed = msg_data[b"data"]
                candle = msgpack.unpackb(packed, raw=False)
                candles.append(candle)
            
            return candles
            
        except Exception as e:
            logger.error("get_candles_error", error=str(e))
            return []
    
    async def start_flush_loop(self) -> None:
        """
        Start background task to flush buffered messages.
        Useful for batching if needed in the future.
        """
        self.is_running = True
        self.flush_task = asyncio.create_task(self._flush_loop())
    
    async def stop_flush_loop(self) -> None:
        """Stop flush loop"""
        self.is_running = False
        if self.flush_task:
            self.flush_task.cancel()
            try:
                await self.flush_task
            except asyncio.CancelledError:
                pass
    
    async def _flush_loop(self) -> None:
        """Background task to flush buffers periodically"""
        while self.is_running:
            try:
                # Flush every 100ms
                await asyncio.sleep(0.1)
                # Future: implement batching logic here
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error("flush_loop_error", error=str(e))
