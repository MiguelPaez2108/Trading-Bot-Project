"""
Market Data Validator.

Validates market data quality and detects anomalies.
"""
from typing import Optional
from decimal import Decimal
import logging

from src.python.domain.entities.candle import Candle

logger = logging.getLogger(__name__)


class MarketDataValidator:
    """
    Validates market data quality.
    
    Checks for:
    - OHLC relationships
    - Price anomalies
    - Volume anomalies
    - Missing data
    """
    
    def __init__(
        self,
        max_price_change_pct: Decimal = Decimal('0.20'),  # 20%
        min_volume: Decimal = Decimal('0.0001')
    ):
        """
        Initialize validator.
        
        Args:
            max_price_change_pct: Max allowed price change between candles
            min_volume: Minimum volume threshold
        """
        self.max_price_change_pct = max_price_change_pct
        self.min_volume = min_volume
    
    def validate_candle(
        self,
        candle: Candle,
        previous_candle: Optional[Candle] = None
    ) -> tuple[bool, Optional[str]]:
        """
        Validate candle data.
        
        Args:
            candle: Candle to validate
            previous_candle: Previous candle for comparison
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check OHLC relationships
        if not self._validate_ohlc(candle):
            return False, "Invalid OHLC relationships"
        
        # Check for zero/negative values
        if not self._validate_positive_values(candle):
            return False, "Zero or negative values found"
        
        # Check volume
        if candle.volume < self.min_volume:
            return False, f"Volume too low: {candle.volume}"
        
        # Check price change if previous candle available
        if previous_candle:
            if not self._validate_price_change(candle, previous_candle):
                return False, "Excessive price change detected"
        
        return True, None
    
    def _validate_ohlc(self, candle: Candle) -> bool:
        """
        Validate OHLC relationships.
        
        Rules:
        - high >= low
        - high >= open
        - high >= close
        - low <= open
        - low <= close
        """
        if candle.high < candle.low:
            logger.warning(f"High < Low: {candle.high} < {candle.low}")
            return False
        
        if candle.high < candle.open:
            logger.warning(f"High < Open: {candle.high} < {candle.open}")
            return False
        
        if candle.high < candle.close:
            logger.warning(f"High < Close: {candle.high} < {candle.close}")
            return False
        
        if candle.low > candle.open:
            logger.warning(f"Low > Open: {candle.low} > {candle.open}")
            return False
        
        if candle.low > candle.close:
            logger.warning(f"Low > Close: {candle.low} > {candle.close}")
            return False
        
        return True
    
    def _validate_positive_values(self, candle: Candle) -> bool:
        """Check all values are positive."""
        if candle.open <= 0:
            logger.warning(f"Open <= 0: {candle.open}")
            return False
        
        if candle.high <= 0:
            logger.warning(f"High <= 0: {candle.high}")
            return False
        
        if candle.low <= 0:
            logger.warning(f"Low <= 0: {candle.low}")
            return False
        
        if candle.close <= 0:
            logger.warning(f"Close <= 0: {candle.close}")
            return False
        
        if candle.volume < 0:
            logger.warning(f"Volume < 0: {candle.volume}")
            return False
        
        return True
    
    def _validate_price_change(
        self,
        candle: Candle,
        previous_candle: Candle
    ) -> bool:
        """
        Validate price change between candles.
        
        Detects flash crashes and data errors.
        """
        # Calculate price change
        price_change = abs(candle.close - previous_candle.close) / previous_candle.close
        
        if price_change > self.max_price_change_pct:
            logger.warning(
                f"Excessive price change: {price_change:.2%} "
                f"(from {previous_candle.close} to {candle.close})"
            )
            return False
        
        return True
    
    def detect_gap(
        self,
        candle: Candle,
        previous_candle: Candle,
        gap_threshold_pct: Decimal = Decimal('0.01')  # 1%
    ) -> bool:
        """
        Detect price gap between candles.
        
        Args:
            candle: Current candle
            previous_candle: Previous candle
            gap_threshold_pct: Gap threshold percentage
        
        Returns:
            True if gap detected
        """
        # Gap up: current low > previous high
        if candle.low > previous_candle.high:
            gap_size = (candle.low - previous_candle.high) / previous_candle.high
            if gap_size > gap_threshold_pct:
                logger.info(f"Gap up detected: {gap_size:.2%}")
                return True
        
        # Gap down: current high < previous low
        if candle.high < previous_candle.low:
            gap_size = (previous_candle.low - candle.high) / previous_candle.low
            if gap_size > gap_threshold_pct:
                logger.info(f"Gap down detected: {gap_size:.2%}")
                return True
        
        return False
