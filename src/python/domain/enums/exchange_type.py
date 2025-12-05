"""
Domain Enums - Exchange Type
Exchanges soportados por el sistema
"""
from enum import Enum


class ExchangeType(str, Enum):
    """Tipo de exchange"""
    
    BINANCE = "BINANCE"
    BINANCE_US = "BINANCE_US"
    BINANCE_FUTURES = "BINANCE_FUTURES"
    BYBIT = "BYBIT"
    BYBIT_FUTURES = "BYBIT_FUTURES"
    COINBASE = "COINBASE"
    KRAKEN = "KRAKEN"
    KUCOIN = "KUCOIN"
    OKX = "OKX"
    BITFINEX = "BITFINEX"
    
    def __str__(self) -> str:
        return self.value
    
    @property
    def is_futures(self) -> bool:
        """Indica si es un exchange de futuros"""
        return "FUTURES" in self.value
    
    @property
    def is_spot(self) -> bool:
        """Indica si es un exchange spot"""
        return not self.is_futures
    
    @property
    def supports_websocket(self) -> bool:
        """Indica si el exchange soporta WebSocket"""
        # Todos los exchanges principales soportan WebSocket
        return True
    
    @property
    def base_url(self) -> str:
        """Retorna la URL base del exchange"""
        urls = {
            ExchangeType.BINANCE: "https://api.binance.com",
            ExchangeType.BINANCE_US: "https://api.binance.us",
            ExchangeType.BINANCE_FUTURES: "https://fapi.binance.com",
            ExchangeType.BYBIT: "https://api.bybit.com",
            ExchangeType.BYBIT_FUTURES: "https://api.bybit.com",
            ExchangeType.COINBASE: "https://api.coinbase.com",
            ExchangeType.KRAKEN: "https://api.kraken.com",
            ExchangeType.KUCOIN: "https://api.kucoin.com",
            ExchangeType.OKX: "https://www.okx.com",
            ExchangeType.BITFINEX: "https://api.bitfinex.com",
        }
        return urls.get(self, "")
