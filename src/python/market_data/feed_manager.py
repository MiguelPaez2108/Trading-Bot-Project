"""
Feed Manager
Orchestrates multiple market data feeds
"""
from typing import Dict, List, Optional
import asyncio
import structlog

from src.python.domain.value_objects import Symbol
from src.python.market_data.feeds.base_feed import MarketDataFeed, FeedStatus

logger = structlog.get_logger(__name__)


class FeedManager:
    """
    Manages multiple market data feeds.
    Handles starting, stopping, health monitoring, and auto-reconnect.
    """
    
    def __init__(self):
        """Initialize feed manager"""
        self.feeds: Dict[str, MarketDataFeed] = {}
        self.monitoring_task: Optional[asyncio.Task] = None
        self.is_running = False
    
    def register_feed(self, exchange: str, feed: MarketDataFeed) -> None:
        """
        Register a feed for an exchange.
        
        Args:
            exchange: Exchange name
            feed: MarketDataFeed instance
        """
        self.feeds[exchange] = feed
        logger.info("feed_registered", exchange=exchange)
    
    async def start_feed(self, exchange: str) -> bool:
        """
        Start a specific feed.
        
        Args:
            exchange: Exchange name
        
        Returns:
            True if started successfully
        """
        if exchange not in self.feeds:
            logger.error("feed_not_found", exchange=exchange)
            return False
        
        feed = self.feeds[exchange]
        
        try:
            success = await feed.connect()
            if success:
                logger.info("feed_started", exchange=exchange)
            return success
        except Exception as e:
            logger.error("feed_start_error", exchange=exchange, error=str(e))
            return False
    
    async def stop_feed(self, exchange: str) -> None:
        """
        Stop a specific feed.
        
        Args:
            exchange: Exchange name
        """
        if exchange not in self.feeds:
            logger.warning("feed_not_found_for_stop", exchange=exchange)
            return
        
        feed = self.feeds[exchange]
        await feed.disconnect()
        logger.info("feed_stopped", exchange=exchange)
    
    async def restart_feed(self, exchange: str) -> bool:
        """
        Restart a specific feed.
        
        Args:
            exchange: Exchange name
        
        Returns:
            True if restarted successfully
        """
        logger.info("restarting_feed", exchange=exchange)
        await self.stop_feed(exchange)
        await asyncio.sleep(2)  # Brief pause before reconnect
        return await self.start_feed(exchange)
    
    async def subscribe_symbols(self, exchange: str, symbols: List[Symbol]) -> None:
        """
        Subscribe to symbols on a feed.
        
        Args:
            exchange: Exchange name
            symbols: List of symbols to subscribe
        """
        if exchange not in self.feeds:
            logger.error("feed_not_found_for_subscribe", exchange=exchange)
            return
        
        feed = self.feeds[exchange]
        await feed.subscribe(symbols)
        logger.info("symbols_subscribed", exchange=exchange, count=len(symbols))
    
    async def unsubscribe_symbols(self, exchange: str, symbols: List[Symbol]) -> None:
        """
        Unsubscribe from symbols on a feed.
        
        Args:
            exchange: Exchange name
            symbols: List of symbols to unsubscribe
        """
        if exchange not in self.feeds:
            logger.error("feed_not_found_for_unsubscribe", exchange=exchange)
            return
        
        feed = self.feeds[exchange]
        await feed.unsubscribe(symbols)
        logger.info("symbols_unsubscribed", exchange=exchange, count=len(symbols))
    
    async def start_all(self) -> None:
        """Start all registered feeds"""
        logger.info("starting_all_feeds", count=len(self.feeds))
        
        tasks = [self.start_feed(exchange) for exchange in self.feeds.keys()]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        success_count = sum(1 for r in results if r is True)
        logger.info("feeds_started", total=len(self.feeds), success=success_count)
        
        # Start health monitoring
        self.is_running = True
        self.monitoring_task = asyncio.create_task(self._monitor_health())
    
    async def stop_all(self) -> None:
        """Stop all registered feeds"""
        logger.info("stopping_all_feeds")
        
        # Stop monitoring
        self.is_running = False
        if self.monitoring_task:
            self.monitoring_task.cancel()
            try:
                await self.monitoring_task
            except asyncio.CancelledError:
                pass
        
        # Stop all feeds
        tasks = [self.stop_feed(exchange) for exchange in self.feeds.keys()]
        await asyncio.gather(*tasks, return_exceptions=True)
        
        logger.info("all_feeds_stopped")
    
    async def _monitor_health(self) -> None:
        """
        Monitor health of all feeds and auto-reconnect if needed.
        Runs continuously while feeds are active.
        """
        logger.info("health_monitoring_started")
        
        while self.is_running:
            try:
                for exchange, feed in self.feeds.items():
                    # Check connection status
                    if feed.get_status() == FeedStatus.ERROR:
                        logger.warning("feed_in_error_state", exchange=exchange)
                        await self.restart_feed(exchange)
                    
                    # Check heartbeat
                    elif feed.is_connected() and not feed.is_heartbeat_alive(timeout_seconds=60):
                        logger.warning("feed_heartbeat_timeout", exchange=exchange)
                        await self.restart_feed(exchange)
                
                # Check every 30 seconds
                await asyncio.sleep(30)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error("health_monitoring_error", error=str(e))
                await asyncio.sleep(30)
        
        logger.info("health_monitoring_stopped")
    
    def get_feed_status(self, exchange: str) -> Optional[FeedStatus]:
        """
        Get status of a specific feed.
        
        Args:
            exchange: Exchange name
        
        Returns:
            FeedStatus or None if not found
        """
        if exchange in self.feeds:
            return self.feeds[exchange].get_status()
        return None
    
    def get_all_statuses(self) -> Dict[str, FeedStatus]:
        """
        Get status of all feeds.
        
        Returns:
            Dict mapping exchange to status
        """
        return {
            exchange: feed.get_status()
            for exchange, feed in self.feeds.items()
        }
