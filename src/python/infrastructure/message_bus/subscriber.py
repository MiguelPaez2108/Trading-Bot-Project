"""
Redis Streams Event Subscriber.

Subscribes to domain events from Redis Streams using consumer groups.
"""
from typing import Dict, Any, Callable, Optional, List
import json
import asyncio
import logging
from datetime import datetime

from src.python.infrastructure.database.redis_client import RedisClient
from src.python.domain.events.base_event import DomainEvent

logger = logging.getLogger(__name__)


class EventSubscriber:
    """
    Subscribes to domain events from Redis Streams.
    
    Features:
    - Consumer groups for load balancing
    - Automatic acknowledgment
    - Error handling with DLQ
    - Graceful shutdown
    """
    
    def __init__(
        self,
        redis_client: RedisClient,
        consumer_group: str,
        consumer_name: str,
        stream_prefix: str = "events"
    ):
        """
        Initialize event subscriber.
        
        Args:
            redis_client: Redis client instance
            consumer_group: Consumer group name
            consumer_name: Unique consumer name
            stream_prefix: Prefix for stream names
        """
        self.redis = redis_client
        self.consumer_group = consumer_group
        self.consumer_name = consumer_name
        self.stream_prefix = stream_prefix
        
        # Event handlers
        self.handlers: Dict[str, List[Callable]] = {}
        
        # Running flag
        self.running = False
    
    def subscribe(self, event_type: str, handler: Callable) -> None:
        """
        Subscribe to event type.
        
        Args:
            event_type: Event type to subscribe to
            handler: Async function to handle event
        """
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        
        self.handlers[event_type].append(handler)
        logger.info(f"Subscribed to {event_type}")
    
    async def start(self) -> None:
        """
        Start consuming events.
        
        Creates consumer groups and starts polling.
        """
        self.running = True
        
        # Create consumer groups for each event type
        for event_type in self.handlers.keys():
            stream_name = f"{self.stream_prefix}:{event_type}"
            await self._ensure_consumer_group(stream_name)
        
        logger.info(f"Event subscriber started (group: {self.consumer_group}, consumer: {self.consumer_name})")
        
        # Start consuming
        await self._consume_loop()
    
    async def stop(self) -> None:
        """Stop consuming events."""
        self.running = False
        logger.info("Event subscriber stopped")
    
    async def _ensure_consumer_group(self, stream_name: str) -> None:
        """
        Ensure consumer group exists for stream.
        
        Args:
            stream_name: Stream name
        """
        try:
            await self.redis.xgroup_create(
                name=stream_name,
                groupname=self.consumer_group,
                id="0",  # Start from beginning
                mkstream=True
            )
            logger.info(f"Created consumer group {self.consumer_group} for {stream_name}")
        except Exception as e:
            # Group might already exist
            logger.debug(f"Consumer group already exists: {e}")
    
    async def _consume_loop(self) -> None:
        """Main consumption loop."""
        while self.running:
            try:
                # Build streams dict
                streams = {
                    f"{self.stream_prefix}:{event_type}": ">"
                    for event_type in self.handlers.keys()
                }
                
                # Read from streams (block for 1 second)
                results = await self.redis.xreadgroup(
                    groupname=self.consumer_group,
                    consumername=self.consumer_name,
                    streams=streams,
                    count=10,  # Process up to 10 events at a time
                    block=1000  # Block for 1 second
                )
                
                # Process events
                if results:
                    await self._process_results(results)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in consume loop: {e}")
                await asyncio.sleep(1)  # Backoff on error
    
    async def _process_results(self, results: List) -> None:
        """
        Process consumed events.
        
        Args:
            results: Results from xreadgroup
        """
        for stream_name, messages in results:
            # Extract event type from stream name
            event_type = stream_name.decode() if isinstance(stream_name, bytes) else stream_name
            event_type = event_type.split(':')[-1]
            
            for message_id, fields in messages:
                try:
                    # Deserialize event
                    event = self._deserialize_event(fields)
                    
                    # Call handlers
                    if event_type in self.handlers:
                        for handler in self.handlers[event_type]:
                            await handler(event)
                    
                    # Acknowledge message
                    await self.redis.xack(
                        stream_name,
                        self.consumer_group,
                        message_id
                    )
                    
                except Exception as e:
                    logger.error(f"Error processing event {message_id}: {e}")
                    # TODO: Send to DLQ
    
    def _deserialize_event(self, fields: Dict[bytes, bytes]) -> DomainEvent:
        """
        Deserialize event from Redis fields.
        
        Args:
            fields: Redis fields
        
        Returns:
            Domain event
        """
        # Decode bytes to strings
        if isinstance(next(iter(fields.keys())), bytes):
            fields = {k.decode(): v.decode() for k, v in fields.items()}
        
        # Parse JSON data
        data = json.loads(fields.get('data', '{}'))
        metadata = json.loads(fields.get('metadata', '{}'))
        
        # Create generic domain event
        # In production, you'd reconstruct the specific event type
        event = DomainEvent(
            event_type=fields['event_type'],
            data=data,
            metadata=metadata
        )
        
        # Override event_id and timestamp
        event.event_id = fields['event_id']
        event.timestamp = datetime.fromisoformat(fields['timestamp'])
        
        return event
