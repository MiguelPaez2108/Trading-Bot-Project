"""
Domain Exceptions
Excepciones específicas del dominio de trading
"""


class DomainException(Exception):
    """Excepción base para todas las excepciones del dominio"""
    pass


class InvalidOrderError(DomainException):
    """Excepción lanzada cuando una orden es inválida"""
    
    def __init__(self, message: str, order_id: str = None):
        self.order_id = order_id
        super().__init__(f"Invalid order{f' {order_id}' if order_id else ''}: {message}")


class InsufficientFundsError(DomainException):
    """Excepción lanzada cuando no hay fondos suficientes"""
    
    def __init__(self, required: float, available: float, currency: str = "USDT"):
        self.required = required
        self.available = available
        self.currency = currency
        super().__init__(
            f"Insufficient funds: required {required} {currency}, "
            f"available {available} {currency}"
        )


class InvalidSymbolError(DomainException):
    """Excepción lanzada cuando un símbolo es inválido"""
    
    def __init__(self, symbol: str, reason: str = ""):
        self.symbol = symbol
        super().__init__(f"Invalid symbol '{symbol}'{f': {reason}' if reason else ''}")


class InvalidPriceError(DomainException):
    """Excepción lanzada cuando un precio es inválido"""
    
    def __init__(self, price: float, reason: str = ""):
        self.price = price
        super().__init__(f"Invalid price {price}{f': {reason}' if reason else ''}")


class InvalidQuantityError(DomainException):
    """Excepción lanzada cuando una cantidad es inválida"""
    
    def __init__(self, quantity: float, reason: str = ""):
        self.quantity = quantity
        super().__init__(f"Invalid quantity {quantity}{f': {reason}' if reason else ''}")


class PositionNotFoundError(DomainException):
    """Excepción lanzada cuando no se encuentra una posición"""
    
    def __init__(self, symbol: str):
        self.symbol = symbol
        super().__init__(f"Position not found for symbol '{symbol}'")


class OrderNotFoundError(DomainException):
    """Excepción lanzada cuando no se encuentra una orden"""
    
    def __init__(self, order_id: str):
        self.order_id = order_id
        super().__init__(f"Order not found: {order_id}")


class RiskLimitExceededError(DomainException):
    """Excepción lanzada cuando se excede un límite de riesgo"""
    
    def __init__(self, limit_type: str, current: float, maximum: float):
        self.limit_type = limit_type
        self.current = current
        self.maximum = maximum
        super().__init__(
            f"Risk limit exceeded for {limit_type}: "
            f"current {current}, maximum {maximum}"
        )


class ValidationError(DomainException):
    """Excepción lanzada cuando falla una validación"""
    
    def __init__(self, field: str, value: any, reason: str):
        self.field = field
        self.value = value
        self.reason = reason
        super().__init__(f"Validation error for {field}={value}: {reason}")
