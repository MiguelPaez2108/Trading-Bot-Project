"""
Candle Repository Implementation.

Handles OHLCV candle data persistence in TimescaleDB.
"""
from typing import List, Optional
from datetime import datetime, timedelta
from decimal import Decimal
import logging

from src.python.infrastructure.database.timescale_client import TimescaleClient
from src.python.domain.entities.candle import Candle
from src.python.domain.value_objects.symbol import TradingPair

logger = logging.getLogger(__name__)


class CandleRepositoryImpl:
    """
    Candle repository implementation using TimescaleDB.
    
    Provides high-performance time-series data storage and retrieval.
    """
    
    def __init__(self, client: TimescaleClient):
        """
        Initialize repository.
        
        Args:
            client: TimescaleDB client instance
        """
        self.client = client
    
    async def save(self, candle: Candle) -> None:
        """
        Save single candle.
        
        Args:
            candle: Candle entity to save
        """
        query = """
            INSERT INTO candles (
                time, symbol, timeframe, open, high, low, close,
                volume, quote_volume, trades_count
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
            ON CONFLICT (time, symbol, timeframe) DO UPDATE SET
                open = EXCLUDED.open,
                high = EXCLUDED.high,
                low = EXCLUDED.low,
                close = EXCLUDED.close,
                volume = EXCLUDED.volume,
                quote_volume = EXCLUDED.quote_volume,
                trades_count = EXCLUDED.trades_count
        """
        
        await self.client.execute(
            query,
            candle.time,
            str(candle.symbol),
            candle.timeframe,
            candle.open,
            candle.high,
            candle.low,
            candle.close,
            candle.volume,
            candle.quote_volume,
            candle.trades_count
        )
    
    async def save_many(self, candles: List[Candle]) -> None:
        """
        Save multiple candles efficiently using COPY.
        
        Args:
            candles: List of candle entities
        """
        if not candles:
            return
        
        records = [
            (
                c.time,
                str(c.symbol),
                c.timeframe,
                c.open,
                c.high,
                c.low,
                c.close,
                c.volume,
                c.quote_volume,
                c.trades_count
            )
            for c in candles
        ]
        
        columns = [
            'time', 'symbol', 'timeframe', 'open', 'high', 'low', 'close',
            'volume', 'quote_volume', 'trades_count'
        ]
        
        await self.client.copy_records_to_table(
            'candles',
            records=records,
            columns=columns
        )
        
        logger.info(f"Saved {len(candles)} candles to database")
    
    async def get_latest(
        self,
        symbol: TradingPair,
        timeframe: str,
        limit: int = 100
    ) -> List[Candle]:
        """
        Get latest candles for symbol.
        
        Args:
            symbol: Trading pair
            timeframe: Timeframe (1m, 5m, 1h, etc.)
            limit: Number of candles to retrieve
        
        Returns:
            List of candles ordered by time descending
        """
        query = """
            SELECT time, symbol, timeframe, open, high, low, close,
                   volume, quote_volume, trades_count
            FROM candles
            WHERE symbol = $1 AND timeframe = $2
            ORDER BY time DESC
            LIMIT $3
        """
        
        rows = await self.client.fetch(query, str(symbol), timeframe, limit)
        
        return [self._row_to_candle(row) for row in rows]
    
    async def get_range(
        self,
        symbol: TradingPair,
        timeframe: str,
        start_time: datetime,
        end_time: datetime
    ) -> List[Candle]:
        """
        Get candles in time range.
        
        Args:
            symbol: Trading pair
            timeframe: Timeframe
            start_time: Start of range (inclusive)
            end_time: End of range (inclusive)
        
        Returns:
            List of candles ordered by time ascending
        """
        query = """
            SELECT time, symbol, timeframe, open, high, low, close,
                   volume, quote_volume, trades_count
            FROM candles
            WHERE symbol = $1 
              AND timeframe = $2
              AND time >= $3 
              AND time <= $4
            ORDER BY time ASC
        """
        
        rows = await self.client.fetch(
            query,
            str(symbol),
            timeframe,
            start_time,
            end_time
        )
        
        return [self._row_to_candle(row) for row in rows]
    
    async def get_last_candle(
        self,
        symbol: TradingPair,
        timeframe: str
    ) -> Optional[Candle]:
        """
        Get most recent candle.
        
        Args:
            symbol: Trading pair
            timeframe: Timeframe
        
        Returns:
            Latest candle or None if not found
        """
        query = """
            SELECT time, symbol, timeframe, open, high, low, close,
                   volume, quote_volume, trades_count
            FROM candles
            WHERE symbol = $1 AND timeframe = $2
            ORDER BY time DESC
            LIMIT 1
        """
        
        row = await self.client.fetchrow(query, str(symbol), timeframe)
        
        if row is None:
            return None
        
        return self._row_to_candle(row)
    
    async def count(
        self,
        symbol: TradingPair,
        timeframe: str,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> int:
        """
        Count candles.
        
        Args:
            symbol: Trading pair
            timeframe: Timeframe
            start_time: Optional start time
            end_time: Optional end time
        
        Returns:
            Number of candles
        """
        if start_time and end_time:
            query = """
                SELECT COUNT(*) FROM candles
                WHERE symbol = $1 AND timeframe = $2
                  AND time >= $3 AND time <= $4
            """
            return await self.client.fetchval(
                query, str(symbol), timeframe, start_time, end_time
            )
        else:
            query = """
                SELECT COUNT(*) FROM candles
                WHERE symbol = $1 AND timeframe = $2
            """
            return await self.client.fetchval(query, str(symbol), timeframe)
    
    async def delete_old(
        self,
        symbol: TradingPair,
        timeframe: str,
        older_than: datetime
    ) -> int:
        """
        Delete candles older than specified time.
        
        Args:
            symbol: Trading pair
            timeframe: Timeframe
            older_than: Delete candles before this time
        
        Returns:
            Number of deleted candles
        """
        query = """
            DELETE FROM candles
            WHERE symbol = $1 
              AND timeframe = $2
              AND time < $3
        """
        
        result = await self.client.execute(
            query,
            str(symbol),
            timeframe,
            older_than
        )
        
        # Extract count from result string "DELETE N"
        count = int(result.split()[-1]) if result else 0
        logger.info(f"Deleted {count} old candles for {symbol} {timeframe}")
        
        return count
    
    def _row_to_candle(self, row) -> Candle:
        """
        Convert database row to Candle entity.
        
        Args:
            row: Database row
        
        Returns:
            Candle entity
        """
        return Candle(
            time=row['time'],
            symbol=TradingPair.from_string(row['symbol']),
            timeframe=row['timeframe'],
            open=Decimal(str(row['open'])),
            high=Decimal(str(row['high'])),
            low=Decimal(str(row['low'])),
            close=Decimal(str(row['close'])),
            volume=Decimal(str(row['volume'])),
            quote_volume=Decimal(str(row['quote_volume'])) if row['quote_volume'] else None,
            trades_count=row['trades_count']
        )
