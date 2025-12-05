"""
Value Object - Money
Representa dinero con currency
"""
from dataclasses import dataclass
from decimal import Decimal
from typing import Union
from ..exceptions import ValidationError


@dataclass(frozen=True)
class Money:
    """
    Value object que representa dinero con su currency.
    
    Examples:
        >>> money = Money(1000, "USDT")
        >>> str(money)
        '1000 USDT'
        >>> money + Money(500, "USDT")
        Money(Decimal('1500'), 'USDT')
    """
    
    amount: Decimal
    currency: str
    
    def __init__(self, amount: Union[float, int, str, Decimal], currency: str):
        """
        Inicializa Money.
        
        Args:
            amount: Cantidad de dinero
            currency: Código de moneda (ej: "USDT", "BTC")
        
        Raises:
            ValidationError: Si la cantidad es negativa o currency es inválida
        """
        if isinstance(amount, Decimal):
            decimal_amount = amount
        else:
            decimal_amount = Decimal(str(amount))
        
        if decimal_amount < 0:
            raise ValidationError("amount", amount, "Amount cannot be negative")
        
        if not currency or not isinstance(currency, str):
            raise ValidationError("currency", currency, "Currency must be a non-empty string")
        
        object.__setattr__(self, 'amount', decimal_amount)
        object.__setattr__(self, 'currency', currency.upper())
    
    def __str__(self) -> str:
        return f"{self.amount} {self.currency}"
    
    def __repr__(self) -> str:
        return f"Money({self.amount}, '{self.currency}')"
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Money):
            return self.amount == other.amount and self.currency == other.currency
        return False
    
    def __add__(self, other: 'Money') -> 'Money':
        """Suma de Money (debe ser misma currency)"""
        if self.currency != other.currency:
            raise ValidationError(
                "currency",
                other.currency,
                f"Cannot add {self.currency} and {other.currency}"
            )
        return Money(self.amount + other.amount, self.currency)
    
    def __sub__(self, other: 'Money') -> 'Money':
        """Resta de Money (debe ser misma currency)"""
        if self.currency != other.currency:
            raise ValidationError(
                "currency",
                other.currency,
                f"Cannot subtract {self.currency} and {other.currency}"
            )
        
        result = self.amount - other.amount
        if result < 0:
            raise ValidationError("amount", result, "Result cannot be negative")
        
        return Money(result, self.currency)
    
    def __mul__(self, multiplier: Union[int, float, Decimal]) -> 'Money':
        """Multiplicación por escalar"""
        return Money(self.amount * Decimal(str(multiplier)), self.currency)
    
    def __truediv__(self, divisor: Union[int, float, Decimal]) -> 'Money':
        """División por escalar"""
        return Money(self.amount / Decimal(str(divisor)), self.currency)
    
    def is_zero(self) -> bool:
        """Verifica si el monto es cero"""
        return self.amount == 0
    
    def is_positive(self) -> bool:
        """Verifica si el monto es positivo"""
        return self.amount > 0
    
    @classmethod
    def zero(cls, currency: str) -> 'Money':
        """Crea Money con monto cero"""
        return cls(Decimal('0'), currency)
