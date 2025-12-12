"""
Redis client with connection pooling.

Provides async Redis access using aioredis.
"""
import redis.asyncio as aioredis
from typing import Optional, Any, List, Dict
import json
import logging
from datetime import timedelta

from src.python.infrastructure.config.settings import get_settings

logger = logging.getLogger(__name__)


class RedisClient:
    """
    Redis client with connection pooling.
    
    Features:
    - Async connection pooling
    - JSON serialization
    - TTL support
    - Pub/Sub support
    - Streams support
    """
    
    def __init__(self):
        """Initialize Redis client."""
        self.settings = get_settings().redis
        self.client: Optional[aioredis.Redis] = None
        self.pool: Optional[aioredis.ConnectionPool] = None
    
    async def connect(self) -> None:
        """
        Create connection pool and client.
        
        Raises:
            Exception: If connection fails
        """
        try:
            self.pool = aioredis.ConnectionPool(
                host=self.settings.host,
                port=self.settings.port,
                db=self.settings.db,
                password=self.settings.password,
                max_connections=self.settings.max_connections,
                socket_timeout=self.settings.socket_timeout,
                socket_connect_timeout=self.settings.socket_connect_timeout,
                decode_responses=self.settings.decode_responses,
            )
            
            self.client = aioredis.Redis(connection_pool=self.pool)
            
            # Test connection
            await self.client.ping()
            
            logger.info(
                f"Connected to Redis at {self.settings.host}:{self.settings.port}"
            )
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise
    
    async def disconnect(self) -> None:
        """Close connection pool."""
        if self.client:
            await self.client.close()
            logger.info("Disconnected from Redis")
    
    # ========================================================================
    # Basic Operations
    # ========================================================================
    
    async def get(self, key: str) -> Optional[str]:
        """
        Get value by key.
        
        Args:
            key: Redis key
        
        Returns:
            Value or None if not found
        """
        return await self.client.get(key)
    
    async def set(
        self,
        key: str,
        value: str,
        ex: Optional[int] = None,
        px: Optional[int] = None,
        nx: bool = False,
        xx: bool = False
    ) -> bool:
        """
        Set key to value.
        
        Args:
            key: Redis key
            value: Value to set
            ex: Expire time in seconds
            px: Expire time in milliseconds
            nx: Only set if key doesn't exist
            xx: Only set if key exists
        
        Returns:
            True if successful
        """
        return await self.client.set(key, value, ex=ex, px=px, nx=nx, xx=xx)
    
    async def delete(self, *keys: str) -> int:
        """
        Delete one or more keys.
        
        Args:
            *keys: Keys to delete
        
        Returns:
            Number of keys deleted
        """
        return await self.client.delete(*keys)
    
    async def exists(self, *keys: str) -> int:
        """
        Check if keys exist.
        
        Args:
            *keys: Keys to check
        
        Returns:
            Number of existing keys
        """
        return await self.client.exists(*keys)
    
    async def expire(self, key: str, seconds: int) -> bool:
        """
        Set key expiration.
        
        Args:
            key: Redis key
            seconds: Seconds until expiration
        
        Returns:
            True if successful
        """
        return await self.client.expire(key, seconds)
    
    async def ttl(self, key: str) -> int:
        """
        Get time to live for key.
        
        Args:
            key: Redis key
        
        Returns:
            TTL in seconds, -1 if no expiry, -2 if key doesn't exist
        """
        return await self.client.ttl(key)
    
    # ========================================================================
    # JSON Operations
    # ========================================================================
    
    async def get_json(self, key: str) -> Optional[Any]:
        """
        Get JSON value by key.
        
        Args:
            key: Redis key
        
        Returns:
            Deserialized JSON or None
        """
        value = await self.get(key)
        if value is None:
            return None
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            logger.error(f"Failed to decode JSON for key: {key}")
            return None
    
    async def set_json(
        self,
        key: str,
        value: Any,
        ex: Optional[int] = None
    ) -> bool:
        """
        Set JSON value.
        
        Args:
            key: Redis key
            value: Value to serialize and set
            ex: Expire time in seconds
        
        Returns:
            True if successful
        """
        try:
            json_value = json.dumps(value)
            return await self.set(key, json_value, ex=ex)
        except (TypeError, ValueError) as e:
            logger.error(f"Failed to serialize JSON for key {key}: {e}")
            return False
    
    # ========================================================================
    # Hash Operations
    # ========================================================================
    
    async def hget(self, name: str, key: str) -> Optional[str]:
        """Get hash field value."""
        return await self.client.hget(name, key)
    
    async def hset(
        self,
        name: str,
        key: Optional[str] = None,
        value: Optional[str] = None,
        mapping: Optional[Dict] = None
    ) -> int:
        """Set hash field value."""
        return await self.client.hset(name, key, value, mapping=mapping)
    
    async def hgetall(self, name: str) -> Dict:
        """Get all hash fields."""
        return await self.client.hgetall(name)
    
    async def hdel(self, name: str, *keys: str) -> int:
        """Delete hash fields."""
        return await self.client.hdel(name, *keys)
    
    # ========================================================================
    # List Operations
    # ========================================================================
    
    async def lpush(self, key: str, *values: str) -> int:
        """Push values to left of list."""
        return await self.client.lpush(key, *values)
    
    async def rpush(self, key: str, *values: str) -> int:
        """Push values to right of list."""
        return await self.client.rpush(key, *values)
    
    async def lpop(self, key: str) -> Optional[str]:
        """Pop value from left of list."""
        return await self.client.lpop(key)
    
    async def rpop(self, key: str) -> Optional[str]:
        """Pop value from right of list."""
        return await self.client.rpop(key)
    
    async def lrange(self, key: str, start: int, end: int) -> List[str]:
        """Get range of list elements."""
        return await self.client.lrange(key, start, end)
    
    async def llen(self, key: str) -> int:
        """Get list length."""
        return await self.client.llen(key)
    
    # ========================================================================
    # Pub/Sub Operations
    # ========================================================================
    
    async def publish(self, channel: str, message: str) -> int:
        """
        Publish message to channel.
        
        Args:
            channel: Channel name
            message: Message to publish
        
        Returns:
            Number of subscribers that received the message
        """
        return await self.client.publish(channel, message)
    
    async def subscribe(self, *channels: str):
        """
        Subscribe to channels.
        
        Args:
            *channels: Channel names
        
        Returns:
            PubSub object
        """
        pubsub = self.client.pubsub()
        await pubsub.subscribe(*channels)
        return pubsub
    
    # ========================================================================
    # Streams Operations
    # ========================================================================
    
    async def xadd(
        self,
        name: str,
        fields: Dict[str, str],
        id: str = "*",
        maxlen: Optional[int] = None
    ) -> str:
        """
        Add entry to stream.
        
        Args:
            name: Stream name
            fields: Field-value pairs
            id: Entry ID (default: auto-generate)
            maxlen: Max stream length (trim old entries)
        
        Returns:
            Entry ID
        """
        return await self.client.xadd(name, fields, id=id, maxlen=maxlen)
    
    async def xread(
        self,
        streams: Dict[str, str],
        count: Optional[int] = None,
        block: Optional[int] = None
    ) -> List:
        """
        Read from streams.
        
        Args:
            streams: Dict of {stream_name: last_id}
            count: Max entries to return
            block: Block for milliseconds if no data
        
        Returns:
            List of stream entries
        """
        return await self.client.xread(streams, count=count, block=block)
    
    async def xgroup_create(
        self,
        name: str,
        groupname: str,
        id: str = "$",
        mkstream: bool = True
    ) -> bool:
        """
        Create consumer group.
        
        Args:
            name: Stream name
            groupname: Group name
            id: Start reading from this ID
            mkstream: Create stream if doesn't exist
        
        Returns:
            True if successful
        """
        try:
            await self.client.xgroup_create(name, groupname, id=id, mkstream=mkstream)
            return True
        except aioredis.ResponseError as e:
            if "BUSYGROUP" in str(e):
                # Group already exists
                return True
            raise
    
    async def xreadgroup(
        self,
        groupname: str,
        consumername: str,
        streams: Dict[str, str],
        count: Optional[int] = None,
        block: Optional[int] = None
    ) -> List:
        """
        Read from streams as consumer group member.
        
        Args:
            groupname: Consumer group name
            consumername: Consumer name
            streams: Dict of {stream_name: last_id}
            count: Max entries to return
            block: Block for milliseconds if no data
        
        Returns:
            List of stream entries
        """
        return await self.client.xreadgroup(
            groupname,
            consumername,
            streams,
            count=count,
            block=block
        )
    
    async def xack(self, name: str, groupname: str, *ids: str) -> int:
        """
        Acknowledge stream entries.
        
        Args:
            name: Stream name
            groupname: Group name
            *ids: Entry IDs to acknowledge
        
        Returns:
            Number of acknowledged entries
        """
        return await self.client.xack(name, groupname, *ids)
    
    # ========================================================================
    # Utility
    # ========================================================================
    
    async def health_check(self) -> bool:
        """
        Check Redis health.
        
        Returns:
            True if healthy, False otherwise
        """
        try:
            return await self.client.ping()
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False
    
    async def flushdb(self) -> bool:
        """
        Flush current database.
        
        WARNING: Deletes all keys in current DB!
        
        Returns:
            True if successful
        """
        return await self.client.flushdb()


# Global client instance
_redis_client: Optional[RedisClient] = None


async def get_redis_client() -> RedisClient:
    """
    Get global Redis client instance.
    
    Returns:
        RedisClient instance
    """
    global _redis_client
    
    if _redis_client is None:
        _redis_client = RedisClient()
        await _redis_client.connect()
    
    return _redis_client


async def close_redis_client() -> None:
    """Close global Redis client."""
    global _redis_client
    
    if _redis_client is not None:
        await _redis_client.disconnect()
        _redis_client = None
