"""
Trade Entity - Executed trade record.

Path: src/python/domain/entities/trade.py
"""
from dataclasses import dataclass, field
from typing import Optional
from decimal import Decimal
from datetime import datetime, timezone
from uuid import UUID, uuid4

from src.python.domain.value_objects.symbol import TradingPair


@dataclass
class Trade:
    """
    Trade entity representing an executed trade.
    
    This is the result of an order being filled.
    Immutable after creation.
    """
    # Identity
    id: UUID = field(default_factory=uuid4)
    order_id: Optional[UUID] = None
    exchange_trade_id: Optional[str] = None
    
    # Trade details
    symbol: Optional[TradingPair] = None
    side: Optional[str] = None  # "BUY" or "SELL"
    
    # Execution
    price: Optional[Decimal] = None
    size: Optional[Decimal] = None
    
    # Costs
    commission: Decimal = Decimal('0')
    commission_asset: str = "USDT"
    
    # P&L (only for closing trades)
    realized_pnl: Optional[Decimal] = None
    
    # Timestamp
    executed_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def __post_init__(self):
        """Validate trade on creation."""
        if self.symbol is None:
            raise ValueError("Symbol is required")
        if self.side is None:
            raise ValueError("Side is required")
        if self.price is None or self.price <= 0:
            raise ValueError("Price must be positive")
        if self.size is None or self.size <= 0:
            raise ValueError("Size must be positive")
        
        # Ensure Decimal types only for non-Decimal inputs (runtime safety)
        if self.price is not None and not isinstance(self.price, Decimal):  # type: ignore[misc]
            object.__setattr__(self, 'price', Decimal(str(self.price)))
        if self.size is not None and not isinstance(self.size, Decimal):  # type: ignore[misc]
            object.__setattr__(self, 'size', Decimal(str(self.size)))
        if self.commission is not None and not isinstance(self.commission, Decimal):  # type: ignore[misc]
            object.__setattr__(self, 'commission', Decimal(str(self.commission)))
    
    def notional_value(self) -> Decimal:
        """
        Get notional value (size * price).
        
        Returns:
            Notional value in quote currency
        """
        # Type checker: size and price are validated as non-None in __post_init__
        return self.size * self.price  # type: ignore[operator]
    
    def net_value(self) -> Decimal:
        """
        Get net value after commission.
        
        Returns:
            Net value = notional - commission
        """
        return self.notional_value() - self.commission
    
    def is_buy(self) -> bool:
        """Check if trade is buy."""
        return self.side == "BUY"
    
    def is_sell(self) -> bool:
        """Check if trade is sell."""
        return self.side == "SELL"
    
    def __str__(self) -> str:
        """String representation."""
        return (
            f"Trade(id={self.id}, {self.symbol} {self.side} "
            f"size={self.size} @ {self.price} = {self.notional_value():.2f} "
            f"commission={self.commission})"
        )
    
    def __repr__(self) -> str:
        """Detailed representation."""
        return self.__str__()