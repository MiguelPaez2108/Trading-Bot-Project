"""
Domain Entity - Trade
Representa una ejecución/fill de una orden
"""
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
import uuid

from ..enums import OrderSide
from ..value_objects import Symbol, Price, Quantity, Money


@dataclass
class Trade:
    """
    Entidad que representa un trade (fill de una orden).
    
    Un trade es el resultado de una orden ejecutada (parcial o totalmente).
    Es inmutable una vez creado.
    
    Examples:
        >>> trade = Trade.create(
        ...     symbol=Symbol("BTC", "USDT"),
        ...     side=OrderSide.BUY,
        ...     quantity=Quantity(0.1),
        ...     price=Price(50000),
        ...     order_id="order123"
        ... )
        >>> trade.notional_value
        Decimal('5000')
    """
    
    # Identidad
    trade_id: str
    order_id: str
    
    # Datos del trade
    symbol: Symbol
    side: OrderSide
    quantity: Quantity
    price: Price
    
    # Fees
    commission: Money
    commission_asset: str = "USDT"
    
    # Metadata
    exchange_trade_id: Optional[str] = None
    is_maker: bool = False  # True si fue maker, False si fue taker
    
    # Timestamp
    executed_at: datetime = field(default_factory=datetime.utcnow)
    
    @classmethod
    def create(
        cls,
        symbol: Symbol,
        side: OrderSide,
        quantity: Quantity,
        price: Price,
        order_id: str,
        commission: Optional[Money] = None,
        is_maker: bool = False,
        exchange_trade_id: Optional[str] = None
    ) -> 'Trade':
        """
        Crea un nuevo trade.
        
        Args:
            symbol: Símbolo tradeado
            side: BUY o SELL
            quantity: Cantidad ejecutada
            price: Precio de ejecución
            order_id: ID de la orden padre
            commission: Comisión pagada
            is_maker: Si fue maker o taker
            exchange_trade_id: ID del trade en el exchange
        
        Returns:
            Nuevo trade
        """
        if commission is None:
            commission = Money(0, symbol.quote)
        
        return cls(
            trade_id=str(uuid.uuid4()),
            order_id=order_id,
            symbol=symbol,
            side=side,
            quantity=quantity,
            price=price,
            commission=commission,
            is_maker=is_maker,
            exchange_trade_id=exchange_trade_id
        )
    
    @property
    def notional_value(self) -> Decimal:
        """Valor nocional del trade (quantity * price)"""
        return self.quantity.value * self.price.value
    
    @property
    def net_value(self) -> Money:
        """Valor neto después de comisiones"""
        gross = Money(self.notional_value, self.symbol.quote)
        return gross - self.commission
    
    @property
    def commission_percentage(self) -> Decimal:
        """Comisión como porcentaje del valor nocional"""
        if self.notional_value == 0:
            return Decimal('0')
        return (self.commission.amount / self.notional_value) * 100
    
    def __repr__(self) -> str:
        return (
            f"Trade(id={self.trade_id[:8]}, "
            f"symbol={self.symbol}, "
            f"side={self.side}, "
            f"qty={self.quantity}, "
            f"price={self.price}, "
            f"value={self.notional_value})"
        )


# Necesitamos importar Optional
from typing import Optional
