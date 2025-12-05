"""
Value Object - Symbol
Representa un par de trading (ej: BTC/USDT)
"""
from dataclasses import dataclass
from typing import Optional
from ..exceptions import InvalidSymbolError


@dataclass(frozen=True)
class Symbol:
    """
    Value object que representa un símbolo de trading.
    Inmutable y validado.
    
    Examples:
        >>> symbol = Symbol("BTC", "USDT")
        >>> str(symbol)
        'BTC/USDT'
        >>> symbol.exchange_format("binance")
        'BTCUSDT'
    """
    
    base: str      # Moneda base (ej: BTC)
    quote: str     # Moneda cotización (ej: USDT)
    
    def __post_init__(self):
        """Validación post-inicialización"""
        if not self.base or not isinstance(self.base, str):
            raise InvalidSymbolError(f"{self.base}/{self.quote}", "Base currency must be a non-empty string")
        
        if not self.quote or not isinstance(self.quote, str):
            raise InvalidSymbolError(f"{self.base}/{self.quote}", "Quote currency must be a non-empty string")
        
        # Convertir a mayúsculas
        object.__setattr__(self, 'base', self.base.upper())
        object.__setattr__(self, 'quote', self.quote.upper())
    
    def __str__(self) -> str:
        """Formato estándar: BTC/USDT"""
        return f"{self.base}/{self.quote}"
    
    def __repr__(self) -> str:
        return f"Symbol('{self.base}', '{self.quote}')"
    
    @classmethod
    def from_string(cls, symbol_str: str, separator: str = "/") -> 'Symbol':
        """
        Crea un Symbol desde un string.
        
        Args:
            symbol_str: String del símbolo (ej: "BTC/USDT" o "BTCUSDT")
            separator: Separador a usar (default: "/")
        
        Returns:
            Symbol instance
        
        Examples:
            >>> Symbol.from_string("BTC/USDT")
            Symbol('BTC', 'USDT')
            >>> Symbol.from_string("BTCUSDT", separator="")
            Symbol('BTC', 'USDT')
        """
        if separator and separator in symbol_str:
            parts = symbol_str.split(separator)
            if len(parts) != 2:
                raise InvalidSymbolError(symbol_str, f"Expected format: BASE{separator}QUOTE")
            return cls(parts[0], parts[1])
        else:
            # Intentar parsear sin separador (ej: BTCUSDT)
            # Asumimos que las monedas comunes son de 3-4 caracteres
            common_quotes = ["USDT", "BUSD", "USD", "EUR", "BTC", "ETH", "BNB"]
            
            for quote in common_quotes:
                if symbol_str.upper().endswith(quote):
                    base = symbol_str[:-len(quote)]
                    return cls(base, quote)
            
            raise InvalidSymbolError(
                symbol_str,
                "Cannot parse symbol without separator. Use format 'BASE/QUOTE'"
            )
    
    def exchange_format(self, exchange: str = "binance") -> str:
        """
        Retorna el símbolo en el formato del exchange.
        
        Args:
            exchange: Nombre del exchange
        
        Returns:
            Símbolo formateado para el exchange
        
        Examples:
            >>> symbol = Symbol("BTC", "USDT")
            >>> symbol.exchange_format("binance")
            'BTCUSDT'
            >>> symbol.exchange_format("kraken")
            'BTC/USDT'
        """
        exchange = exchange.lower()
        
        # La mayoría de exchanges usan formato sin separador
        if exchange in ["binance", "bybit", "okx", "kucoin"]:
            return f"{self.base}{self.quote}"
        # Algunos usan separador
        elif exchange in ["kraken", "coinbase"]:
            return f"{self.base}/{self.quote}"
        # Default: sin separador
        else:
            return f"{self.base}{self.quote}"
    
    @property
    def is_stablecoin_pair(self) -> bool:
        """Indica si el par involucra stablecoins"""
        stablecoins = {"USDT", "USDC", "BUSD", "DAI", "TUSD", "UST"}
        return self.base in stablecoins or self.quote in stablecoins
    
    @property
    def is_fiat_pair(self) -> bool:
        """Indica si el par involucra moneda fiat"""
        fiats = {"USD", "EUR", "GBP", "JPY", "AUD", "CAD"}
        return self.base in fiats or self.quote in fiats
