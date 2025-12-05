"""
Data Normalizer
Converts exchange-specific formats to internal domain format
"""
from decimal import Decimal
from datetime import datetime
from typing import Dict, Any
import structlog

from src.python.domain.entities import Candle
from src.python.domain.value_objects import Symbol, Price, Quantity, Timeframe

logger = structlog.get_logger(__name__)


class DataNormalizer:
    """
    Normalizes market data from different exchanges to internal format.
    Handles timezone conversion, precision, and validation.
    """
    
    @staticmethod
    def normalize_candle(raw_data: Dict[str, Any], exchange: str) -> Candle:
        """
        Normalize candle data from exchange format.
        
        Args:
            raw_data: Raw candle data from exchange
            exchange: Exchange name
        
        Returns:
            Candle domain entity
        
        Raises:
            ValueError: If data is invalid
        """
        try:
            # Parse symbol
            symbol = Symbol.from_string(raw_data["symbol"])
            
            # Parse timeframe
            timeframe = Timeframe(raw_data["interval"])
            
            # Parse OHLCV with Decimal for precision
            open_price = Price(Decimal(str(raw_data["open"])))
            high_price = Price(Decimal(str(raw_data["high"])))
            low_price = Price(Decimal(str(raw_data["low"])))
            close_price = Price(Decimal(str(raw_data["close"])))
            volume = Quantity(Decimal(str(raw_data["volume"])))
            
            # Validate prices
            if high_price < low_price:
                raise ValueError(f"High price {high_price} < Low price {low_price}")
            if high_price < open_price or high_price < close_price:
                raise ValueError(f"High price {high_price} is not the highest")
            if low_price > open_price or low_price > close_price:
                raise ValueError(f"Low price {low_price} is not the lowest")
            
            # Parse timestamp (convert to UTC if needed)
            timestamp = datetime.fromtimestamp(raw_data["timestamp"] / 1000)
            
            # Validate timestamp is not in future
            if timestamp > datetime.utcnow():
                raise ValueError(f"Timestamp {timestamp} is in the future")
            
            # Create Candle entity
            candle = Candle(
                symbol=symbol,
                timeframe=timeframe,
                open=open_price,
                high=high_price,
                low=low_price,
                close=close_price,
                volume=volume,
                timestamp=timestamp,
                exchange=exchange,
            )
            
            return candle
            
        except KeyError as e:
            logger.error("missing_field_in_candle", field=str(e), exchange=exchange)
            raise ValueError(f"Missing required field: {e}")
        except Exception as e:
            logger.error("candle_normalization_error", error=str(e), exchange=exchange)
            raise
    
    @staticmethod
    def normalize_trade(raw_data: Dict[str, Any], exchange: str) -> Dict[str, Any]:
        """
        Normalize trade data from exchange format.
        
        Args:
            raw_data: Raw trade data from exchange
            exchange: Exchange name
        
        Returns:
            Normalized trade dict
        """
        try:
            symbol = Symbol.from_string(raw_data["symbol"])
            price = Price(Decimal(str(raw_data["price"])))
            quantity = Quantity(Decimal(str(raw_data["quantity"])))
            timestamp = datetime.fromtimestamp(raw_data["timestamp"] / 1000)
            
            # Validate
            if price.value <= 0:
                raise ValueError(f"Invalid price: {price}")
            if quantity.value <= 0:
                raise ValueError(f"Invalid quantity: {quantity}")
            
            return {
                "symbol": symbol,
                "price": price,
                "quantity": quantity,
                "side": raw_data.get("side", "UNKNOWN"),
                "timestamp": timestamp,
                "exchange": exchange,
                "trade_id": raw_data.get("trade_id"),
                "is_buyer_maker": raw_data.get("is_buyer_maker", False),
            }
            
        except Exception as e:
            logger.error("trade_normalization_error", error=str(e), exchange=exchange)
            raise
    
    @staticmethod
    def validate_data(data: Dict[str, Any]) -> bool:
        """
        Validate normalized data.
        
        Args:
            data: Normalized data dict
        
        Returns:
            True if valid
        """
        # Basic validation
        if not data:
            return False
        
        # Check for required fields based on data type
        if "open" in data:  # Candle
            required = ["symbol", "open", "high", "low", "close", "volume", "timestamp"]
        elif "price" in data and "quantity" in data:  # Trade
            required = ["symbol", "price", "quantity", "timestamp"]
        else:
            return False
        
        return all(field in data for field in required)
