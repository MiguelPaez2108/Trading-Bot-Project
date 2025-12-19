"""
Order Entity - Trading order representation.

Path: src/python/domain/entities/order.py
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from decimal import Decimal
from datetime import datetime
from uuid import UUID, uuid4

from src.python.domain.value_objects.symbol import TradingPair


class OrderSide(str, Enum):
    """Order side."""
    BUY = "BUY"
    SELL = "SELL"


class OrderType(str, Enum):
    """Order type."""
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP_LOSS = "STOP_LOSS"
    TAKE_PROFIT = "TAKE_PROFIT"
    OCO = "OCO"  # One-Cancels-Other


class OrderStatus(str, Enum):
    """Order status."""
    PENDING = "PENDING"
    OPEN = "OPEN"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FILLED = "FILLED"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"


@dataclass
class Order:
    """
    Order entity representing a trading order.
    
    This is an ENTITY (has identity via id).
    Mutable status but immutable order parameters.
    """
    # Identity
    id: UUID = field(default_factory=uuid4)
    exchange_order_id: Optional[str] = None
    
    # Order details
    symbol: Optional[TradingPair] = None
    side: Optional[OrderSide] = None
    order_type: Optional[OrderType] = None
    status: OrderStatus = OrderStatus.PENDING
    
    # Pricing
    price: Optional[Decimal] = None  # None for market orders
    stop_price: Optional[Decimal] = None  # For stop orders
    size: Optional[Decimal] = None
    
    # Risk management
    stop_loss: Optional[Decimal] = None
    take_profit: Optional[Decimal] = None
    
    # Fill tracking
    filled_size: Decimal = Decimal('0')
    average_fill_price: Optional[Decimal] = None
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    filled_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validate order on creation."""
        if self.symbol is None:
            raise ValueError("Symbol is required")
        if self.side is None:
            raise ValueError("Side is required")
        if self.order_type is None:
            raise ValueError("Order type is required")
        if self.size is None or self.size <= 0:
            raise ValueError("Size must be positive")
        
        # Ensure Decimal types only for non-Decimal inputs
        if self.size is not None and not isinstance(self.size, Decimal):
            object.__setattr__(self, 'size', Decimal(str(self.size)))
        if self.price is not None and not isinstance(self.price, Decimal):
            object.__setattr__(self, 'price', Decimal(str(self.price)))
        if self.stop_loss is not None and not isinstance(self.stop_loss, Decimal):
            object.__setattr__(self, 'stop_loss', Decimal(str(self.stop_loss)))
        if self.take_profit is not None and not isinstance(self.take_profit, Decimal):
            object.__setattr__(self, 'take_profit', Decimal(str(self.take_profit)))
    
    @classmethod
    def create_market_order(
        cls,
        symbol: TradingPair,
        side: OrderSide,
        size: Decimal,
        stop_loss: Optional[Decimal] = None,
        take_profit: Optional[Decimal] = None
    ) -> "Order":
        """
        Create market order.
        
        Args:
            symbol: Trading pair
            side: BUY or SELL
            size: Order size
            stop_loss: Stop loss price
            take_profit: Take profit price
        
        Returns:
            Order instance
        """
        return cls(
            symbol=symbol,
            side=side,
            order_type=OrderType.MARKET,
            size=size,
            stop_loss=stop_loss,
            take_profit=take_profit
        )
    
    @classmethod
    def create_limit_order(
        cls,
        symbol: TradingPair,
        side: OrderSide,
        price: Decimal,
        size: Decimal,
        stop_loss: Optional[Decimal] = None,
        take_profit: Optional[Decimal] = None
    ) -> "Order":
        """Create limit order."""
        return cls(
            symbol=symbol,
            side=side,
            order_type=OrderType.LIMIT,
            price=price,
            size=size,
            stop_loss=stop_loss,
            take_profit=take_profit
        )
    
    def update_status(self, new_status: OrderStatus) -> None:
        """
        Update order status.
        
        Args:
            new_status: New status
        """
        self.status = new_status
        self.updated_at = datetime.utcnow()
        
        if new_status == OrderStatus.FILLED:
            self.filled_at = datetime.utcnow()
    
    def update_fill(
        self,
        filled_size: Decimal,
        fill_price: Decimal
    ) -> None:
        """
        Update fill information.
        
        Args:
            filled_size: Size filled
            fill_price: Fill price
        """
        # Calculate weighted average fill price
        if self.average_fill_price is None:
            self.average_fill_price = fill_price
            self.filled_size = filled_size
        else:
            total_value = (self.filled_size * self.average_fill_price) + (filled_size * fill_price)
            self.filled_size += filled_size
            self.average_fill_price = total_value / self.filled_size
        
        self.updated_at = datetime.utcnow()
        
        # Update status
        if self.filled_size >= self.size:
            self.update_status(OrderStatus.FILLED)
        elif self.filled_size > 0:
            self.update_status(OrderStatus.PARTIALLY_FILLED)
    
    def is_filled(self) -> bool:
        """Check if order is completely filled."""
        return self.status == OrderStatus.FILLED
    
    def is_open(self) -> bool:
        """Check if order is open."""
        return self.status in [OrderStatus.PENDING, OrderStatus.OPEN, OrderStatus.PARTIALLY_FILLED]
    
    def is_closed(self) -> bool:
        """Check if order is closed."""
        return self.status in [OrderStatus.FILLED, OrderStatus.CANCELLED, OrderStatus.REJECTED, OrderStatus.EXPIRED]
    
    def remaining_size(self) -> Decimal:
        """Get remaining unfilled size."""
        return self.size - self.filled_size
    
    def notional_value(self) -> Optional[Decimal]:
        """
        Get notional value (size * price).
        
        Returns None for market orders without fill price.
        """
        price = self.average_fill_price or self.price
        if price is None:
            return None
        return self.size * price
    
    def __str__(self) -> str:
        """String representation."""
        return (
            f"Order(id={self.id}, {self.symbol} {self.side.value} {self.order_type.value} "
            f"size={self.size} price={self.price} status={self.status.value})"
        )