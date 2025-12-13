"""
Exchange-specific exceptions.
"""


class ExchangeError(Exception):
    """Base exception for exchange errors."""
    pass


class RateLimitError(ExchangeError):
    """Rate limit exceeded."""
    pass


class AuthenticationError(ExchangeError):
    """Authentication failed."""
    pass


class InsufficientBalanceError(ExchangeError):
    """Insufficient balance for order."""
    pass


class InvalidOrderError(ExchangeError):
    """Invalid order parameters."""
    pass


class OrderNotFoundError(ExchangeError):
    """Order not found."""
    pass


class MarketNotFoundError(ExchangeError):
    """Market/symbol not found."""
    pass


class NetworkError(ExchangeError):
    """Network/connection error."""
    pass


class ExchangeMaintenanceError(ExchangeError):
    """Exchange is under maintenance."""
    pass
