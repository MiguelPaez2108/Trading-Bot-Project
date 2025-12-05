"""
Domain Entity - Order
Representa una orden de trading
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from decimal import Decimal
import uuid

from ..enums import OrderSide, OrderType, OrderStatus, ExchangeType
from ..value_objects import Symbol, Price, Quantity
from ..exceptions import InvalidOrderError, ValidationError


@dataclass
class Order:
    """
    Entidad que representa una orden de trading.
    
    Esta es una entidad del dominio con identidad única (order_id).
    Contiene toda la lógica de negocio relacionada con órdenes.
    
    Examples:
        >>> order = Order.create_market_order(
        ...     symbol=Symbol("BTC", "USDT"),
        ...     side=OrderSide.BUY,
        ...     quantity=Quantity(0.1)
        ... )
        >>> order.is_active
        True
    """
    
    # Identidad
    order_id: str
    
    # Atributos básicos
    symbol: Symbol
    side: OrderSide
    order_type: OrderType
    quantity: Quantity
    
    # Precios (opcionales según tipo de orden)
    price: Optional[Price] = None
    stop_price: Optional[Price] = None
    
    # Estado
    status: OrderStatus = OrderStatus.PENDING
    filled_quantity: Quantity = field(default_factory=lambda: Quantity(0.01))
    
    # Metadata
    exchange: Optional[ExchangeType] = None
    exchange_order_id: Optional[str] = None
    client_order_id: Optional[str] = None
    
    # Timestamps
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    filled_at: Optional[datetime] = None
    
    # Fees y costos
    commission: Decimal = Decimal('0')
    commission_asset: str = "USDT"
    
    def __post_init__(self):
        """Validación post-inicialización"""
        self._validate()
    
    def _validate(self):
        """Valida la orden según reglas de negocio"""
        # Validar que price esté presente si es requerido
        if self.order_type.requires_price and not self.price:
            raise InvalidOrderError(
                f"Order type {self.order_type} requires price",
                self.order_id
            )
        
        # Validar que stop_price esté presente si es requerido
        if self.order_type.requires_stop_price and not self.stop_price:
            raise InvalidOrderError(
                f"Order type {self.order_type} requires stop_price",
                self.order_id
            )
        
        # Validar que filled_quantity no exceda quantity
        if self.filled_quantity > self.quantity:
            raise InvalidOrderError(
                f"Filled quantity {self.filled_quantity} exceeds order quantity {self.quantity}",
                self.order_id
            )
    
    @classmethod
    def create_market_order(
        cls,
        symbol: Symbol,
        side: OrderSide,
        quantity: Quantity,
        exchange: Optional[ExchangeType] = None
    ) -> 'Order':
        """
        Crea una orden de mercado.
        
        Args:
            symbol: Símbolo a tradear
            side: BUY o SELL
            quantity: Cantidad a tradear
            exchange: Exchange donde ejecutar
        
        Returns:
            Nueva orden de mercado
        """
        return cls(
            order_id=str(uuid.uuid4()),
            symbol=symbol,
            side=side,
            order_type=OrderType.MARKET,
            quantity=quantity,
            exchange=exchange,
            client_order_id=f"market_{uuid.uuid4().hex[:8]}"
        )
    
    @classmethod
    def create_limit_order(
        cls,
        symbol: Symbol,
        side: OrderSide,
        quantity: Quantity,
        price: Price,
        exchange: Optional[ExchangeType] = None
    ) -> 'Order':
        """
        Crea una orden límite.
        
        Args:
            symbol: Símbolo a tradear
            side: BUY o SELL
            quantity: Cantidad a tradear
            price: Precio límite
            exchange: Exchange donde ejecutar
        
        Returns:
            Nueva orden límite
        """
        return cls(
            order_id=str(uuid.uuid4()),
            symbol=symbol,
            side=side,
            order_type=OrderType.LIMIT,
            quantity=quantity,
            price=price,
            exchange=exchange,
            client_order_id=f"limit_{uuid.uuid4().hex[:8]}"
        )
    
    @classmethod
    def create_stop_loss_order(
        cls,
        symbol: Symbol,
        side: OrderSide,
        quantity: Quantity,
        stop_price: Price,
        exchange: Optional[ExchangeType] = None
    ) -> 'Order':
        """
        Crea una orden stop-loss.
        
        Args:
            symbol: Símbolo a tradear
            side: BUY o SELL
            quantity: Cantidad a tradear
            stop_price: Precio de activación del stop
            exchange: Exchange donde ejecutar
        
        Returns:
            Nueva orden stop-loss
        """
        return cls(
            order_id=str(uuid.uuid4()),
            symbol=symbol,
            side=side,
            order_type=OrderType.STOP_LOSS,
            quantity=quantity,
            stop_price=stop_price,
            exchange=exchange,
            client_order_id=f"stop_{uuid.uuid4().hex[:8]}"
        )
    
    # Métodos de negocio
    
    def submit(self, exchange_order_id: str):
        """Marca la orden como enviada al exchange"""
        if self.status != OrderStatus.PENDING:
            raise InvalidOrderError(
                f"Cannot submit order in status {self.status}",
                self.order_id
            )
        
        self.status = OrderStatus.SUBMITTED
        self.exchange_order_id = exchange_order_id
        self.updated_at = datetime.utcnow()
    
    def fill(self, filled_qty: Quantity, commission: Decimal = Decimal('0')):
        """
        Registra un fill (ejecución parcial o total).
        
        Args:
            filled_qty: Cantidad ejecutada
            commission: Comisión cobrada
        """
        if not self.is_active:
            raise InvalidOrderError(
                f"Cannot fill order in status {self.status}",
                self.order_id
            )
        
        self.filled_quantity = self.filled_quantity + filled_qty
        self.commission = self.commission + commission
        self.updated_at = datetime.utcnow()
        
        # Actualizar estado
        if self.filled_quantity >= self.quantity:
            self.status = OrderStatus.FILLED
            self.filled_at = datetime.utcnow()
        elif self.filled_quantity > Quantity(0.01):
            self.status = OrderStatus.PARTIALLY_FILLED
    
    def cancel(self):
        """Cancela la orden"""
        if not self.is_active:
            raise InvalidOrderError(
                f"Cannot cancel order in status {self.status}",
                self.order_id
            )
        
        self.status = OrderStatus.CANCELLED
        self.updated_at = datetime.utcnow()
    
    def reject(self, reason: str = ""):
        """Marca la orden como rechazada"""
        self.status = OrderStatus.REJECTED
        self.updated_at = datetime.utcnow()
    
    # Propiedades calculadas
    
    @property
    def is_active(self) -> bool:
        """Indica si la orden está activa"""
        return self.status.is_active
    
    @property
    def is_filled(self) -> bool:
        """Indica si la orden está completamente ejecutada"""
        return self.status.is_filled
    
    @property
    def is_terminal(self) -> bool:
        """Indica si la orden está en estado terminal"""
        return self.status.is_terminal
    
    @property
    def remaining_quantity(self) -> Quantity:
        """Cantidad pendiente de ejecutar"""
        return self.quantity - self.filled_quantity
    
    @property
    def fill_percentage(self) -> Decimal:
        """Porcentaje de ejecución (0.0 a 1.0)"""
        return self.filled_quantity.value / self.quantity.value
    
    @property
    def notional_value(self) -> Optional[Decimal]:
        """Valor nocional de la orden (quantity * price)"""
        if self.price:
            return self.quantity.value * self.price.value
        return None
    
    def __repr__(self) -> str:
        return (
            f"Order(id={self.order_id[:8]}, "
            f"symbol={self.symbol}, "
            f"side={self.side}, "
            f"type={self.order_type}, "
            f"qty={self.quantity}, "
            f"status={self.status})"
        )
