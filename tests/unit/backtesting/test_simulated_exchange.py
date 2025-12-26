"""
Unit tests for Simulated Exchange.
"""
import pytest
from decimal import Decimal
from datetime import datetime, timezone

from src.python.backtesting.simulated_exchange import SimulatedExchange
from src.python.domain.entities.order import Order, OrderSide, OrderType, OrderStatus
from src.python.domain.entities.candle import Candle
from src.python.domain.value_objects.symbol import TradingPair


class TestSimulatedExchange:
    """Test suite for SimulatedExchange."""
    
    @pytest.fixture
    def exchange(self):
        """Create simulated exchange instance."""
        return SimulatedExchange(
            maker_fee=Decimal('0.001'),
            taker_fee=Decimal('0.001'),
            slippage_pct=Decimal('0.0005')
        )
    
    @pytest.fixture
    def symbol(self):
        """Create trading pair."""
        return TradingPair(base="BTC", quote="USDT")
    
    @pytest.fixture
    def candle(self, symbol):
        """Create test candle."""
        return Candle(
            time=datetime.now(timezone.utc),
            symbol=symbol,
            timeframe="1h",
            open=Decimal('50000'),
            high=Decimal('51000'),
            low=Decimal('49000'),
            close=Decimal('50500'),
            volume=Decimal('100')
        )
    
    def test_place_order(self, exchange, symbol):
        """Test placing an order."""
        order = Order.create_market_order(
            symbol=symbol,
            side=OrderSide.BUY,
            size=Decimal('0.1')
        )
        
        result = exchange.place_order(order)
        
        assert result is True
        assert order.status == OrderStatus.OPEN
        assert len(exchange.pending_orders) == 1
    
    def test_cancel_order(self, exchange, symbol):
        """Test cancelling an order."""
        order = Order.create_market_order(
            symbol=symbol,
            side=OrderSide.BUY,
            size=Decimal('0.1')
        )
        
        exchange.place_order(order)
        result = exchange.cancel_order(str(order.id))
        
        assert result is True
        assert order.status == OrderStatus.CANCELLED
        assert len(exchange.pending_orders) == 0
    
    def test_match_market_buy_order(self, exchange, symbol, candle):
        """Test matching a market buy order."""
        order = Order.create_market_order(
            symbol=symbol,
            side=OrderSide.BUY,
            size=Decimal('0.1')
        )
        
        exchange.place_order(order)
        trades = exchange.match_orders(candle)
        
        assert len(trades) == 1
        trade = trades[0]
        
        # Market buy should fill at close + slippage
        expected_price = candle.close * (Decimal('1') + Decimal('0.0005'))
        assert trade.price == expected_price
        assert trade.size == Decimal('0.1')
        assert trade.side == "BUY"
        
        # Check commission
        notional = trade.size * trade.price
        expected_commission = notional * Decimal('0.001')
        assert trade.commission == expected_commission
        
        # Order should be filled
        assert order.status == OrderStatus.FILLED
        assert len(exchange.pending_orders) == 0
        assert len(exchange.filled_orders) == 1
    
    def test_match_market_sell_order(self, exchange, symbol, candle):
        """Test matching a market sell order."""
        order = Order.create_market_order(
            symbol=symbol,
            side=OrderSide.SELL,
            size=Decimal('0.1')
        )
        
        exchange.place_order(order)
        trades = exchange.match_orders(candle)
        
        assert len(trades) == 1
        trade = trades[0]
        
        # Market sell should fill at close - slippage
        expected_price = candle.close * (Decimal('1') - Decimal('0.0005'))
        assert trade.price == expected_price
    
    def test_match_limit_buy_order_filled(self, exchange, symbol, candle):
        """Test matching a limit buy order that gets filled."""
        order = Order.create_limit_order(
            symbol=symbol,
            side=OrderSide.BUY,
            price=Decimal('49500'),  # Below candle low
            size=Decimal('0.1')
        )
        
        exchange.place_order(order)
        trades = exchange.match_orders(candle)
        
        assert len(trades) == 1
        trade = trades[0]
        
        # Limit buy fills at limit price
        assert trade.price == Decimal('49500')
        assert order.status == OrderStatus.FILLED
    
    def test_match_limit_buy_order_not_filled(self, exchange, symbol, candle):
        """Test limit buy order that doesn't get filled."""
        order = Order.create_limit_order(
            symbol=symbol,
            side=OrderSide.BUY,
            price=Decimal('48000'),  # Below candle low
            size=Decimal('0.1')
        )
        
        exchange.place_order(order)
        trades = exchange.match_orders(candle)
        
        assert len(trades) == 0
        assert order.status == OrderStatus.OPEN
        assert len(exchange.pending_orders) == 1
    
    def test_match_limit_sell_order_filled(self, exchange, symbol, candle):
        """Test matching a limit sell order that gets filled."""
        order = Order.create_limit_order(
            symbol=symbol,
            side=OrderSide.SELL,
            price=Decimal('50500'),  # At or below candle high
            size=Decimal('0.1')
        )
        
        exchange.place_order(order)
        trades = exchange.match_orders(candle)
        
        assert len(trades) == 1
        trade = trades[0]
        
        # Limit sell fills at limit price
        assert trade.price == Decimal('50500')
        assert order.status == OrderStatus.FILLED
    
    def test_reset(self, exchange, symbol):
        """Test exchange reset."""
        order = Order.create_market_order(
            symbol=symbol,
            side=OrderSide.BUY,
            size=Decimal('0.1')
        )
        
        exchange.place_order(order)
        exchange.reset()
        
        assert len(exchange.pending_orders) == 0
        assert len(exchange.filled_orders) == 0
        assert len(exchange.trades) == 0
