"""
Value Object - Quantity
Representa una cantidad/volumen con precisión decimal
"""
from dataclasses import dataclass
from decimal import Decimal, ROUND_DOWN
from typing import Union
from ..exceptions import InvalidQuantityError


@dataclass(frozen=True)
class Quantity:
    """
    Value object que representa una cantidad/volumen.
    Usa Decimal internamente para precisión.
    
    Examples:
        >>> qty = Quantity(1.5)
        >>> qty.value
        Decimal('1.5')
        >>> qty * 2
        Quantity(Decimal('3.0'))
    """
    
    value: Decimal
    
    def __init__(self, value: Union[float, int, str, Decimal]):
        """
        Inicializa una Quantity.
        
        Args:
            value: Valor de la cantidad
        
        Raises:
            InvalidQuantityError: Si la cantidad es negativa o cero
        """
        if isinstance(value, Decimal):
            decimal_value = value
        else:
            decimal_value = Decimal(str(value))
        
        if decimal_value <= 0:
            raise InvalidQuantityError(float(decimal_value), "Quantity must be positive")
        
        object.__setattr__(self, 'value', decimal_value)
    
    def __str__(self) -> str:
        return str(self.value)
    
    def __repr__(self) -> str:
        return f"Quantity({self.value})"
    
    def __float__(self) -> float:
        return float(self.value)
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Quantity):
            return self.value == other.value
        return False
    
    def __lt__(self, other: 'Quantity') -> bool:
        return self.value < other.value
    
    def __le__(self, other: 'Quantity') -> bool:
        return self.value <= other.value
    
    def __gt__(self, other: 'Quantity') -> bool:
        return self.value > other.value
    
    def __ge__(self, other: 'Quantity') -> bool:
        return self.value >= other.value
    
    def __add__(self, other: Union['Quantity', Decimal, float, int]) -> 'Quantity':
        """Suma de cantidades"""
        if isinstance(other, Quantity):
            return Quantity(self.value + other.value)
        return Quantity(self.value + Decimal(str(other)))
    
    def __sub__(self, other: Union['Quantity', Decimal, float, int]) -> 'Quantity':
        """Resta de cantidades"""
        if isinstance(other, Quantity):
            result = self.value - other.value
        else:
            result = self.value - Decimal(str(other))
        
        if result <= 0:
            raise InvalidQuantityError(float(result), "Result must be positive")
        return Quantity(result)
    
    def __mul__(self, other: Union[Decimal, float, int]) -> 'Quantity':
        """Multiplicación por escalar"""
        return Quantity(self.value * Decimal(str(other)))
    
    def __truediv__(self, other: Union[Decimal, float, int]) -> 'Quantity':
        """División por escalar"""
        return Quantity(self.value / Decimal(str(other)))
    
    def round(self, precision: int = 8) -> 'Quantity':
        """
        Redondea la cantidad a la precisión especificada.
        Usa ROUND_DOWN para evitar exceder cantidades disponibles.
        
        Args:
            precision: Número de decimales
        
        Returns:
            Nueva Quantity redondeada
        
        Examples:
            >>> Quantity(1.123456789).round(4)
            Quantity(Decimal('1.1234'))
        """
        quantize_value = Decimal('0.1') ** precision
        rounded = self.value.quantize(quantize_value, rounding=ROUND_DOWN)
        
        if rounded <= 0:
            raise InvalidQuantityError(float(rounded), "Rounded quantity must be positive")
        
        return Quantity(rounded)
    
    def is_greater_than(self, other: 'Quantity') -> bool:
        """Verifica si esta cantidad es mayor que otra"""
        return self.value > other.value
    
    def is_less_than(self, other: 'Quantity') -> bool:
        """Verifica si esta cantidad es menor que otra"""
        return self.value < other.value
    
    @classmethod
    def from_notional(cls, notional: Decimal, price: Decimal) -> 'Quantity':
        """
        Crea una Quantity desde un valor nocional y precio.
        
        Args:
            notional: Valor nocional (ej: 1000 USDT)
            price: Precio unitario
        
        Returns:
            Quantity calculada
        
        Examples:
            >>> Quantity.from_notional(Decimal('1000'), Decimal('50000'))
            Quantity(Decimal('0.02'))
        """
        if price <= 0:
            raise InvalidQuantityError(0, "Price must be positive")
        
        quantity = notional / price
        return cls(quantity)
