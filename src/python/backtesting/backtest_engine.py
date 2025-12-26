"""
Backtest Engine - Event-driven backtesting orchestrator.

Coordinates strategy execution, order management, and performance tracking.
"""
from typing import List, Dict, Optional
from decimal import Decimal
from datetime import datetime
import logging

from src.python.strategies.base_strategy import BaseStrategy
from src.python.backtesting.simulated_exchange import SimulatedExchange
from src.python.backtesting.portfolio_manager import PortfolioManager
from src.python.domain.entities.candle import Candle
from src.python.domain.entities.order import Order, OrderSide, OrderType
from src.python.domain.entities.signal import Signal, SignalType
from src.python.domain.value_objects.symbol import TradingPair

logger = logging.getLogger(__name__)


class BacktestEngine:
    """
    Event-driven backtest engine.
    
    Orchestrates:
    - Historical data replay
    - Strategy execution
    - Order management
    - Portfolio tracking
    - Performance calculation
    """
    
    def __init__(
        self,
        strategy: BaseStrategy,
        initial_capital: Decimal = Decimal('10000'),
        maker_fee: Decimal = Decimal('0.001'),
        taker_fee: Decimal = Decimal('0.001'),
        slippage_pct: Decimal = Decimal('0.0005')
    ):
        """
        Initialize backtest engine.
        
        Args:
            strategy: Trading strategy to backtest
            initial_capital: Starting capital
            maker_fee: Maker fee percentage
            taker_fee: Taker fee percentage
            slippage_pct: Slippage percentage
        """
        self.strategy = strategy
        self.initial_capital = initial_capital
        
        # Components
        self.exchange = SimulatedExchange(maker_fee, taker_fee, slippage_pct)
        self.portfolio = PortfolioManager(initial_capital)
        
        # State
        self.current_time: Optional[datetime] = None
        self.candles_processed = 0
    
    def run(
        self,
        candles: List[Candle],
        warmup_period: int = 100
    ) -> Dict:
        """
        Run backtest on historical data.
        
        Args:
            candles: Historical candle data
            warmup_period: Number of candles for strategy initialization
        
        Returns:
            Backtest results dictionary
        """
        logger.info(
            f"Starting backtest: {self.strategy.name} on {len(candles)} candles"
        )
        
        # Reset state
        self._reset()
        
        # Initialize strategy with warmup data
        if len(candles) > warmup_period:
            warmup_candles = candles[:warmup_period]
            self.strategy.initialize(warmup_candles)
            start_idx = warmup_period
        else:
            start_idx = 0
        
        # Main backtest loop
        for i in range(start_idx, len(candles)):
            candle = candles[i]
            self._process_candle(candle)
        
        # Close any remaining positions
        if candles:
            last_candle = candles[-1]
            self._close_all_positions(last_candle.close)
        
        # Calculate results
        results = self._calculate_results()
        
        logger.info(
            f"Backtest complete: {self.candles_processed} candles processed, "
            f"Total Return: {results['total_return_pct']:.2f}%"
        )
        
        return results
    
    def _process_candle(self, candle: Candle) -> None:
        """
        Process a single candle.
        
        Args:
            candle: Candle to process
        """
        self.current_time = candle.time
        self.candles_processed += 1
        
        # 1. Match pending orders against this candle
        trades = self.exchange.match_orders(candle)
        
        # 2. Update portfolio with trades
        for trade in trades:
            self.portfolio.add_trade(trade)
        
        # 3. Send candle to strategy
        signal = self.strategy.on_candle(candle)
        
        # 4. Process signal if generated
        if signal:
            self._process_signal(signal, candle)
        
        # 5. Update equity curve
        current_prices = {candle.symbol: candle.close}
        self.portfolio.update_equity_curve(candle.time, current_prices)
        
        # Log progress periodically
        if self.candles_processed % 1000 == 0:
            logger.debug(f"Processed {self.candles_processed} candles")
    
    def _process_signal(self, signal: Signal, candle: Candle) -> None:
        """
        Process trading signal.
        
        Args:
            signal: Trading signal
            candle: Current candle
        """
        # Check if signal is expired
        if signal.is_expired():
            logger.debug(f"Signal expired: {signal}")
            return
        
        # Handle different signal types
        if signal.signal_type == SignalType.BUY:
            self._handle_buy_signal(signal)
        
        elif signal.signal_type == SignalType.SELL:
            self._handle_sell_signal(signal)
        
        elif signal.signal_type in [SignalType.CLOSE_LONG, SignalType.CLOSE_SHORT]:
            self._handle_close_signal(signal, candle.close)
    
    def _handle_buy_signal(self, signal: Signal) -> None:
        """
        Handle BUY signal.
        
        Args:
            signal: Buy signal
        """
        # Check if we already have a position
        if self.portfolio.has_position(signal.symbol):
            logger.debug(f"Already have position for {signal.symbol}, ignoring BUY signal")
            return
        
        # Calculate position size (use all available capital for simplicity)
        # In production, you'd use proper position sizing
        available_capital = self.portfolio.cash * Decimal('0.95')  # Use 95% of cash
        size = available_capital / signal.price  # type: ignore[operator]
        
        if size <= 0:
            logger.warning("Insufficient capital for BUY signal")
            return
        
        # Create market order
        order = Order.create_market_order(
            symbol=signal.symbol,
            side=OrderSide.BUY,
            size=size,
            stop_loss=signal.stop_loss,
            take_profit=signal.target_price
        )
        
        # Place order
        self.exchange.place_order(order)
        logger.debug(f"Placed BUY order: {order}")
    
    def _handle_sell_signal(self, signal: Signal) -> None:
        """
        Handle SELL signal (short selling).
        
        Args:
            signal: Sell signal
        """
        # For simplicity, we'll treat SELL as closing long positions
        # Full short selling support would require more complex logic
        position = self.portfolio.get_position(signal.symbol)
        
        if position and position.is_open():
            # Close the long position
            self.portfolio.close_position(signal.symbol, signal.price)
            logger.debug(f"Closed position on SELL signal: {signal.symbol}")
    
    def _handle_close_signal(self, signal: Signal, current_price: Decimal) -> None:
        """
        Handle CLOSE signal.
        
        Args:
            signal: Close signal
            current_price: Current price
        """
        position = self.portfolio.get_position(signal.symbol)
        
        if position and position.is_open():
            self.portfolio.close_position(signal.symbol, current_price)
            logger.debug(f"Closed position: {signal.symbol}")
    
    def _close_all_positions(self, final_price: Decimal) -> None:
        """
        Close all open positions at end of backtest.
        
        Args:
            final_price: Final price to close at
        """
        symbols_to_close = list(self.portfolio.positions.keys())
        
        for symbol_str in symbols_to_close:
            # Parse symbol
            parts = symbol_str.split('/')
            if len(parts) == 2:
                symbol = TradingPair(base=parts[0], quote=parts[1])
                self.portfolio.close_position(symbol, final_price)
                logger.debug(f"Closed final position: {symbol}")
    
    def _calculate_results(self) -> Dict:
        """
        Calculate backtest results.
        
        Returns:
            Results dictionary
        """
        portfolio_stats = self.portfolio.get_stats()
        
        # Add strategy stats
        strategy_stats = self.strategy.get_performance_stats()
        
        # Combine results
        results = {
            **portfolio_stats,
            **strategy_stats,
            'candles_processed': self.candles_processed,
            'equity_curve': self.portfolio.equity_curve,
            'trades': self.portfolio.trades
        }
        
        return results
    
    def _reset(self) -> None:
        """Reset backtest state."""
        self.exchange.reset()
        self.portfolio.reset()
        self.strategy.reset()
        self.current_time = None
        self.candles_processed = 0
