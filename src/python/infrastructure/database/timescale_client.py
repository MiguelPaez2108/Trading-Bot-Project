"""
TimescaleDB client with connection pooling.

Provides async database access using asyncpg.
"""
import asyncpg
from typing import Optional, List, Dict, Any
from contextlib import asynccontextmanager
import logging
from decimal import Decimal
from datetime import datetime

from src.python.infrastructure.config.settings import get_settings

logger = logging.getLogger(__name__)


class TimescaleClient:
    """
    TimescaleDB client with connection pooling.
    
    Features:
    - Async connection pooling
    - Automatic reconnection
    - Query timeout handling
    - Prepared statements
    """
    
    def __init__(self):
        """Initialize TimescaleDB client."""
        self.settings = get_settings().database
        self.pool: Optional[asyncpg.Pool] = None
        
    async def connect(self) -> None:
        """
        Create connection pool.
        
        Raises:
            Exception: If connection fails
        """
        try:
            self.pool = await asyncpg.create_pool(
                host=self.settings.host,
                port=self.settings.port,
                database=self.settings.name,
                user=self.settings.user,
                password=self.settings.password,
                min_size=5,
                max_size=self.settings.pool_size,
                max_inactive_connection_lifetime=300,
                command_timeout=self.settings.pool_timeout,
            )
            logger.info(
                f"Connected to TimescaleDB at {self.settings.host}:{self.settings.port}"
            )
        except Exception as e:
            logger.error(f"Failed to connect to TimescaleDB: {e}")
            raise
    
    async def disconnect(self) -> None:
        """Close connection pool."""
        if self.pool:
            await self.pool.close()
            logger.info("Disconnected from TimescaleDB")
    
    @asynccontextmanager
    async def acquire(self):
        """
        Acquire connection from pool.
        
        Usage:
            async with client.acquire() as conn:
                result = await conn.fetch("SELECT * FROM candles")
        
        Yields:
            asyncpg.Connection
        """
        if not self.pool:
            raise RuntimeError("Database pool not initialized. Call connect() first.")
        
        async with self.pool.acquire() as connection:
            yield connection
    
    async def execute(
        self,
        query: str,
        *args,
        timeout: Optional[float] = None
    ) -> str:
        """
        Execute a query without returning results.
        
        Args:
            query: SQL query
            *args: Query parameters
            timeout: Query timeout in seconds
        
        Returns:
            Status message from database
        """
        async with self.acquire() as conn:
            return await conn.execute(query, *args, timeout=timeout)
    
    async def fetch(
        self,
        query: str,
        *args,
        timeout: Optional[float] = None
    ) -> List[asyncpg.Record]:
        """
        Fetch multiple rows.
        
        Args:
            query: SQL query
            *args: Query parameters
            timeout: Query timeout in seconds
        
        Returns:
            List of records
        """
        async with self.acquire() as conn:
            return await conn.fetch(query, *args, timeout=timeout)
    
    async def fetchrow(
        self,
        query: str,
        *args,
        timeout: Optional[float] = None
    ) -> Optional[asyncpg.Record]:
        """
        Fetch single row.
        
        Args:
            query: SQL query
            *args: Query parameters
            timeout: Query timeout in seconds
        
        Returns:
            Single record or None
        """
        async with self.acquire() as conn:
            return await conn.fetchrow(query, *args, timeout=timeout)
    
    async def fetchval(
        self,
        query: str,
        *args,
        column: int = 0,
        timeout: Optional[float] = None
    ) -> Any:
        """
        Fetch single value.
        
        Args:
            query: SQL query
            *args: Query parameters
            column: Column index to return
            timeout: Query timeout in seconds
        
        Returns:
            Single value
        """
        async with self.acquire() as conn:
            return await conn.fetchval(query, *args, column=column, timeout=timeout)
    
    async def executemany(
        self,
        query: str,
        args: List[tuple],
        timeout: Optional[float] = None
    ) -> None:
        """
        Execute query multiple times with different parameters.
        
        Useful for batch inserts.
        
        Args:
            query: SQL query
            args: List of parameter tuples
            timeout: Query timeout in seconds
        """
        async with self.acquire() as conn:
            await conn.executemany(query, args, timeout=timeout)
    
    async def copy_records_to_table(
        self,
        table_name: str,
        records: List[tuple],
        columns: List[str],
        timeout: Optional[float] = None
    ) -> str:
        """
        Efficiently copy records to table using COPY.
        
        Much faster than INSERT for bulk operations.
        
        Args:
            table_name: Target table name
            records: List of record tuples
            columns: Column names
            timeout: Query timeout in seconds
        
        Returns:
            Status message
        """
        async with self.acquire() as conn:
            return await conn.copy_records_to_table(
                table_name,
                records=records,
                columns=columns,
                timeout=timeout
            )
    
    async def transaction(self):
        """
        Create transaction context.
        
        Usage:
            async with client.transaction():
                await client.execute("INSERT ...")
                await client.execute("UPDATE ...")
        """
        async with self.acquire() as conn:
            async with conn.transaction():
                yield conn
    
    async def health_check(self) -> bool:
        """
        Check database health.
        
        Returns:
            True if healthy, False otherwise
        """
        try:
            result = await self.fetchval("SELECT 1")
            return result == 1
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False


# Global client instance
_timescale_client: Optional[TimescaleClient] = None


async def get_timescale_client() -> TimescaleClient:
    """
    Get global TimescaleDB client instance.
    
    Returns:
        TimescaleClient instance
    """
    global _timescale_client
    
    if _timescale_client is None:
        _timescale_client = TimescaleClient()
        await _timescale_client.connect()
    
    return _timescale_client


async def close_timescale_client() -> None:
    """Close global TimescaleDB client."""
    global _timescale_client
    
    if _timescale_client is not None:
        await _timescale_client.disconnect()
        _timescale_client = None
