"""
Token Bucket Rate Limiter.

Prevents exceeding exchange API rate limits.
"""
import time
import asyncio
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class TokenBucketRateLimiter:
    """
    Token bucket algorithm for rate limiting.
    
    Allows bursts while maintaining average rate.
    
    Example:
        limiter = TokenBucketRateLimiter(rate=10, capacity=20)
        
        async with limiter:
            # Make API call
            result = await exchange.get_ticker(symbol)
    """
    
    def __init__(
        self,
        rate: float,
        capacity: Optional[float] = None,
        initial_tokens: Optional[float] = None
    ):
        """
        Initialize rate limiter.
        
        Args:
            rate: Tokens per second
            capacity: Max tokens (default: rate * 2)
            initial_tokens: Starting tokens (default: capacity)
        """
        self.rate = rate
        self.capacity = capacity or (rate * 2)
        self.tokens = initial_tokens if initial_tokens is not None else self.capacity
        self.last_update = time.monotonic()
        self.lock = asyncio.Lock()
    
    async def acquire(self, tokens: float = 1.0) -> None:
        """
        Acquire tokens (wait if not available).
        
        Args:
            tokens: Number of tokens to acquire
        """
        async with self.lock:
            while True:
                now = time.monotonic()
                elapsed = now - self.last_update
                
                # Add tokens based on elapsed time
                self.tokens = min(
                    self.capacity,
                    self.tokens + elapsed * self.rate
                )
                self.last_update = now
                
                if self.tokens >= tokens:
                    self.tokens -= tokens
                    return
                
                # Calculate wait time
                deficit = tokens - self.tokens
                wait_time = deficit / self.rate
                
                logger.debug(f"Rate limit: waiting {wait_time:.2f}s")
                await asyncio.sleep(wait_time)
    
    async def try_acquire(self, tokens: float = 1.0) -> bool:
        """
        Try to acquire tokens without waiting.
        
        Args:
            tokens: Number of tokens to acquire
        
        Returns:
            True if acquired, False if not enough tokens
        """
        async with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_update
            
            # Add tokens based on elapsed time
            self.tokens = min(
                self.capacity,
                self.tokens + elapsed * self.rate
            )
            self.last_update = now
            
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            
            return False
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self.acquire()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        pass
    
    def get_available_tokens(self) -> float:
        """
        Get current available tokens.
        
        Returns:
            Number of available tokens
        """
        now = time.monotonic()
        elapsed = now - self.last_update
        return min(self.capacity, self.tokens + elapsed * self.rate)


class MultiRateLimiter:
    """
    Multiple rate limiters for different endpoints.
    
    Example:
        limiter = MultiRateLimiter({
            'orders': TokenBucketRateLimiter(rate=10),
            'market_data': TokenBucketRateLimiter(rate=100),
        })
        
        async with limiter.get('orders'):
            await exchange.place_order(...)
    """
    
    def __init__(self, limiters: dict[str, TokenBucketRateLimiter]):
        """
        Initialize multi-rate limiter.
        
        Args:
            limiters: Dict of {endpoint_name: rate_limiter}
        """
        self.limiters = limiters
    
    def get(self, endpoint: str) -> TokenBucketRateLimiter:
        """
        Get rate limiter for endpoint.
        
        Args:
            endpoint: Endpoint name
        
        Returns:
            Rate limiter instance
        
        Raises:
            KeyError: If endpoint not found
        """
        return self.limiters[endpoint]
    
    async def acquire(self, endpoint: str, tokens: float = 1.0) -> None:
        """
        Acquire tokens for endpoint.
        
        Args:
            endpoint: Endpoint name
            tokens: Number of tokens
        """
        await self.limiters[endpoint].acquire(tokens)
