"""
Performance Metrics Calculator.

Calculates comprehensive performance metrics for backtesting results.
"""
from typing import List, Dict, Tuple
from decimal import Decimal
from datetime import datetime
import math
import logging

from src.python.domain.entities.trade import Trade

logger = logging.getLogger(__name__)


class PerformanceMetrics:
    """
    Calculates trading strategy performance metrics.
    
    Metrics include:
    - Total Return
    - Sharpe Ratio
    - Sortino Ratio
    - Max Drawdown
    - Win Rate
    - Profit Factor
    - And more...
    """
    
    @staticmethod
    def calculate_all(
        initial_capital: Decimal,
        final_equity: Decimal,
        equity_curve: List[Tuple[datetime, Decimal]],
        trades: List[Trade],
        risk_free_rate: Decimal = Decimal('0.02')  # 2% annual
    ) -> Dict:
        """
        Calculate all performance metrics.
        
        Args:
            initial_capital: Starting capital
            final_equity: Final equity
            equity_curve: List of (timestamp, equity) tuples
            trades: List of executed trades
            risk_free_rate: Annual risk-free rate
        
        Returns:
            Dict with all metrics
        """
        if not equity_curve or not trades:
            return PerformanceMetrics._empty_metrics()
        
        # Basic metrics
        total_return = PerformanceMetrics.total_return(initial_capital, final_equity)
        total_return_pct = total_return * Decimal('100')
        
        # Returns series
        returns = PerformanceMetrics._calculate_returns(equity_curve)
        
        # Risk metrics
        sharpe = PerformanceMetrics.sharpe_ratio(returns, risk_free_rate)
        sortino = PerformanceMetrics.sortino_ratio(returns, risk_free_rate)
        max_dd, max_dd_duration = PerformanceMetrics.max_drawdown(equity_curve)
        
        # Trade metrics
        win_rate = PerformanceMetrics.win_rate(trades)
        profit_factor = PerformanceMetrics.profit_factor(trades)
        avg_win, avg_loss = PerformanceMetrics.average_win_loss(trades)
        
        # Risk-adjusted metrics
        calmar = PerformanceMetrics.calmar_ratio(total_return, max_dd)
        
        return {
            'total_return': float(total_return),
            'total_return_pct': float(total_return_pct),
            'sharpe_ratio': float(sharpe),
            'sortino_ratio': float(sortino),
            'max_drawdown': float(max_dd),
            'max_drawdown_pct': float(max_dd * Decimal('100')),
            'max_drawdown_duration_days': max_dd_duration,
            'win_rate': float(win_rate),
            'win_rate_pct': float(win_rate * Decimal('100')),
            'profit_factor': float(profit_factor),
            'average_win': float(avg_win),
            'average_loss': float(avg_loss),
            'calmar_ratio': float(calmar),
            'total_trades': len(trades),
            'winning_trades': sum(1 for t in trades if t.realized_pnl and t.realized_pnl > 0),
            'losing_trades': sum(1 for t in trades if t.realized_pnl and t.realized_pnl < 0)
        }
    
    @staticmethod
    def total_return(initial_capital: Decimal, final_equity: Decimal) -> Decimal:
        """Calculate total return."""
        return (final_equity - initial_capital) / initial_capital
    
    @staticmethod
    def sharpe_ratio(
        returns: List[Decimal],
        risk_free_rate: Decimal = Decimal('0.02'),
        periods_per_year: int = 252
    ) -> Decimal:
        """
        Calculate Sharpe ratio.
        
        Args:
            returns: List of period returns
            risk_free_rate: Annual risk-free rate
            periods_per_year: Trading periods per year
        
        Returns:
            Sharpe ratio
        """
        if not returns or len(returns) < 2:
            return Decimal('0')
        
        # Convert to float for calculation
        returns_float = [float(r) for r in returns]
        
        mean_return = sum(returns_float) / len(returns_float)
        
        # Calculate standard deviation
        variance = sum((r - mean_return) ** 2 for r in returns_float) / len(returns_float)
        std_dev = math.sqrt(variance)
        
        if std_dev == 0:
            return Decimal('0')
        
        # Annualize
        annual_return = mean_return * periods_per_year
        annual_std = std_dev * math.sqrt(periods_per_year)
        
        sharpe = (annual_return - float(risk_free_rate)) / annual_std
        
        return Decimal(str(sharpe))
    
    @staticmethod
    def sortino_ratio(
        returns: List[Decimal],
        risk_free_rate: Decimal = Decimal('0.02'),
        periods_per_year: int = 252
    ) -> Decimal:
        """
        Calculate Sortino ratio (uses downside deviation).
        
        Args:
            returns: List of period returns
            risk_free_rate: Annual risk-free rate
            periods_per_year: Trading periods per year
        
        Returns:
            Sortino ratio
        """
        if not returns or len(returns) < 2:
            return Decimal('0')
        
        returns_float = [float(r) for r in returns]
        mean_return = sum(returns_float) / len(returns_float)
        
        # Calculate downside deviation (only negative returns)
        downside_returns = [r for r in returns_float if r < 0]
        
        if not downside_returns:
            return Decimal('999')  # No downside = very high Sortino
        
        downside_variance = sum(r ** 2 for r in downside_returns) / len(returns_float)
        downside_std = math.sqrt(downside_variance)
        
        if downside_std == 0:
            return Decimal('0')
        
        # Annualize
        annual_return = mean_return * periods_per_year
        annual_downside_std = downside_std * math.sqrt(periods_per_year)
        
        sortino = (annual_return - float(risk_free_rate)) / annual_downside_std
        
        return Decimal(str(sortino))
    
    @staticmethod
    def max_drawdown(
        equity_curve: List[Tuple[datetime, Decimal]]
    ) -> Tuple[Decimal, int]:
        """
        Calculate maximum drawdown and its duration.
        
        Args:
            equity_curve: List of (timestamp, equity) tuples
        
        Returns:
            Tuple of (max_drawdown, duration_in_days)
        """
        if not equity_curve:
            return Decimal('0'), 0
        
        max_dd = Decimal('0')
        peak = equity_curve[0][1]
        peak_time = equity_curve[0][0]
        max_dd_duration = 0
        current_dd_start = None
        
        for timestamp, equity in equity_curve:
            if equity > peak:
                peak = equity
                peak_time = timestamp
                current_dd_start = None
            else:
                dd = (peak - equity) / peak
                if dd > max_dd:
                    max_dd = dd
                    if current_dd_start is None:
                        current_dd_start = peak_time
                    duration = (timestamp - current_dd_start).days
                    if duration > max_dd_duration:
                        max_dd_duration = duration
        
        return max_dd, max_dd_duration
    
    @staticmethod
    def win_rate(trades: List[Trade]) -> Decimal:
        """Calculate win rate."""
        if not trades:
            return Decimal('0')
        
        winning_trades = sum(
            1 for t in trades
            if t.realized_pnl and t.realized_pnl > 0
        )
        
        return Decimal(str(winning_trades)) / Decimal(str(len(trades)))
    
    @staticmethod
    def profit_factor(trades: List[Trade]) -> Decimal:
        """
        Calculate profit factor (gross profit / gross loss).
        
        Returns:
            Profit factor
        """
        gross_profit = sum(
            t.realized_pnl for t in trades
            if t.realized_pnl and t.realized_pnl > 0
        )
        
        gross_loss = abs(sum(
            t.realized_pnl for t in trades
            if t.realized_pnl and t.realized_pnl < 0
        ))
        
        if gross_loss == 0:
            return Decimal('999') if gross_profit > 0 else Decimal('0')
        
        return gross_profit / gross_loss
    
    @staticmethod
    def average_win_loss(trades: List[Trade]) -> Tuple[Decimal, Decimal]:
        """
        Calculate average win and average loss.
        
        Returns:
            Tuple of (average_win, average_loss)
        """
        winning_trades = [
            t.realized_pnl for t in trades
            if t.realized_pnl and t.realized_pnl > 0
        ]
        
        losing_trades = [
            t.realized_pnl for t in trades
            if t.realized_pnl and t.realized_pnl < 0
        ]
        
        avg_win = (
            sum(winning_trades) / Decimal(str(len(winning_trades)))
            if winning_trades else Decimal('0')
        )
        
        avg_loss = (
            sum(losing_trades) / Decimal(str(len(losing_trades)))
            if losing_trades else Decimal('0')
        )
        
        return avg_win, avg_loss
    
    @staticmethod
    def calmar_ratio(total_return: Decimal, max_drawdown: Decimal) -> Decimal:
        """
        Calculate Calmar ratio (return / max drawdown).
        
        Args:
            total_return: Total return
            max_drawdown: Maximum drawdown
        
        Returns:
            Calmar ratio
        """
        if max_drawdown == 0:
            return Decimal('999') if total_return > 0 else Decimal('0')
        
        return total_return / max_drawdown
    
    @staticmethod
    def _calculate_returns(
        equity_curve: List[Tuple[datetime, Decimal]]
    ) -> List[Decimal]:
        """Calculate period returns from equity curve."""
        if len(equity_curve) < 2:
            return []
        
        returns = []
        for i in range(1, len(equity_curve)):
            prev_equity = equity_curve[i-1][1]
            curr_equity = equity_curve[i][1]
            
            if prev_equity > 0:
                ret = (curr_equity - prev_equity) / prev_equity
                returns.append(ret)
        
        return returns
    
    @staticmethod
    def _empty_metrics() -> Dict:
        """Return empty metrics dict."""
        return {
            'total_return': 0.0,
            'total_return_pct': 0.0,
            'sharpe_ratio': 0.0,
            'sortino_ratio': 0.0,
            'max_drawdown': 0.0,
            'max_drawdown_pct': 0.0,
            'max_drawdown_duration_days': 0,
            'win_rate': 0.0,
            'win_rate_pct': 0.0,
            'profit_factor': 0.0,
            'average_win': 0.0,
            'average_loss': 0.0,
            'calmar_ratio': 0.0,
            'total_trades': 0,
            'winning_trades': 0,
            'losing_trades': 0
        }
