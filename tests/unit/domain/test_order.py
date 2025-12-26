"""
Unit tests for Order entity (src/python/domain/entities/order.py)

Path: tests/unit/domain/test_order.py
"""
import pytest
from decimal import Decimal
from datetime import datetime
from uuid import uuid4

from src.python.domain.entities.order import Order, OrderSide, OrderType, OrderStatus
from src.python.domain.value_objects.symbol import TradingPair


class TestOrderSideEnum:
    """Test OrderSide enum."""
    
    def test_order_side_buy(self):
        """Test BUY side."""
        assert OrderSide.BUY.value == "BUY"
    
    def test_order_side_sell(self):
        """Test SELL side."""
        assert OrderSide.SELL.value == "SELL"
    
    def test_order_side_string_conversion(self):
        """Test OrderSide string conversion."""
        assert str(OrderSide.BUY) == "OrderSide.BUY"
        assert OrderSide.BUY == OrderSide("BUY")


class TestOrderTypeEnum:
    """Test OrderType enum."""
    
    def test_all_order_types_defined(self):
        """Test that all standard order types are defined."""
        assert OrderType.MARKET
        assert OrderType.LIMIT
        assert OrderType.STOP_LOSS
        assert OrderType.TAKE_PROFIT
        assert OrderType.OCO
    
    def test_order_type_values(self):
        """Test OrderType values."""
        assert OrderType.MARKET.value == "MARKET"
        assert OrderType.LIMIT.value == "LIMIT"
        assert OrderType.STOP_LOSS.value == "STOP_LOSS"


class TestOrderStatusEnum:
    """Test OrderStatus enum."""
    
    def test_all_order_statuses_defined(self):
        """Test that all standard order statuses are defined."""
        assert OrderStatus.PENDING
        assert OrderStatus.OPEN
        assert OrderStatus.PARTIALLY_FILLED
        assert OrderStatus.FILLED
        assert OrderStatus.CANCELLED
        assert OrderStatus.REJECTED
        assert OrderStatus.EXPIRED
    
    def test_initial_status_is_pending(self):
        """Test that default status is PENDING."""
        assert OrderStatus.PENDING.value == "PENDING"


class TestOrderCreation:
    """Test Order entity instantiation and validation."""
    
    def test_order_market_creation_valid(self):
        """Test creating a valid market Order."""
        symbol = TradingPair(base="BTC", quote="USDT")
        order = Order(
            symbol=symbol,
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            size=Decimal("1.5")
        )
        
        assert order.symbol == symbol
        assert order.side == OrderSide.BUY
        assert order.order_type == OrderType.MARKET
        assert order.size == Decimal("1.5")
        assert order.status == OrderStatus.PENDING
        assert order.price is None  # Market orders have no price
        assert order.id is not None
        assert order.created_at is not None
        assert order.filled_size == Decimal("0")
        assert order.average_fill_price is None
    
    def test_order_limit_creation_valid(self):
        """Test creating a valid limit Order."""
        symbol = TradingPair(base="ETH", quote="USDT")
        order = Order(
            symbol=symbol,
            side=OrderSide.SELL,
            order_type=OrderType.LIMIT,
            price=Decimal("3000"),
            size=Decimal("2.0")
        )
        
        assert order.symbol == symbol
        assert order.side == OrderSide.SELL
        assert order.order_type == OrderType.LIMIT
        assert order.price == Decimal("3000")
        assert order.size == Decimal("2.0")
    
    def test_order_missing_symbol_raises_error(self):
        """Test that Order requires symbol."""
        with pytest.raises(ValueError, match="Symbol is required"):
            Order(
                symbol=None,
                side=OrderSide.BUY,
                order_type=OrderType.MARKET,
                size=Decimal("1.5")
            )
    
    def test_order_missing_side_raises_error(self):
        """Test that Order requires side."""
        symbol = TradingPair(base="BTC", quote="USDT")
        with pytest.raises(ValueError, match="Side is required"):
            Order(
                symbol=symbol,
                side=None,
                order_type=OrderType.MARKET,
                size=Decimal("1.5")
            )
    
    def test_order_missing_type_raises_error(self):
        """Test that Order requires order_type."""
        symbol = TradingPair(base="BTC", quote="USDT")
        with pytest.raises(ValueError, match="Order type is required"):
            Order(
                symbol=symbol,
                side=OrderSide.BUY,
                order_type=None,
                size=Decimal("1.5")
            )
    
    def test_order_invalid_size_raises_error(self):
        """Test that Order requires positive size."""
        symbol = TradingPair(base="BTC", quote="USDT")
        
        # Negative size
        with pytest.raises(ValueError, match="Size must be positive"):
            Order(
                symbol=symbol,
                side=OrderSide.BUY,
                order_type=OrderType.MARKET,
                size=Decimal("-1.5")
            )
        
        # Zero size
        with pytest.raises(ValueError, match="Size must be positive"):
            Order(
                symbol=symbol,
                side=OrderSide.BUY,
                order_type=OrderType.MARKET,
                size=Decimal("0")
            )
        
        # None size
        with pytest.raises(ValueError, match="Size must be positive"):
            Order(
                symbol=symbol,
                side=OrderSide.BUY,
                order_type=OrderType.MARKET,
                size=None
            )


class TestOrderRiskManagement:
    """Test Order risk management fields (stop_loss, take_profit)."""
    
    def test_order_with_stop_loss(self):
        """Test creating order with stop_loss."""
        symbol = TradingPair(base="BTC", quote="USDT")
        order = Order(
            symbol=symbol,
            side=OrderSide.BUY,
            order_type=OrderType.LIMIT,
            price=Decimal("50000"),
            size=Decimal("1.0"),
            stop_loss=Decimal("45000")
        )
        
        assert order.stop_loss == Decimal("45000")
    
    def test_order_with_take_profit(self):
        """Test creating order with take_profit."""
        symbol = TradingPair(base="BTC", quote="USDT")
        order = Order(
            symbol=symbol,
            side=OrderSide.BUY,
            order_type=OrderType.LIMIT,
            price=Decimal("50000"),
            size=Decimal("1.0"),
            take_profit=Decimal("55000")
        )
        
        assert order.take_profit == Decimal("55000")
    
    def test_order_with_stop_loss_and_take_profit(self):
        """Test creating order with both stop_loss and take_profit."""
        symbol = TradingPair(base="BTC", quote="USDT")
        order = Order(
            symbol=symbol,
            side=OrderSide.BUY,
            order_type=OrderType.LIMIT,
            price=Decimal("50000"),
            size=Decimal("1.0"),
            stop_loss=Decimal("45000"),
            take_profit=Decimal("55000")
        )
        
        assert order.stop_loss == Decimal("45000")
        assert order.take_profit == Decimal("55000")


class TestOrderDecimalConversion:
    """Test automatic Decimal conversion for numeric fields."""
    
    def test_size_converted_to_decimal(self):
        """Test that int/float size is converted to Decimal."""
        symbol = TradingPair(base="BTC", quote="USDT")
        
        # From int
        order_int = Order(
            symbol=symbol,
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            size=2
        )
        assert isinstance(order_int.size, Decimal)
        assert order_int.size == Decimal("2")
        
        # From float
        order_float = Order(
            symbol=symbol,
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            size=1.5
        )
        assert isinstance(order_float.size, Decimal)
        assert order_float.size == Decimal("1.5")
    
    def test_price_converted_to_decimal(self):
        """Test that int/float price is converted to Decimal."""
        symbol = TradingPair(base="BTC", quote="USDT")
        
        # From int
        order_int = Order(
            symbol=symbol,
            side=OrderSide.BUY,
            order_type=OrderType.LIMIT,
            price=50000,
            size=Decimal("1.0")
        )
        assert isinstance(order_int.price, Decimal)
        assert order_int.price == Decimal("50000")
        
        # From float
        order_float = Order(
            symbol=symbol,
            side=OrderSide.BUY,
            order_type=OrderType.LIMIT,
            price=50000.5,
            size=Decimal("1.0")
        )
        assert isinstance(order_float.price, Decimal)
        assert order_float.price == Decimal("50000.5")


class TestOrderFillTracking:
    """Test Order fill tracking fields."""
    
    def test_order_partial_fill(self):
        """Test order with partial fill."""
        symbol = TradingPair(base="BTC", quote="USDT")
        order = Order(
            symbol=symbol,
            side=OrderSide.BUY,
            order_type=OrderType.LIMIT,
            price=Decimal("50000"),
            size=Decimal("2.0"),
            filled_size=Decimal("1.0"),
            average_fill_price=Decimal("50000")
        )
        
        assert order.filled_size == Decimal("1.0")
        assert order.average_fill_price == Decimal("50000")
        assert order.status == OrderStatus.PENDING  # Status not auto-updated
    
    def test_order_fully_filled(self):
        """Test order with full fill."""
        symbol = TradingPair(base="BTC", quote="USDT")
        now = datetime.utcnow()
        order = Order(
            symbol=symbol,
            side=OrderSide.BUY,
            order_type=OrderType.LIMIT,
            price=Decimal("50000"),
            size=Decimal("1.0"),
            filled_size=Decimal("1.0"),
            average_fill_price=Decimal("50000"),
            status=OrderStatus.FILLED,
            filled_at=now
        )
        
        assert order.filled_size == Decimal("1.0")
        assert order.average_fill_price == Decimal("50000")
        assert order.status == OrderStatus.FILLED
        assert order.filled_at == now


class TestOrderStringRepresentation:
    """Test Order string methods."""
    
    def test_order_representation(self):
        """Test Order can be represented as string."""
        symbol = TradingPair(base="BTC", quote="USDT")
        order = Order(
            symbol=symbol,
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            size=Decimal("1.5")
        )
        
        repr_str = repr(order)
        assert "Order" in repr_str


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
