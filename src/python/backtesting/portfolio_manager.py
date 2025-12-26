"""
Portfolio Manager for Backtesting.

Tracks positions, cash, and P&L during backtesting.
"""
from typing import Dict, List, Optional
from decimal import Decimal
from datetime import datetime
import logging

from src.python.domain.entities.position import Position, PositionSide, PositionStatus
from src.python.domain.entities.trade import Trade
from src.python.domain.value_objects.symbol import TradingPair

logger = logging.getLogger(__name__)


class PortfolioManager:
    """
    Manages portfolio state during backtesting.
    
    Tracks:
    - Cash balance
    - Open positions
    - Closed positions
    - Trade history
    - Equity curve
    """
    
    def __init__(
        self,
        initial_capital: Decimal,
        leverage: Decimal = Decimal('1.0')
    ):
        """
        Initialize portfolio manager.
        
        Args:
            initial_capital: Starting capital
            leverage: Maximum leverage allowed
        """
        self.initial_capital = initial_capital
        self.leverage = leverage
        
        # Current state
        self.cash = initial_capital
        self.positions: Dict[str, Position] = {}  # symbol -> Position
        self.closed_positions: List[Position] = []
        self.trades: List[Trade] = []
        
        # Performance tracking
        self.equity_curve: List[tuple[datetime, Decimal]] = []
        self.peak_equity = initial_capital
        self.max_drawdown = Decimal('0')
    
    def get_equity(self, current_prices: Dict[TradingPair, Decimal]) -> Decimal:
        """
        Calculate total equity (cash + position values).
        
        Args:
            current_prices: Current prices for all symbols
        
        Returns:
            Total equity
        """
        equity = self.cash
        
        for symbol_str, position in self.positions.items():
            if position.is_open():
                # Get current price
                current_price = current_prices.get(position.symbol)
                if current_price:
                    # Update position price
                    position.update_price(current_price)
                    # Add position value
                    equity += position.unrealized_pnl
        
        return equity
    
    def update_equity_curve(
        self,
        timestamp: datetime,
        current_prices: Dict[TradingPair, Decimal]
    ) -> None:
        """
        Update equity curve and drawdown tracking.
        
        Args:
            timestamp: Current timestamp
            current_prices: Current prices
        """
        equity = self.get_equity(current_prices)
        self.equity_curve.append((timestamp, equity))
        
        # Update peak and drawdown
        if equity > self.peak_equity:
            self.peak_equity = equity
        
        drawdown = (self.peak_equity - equity) / self.peak_equity
        if drawdown > self.max_drawdown:
            self.max_drawdown = drawdown
    
    def open_position(
        self,
        symbol: TradingPair,
        side: PositionSide,
        size: Decimal,
        entry_price: Decimal,
        stop_loss: Optional[Decimal] = None,
        take_profit: Optional[Decimal] = None
    ) -> Optional[Position]:
        """
        Open a new position.
        
        Args:
            symbol: Trading pair
            side: LONG or SHORT
            size: Position size
            entry_price: Entry price
            stop_loss: Stop loss price
            take_profit: Take profit price
        
        Returns:
            Position if opened, None if insufficient funds
        """
        # Calculate required capital
        notional = size * entry_price  # type: ignore[operator]
        required_capital = notional / self.leverage
        
        # Check if we have enough cash
        if required_capital > self.cash:
            logger.warning(
                f"Insufficient funds to open position: "
                f"required={required_capital}, available={self.cash}"
            )
            return None
        
        # Create position
        position = Position(
            symbol=symbol,
            side=side,
            size=size,
            entry_price=entry_price,
            current_price=entry_price,
            stop_loss=stop_loss,
            take_profit=take_profit
        )
        
        # Deduct capital
        self.cash -= required_capital
        
        # Store position
        symbol_str = str(symbol)
        self.positions[symbol_str] = position
        
        logger.info(f"Opened position: {position}")
        return position
    
    def close_position(
        self,
        symbol: TradingPair,
        close_price: Decimal
    ) -> Optional[Position]:
        """
        Close an open position.
        
        Args:
            symbol: Trading pair
            close_price: Closing price
        
        Returns:
            Closed position or None if not found
        """
        symbol_str = str(symbol)
        position = self.positions.get(symbol_str)
        
        if not position or not position.is_open():
            logger.warning(f"No open position found for {symbol}")
            return None
        
        # Calculate P&L
        realized_pnl = position.calculate_pnl(close_price)
        
        # Close position
        position.close(close_price, realized_pnl)
        
        # Return capital + P&L
        notional = position.size * position.entry_price  # type: ignore[operator]
        returned_capital = notional / self.leverage
        self.cash += returned_capital + realized_pnl
        
        # Move to closed positions
        self.closed_positions.append(position)
        del self.positions[symbol_str]
        
        logger.info(
            f"Closed position: {symbol} at {close_price}, "
            f"P&L={realized_pnl:.2f}, Cash={self.cash:.2f}"
        )
        
        return position
    
    def add_trade(self, trade: Trade) -> None:
        """
        Record a trade.
        
        Args:
            trade: Trade to record
        """
        self.trades.append(trade)
    
    def get_position(self, symbol: TradingPair) -> Optional[Position]:
        """
        Get open position for symbol.
        
        Args:
            symbol: Trading pair
        
        Returns:
            Position or None
        """
        return self.positions.get(str(symbol))
    
    def has_position(self, symbol: TradingPair) -> bool:
        """
        Check if we have an open position.
        
        Args:
            symbol: Trading pair
        
        Returns:
            True if position exists
        """
        position = self.get_position(symbol)
        return position is not None and position.is_open()
    
    def get_total_pnl(self) -> Decimal:
        """
        Get total realized P&L.
        
        Returns:
            Total P&L
        """
        return sum(p.realized_pnl for p in self.closed_positions)
    
    def get_stats(self) -> Dict:
        """
        Get portfolio statistics.
        
        Returns:
            Dict with portfolio stats
        """
        total_pnl = self.get_total_pnl()
        total_return = (total_pnl / self.initial_capital) * Decimal('100')
        
        return {
            'initial_capital': float(self.initial_capital),
            'current_cash': float(self.cash),
            'total_pnl': float(total_pnl),
            'total_return_pct': float(total_return),
            'open_positions': len(self.positions),
            'closed_positions': len(self.closed_positions),
            'total_trades': len(self.trades),
            'max_drawdown_pct': float(self.max_drawdown * Decimal('100'))
        }
    
    def reset(self) -> None:
        """Reset portfolio to initial state."""
        self.cash = self.initial_capital
        self.positions = {}
        self.closed_positions = []
        self.trades = []
        self.equity_curve = []
        self.peak_equity = self.initial_capital
        self.max_drawdown = Decimal('0')
