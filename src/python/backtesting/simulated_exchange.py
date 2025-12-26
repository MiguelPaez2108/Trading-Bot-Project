"""
Simulated Exchange for Backtesting.

Mimics real exchange behavior for realistic backtesting.
"""
from typing import Dict, List, Optional
from decimal import Decimal
from datetime import datetime
import logging

from src.python.domain.entities.order import Order, OrderSide, OrderType, OrderStatus
from src.python.domain.entities.trade import Trade
from src.python.domain.entities.candle import Candle
from src.python.domain.value_objects.symbol import TradingPair

logger = logging.getLogger(__name__)


class SimulatedExchange:
    """
    Simulates exchange behavior for backtesting.
    
    Features:
    - Order matching against historical candles
    - Slippage simulation
    - Fee calculation
    - Realistic fill prices
    """
    
    def __init__(
        self,
        maker_fee: Decimal = Decimal('0.001'),  # 0.1%
        taker_fee: Decimal = Decimal('0.001'),  # 0.1%
        slippage_pct: Decimal = Decimal('0.0005')  # 0.05%
    ):
        """
        Initialize simulated exchange.
        
        Args:
            maker_fee: Maker fee percentage
            taker_fee: Taker fee percentage
            slippage_pct: Slippage percentage
        """
        self.maker_fee = maker_fee
        self.taker_fee = taker_fee
        self.slippage_pct = slippage_pct
        
        # State
        self.pending_orders: Dict[str, Order] = {}  # order_id -> Order
        self.filled_orders: List[Order] = []
        self.trades: List[Trade] = []
    
    def place_order(self, order: Order) -> bool:
        """
        Place an order.
        
        Args:
            order: Order to place
        
        Returns:
            True if order placed successfully
        """
        order.update_status(OrderStatus.OPEN)
        self.pending_orders[str(order.id)] = order
        logger.debug(f"Placed order: {order}")
        return True
    
    def cancel_order(self, order_id: str) -> bool:
        """
        Cancel a pending order.
        
        Args:
            order_id: Order ID
        
        Returns:
            True if cancelled
        """
        order = self.pending_orders.get(order_id)
        if order:
            order.update_status(OrderStatus.CANCELLED)
            del self.pending_orders[order_id]
            logger.debug(f"Cancelled order: {order_id}")
            return True
        return False
    
    def match_orders(self, candle: Candle) -> List[Trade]:
        """
        Match pending orders against current candle.
        
        Args:
            candle: Current candle
        
        Returns:
            List of executed trades
        """
        trades = []
        filled_order_ids = []
        
        for order_id, order in self.pending_orders.items():
            # Only match orders for this symbol
            if order.symbol != candle.symbol:
                continue
            
            # Try to fill order
            fill_price = self._get_fill_price(order, candle)
            
            if fill_price is not None:
                # Create trade
                trade = self._create_trade(order, fill_price, candle.time)
                trades.append(trade)
                self.trades.append(trade)
                
                # Update order
                order.update_fill(order.size, fill_price)
                order.update_status(OrderStatus.FILLED)
                
                self.filled_orders.append(order)
                filled_order_ids.append(order_id)
                
                logger.debug(f"Filled order: {order_id} at {fill_price}")
        
        # Remove filled orders from pending
        for order_id in filled_order_ids:
            del self.pending_orders[order_id]
        
        return trades
    
    def _get_fill_price(
        self,
        order: Order,
        candle: Candle
    ) -> Optional[Decimal]:
        """
        Determine if order can be filled and at what price.
        
        Args:
            order: Order to fill
            candle: Current candle
        
        Returns:
            Fill price or None if not fillable
        """
        if order.order_type == OrderType.MARKET:
            # Market orders fill at current price + slippage
            base_price = candle.close
            slippage = base_price * self.slippage_pct
            
            if order.side == OrderSide.BUY:
                return base_price + slippage
            else:
                return base_price - slippage
        
        elif order.order_type == OrderType.LIMIT:
            # Limit orders fill if price touched the limit
            if order.side == OrderSide.BUY:
                # Buy limit: fill if low <= limit price
                if candle.low <= order.price:  # type: ignore[operator]
                    return order.price
            else:
                # Sell limit: fill if high >= limit price
                if candle.high >= order.price:  # type: ignore[operator]
                    return order.price
        
        return None
    
    def _create_trade(
        self,
        order: Order,
        fill_price: Decimal,
        executed_at: datetime
    ) -> Trade:
        """
        Create trade from filled order.
        
        Args:
            order: Filled order
            fill_price: Fill price
            executed_at: Execution timestamp
        
        Returns:
            Trade
        """
        # Calculate commission
        notional = order.size * fill_price  # type: ignore[operator]
        
        # Use taker fee for market orders, maker fee for limit orders
        fee_rate = self.taker_fee if order.order_type == OrderType.MARKET else self.maker_fee
        commission = notional * fee_rate
        
        return Trade(
            order_id=order.id,
            symbol=order.symbol,
            side=order.side.value,
            price=fill_price,
            size=order.size,
            commission=commission,
            commission_asset="USDT",
            executed_at=executed_at
        )
    
    def get_pending_orders(self, symbol: Optional[TradingPair] = None) -> List[Order]:
        """
        Get pending orders.
        
        Args:
            symbol: Filter by symbol (optional)
        
        Returns:
            List of pending orders
        """
        if symbol is None:
            return list(self.pending_orders.values())
        
        return [
            order for order in self.pending_orders.values()
            if order.symbol == symbol
        ]
    
    def reset(self) -> None:
        """Reset exchange state."""
        self.pending_orders = {}
        self.filled_orders = []
        self.trades = []
