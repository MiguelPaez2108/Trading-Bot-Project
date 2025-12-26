"""
Unit tests for Portfolio Manager.
"""
import pytest
from decimal import Decimal
from datetime import datetime, timezone

from src.python.backtesting.portfolio_manager import PortfolioManager
from src.python.domain.entities.position import PositionSide
from src.python.domain.value_objects.symbol import TradingPair


class TestPortfolioManager:
    """Test suite for PortfolioManager."""
    
    @pytest.fixture
    def portfolio(self):
        """Create portfolio manager instance."""
        return PortfolioManager(
            initial_capital=Decimal('10000'),
            leverage=Decimal('1.0')
        )
    
    @pytest.fixture
    def symbol(self):
        """Create trading pair."""
        return TradingPair(base="BTC", quote="USDT")
    
    def test_initialization(self, portfolio):
        """Test portfolio initialization."""
        assert portfolio.initial_capital == Decimal('10000')
        assert portfolio.cash == Decimal('10000')
        assert len(portfolio.positions) == 0
        assert len(portfolio.closed_positions) == 0
        assert len(portfolio.trades) == 0
    
    def test_open_long_position(self, portfolio, symbol):
        """Test opening a long position."""
        position = portfolio.open_position(
            symbol=symbol,
            side=PositionSide.LONG,
            size=Decimal('0.1'),
            entry_price=Decimal('50000')
        )
        
        assert position is not None
        assert position.symbol == symbol
        assert position.side == PositionSide.LONG
        assert position.size == Decimal('0.1')
        assert position.entry_price == Decimal('50000')
        
        # Check cash was deducted
        expected_cash = Decimal('10000') - (Decimal('0.1') * Decimal('50000'))
        assert portfolio.cash == expected_cash
        
        # Check position is tracked
        assert len(portfolio.positions) == 1
        assert portfolio.has_position(symbol)
    
    def test_open_position_insufficient_funds(self, portfolio, symbol):
        """Test opening position with insufficient funds."""
        position = portfolio.open_position(
            symbol=symbol,
            side=PositionSide.LONG,
            size=Decimal('1.0'),  # Too large
            entry_price=Decimal('50000')
        )
        
        assert position is None
        assert portfolio.cash == Decimal('10000')
        assert len(portfolio.positions) == 0
    
    def test_close_position_with_profit(self, portfolio, symbol):
        """Test closing position with profit."""
        # Open position
        portfolio.open_position(
            symbol=symbol,
            side=PositionSide.LONG,
            size=Decimal('0.1'),
            entry_price=Decimal('50000')
        )
        
        # Close at higher price
        closed_position = portfolio.close_position(
            symbol=symbol,
            close_price=Decimal('55000')
        )
        
        assert closed_position is not None
        assert closed_position.realized_pnl == Decimal('500')  # (55000 - 50000) * 0.1
        
        # Check cash updated
        expected_cash = Decimal('10000') + Decimal('500')
        assert portfolio.cash == expected_cash
        
        # Check position moved to closed
        assert len(portfolio.positions) == 0
        assert len(portfolio.closed_positions) == 1
    
    def test_close_position_with_loss(self, portfolio, symbol):
        """Test closing position with loss."""
        # Open position
        portfolio.open_position(
            symbol=symbol,
            side=PositionSide.LONG,
            size=Decimal('0.1'),
            entry_price=Decimal('50000')
        )
        
        # Close at lower price
        closed_position = portfolio.close_position(
            symbol=symbol,
            close_price=Decimal('45000')
        )
        
        assert closed_position is not None
        assert closed_position.realized_pnl == Decimal('-500')  # (45000 - 50000) * 0.1
        
        # Check cash updated
        expected_cash = Decimal('10000') - Decimal('500')
        assert portfolio.cash == expected_cash
    
    def test_get_equity(self, portfolio, symbol):
        """Test equity calculation."""
        # Open position
        portfolio.open_position(
            symbol=symbol,
            side=PositionSide.LONG,
            size=Decimal('0.1'),
            entry_price=Decimal('50000')
        )
        
        # Calculate equity at different price
        current_prices = {symbol: Decimal('55000')}
        equity = portfolio.get_equity(current_prices)
        
        # Equity = cash + unrealized P&L
        # Cash after opening = 10000 - 5000 = 5000
        # Unrealized P&L = (55000 - 50000) * 0.1 = 500
        # Total equity = 5000 + 500 = 5500... wait, that's wrong
        # Actually: equity = cash + position value
        # Position value at entry = 5000
        # Position value at current = 5500
        # Unrealized P&L = 500
        # Equity = 5000 (cash) + 500 (unrealized) = 5500... still wrong
        
        # Let me recalculate:
        # Initial: 10000
        # After opening: cash = 5000, position value = 5000
        # At 55000: cash = 5000, position value = 5500, unrealized = 500
        # Equity = cash + unrealized = 5000 + 500 = 5500
        # But we started with 10000, so equity should be 10500
        
        # Actually the formula should be:
        # Equity = initial_capital + total_pnl
        # Or: Equity = cash + sum(position_values)
        
        expected_equity = Decimal('10000') + Decimal('500')  # Initial + unrealized P&L
        assert equity == expected_equity
    
    def test_reset(self, portfolio, symbol):
        """Test portfolio reset."""
        # Open and close some positions
        portfolio.open_position(
            symbol=symbol,
            side=PositionSide.LONG,
            size=Decimal('0.1'),
            entry_price=Decimal('50000')
        )
        portfolio.close_position(symbol, Decimal('55000'))
        
        # Reset
        portfolio.reset()
        
        assert portfolio.cash == Decimal('10000')
        assert len(portfolio.positions) == 0
        assert len(portfolio.closed_positions) == 0
        assert len(portfolio.trades) == 0
        assert len(portfolio.equity_curve) == 0
