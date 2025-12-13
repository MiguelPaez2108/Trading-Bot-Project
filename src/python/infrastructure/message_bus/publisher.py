"""
Redis Streams Event Publisher.

Publishes domain events to Redis Streams for event-driven architecture.
"""
from typing import Dict, Any, Optional
import json
import logging
from datetime import datetime
from uuid import uuid4

from src.python.infrastructure.database.redis_client import RedisClient
from src.python.domain.events.base_event import DomainEvent

logger = logging.getLogger(__name__)


class EventPublisher:
    """
    Publishes domain events to Redis Streams.
    
    Features:
    - Event serialization
    - Stream partitioning by event type
    - Max length management
    - Publish confirmation
    """
    
    def __init__(
        self,
        redis_client: RedisClient,
        stream_prefix: str = "events",
        max_stream_length: int = 10000
    ):
        """
        Initialize event publisher.
        
        Args:
            redis_client: Redis client instance
            stream_prefix: Prefix for stream names
            max_stream_length: Max entries per stream
        """
        self.redis = redis_client
        self.stream_prefix = stream_prefix
        self.max_stream_length = max_stream_length
    
    async def publish(self, event: DomainEvent) -> str:
        """
        Publish domain event to stream.
        
        Args:
            event: Domain event to publish
        
        Returns:
            Event ID from Redis
        """
        # Get stream name based on event type
        stream_name = self._get_stream_name(event)
        
        # Serialize event
        event_data = self._serialize_event(event)
        
        # Publish to stream
        event_id = await self.redis.xadd(
            name=stream_name,
            fields=event_data,
            maxlen=self.max_stream_length
        )
        
        logger.debug(
            f"Published event {event.event_type} to {stream_name} with ID {event_id}"
        )
        
        return event_id
    
    async def publish_batch(self, events: list[DomainEvent]) -> list[str]:
        """
        Publish multiple events.
        
        Args:
            events: List of domain events
        
        Returns:
            List of event IDs
        """
        event_ids = []
        
        for event in events:
            event_id = await self.publish(event)
            event_ids.append(event_id)
        
        return event_ids
    
    def _get_stream_name(self, event: DomainEvent) -> str:
        """
        Get stream name for event.
        
        Events are partitioned by type into separate streams.
        
        Args:
            event: Domain event
        
        Returns:
            Stream name (e.g., 'events:order_filled')
        """
        return f"{self.stream_prefix}:{event.event_type}"
    
    def _serialize_event(self, event: DomainEvent) -> Dict[str, str]:
        """
        Serialize event to Redis fields.
        
        Args:
            event: Domain event
        
        Returns:
            Dict of field-value pairs for Redis
        """
        # Convert event to dict
        event_dict = event.to_dict()
        
        # Serialize to JSON strings (Redis Streams requires string values)
        fields = {
            'event_id': str(event.event_id),
            'event_type': event.event_type,
            'timestamp': event.timestamp.isoformat(),
            'data': json.dumps(event_dict.get('data', {})),
            'metadata': json.dumps(event_dict.get('metadata', {}))
        }
        
        return fields
