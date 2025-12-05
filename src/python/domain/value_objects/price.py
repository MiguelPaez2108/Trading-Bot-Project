"""
Value Object - Price
Representa un precio con precisión decimal
"""
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from typing import Union
from ..exceptions import InvalidPriceError


@dataclass(frozen=True)
class Price:
    """
    Value object que representa un precio.
    Usa Decimal internamente para evitar problemas de precisión de punto flotante.
    
    Examples:
        >>> price = Price(50000.50)
        >>> price.value
        Decimal('50000.50')
        >>> price * 2
        Price(Decimal('100001.00'))
    """
    
    value: Decimal
    
    def __init__(self, value: Union[float, int, str, Decimal]):
        """
        Inicializa un Price.
        
        Args:
            value: Valor del precio (float, int, str, o Decimal)
        
        Raises:
            InvalidPriceError: Si el precio es negativo o cero
        """
        if isinstance(value, Decimal):
            decimal_value = value
        else:
            decimal_value = Decimal(str(value))
        
        if decimal_value <= 0:
            raise InvalidPriceError(float(decimal_value), "Price must be positive")
        
        object.__setattr__(self, 'value', decimal_value)
    
    def __str__(self) -> str:
        return str(self.value)
    
    def __repr__(self) -> str:
        return f"Price({self.value})"
    
    def __float__(self) -> float:
        return float(self.value)
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Price):
            return self.value == other.value
        return False
    
    def __lt__(self, other: 'Price') -> bool:
        return self.value < other.value
    
    def __le__(self, other: 'Price') -> bool:
        return self.value <= other.value
    
    def __gt__(self, other: 'Price') -> bool:
        return self.value > other.value
    
    def __ge__(self, other: 'Price') -> bool:
        return self.value >= other.value
    
    def __add__(self, other: Union['Price', Decimal, float, int]) -> 'Price':
        """Suma de precios"""
        if isinstance(other, Price):
            return Price(self.value + other.value)
        return Price(self.value + Decimal(str(other)))
    
    def __sub__(self, other: Union['Price', Decimal, float, int]) -> 'Price':
        """Resta de precios"""
        if isinstance(other, Price):
            result = self.value - other.value
        else:
            result = self.value - Decimal(str(other))
        
        if result <= 0:
            raise InvalidPriceError(float(result), "Result must be positive")
        return Price(result)
    
    def __mul__(self, other: Union[Decimal, float, int]) -> 'Price':
        """Multiplicación por escalar"""
        return Price(self.value * Decimal(str(other)))
    
    def __truediv__(self, other: Union[Decimal, float, int]) -> 'Price':
        """División por escalar"""
        return Price(self.value / Decimal(str(other)))
    
    def round(self, precision: int = 2) -> 'Price':
        """
        Redondea el precio a la precisión especificada.
        
        Args:
            precision: Número de decimales
        
        Returns:
            Nuevo Price redondeado
        
        Examples:
            >>> Price(50000.12345).round(2)
            Price(Decimal('50000.12'))
        """
        quantize_value = Decimal('0.1') ** precision
        rounded = self.value.quantize(quantize_value, rounding=ROUND_HALF_UP)
        return Price(rounded)
    
    def percentage_change(self, other: 'Price') -> Decimal:
        """
        Calcula el cambio porcentual respecto a otro precio.
        
        Args:
            other: Precio de referencia
        
        Returns:
            Cambio porcentual (ej: 0.05 = 5%)
        
        Examples:
            >>> Price(105).percentage_change(Price(100))
            Decimal('0.05')
        """
        return (self.value - other.value) / other.value
    
    @classmethod
    def zero(cls) -> 'Price':
        """Retorna un precio de 0.01 (el mínimo permitido)"""
        return cls(Decimal('0.01'))
