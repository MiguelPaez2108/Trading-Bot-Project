"""
Simple Moving Average Crossover Strategy.

Classic trend-following strategy using two SMAs.
"""
from typing import List, Optional
from decimal import Decimal
import logging

from src.python.strategies.base_strategy import BaseStrategy
from src.python.domain.entities.candle import Candle
from src.python.domain.entities.signal import Signal, SignalType, SignalStrength
from src.python.domain.value_objects.symbol import TradingPair

logger = logging.getLogger(__name__)


class SMAStrategy(BaseStrategy):
    """
    Simple Moving Average Crossover Strategy.
    
    Generates BUY signal when fast SMA crosses above slow SMA.
    Generates SELL signal when fast SMA crosses below slow SMA.
    
    Parameters:
        - fast_period: Fast SMA period (default: 20)
        - slow_period: Slow SMA period (default: 50)
        - stop_loss_pct: Stop loss percentage (default: 0.02 = 2%)
        - take_profit_pct: Take profit percentage (default: 0.04 = 4%)
    """
    
    def __init__(
        self,
        symbol: TradingPair,
        timeframe: str = "1h",
        fast_period: int = 20,
        slow_period: int = 50,
        stop_loss_pct: float = 0.02,
        take_profit_pct: float = 0.04
    ):
        """Initialize SMA strategy."""
        parameters = {
            'fast_period': fast_period,
            'slow_period': slow_period,
            'stop_loss_pct': stop_loss_pct,
            'take_profit_pct': take_profit_pct
        }
        
        super().__init__(
            name="SMA Crossover",
            symbol=symbol,
            timeframe=timeframe,
            parameters=parameters
        )
        
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.stop_loss_pct = Decimal(str(stop_loss_pct))
        self.take_profit_pct = Decimal(str(take_profit_pct))
        
        # State
        self.last_signal_type: Optional[SignalType] = None
    
    def initialize(self, historical_candles: List[Candle]) -> None:
        """
        Initialize with historical data.
        
        Args:
            historical_candles: Historical candles
        """
        self.candles = historical_candles
        self.is_initialized = True
        logger.info(f"Initialized {self.name} with {len(historical_candles)} candles")
    
    def on_candle(self, candle: Candle) -> Optional[Signal]:
        """
        Process new candle and generate signal if crossover detected.
        
        Args:
            candle: New candle
        
        Returns:
            Signal if generated, None otherwise
        """
        # Add candle to buffer
        self.add_candle(candle)
        
        # Need enough candles for slow SMA
        if len(self.candles) < self.slow_period:
            return None
        
        # Calculate SMAs
        fast_sma = self._calculate_sma(self.fast_period)
        slow_sma = self._calculate_sma(self.slow_period)
        
        # Previous SMAs (for crossover detection)
        if len(self.candles) < self.slow_period + 1:
            return None
        
        prev_fast_sma = self._calculate_sma(self.fast_period, offset=1)
        prev_slow_sma = self._calculate_sma(self.slow_period, offset=1)
        
        # Detect crossover
        signal = None
        
        # Bullish crossover: fast crosses above slow
        if prev_fast_sma <= prev_slow_sma and fast_sma > slow_sma:
            if self.last_signal_type != SignalType.BUY:
                signal = self._create_buy_signal(candle, fast_sma, slow_sma)
                self.last_signal_type = SignalType.BUY
        
        # Bearish crossover: fast crosses below slow
        elif prev_fast_sma >= prev_slow_sma and fast_sma < slow_sma:
            if self.last_signal_type != SignalType.SELL:
                signal = self._create_sell_signal(candle, fast_sma, slow_sma)
                self.last_signal_type = SignalType.SELL
        
        if signal:
            self.signals.append(signal)
            self.total_signals += 1
            logger.info(f"Generated signal: {signal}")
        
        return signal
    
    def _calculate_sma(self, period: int, offset: int = 0) -> Decimal:
        """
        Calculate Simple Moving Average.
        
        Args:
            period: SMA period
            offset: Offset from end (0 = most recent)
        
        Returns:
            SMA value
        """
        end_idx = len(self.candles) - offset
        start_idx = end_idx - period
        
        if start_idx < 0:
            return Decimal('0')
        
        candles_slice = self.candles[start_idx:end_idx]
        prices = [c.close for c in candles_slice]
        
        return sum(prices) / Decimal(str(len(prices)))
    
    def _create_buy_signal(
        self,
        candle: Candle,
        fast_sma: Decimal,
        slow_sma: Decimal
    ) -> Signal:
        """Create BUY signal."""
        price = candle.close
        stop_loss = price * (Decimal('1') - self.stop_loss_pct)
        target_price = price * (Decimal('1') + self.take_profit_pct)
        
        # Calculate confidence based on SMA separation
        sma_diff_pct = (fast_sma - slow_sma) / slow_sma
        confidence = min(Decimal('0.5') + sma_diff_pct * Decimal('10'), Decimal('1.0'))
        
        return Signal(
            symbol=self.symbol,
            signal_type=SignalType.BUY,
            strength=self._get_strength(confidence),
            price=price,
            target_price=target_price,
            stop_loss=stop_loss,
            strategy_name=self.name,
            timeframe=self.timeframe,
            confidence=confidence,
            indicators={
                'fast_sma': float(fast_sma),
                'slow_sma': float(slow_sma),
                'sma_diff_pct': float(sma_diff_pct)
            }
        )
    
    def _create_sell_signal(
        self,
        candle: Candle,
        fast_sma: Decimal,
        slow_sma: Decimal
    ) -> Signal:
        """Create SELL signal."""
        price = candle.close
        stop_loss = price * (Decimal('1') + self.stop_loss_pct)
        target_price = price * (Decimal('1') - self.take_profit_pct)
        
        # Calculate confidence
        sma_diff_pct = (slow_sma - fast_sma) / slow_sma
        confidence = min(Decimal('0.5') + sma_diff_pct * Decimal('10'), Decimal('1.0'))
        
        return Signal(
            symbol=self.symbol,
            signal_type=SignalType.SELL,
            strength=self._get_strength(confidence),
            price=price,
            target_price=target_price,
            stop_loss=stop_loss,
            strategy_name=self.name,
            timeframe=self.timeframe,
            confidence=confidence,
            indicators={
                'fast_sma': float(fast_sma),
                'slow_sma': float(slow_sma),
                'sma_diff_pct': float(sma_diff_pct)
            }
        )
    
    def _get_strength(self, confidence: Decimal) -> SignalStrength:
        """Convert confidence to signal strength."""
        if confidence >= Decimal('0.75'):
            return SignalStrength.STRONG
        elif confidence >= Decimal('0.5'):
            return SignalStrength.MEDIUM
        else:
            return SignalStrength.WEAK
