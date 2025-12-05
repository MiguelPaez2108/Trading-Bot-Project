"""
Domain Enums - Order Side
Representa el lado de una orden: BUY o SELL
"""
from enum import Enum


class OrderSide(str, Enum):
    """Lado de la orden de trading"""
    
    BUY = "BUY"
    SELL = "SELL"
    
    def __str__(self) -> str:
        return self.value
    
    def opposite(self) -> 'OrderSide':
        """Retorna el lado opuesto"""
        return OrderSide.SELL if self == OrderSide.BUY else OrderSide.BUY
    
    @property
    def multiplier(self) -> int:
        """Retorna 1 para BUY, -1 para SELL (útil para cálculos de PnL)"""
        return 1 if self == OrderSide.BUY else -1
