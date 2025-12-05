"""
Domain Enums - Order Type
Tipos de órdenes soportadas por el sistema
"""
from enum import Enum


class OrderType(str, Enum):
    """Tipo de orden de trading"""
    
    MARKET = "MARKET"           # Orden a mercado (ejecución inmediata)
    LIMIT = "LIMIT"             # Orden límite (precio específico)
    STOP_LOSS = "STOP_LOSS"     # Stop loss (se activa al alcanzar precio)
    STOP_LOSS_LIMIT = "STOP_LOSS_LIMIT"  # Stop loss con límite
    TAKE_PROFIT = "TAKE_PROFIT"          # Take profit
    TAKE_PROFIT_LIMIT = "TAKE_PROFIT_LIMIT"  # Take profit con límite
    LIMIT_MAKER = "LIMIT_MAKER"          # Limit maker (solo maker fees)
    
    def __str__(self) -> str:
        return self.value
    
    @property
    def requires_price(self) -> bool:
        """Indica si este tipo de orden requiere precio"""
        return self in {
            OrderType.LIMIT,
            OrderType.STOP_LOSS_LIMIT,
            OrderType.TAKE_PROFIT_LIMIT,
            OrderType.LIMIT_MAKER
        }
    
    @property
    def requires_stop_price(self) -> bool:
        """Indica si este tipo de orden requiere stop price"""
        return self in {
            OrderType.STOP_LOSS,
            OrderType.STOP_LOSS_LIMIT,
            OrderType.TAKE_PROFIT,
            OrderType.TAKE_PROFIT_LIMIT
        }
    
    @property
    def is_market_order(self) -> bool:
        """Indica si es una orden de mercado"""
        return self == OrderType.MARKET
