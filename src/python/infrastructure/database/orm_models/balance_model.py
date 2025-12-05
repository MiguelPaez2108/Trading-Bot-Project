"""
SQLAlchemy ORM Model - Balance
"""
from datetime import datetime
from sqlalchemy import Column, String, Numeric, DateTime
from sqlalchemy.schema import PrimaryKeyConstraint

from ..connection import Base


class BalanceModel(Base):
    """
    ORM model for account balances.
    Maps to trading.balances table.
    """
    
    __tablename__ = "balances"
    __table_args__ = (
        PrimaryKeyConstraint("exchange", "currency"),
        {"schema": "trading"}
    )
    
    # Composite Primary Key
    exchange = Column(String(20), nullable=False)
    currency = Column(String(10), nullable=False)
    
    # Balance Details
    free = Column(Numeric(20, 8), nullable=False, default=0)
    locked = Column(Numeric(20, 8), nullable=False, default=0)
    total = Column(Numeric(20, 8), nullable=False, default=0)
    
    # Timestamp
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self) -> str:
        return (
            f"<BalanceModel(exchange={self.exchange}, currency={self.currency}, "
            f"total={self.total})>"
        )
