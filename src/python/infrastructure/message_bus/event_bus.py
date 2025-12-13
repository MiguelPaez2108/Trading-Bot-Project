"""
Event Bus orchestrator.

Coordinates event publishing and subscription.
"""
from typing import Dict, List, Callable, Optional
import logging

from src.python.infrastructure.database.redis_client import RedisClient, get_redis_client
from src.python.infrastructure.message_bus.publisher import EventPublisher
from src.python.infrastructure.message_bus.subscriber import EventSubscriber
from src.python.domain.events.base_event import DomainEvent

logger = logging.getLogger(__name__)


class EventBus:
    """
    Event bus for domain events.
    
    Coordinates:
    - Event publishing
    - Event subscription
    - Handler registration
    - Lifecycle management
    """
    
    def __init__(
        self,
        redis_client: Optional[RedisClient] = None,
        consumer_group: str = "trading-system",
        consumer_name: str = "main"
    ):
        """
        Initialize event bus.
        
        Args:
            redis_client: Redis client (optional, will create if not provided)
            consumer_group: Consumer group name
            consumer_name: Consumer name
        """
        self.redis_client = redis_client
        self.consumer_group = consumer_group
        self.consumer_name = consumer_name
        
        self.publisher: Optional[EventPublisher] = None
        self.subscriber: Optional[EventSubscriber] = None
        
        # Local handlers (in-memory, synchronous)
        self.local_handlers: Dict[str, List[Callable]] = {}
    
    async def initialize(self) -> None:
        """Initialize event bus."""
        # Get Redis client if not provided
        if self.redis_client is None:
            self.redis_client = await get_redis_client()
        
        # Create publisher
        self.publisher = EventPublisher(self.redis_client)
        
        # Create subscriber
        self.subscriber = EventSubscriber(
            self.redis_client,
            self.consumer_group,
            self.consumer_name
        )
        
        logger.info("Event bus initialized")
    
    async def start(self) -> None:
        """Start event bus (begin consuming events)."""
        if not self.subscriber:
            await self.initialize()
        
        # Start subscriber
        await self.subscriber.start()
    
    async def stop(self) -> None:
        """Stop event bus."""
        if self.subscriber:
            await self.subscriber.stop()
        
        logger.info("Event bus stopped")
    
    # ========================================================================
    # Publishing
    # ========================================================================
    
    async def publish(self, event: DomainEvent) -> None:
        """
        Publish event.
        
        Publishes to both:
        - Redis Streams (for distributed consumption)
        - Local handlers (for in-process consumption)
        
        Args:
            event: Domain event to publish
        """
        # Publish to Redis Streams
        if self.publisher:
            await self.publisher.publish(event)
        
        # Call local handlers
        await self._call_local_handlers(event)
    
    async def publish_batch(self, events: List[DomainEvent]) -> None:
        """
        Publish multiple events.
        
        Args:
            events: List of domain events
        """
        if self.publisher:
            await self.publisher.publish_batch(events)
        
        for event in events:
            await self._call_local_handlers(event)
    
    # ========================================================================
    # Subscription
    # ========================================================================
    
    def subscribe(
        self,
        event_type: str,
        handler: Callable,
        local_only: bool = False
    ) -> None:
        """
        Subscribe to event type.
        
        Args:
            event_type: Event type to subscribe to
            handler: Async function to handle event
            local_only: Only handle local events (not from Redis)
        """
        if local_only:
            # Register local handler only
            if event_type not in self.local_handlers:
                self.local_handlers[event_type] = []
            self.local_handlers[event_type].append(handler)
        else:
            # Register with subscriber (Redis Streams)
            if self.subscriber:
                self.subscriber.subscribe(event_type, handler)
            
            # Also register locally
            if event_type not in self.local_handlers:
                self.local_handlers[event_type] = []
            self.local_handlers[event_type].append(handler)
    
    async def _call_local_handlers(self, event: DomainEvent) -> None:
        """
        Call local event handlers.
        
        Args:
            event: Domain event
        """
        event_type = event.event_type
        
        if event_type in self.local_handlers:
            for handler in self.local_handlers[event_type]:
                try:
                    await handler(event)
                except Exception as e:
                    logger.error(f"Error in local handler for {event_type}: {e}")
    
    # ========================================================================
    # Context Manager
    # ========================================================================
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self.initialize()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.stop()


# Global event bus instance
_event_bus: Optional[EventBus] = None


async def get_event_bus() -> EventBus:
    """
    Get global event bus instance.
    
    Returns:
        EventBus instance
    """
    global _event_bus
    
    if _event_bus is None:
        _event_bus = EventBus()
        await _event_bus.initialize()
    
    return _event_bus


async def close_event_bus() -> None:
    """Close global event bus."""
    global _event_bus
    
    if _event_bus is not None:
        await _event_bus.stop()
        _event_bus = None
