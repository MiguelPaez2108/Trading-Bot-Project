"""
Domain Enums - Order Status
Estados posibles de una orden en su ciclo de vida
"""
from enum import Enum


class OrderStatus(str, Enum):
    """Estado de una orden de trading"""
    
    PENDING = "PENDING"               # Orden creada pero no enviada
    SUBMITTED = "SUBMITTED"           # Orden enviada al exchange
    PARTIALLY_FILLED = "PARTIALLY_FILLED"  # Orden parcialmente ejecutada
    FILLED = "FILLED"                 # Orden completamente ejecutada
    CANCELLED = "CANCELLED"           # Orden cancelada
    REJECTED = "REJECTED"             # Orden rechazada por el exchange
    EXPIRED = "EXPIRED"               # Orden expirada
    
    def __str__(self) -> str:
        return self.value
    
    @property
    def is_active(self) -> bool:
        """Indica si la orden está activa (puede recibir fills)"""
        return self in {
            OrderStatus.PENDING,
            OrderStatus.SUBMITTED,
            OrderStatus.PARTIALLY_FILLED
        }
    
    @property
    def is_terminal(self) -> bool:
        """Indica si la orden está en estado terminal (no cambiará más)"""
        return self in {
            OrderStatus.FILLED,
            OrderStatus.CANCELLED,
            OrderStatus.REJECTED,
            OrderStatus.EXPIRED
        }
    
    @property
    def is_filled(self) -> bool:
        """Indica si la orden está completamente ejecutada"""
        return self == OrderStatus.FILLED
