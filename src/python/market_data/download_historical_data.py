"""
Historical Data Downloader.

Downloads historical candle data from exchanges.
"""
import asyncio
from typing import List, Optional
from datetime import datetime, timedelta
from decimal import Decimal
import logging

from src.python.infrastructure.exchanges.binance_adapter import BinanceAdapter
from src.python.domain.entities.candle import Candle
from src.python.domain.value_objects.symbol import TradingPair
from src.python.market_data.processors.normalizer import MarketDataNormalizer
from src.python.market_data.processors.validator import MarketDataValidator
from src.python.infrastructure.database.repositories.candle_repository_impl import CandleRepositoryImpl
from src.python.infrastructure.database.timescale_client import get_timescale_client

logger = logging.getLogger(__name__)


class HistoricalDataDownloader:
    """
    Downloads historical candle data from exchanges.
    
    Features:
    - Resume capability
    - Progress tracking
    - Data validation
    - Batch storage
    """
    
    def __init__(
        self,
        exchange: BinanceAdapter,
        normalizer: MarketDataNormalizer,
        validator: MarketDataValidator,
        repository: CandleRepositoryImpl
    ):
        """
        Initialize downloader.
        
        Args:
            exchange: Exchange adapter
            normalizer: Data normalizer
            validator: Data validator
            repository: Candle repository
        """
        self.exchange = exchange
        self.normalizer = normalizer
        self.validator = validator
        self.repository = repository
    
    async def download(
        self,
        symbol: TradingPair,
        timeframe: str,
        start_date: datetime,
        end_date: datetime,
        batch_size: int = 1000
    ) -> int:
        """
        Download historical candles.
        
        Args:
            symbol: Trading pair
            timeframe: Timeframe (1m, 5m, 1h, etc.)
            start_date: Start date
            end_date: End date
            batch_size: Candles per request
        
        Returns:
            Number of candles downloaded
        """
        logger.info(
            f"Downloading {symbol} {timeframe} from {start_date} to {end_date}"
        )
        
        total_downloaded = 0
        current_date = start_date
        
        while current_date < end_date:
            try:
                # Calculate batch end date
                batch_end = min(
                    current_date + self._get_batch_duration(timeframe, batch_size),
                    end_date
                )
                
                # Fetch candles
                candles = await self._fetch_candles(
                    symbol,
                    timeframe,
                    current_date,
                    batch_end,
                    batch_size
                )
                
                if not candles:
                    logger.warning(f"No candles returned for {current_date} to {batch_end}")
                    break
                
                # Validate and save
                valid_candles = self._validate_candles(candles)
                
                if valid_candles:
                    await self.repository.save_many(valid_candles)
                    total_downloaded += len(valid_candles)
                    
                    logger.info(
                        f"Downloaded {len(valid_candles)} candles "
                        f"(total: {total_downloaded})"
                    )
                
                # Move to next batch
                current_date = candles[-1].time + timedelta(seconds=1)
                
                # Rate limiting
                await asyncio.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Error downloading batch: {e}")
                # Continue with next batch
                current_date += self._get_batch_duration(timeframe, batch_size)
        
        logger.info(f"Download complete: {total_downloaded} candles")
        return total_downloaded
    
    async def _fetch_candles(
        self,
        symbol: TradingPair,
        timeframe: str,
        start_date: datetime,
        end_date: datetime,
        limit: int
    ) -> List[Candle]:
        """
        Fetch candles from exchange.
        
        Args:
            symbol: Trading pair
            timeframe: Timeframe
            start_date: Start date
            end_date: End date
            limit: Max candles
        
        Returns:
            List of candles
        """
        # Convert to milliseconds timestamp
        since = int(start_date.timestamp() * 1000)
        
        # Fetch from exchange (CCXT format)
        symbol_str = f"{symbol.base}/{symbol.quote}"
        raw_candles = await self.exchange.exchange.fetch_ohlcv(
            symbol_str,
            timeframe=timeframe,
            since=since,
            limit=limit
        )
        
        # Normalize to domain entities
        candles = []
        for raw_candle in raw_candles:
            candle = self.normalizer.normalize_candle(
                raw_candle,
                symbol,
                timeframe,
                source="ccxt"
            )
            candles.append(candle)
        
        return candles
    
    def _validate_candles(self, candles: List[Candle]) -> List[Candle]:
        """
        Validate candles.
        
        Args:
            candles: List of candles
        
        Returns:
            List of valid candles
        """
        valid_candles = []
        previous_candle = None
        
        for candle in candles:
            is_valid, error = self.validator.validate_candle(candle, previous_candle)
            
            if is_valid:
                valid_candles.append(candle)
                previous_candle = candle
            else:
                logger.warning(f"Invalid candle at {candle.time}: {error}")
        
        return valid_candles
    
    def _get_batch_duration(self, timeframe: str, batch_size: int) -> timedelta:
        """
        Calculate batch duration.
        
        Args:
            timeframe: Timeframe
            batch_size: Number of candles
        
        Returns:
            Duration of batch
        """
        # Parse timeframe
        timeframe_map = {
            '1m': timedelta(minutes=1),
            '3m': timedelta(minutes=3),
            '5m': timedelta(minutes=5),
            '15m': timedelta(minutes=15),
            '30m': timedelta(minutes=30),
            '1h': timedelta(hours=1),
            '2h': timedelta(hours=2),
            '4h': timedelta(hours=4),
            '6h': timedelta(hours=6),
            '8h': timedelta(hours=8),
            '12h': timedelta(hours=12),
            '1d': timedelta(days=1),
            '3d': timedelta(days=3),
            '1w': timedelta(weeks=1),
        }
        
        interval = timeframe_map.get(timeframe, timedelta(hours=1))
        return interval * batch_size


async def download_historical_data(
    symbol: str,
    timeframe: str,
    start_date: str,
    end_date: str,
    testnet: bool = True
) -> int:
    """
    Convenience function to download historical data.
    
    Args:
        symbol: Symbol (e.g., 'BTC/USDT')
        timeframe: Timeframe (e.g., '1h')
        start_date: Start date (ISO format)
        end_date: End date (ISO format)
        testnet: Use testnet
    
    Returns:
        Number of candles downloaded
    """
    # Parse symbol
    base, quote = symbol.split('/')
    trading_pair = TradingPair(base=base, quote=quote)
    
    # Parse dates
    start = datetime.fromisoformat(start_date)
    end = datetime.fromisoformat(end_date)
    
    # Initialize components
    exchange = BinanceAdapter(testnet=testnet)
    await exchange.connect()
    
    normalizer = MarketDataNormalizer()
    validator = MarketDataValidator()
    
    db_client = await get_timescale_client()
    repository = CandleRepositoryImpl(db_client)
    
    downloader = HistoricalDataDownloader(
        exchange,
        normalizer,
        validator,
        repository
    )
    
    try:
        # Download
        count = await downloader.download(
            trading_pair,
            timeframe,
            start,
            end
        )
        
        return count
        
    finally:
        await exchange.disconnect()


# CLI usage example
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 5:
        print("Usage: python -m src.python.market_data.download_historical_data <symbol> <timeframe> <start_date> <end_date>")
        print("Example: python -m src.python.market_data.download_historical_data BTC/USDT 1h 2024-01-01 2024-12-01")
        sys.exit(1)
    
    symbol = sys.argv[1]
    timeframe = sys.argv[2]
    start_date = sys.argv[3]
    end_date = sys.argv[4]
    
    count = asyncio.run(download_historical_data(symbol, timeframe, start_date, end_date))
    print(f"Downloaded {count} candles")
