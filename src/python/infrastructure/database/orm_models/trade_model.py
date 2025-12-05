"""
SQLAlchemy ORM Model - Trade
"""
from datetime import datetime
from sqlalchemy import Column, String, Numeric, DateTime, Boolean, Index, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid

from ..connection import Base


class TradeModel(Base):
    """
    ORM model for trade executions.
    Maps to market_data.trades table.
    """
    
    __tablename__ = "trades"
    __table_args__ = (
        Index("idx_trades_order_id", "order_id"),
        Index("idx_trades_symbol_time", "symbol", "timestamp"),
        Index("idx_trades_exchange_time", "exchange", "timestamp"),
        {"schema": "market_data"}
    )
    
    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Foreign Key to Order
    order_id = Column(UUID(as_uuid=True), nullable=True)
    
    # Trade Details
    symbol = Column(String(20), nullable=False)
    exchange = Column(String(20), nullable=False)
    side = Column(String(10), nullable=False)  # BUY, SELL
    
    # Execution Details
    price = Column(Numeric(20, 8), nullable=False)
    quantity = Column(Numeric(20, 8), nullable=False)
    
    # Fees
    fee = Column(Numeric(20, 8), nullable=False, default=0)
    fee_currency = Column(String(10), nullable=True)
    
    # Exchange Info
    exchange_trade_id = Column(String(100), nullable=True)
    is_maker = Column(Boolean, nullable=False, default=False)
    
    # Timestamp
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return (
            f"<TradeModel(id={self.id}, symbol={self.symbol}, "
            f"side={self.side}, price={self.price}, qty={self.quantity})>"
        )
