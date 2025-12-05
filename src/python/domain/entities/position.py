"""
Domain Entity - Position
Representa una posición abierta en un símbolo
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from decimal import Decimal
from enum import Enum

from ..enums import OrderSide
from ..value_objects import Symbol, Price, Quantity, Money
from ..exceptions import ValidationError


class PositionSide(str, Enum):
    """Lado de la posición"""
    LONG = "LONG"
    SHORT = "SHORT"
    
    @classmethod
    def from_order_side(cls, order_side: OrderSide) -> 'PositionSide':
        """Convierte OrderSide a PositionSide"""
        return cls.LONG if order_side == OrderSide.BUY else cls.SHORT


@dataclass
class Position:
    """
    Entidad que representa una posición abierta.
    
    Una posición es el resultado de una o más órdenes ejecutadas.
    Mantiene tracking de PnL realizado y no realizado.
    
    Examples:
        >>> position = Position.open(
        ...     symbol=Symbol("BTC", "USDT"),
        ...     side=PositionSide.LONG,
        ...     quantity=Quantity(0.1),
        ...     entry_price=Price(50000)
        ... )
        >>> position.calculate_unrealized_pnl(Price(51000))
        Money(Decimal('100'), 'USDT')
    """
    
    # Identidad
    symbol: Symbol
    side: PositionSide
    
    # Cantidad
    quantity: Quantity
    
    # Precios
    entry_price: Price
    current_price: Optional[Price] = None
    
    # PnL
    realized_pnl: Money = field(default_factory=lambda: Money(0, "USDT"))
    unrealized_pnl: Money = field(default_factory=lambda: Money(0, "USDT"))
    
    # Fees
    total_fees: Money = field(default_factory=lambda: Money(0, "USDT"))
    
    # Timestamps
    opened_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    closed_at: Optional[datetime] = None
    
    # Estado
    is_open: bool = True
    
    @classmethod
    def open(
        cls,
        symbol: Symbol,
        side: PositionSide,
        quantity: Quantity,
        entry_price: Price,
        fees: Optional[Money] = None
    ) -> 'Position':
        """
        Abre una nueva posición.
        
        Args:
            symbol: Símbolo
            side: LONG o SHORT
            quantity: Cantidad
            entry_price: Precio de entrada
            fees: Fees pagadas
        
        Returns:
            Nueva posición
        """
        position = cls(
            symbol=symbol,
            side=side,
            quantity=quantity,
            entry_price=entry_price,
            current_price=entry_price
        )
        
        if fees:
            position.total_fees = fees
        
        return position
    
    def update_price(self, current_price: Price):
        """
        Actualiza el precio actual y recalcula PnL no realizado.
        
        Args:
            current_price: Precio actual del mercado
        """
        self.current_price = current_price
        self.unrealized_pnl = self.calculate_unrealized_pnl(current_price)
        self.updated_at = datetime.utcnow()
    
    def increase(self, quantity: Quantity, price: Price, fees: Optional[Money] = None):
        """
        Incrementa la posición (averaging).
        
        Args:
            quantity: Cantidad adicional
            price: Precio de la nueva entrada
            fees: Fees adicionales
        """
        if not self.is_open:
            raise ValidationError("position", "closed", "Cannot increase a closed position")
        
        # Calcular nuevo precio promedio
        total_cost = (self.quantity.value * self.entry_price.value) + (quantity.value * price.value)
        new_quantity = self.quantity + quantity
        new_avg_price = Price(total_cost / new_quantity.value)
        
        self.quantity = new_quantity
        self.entry_price = new_avg_price
        
        if fees:
            self.total_fees = self.total_fees + fees
        
        self.updated_at = datetime.utcnow()
    
    def decrease(self, quantity: Quantity, exit_price: Price, fees: Optional[Money] = None) -> Money:
        """
        Reduce la posición (cierre parcial).
        
        Args:
            quantity: Cantidad a cerrar
            exit_price: Precio de salida
            fees: Fees de la operación
        
        Returns:
            PnL realizado de la porción cerrada
        """
        if not self.is_open:
            raise ValidationError("position", "closed", "Cannot decrease a closed position")
        
        if quantity > self.quantity:
            raise ValidationError(
                "quantity",
                quantity,
                f"Cannot decrease by {quantity}, position size is {self.quantity}"
            )
        
        # Calcular PnL realizado
        pnl = self._calculate_pnl(quantity, self.entry_price, exit_price)
        
        # Actualizar posición
        self.quantity = self.quantity - quantity
        self.realized_pnl = self.realized_pnl + pnl
        
        if fees:
            self.total_fees = self.total_fees + fees
            self.realized_pnl = self.realized_pnl - fees
        
        # Si la cantidad es cero, cerrar posición
        if self.quantity.value < Decimal('0.00000001'):  # Threshold muy pequeño
            self.close()
        
        self.updated_at = datetime.utcnow()
        return pnl
    
    def close(self, exit_price: Optional[Price] = None, fees: Optional[Money] = None) -> Money:
        """
        Cierra completamente la posición.
        
        Args:
            exit_price: Precio de salida (si None, usa current_price)
            fees: Fees de cierre
        
        Returns:
            PnL total realizado
        """
        if not self.is_open:
            raise ValidationError("position", "closed", "Position is already closed")
        
        price = exit_price or self.current_price
        if not price:
            raise ValidationError("exit_price", None, "Exit price is required")
        
        # Calcular PnL final
        pnl = self._calculate_pnl(self.quantity, self.entry_price, price)
        self.realized_pnl = self.realized_pnl + pnl
        
        if fees:
            self.total_fees = self.total_fees + fees
            self.realized_pnl = self.realized_pnl - fees
        
        # Marcar como cerrada
        self.is_open = False
        self.closed_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.quantity = Quantity(0.01)  # Reset a mínimo
        
        return self.realized_pnl
    
    def calculate_unrealized_pnl(self, current_price: Price) -> Money:
        """
        Calcula el PnL no realizado.
        
        Args:
            current_price: Precio actual del mercado
        
        Returns:
            PnL no realizado
        """
        if not self.is_open:
            return Money(0, self.realized_pnl.currency)
        
        return self._calculate_pnl(self.quantity, self.entry_price, current_price)
    
    def _calculate_pnl(self, quantity: Quantity, entry: Price, exit: Price) -> Money:
        """
        Calcula PnL para una cantidad específica.
        
        Args:
            quantity: Cantidad
            entry: Precio de entrada
            exit: Precio de salida
        
        Returns:
            PnL calculado
        """
        price_diff = exit.value - entry.value
        
        # Para SHORT, el PnL es inverso
        if self.side == PositionSide.SHORT:
            price_diff = -price_diff
        
        pnl_value = quantity.value * price_diff
        return Money(pnl_value, self.symbol.quote)
    
    @property
    def total_pnl(self) -> Money:
        """PnL total (realizado + no realizado)"""
        return self.realized_pnl + self.unrealized_pnl
    
    @property
    def pnl_percentage(self) -> Decimal:
        """PnL como porcentaje del capital invertido"""
        invested = self.quantity.value * self.entry_price.value
        if invested == 0:
            return Decimal('0')
        return (self.total_pnl.amount / invested) * 100
    
    @property
    def notional_value(self) -> Decimal:
        """Valor nocional de la posición"""
        price = self.current_price or self.entry_price
        return self.quantity.value * price.value
    
    def __repr__(self) -> str:
        return (
            f"Position(symbol={self.symbol}, "
            f"side={self.side}, "
            f"qty={self.quantity}, "
            f"entry={self.entry_price}, "
            f"pnl={self.total_pnl})"
        )
