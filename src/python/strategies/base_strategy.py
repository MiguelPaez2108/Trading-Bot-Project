"""
Strategy Base Class - Abstract interface for trading strategies.

All strategies must inherit from this class.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from decimal import Decimal
from datetime import datetime

from src.python.domain.entities.candle import Candle
from src.python.domain.entities.signal import Signal
from src.python.domain.value_objects.symbol import TradingPair


class BaseStrategy(ABC):
    """
    Abstract base class for trading strategies.
    
    All strategies must implement:
    - on_candle: Process new candle data
    - generate_signals: Generate trading signals
    """
    
    def __init__(
        self,
        name: str,
        symbol: TradingPair,
        timeframe: str,
        parameters: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize strategy.
        
        Args:
            name: Strategy name
            symbol: Trading pair
            timeframe: Timeframe (1m, 5m, 1h, etc.)
            parameters: Strategy parameters
        """
        self.name = name
        self.symbol = symbol
        self.timeframe = timeframe
        self.parameters = parameters or {}
        
        # State
        self.is_initialized = False
        self.candles: List[Candle] = []
        self.signals: List[Signal] = []
        
        # Performance tracking
        self.total_signals = 0
        self.winning_signals = 0
        self.losing_signals = 0
    
    @abstractmethod
    def on_candle(self, candle: Candle) -> Optional[Signal]:
        """
        Process new candle and potentially generate signal.
        
        Args:
            candle: New candle data
        
        Returns:
            Signal if generated, None otherwise
        """
        pass
    
    @abstractmethod
    def initialize(self, historical_candles: List[Candle]) -> None:
        """
        Initialize strategy with historical data.
        
        Args:
            historical_candles: Historical candle data
        """
        pass
    
    def add_candle(self, candle: Candle) -> None:
        """
        Add candle to internal buffer.
        
        Args:
            candle: Candle to add
        """
        self.candles.append(candle)
        
        # Keep only last N candles (memory management)
        max_candles = self.parameters.get('max_candles', 1000)
        if len(self.candles) > max_candles:
            self.candles = self.candles[-max_candles:]
    
    def get_candles(self, lookback: int = 100) -> List[Candle]:
        """
        Get recent candles.
        
        Args:
            lookback: Number of candles to return
        
        Returns:
            List of recent candles
        """
        return self.candles[-lookback:]
    
    def reset(self) -> None:
        """Reset strategy state."""
        self.candles = []
        self.signals = []
        self.total_signals = 0
        self.winning_signals = 0
        self.losing_signals = 0
        self.is_initialized = False
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """
        Get strategy performance statistics.
        
        Returns:
            Dict with performance metrics
        """
        win_rate = (
            (self.winning_signals / self.total_signals * 100)
            if self.total_signals > 0
            else 0
        )
        
        return {
            'name': self.name,
            'symbol': str(self.symbol),
            'timeframe': self.timeframe,
            'total_signals': self.total_signals,
            'winning_signals': self.winning_signals,
            'losing_signals': self.losing_signals,
            'win_rate': win_rate,
            'parameters': self.parameters
        }
    
    def __str__(self) -> str:
        """String representation."""
        return (
            f"{self.name}({self.symbol} {self.timeframe}, "
            f"signals={self.total_signals}, win_rate={self.get_performance_stats()['win_rate']:.1f}%)"
        )
    
    def __repr__(self) -> str:
        """Detailed representation."""
        return self.__str__()
