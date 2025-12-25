"""
Position Entity - Open trading position.

Path: src/python/domain/entities/position.py
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from decimal import Decimal
from datetime import datetime, timezone
from uuid import UUID, uuid4

from src.python.domain.value_objects.symbol import TradingPair


class PositionSide(str, Enum):
    """Position side."""
    LONG = "LONG"
    SHORT = "SHORT"


class PositionStatus(str, Enum):
    """Position status."""
    OPEN = "OPEN"
    CLOSED = "CLOSED"


@dataclass
class Position:
    """
    Position entity representing an open trading position.
    
    Tracks entry, current state, and P&L.
    """
    # Identity
    id: UUID = field(default_factory=uuid4)
    
    # Position details
    symbol: Optional[TradingPair] = None
    side: Optional[PositionSide] = None
    size: Optional[Decimal] = None
    
    # Pricing
    entry_price: Optional[Decimal] = None
    current_price: Optional[Decimal] = None
    
    # Risk management
    stop_loss: Optional[Decimal] = None
    take_profit: Optional[Decimal] = None
    
    # P&L tracking
    unrealized_pnl: Decimal = Decimal('0')
    realized_pnl: Decimal = Decimal('0')
    
    # Status
    status: PositionStatus = PositionStatus.OPEN
    
    # Timestamps
    opened_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    closed_at: Optional[datetime] = None
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def __post_init__(self):
        """Validate position on creation."""
        if self.symbol is None:
            raise ValueError("Symbol is required")
        if self.side is None:
            raise ValueError("Side is required")
        if self.size is None or self.size <= 0:
            raise ValueError("Size must be positive")
        if self.entry_price is None or self.entry_price <= 0:
            raise ValueError("Entry price must be positive")
        
        # Ensure Decimal types only for non-Decimal inputs (runtime safety)
        if self.size is not None and not isinstance(self.size, Decimal):  # type: ignore[misc]
            object.__setattr__(self, 'size', Decimal(str(self.size)))
        if self.entry_price is not None and not isinstance(self.entry_price, Decimal):  # type: ignore[misc]
            object.__setattr__(self, 'entry_price', Decimal(str(self.entry_price)))
        
        # Set current price to entry if not provided
        if self.current_price is None:
            object.__setattr__(self, 'current_price', self.entry_price)
    
    def update_price(self, new_price: Decimal) -> None:
        """
        Update current price and recalculate P&L.
        
        Args:
            new_price: New market price
        """
        self.current_price = new_price
        self.unrealized_pnl = self.calculate_pnl(new_price)
        self.updated_at = datetime.now(timezone.utc)
    
    def calculate_pnl(self, price: Decimal) -> Decimal:
        """
        Calculate P&L at given price.
        
        Args:
            price: Price to calculate P&L at
        
        Returns:
            P&L in quote currency
        """
        if self.side == PositionSide.LONG:
            # Long: profit when price goes up
            pnl = (price - self.entry_price) * self.size  # type: ignore[operator]
        else:
            # Short: profit when price goes down
            pnl = (self.entry_price - price) * self.size  # type: ignore[operator]
        
        return pnl
    
    def calculate_pnl_percentage(self, price: Optional[Decimal] = None) -> Decimal:
        """
        Calculate P&L as percentage.
        
        Args:
            price: Price to calculate at (default: current_price)
        
        Returns:
            P&L percentage (e.g., 0.05 for 5%)
        """
        if price is None:
            price = self.current_price
        
        pnl = self.calculate_pnl(price)
        invested = self.entry_price * self.size  # type: ignore[operator]
        
        return (pnl / invested) * Decimal('100')
    
    def is_stop_loss_hit(self, current_price: Decimal) -> bool:
        """
        Check if stop loss is hit.
        
        Args:
            current_price: Current market price
        
        Returns:
            True if stop loss triggered
        """
        if self.stop_loss is None:
            return False
        
        if self.side == PositionSide.LONG:
            return current_price <= self.stop_loss
        else:
            return current_price >= self.stop_loss
    
    def is_take_profit_hit(self, current_price: Decimal) -> bool:
        """
        Check if take profit is hit.
        
        Args:
            current_price: Current market price
        
        Returns:
            True if take profit triggered
        """
        if self.take_profit is None:
            return False
        
        if self.side == PositionSide.LONG:
            return current_price >= self.take_profit
        else:
            return current_price <= self.take_profit
    
    def close(self, close_price: Decimal, realized_pnl: Decimal) -> None:
        """
        Close position.
        
        Args:
            close_price: Price at which position was closed
            realized_pnl: Realized P&L
        """
        self.status = PositionStatus.CLOSED
        self.current_price = close_price
        self.realized_pnl = realized_pnl
        self.unrealized_pnl = Decimal('0')
        self.closed_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)
    
    def is_open(self) -> bool:
        """Check if position is open."""
        return self.status == PositionStatus.OPEN
    
    def is_closed(self) -> bool:
        """Check if position is closed."""
        return self.status == PositionStatus.CLOSED
    
    def notional_value(self, price: Optional[Decimal] = None) -> Decimal:
        """
        Get notional value (size * price).
        
        Args:
            price: Price to use (default: current_price)
        
        Returns:
            Notional value in quote currency
        """
        if price is None:
            price = self.current_price
        
        return self.size * price  # type: ignore[operator]
    
    def holding_time(self) -> float:
        """
        Get holding time in seconds.
        
        Returns:
            Seconds since position opened
        """
        if self.closed_at:
            end_time = self.closed_at
        else:
            end_time = datetime.now(timezone.utc)
        
        delta = end_time - self.opened_at
        return delta.total_seconds()
    
    def __str__(self) -> str:
        """String representation."""
        return (
            f"Position(id={self.id}, {self.symbol} {self.side.value} "
            f"size={self.size} entry={self.entry_price} "
            f"current={self.current_price} pnl={self.unrealized_pnl:.2f} "
            f"status={self.status.value})"
        )