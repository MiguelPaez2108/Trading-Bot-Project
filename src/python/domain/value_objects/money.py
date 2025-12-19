"""
Money Value Object.

Path: src/python/domain/value_objects/money.py
"""
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Money:
    """
    Immutable money representation with currency.
    
    Always uses Decimal for precision (critical for finance).
    """
    amount: Decimal
    currency: str
    
    def __post_init__(self):
        """Validate on creation."""
        if not isinstance(self.amount, Decimal):
            raise TypeError("Amount must be Decimal")
        
        if not self.currency:
            raise ValueError("Currency must be specified")
        
        # Normalize currency to uppercase
        object.__setattr__(self, 'currency', self.currency.upper())
    
    def __str__(self) -> str:
        """String representation: 1000.50 USDT"""
        return f"{self.amount} {self.currency}"
    
    def __add__(self, other: "Money") -> "Money":
        """Add two Money objects (must be same currency)."""
        if self.currency != other.currency:
            raise ValueError(f"Cannot add {self.currency} and {other.currency}")
        
        return Money(
            amount=self.amount + other.amount,
            currency=self.currency
        )
    
    def __sub__(self, other: "Money") -> "Money":
        """Subtract two Money objects."""
        if self.currency != other.currency:
            raise ValueError(f"Cannot subtract {self.currency} and {other.currency}")
        
        return Money(
            amount=self.amount - other.amount,
            currency=self.currency
        )
    
    def __mul__(self, multiplier: Decimal) -> "Money":
        """Multiply money by scalar."""
        return Money(
            amount=self.amount * multiplier,
            currency=self.currency
        )
    
    def __truediv__(self, divisor: Decimal) -> "Money":
        """Divide money by scalar."""
        return Money(
            amount=self.amount / divisor,
            currency=self.currency
        )
    
    def __lt__(self, other: "Money") -> bool:
        """Less than comparison."""
        if self.currency != other.currency:
            raise ValueError(f"Cannot compare {self.currency} and {other.currency}")
        return self.amount < other.amount
    
    def __le__(self, other: "Money") -> bool:
        """Less than or equal."""
        if self.currency != other.currency:
            raise ValueError(f"Cannot compare {self.currency} and {other.currency}")
        return self.amount <= other.amount
    
    def __gt__(self, other: "Money") -> bool:
        """Greater than."""
        if self.currency != other.currency:
            raise ValueError(f"Cannot compare {self.currency} and {other.currency}")
        return self.amount > other.amount
    
    def __ge__(self, other: "Money") -> bool:
        """Greater than or equal."""
        if self.currency != other.currency:
            raise ValueError(f"Cannot compare {self.currency} and {other.currency}")
        return self.amount >= other.amount
    
    @classmethod
    def from_float(cls, amount: float, currency: str) -> "Money":
        """
        Create Money from float (converts to Decimal).
        
        Args:
            amount: Float amount
            currency: Currency code
        
        Returns:
            Money instance
        
        Example:
            >>> money = Money.from_float(1000.50, "USDT")
            >>> print(money)
            1000.50 USDT
        """
        return cls(amount=Decimal(str(amount)), currency=currency)
    
    def to_float(self) -> float:
        """Convert to float (use with caution - loses precision)."""
        return float(self.amount)
    
    def is_positive(self) -> bool:
        """Check if amount is positive."""
        return self.amount > 0
    
    def is_zero(self) -> bool:
        """Check if amount is zero."""
        return self.amount == 0
    
    def abs(self) -> "Money":
        """Return absolute value."""
        return Money(amount=abs(self.amount), currency=self.currency)