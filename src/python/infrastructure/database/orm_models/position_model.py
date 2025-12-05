"""
SQLAlchemy ORM Model - Position
"""
from datetime import datetime
from sqlalchemy import Column, String, Numeric, DateTime, Index
from sqlalchemy.dialects.postgresql import UUID
import uuid

from ..connection import Base


class PositionModel(Base):
    """
    ORM model for trading positions.
    Maps to trading.positions table.
    """
    
    __tablename__ = "positions"
    __table_args__ = (
        Index("idx_positions_symbol_exchange", "symbol", "exchange", "closed_at"),
        Index("idx_positions_strategy", "strategy_id"),
        {"schema": "trading"}
    )
    
    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Position Details
    symbol = Column(String(20), nullable=False)
    exchange = Column(String(20), nullable=False)
    side = Column(String(10), nullable=False)  # LONG, SHORT
    
    # Prices and Quantities
    entry_price = Column(Numeric(20, 8), nullable=False)
    quantity = Column(Numeric(20, 8), nullable=False)
    current_price = Column(Numeric(20, 8), nullable=True)
    
    # PnL
    realized_pnl = Column(Numeric(20, 8), nullable=False, default=0)
    unrealized_pnl = Column(Numeric(20, 8), nullable=False, default=0)
    total_fees = Column(Numeric(20, 8), nullable=False, default=0)
    
    # Strategy
    strategy_id = Column(String(50), nullable=True)
    
    # Timestamps
    opened_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    closed_at = Column(DateTime, nullable=True)
    
    def __repr__(self) -> str:
        return (
            f"<PositionModel(id={self.id}, symbol={self.symbol}, "
            f"side={self.side}, pnl={self.realized_pnl + self.unrealized_pnl})>"
        )
