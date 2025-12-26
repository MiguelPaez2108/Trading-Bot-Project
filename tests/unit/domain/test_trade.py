"""
Unit tests for Trade entity (src/python/domain/entities/trade.py)

Path: tests/unit/domain/test_trade.py
"""
import pytest
from decimal import Decimal
from datetime import datetime
from uuid import uuid4

from src.python.domain.entities.trade import Trade
from src.python.domain.value_objects.symbol import TradingPair


class TestTradeCreation:
    """Test Trade entity instantiation and validation."""
    
    def test_trade_creation_valid(self):
        """Test creating a valid Trade."""
        symbol = TradingPair(base="BTC", quote="USDT")
        trade = Trade(
            symbol=symbol,
            side="BUY",
            price=Decimal("50000"),
            size=Decimal("1.5")
        )
        
        assert trade.symbol == symbol
        assert trade.side == "BUY"
        assert trade.price == Decimal("50000")
        assert trade.size == Decimal("1.5")
        assert trade.commission == Decimal("0")
        assert trade.realized_pnl is None
        assert trade.id is not None
        assert trade.executed_at is not None
    
    def test_trade_missing_symbol_raises_error(self):
        """Test that Trade requires symbol."""
        with pytest.raises(ValueError, match="Symbol is required"):
            Trade(
                symbol=None,
                side="BUY",
                price=Decimal("50000"),
                size=Decimal("1.5")
            )
    
    def test_trade_missing_side_raises_error(self):
        """Test that Trade requires side."""
        symbol = TradingPair(base="BTC", quote="USDT")
        with pytest.raises(ValueError, match="Side is required"):
            Trade(
                symbol=symbol,
                side=None,
                price=Decimal("50000"),
                size=Decimal("1.5")
            )
    
    def test_trade_invalid_price_raises_error(self):
        """Test that Trade requires positive price."""
        symbol = TradingPair(base="BTC", quote="USDT")
        
        # Negative price
        with pytest.raises(ValueError, match="Price must be positive"):
            Trade(
                symbol=symbol,
                side="BUY",
                price=Decimal("-50000"),
                size=Decimal("1.5")
            )
        
        # Zero price
        with pytest.raises(ValueError, match="Price must be positive"):
            Trade(
                symbol=symbol,
                side="BUY",
                price=Decimal("0"),
                size=Decimal("1.5")
            )
        
        # None price
        with pytest.raises(ValueError, match="Price must be positive"):
            Trade(
                symbol=symbol,
                side="BUY",
                price=None,
                size=Decimal("1.5")
            )
    
    def test_trade_invalid_size_raises_error(self):
        """Test that Trade requires positive size."""
        symbol = TradingPair(base="BTC", quote="USDT")
        
        # Negative size
        with pytest.raises(ValueError, match="Size must be positive"):
            Trade(
                symbol=symbol,
                side="BUY",
                price=Decimal("50000"),
                size=Decimal("-1.5")
            )
        
        # Zero size
        with pytest.raises(ValueError, match="Size must be positive"):
            Trade(
                symbol=symbol,
                side="BUY",
                price=Decimal("50000"),
                size=Decimal("0")
            )
        
        # None size
        with pytest.raises(ValueError, match="Size must be positive"):
            Trade(
                symbol=symbol,
                side="BUY",
                price=Decimal("50000"),
                size=None
            )


class TestTradeCalculations:
    """Test Trade calculation methods."""
    
    @pytest.fixture
    def trade_buy(self):
        """Create a buy trade for testing."""
        symbol = TradingPair(base="BTC", quote="USDT")
        return Trade(
            symbol=symbol,
            side="BUY",
            price=Decimal("50000"),
            size=Decimal("1.0"),
            commission=Decimal("10")
        )
    
    def test_notional_value(self, trade_buy):
        """Test notional value calculation (size * price)."""
        expected = Decimal("50000") * Decimal("1.0")
        assert trade_buy.notional_value() == expected
        assert trade_buy.notional_value() == Decimal("50000")
    
    def test_net_value(self, trade_buy):
        """Test net value calculation (notional - commission)."""
        expected = Decimal("50000") - Decimal("10")
        assert trade_buy.net_value() == expected
        assert trade_buy.net_value() == Decimal("49990")
    
    def test_net_value_with_zero_commission(self):
        """Test net value when commission is zero."""
        symbol = TradingPair(base="ETH", quote="USDT")
        trade = Trade(
            symbol=symbol,
            side="SELL",
            price=Decimal("3000"),
            size=Decimal("2.0")
        )
        
        assert trade.net_value() == Decimal("6000")
    
    def test_is_buy(self):
        """Test is_buy() method."""
        symbol = TradingPair(base="BTC", quote="USDT")
        buy_trade = Trade(
            symbol=symbol,
            side="BUY",
            price=Decimal("50000"),
            size=Decimal("1.0")
        )
        
        assert buy_trade.is_buy() is True
        assert buy_trade.is_sell() is False
    
    def test_is_sell(self):
        """Test is_sell() method."""
        symbol = TradingPair(base="BTC", quote="USDT")
        sell_trade = Trade(
            symbol=symbol,
            side="SELL",
            price=Decimal("50000"),
            size=Decimal("1.0")
        )
        
        assert sell_trade.is_sell() is True
        assert sell_trade.is_buy() is False


class TestTradeDecimalConversion:
    """Test automatic Decimal conversion for numeric fields."""
    
    def test_price_converted_to_decimal(self):
        """Test that int/float price is converted to Decimal."""
        symbol = TradingPair(base="BTC", quote="USDT")
        
        # From int
        trade_int = Trade(
            symbol=symbol,
            side="BUY",
            price=50000,
            size=Decimal("1.0")
        )
        assert isinstance(trade_int.price, Decimal)
        assert trade_int.price == Decimal("50000")
        
        # From float
        trade_float = Trade(
            symbol=symbol,
            side="BUY",
            price=50000.5,
            size=Decimal("1.0")
        )
        assert isinstance(trade_float.price, Decimal)
        assert trade_float.price == Decimal("50000.5")
    
    def test_size_converted_to_decimal(self):
        """Test that int/float size is converted to Decimal."""
        symbol = TradingPair(base="BTC", quote="USDT")
        
        # From int
        trade_int = Trade(
            symbol=symbol,
            side="BUY",
            price=Decimal("50000"),
            size=2
        )
        assert isinstance(trade_int.size, Decimal)
        assert trade_int.size == Decimal("2")
        
        # From float
        trade_float = Trade(
            symbol=symbol,
            side="BUY",
            price=Decimal("50000"),
            size=1.5
        )
        assert isinstance(trade_float.size, Decimal)
        assert trade_float.size == Decimal("1.5")
    
    def test_commission_converted_to_decimal(self):
        """Test that int/float commission is converted to Decimal."""
        symbol = TradingPair(base="BTC", quote="USDT")
        
        # From int
        trade_int = Trade(
            symbol=symbol,
            side="BUY",
            price=Decimal("50000"),
            size=Decimal("1.0"),
            commission=10
        )
        assert isinstance(trade_int.commission, Decimal)
        assert trade_int.commission == Decimal("10")
        
        # From float
        trade_float = Trade(
            symbol=symbol,
            side="BUY",
            price=Decimal("50000"),
            size=Decimal("1.0"),
            commission=5.5
        )
        assert isinstance(trade_float.commission, Decimal)
        assert trade_float.commission == Decimal("5.5")


class TestTradeStringRepresentation:
    """Test Trade string methods."""
    
    def test_str_representation(self):
        """Test __str__() output."""
        symbol = TradingPair(base="BTC", quote="USDT")
        trade = Trade(
            symbol=symbol,
            side="BUY",
            price=Decimal("50000"),
            size=Decimal("1.0")
        )
        
        str_repr = str(trade)
        assert "Trade(" in str_repr
        assert "BTC/USDT" in str_repr or "BTC" in str_repr
        assert "BUY" in str_repr
        assert "1.0" in str_repr
        assert "50000" in str_repr
    
    def test_repr_representation(self):
        """Test __repr__() output."""
        symbol = TradingPair(base="ETH", quote="USDT")
        trade = Trade(
            symbol=symbol,
            side="SELL",
            price=Decimal("3000"),
            size=Decimal("2.0")
        )
        
        repr_str = repr(trade)
        assert "Trade(" in repr_str


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
