"""
SQLAlchemy ORM Model - Order
"""
from datetime import datetime
from decimal import Decimal
from sqlalchemy import Column, String, Numeric, DateTime, CheckConstraint, Index
from sqlalchemy.dialects.postgresql import UUID
import uuid

from ..connection import Base


class OrderModel(Base):
    """
    ORM model for trading orders.
    Maps to trading.orders table.
    """
    
    __tablename__ = "orders"
    __table_args__ = (
        CheckConstraint("filled_quantity <= quantity", name="chk_filled_quantity"),
        Index("idx_orders_symbol_created", "symbol", "created_at"),
        Index("idx_orders_status_exchange", "status", "exchange"),
        Index("idx_orders_strategy", "strategy_id", "created_at"),
        {"schema": "trading"}
    )
    
    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Order Details
    symbol = Column(String(20), nullable=False)
    exchange = Column(String(20), nullable=False)
    side = Column(String(10), nullable=False)  # BUY, SELL
    type = Column(String(20), nullable=False)  # MARKET, LIMIT, etc.
    status = Column(String(20), nullable=False)  # PENDING, FILLED, etc.
    
    # Quantities and Prices
    quantity = Column(Numeric(20, 8), nullable=False)
    price = Column(Numeric(20, 8), nullable=True)
    stop_price = Column(Numeric(20, 8), nullable=True)
    filled_quantity = Column(Numeric(20, 8), nullable=False, default=0)
    average_fill_price = Column(Numeric(20, 8), nullable=True)
    
    # Fees
    commission = Column(Numeric(20, 8), nullable=False, default=0)
    commission_asset = Column(String(10), nullable=True)
    
    # Exchange IDs
    exchange_order_id = Column(String(100), nullable=True)
    client_order_id = Column(String(100), nullable=True)
    
    # Strategy
    strategy_id = Column(String(50), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    filled_at = Column(DateTime, nullable=True)
    
    def __repr__(self) -> str:
        return (
            f"<OrderModel(id={self.id}, symbol={self.symbol}, "
            f"side={self.side}, status={self.status})>"
        )
