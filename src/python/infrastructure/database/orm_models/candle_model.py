"""
SQLAlchemy ORM Model - Candle
"""
from datetime import datetime
from sqlalchemy import Column, String, Numeric, DateTime, Integer, Index
from sqlalchemy.dialects.postgresql import TIMESTAMP

from ..connection import Base


class CandleModel(Base):
    """
    ORM model for OHLCV candles.
    Maps to market_data.candles hypertable.
    """
    
    __tablename__ = "candles"
    __table_args__ = (
        Index("idx_candles_symbol_time", "symbol", "time"),
        Index("idx_candles_symbol_exchange_timeframe", "symbol", "exchange", "timeframe", "time"),
        {"schema": "market_data"}
    )
    
    # TimescaleDB uses time as part of primary key
    time = Column(TIMESTAMP(timezone=True), primary_key=True, nullable=False)
    symbol = Column(String(20), primary_key=True, nullable=False)
    exchange = Column(String(20), primary_key=True, nullable=False)
    timeframe = Column(String(10), primary_key=True, nullable=False)
    
    # OHLCV Data
    open = Column(Numeric(20, 8), nullable=False)
    high = Column(Numeric(20, 8), nullable=False)
    low = Column(Numeric(20, 8), nullable=False)
    close = Column(Numeric(20, 8), nullable=False)
    volume = Column(Numeric(20, 8), nullable=False)
    
    # Additional Data
    quote_volume = Column(Numeric(20, 8), nullable=True)
    trades_count = Column(Integer, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return (
            f"<CandleModel(symbol={self.symbol}, timeframe={self.timeframe}, "
            f"time={self.time}, close={self.close})>"
        )
