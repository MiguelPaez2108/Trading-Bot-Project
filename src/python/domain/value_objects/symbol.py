"""
Trading Symbol Value Object.

Path: src/python/domain/value_objects/symbol.py
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class TradingPair:
    """
    Immutable trading pair (e.g., BTC/USDT).
    
    Value object - identity based on values, not reference.
    """
    base: str   # e.g., "BTC"
    quote: str  # e.g., "USDT"
    exchange: str = "binance"
    
    def __post_init__(self):
        """Validate on creation."""
        if not self.base or not self.quote:
            raise ValueError("Base and quote must be non-empty")
        
        # Normalize to uppercase
        object.__setattr__(self, 'base', self.base.upper())
        object.__setattr__(self, 'quote', self.quote.upper())
        object.__setattr__(self, 'exchange', self.exchange.lower())
    
    def __str__(self) -> str:
        """String representation: BTC/USDT"""
        return f"{self.base}/{self.quote}"
    
    def __repr__(self) -> str:
        """Detailed representation."""
        return f"TradingPair(base='{self.base}', quote='{self.quote}', exchange='{self.exchange}')"
    
    @classmethod
    def from_string(cls, symbol: str, exchange: str = "binance") -> "TradingPair":
        """
        Create from string like 'BTC/USDT'.
        
        Args:
            symbol: Symbol string (e.g., 'BTC/USDT' or 'BTCUSDT')
            exchange: Exchange name
        
        Returns:
            TradingPair instance
        
        Example:
            >>> pair = TradingPair.from_string("BTC/USDT")
            >>> print(pair)
            BTC/USDT
        """
        if '/' in symbol:
            base, quote = symbol.split('/')
        else:
            # Try to parse BTCUSDT format
            # Assume last 3-4 chars are quote
            if symbol.endswith('USDT'):
                base = symbol[:-4]
                quote = 'USDT'
            elif symbol.endswith('USD'):
                base = symbol[:-3]
                quote = 'USD'
            elif symbol.endswith('BTC'):
                base = symbol[:-3]
                quote = 'BTC'
            else:
                raise ValueError(f"Cannot parse symbol: {symbol}")
        
        return cls(base=base, quote=quote, exchange=exchange)
    
    def to_ccxt_format(self) -> str:
        """Convert to CCXT format: BTC/USDT"""
        return f"{self.base}/{self.quote}"
    
    def to_binance_format(self) -> str:
        """Convert to Binance format: BTCUSDT"""
        return f"{self.base}{self.quote}"