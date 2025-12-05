"""
Value Object - Timeframe
Representa intervalos temporales para candlesticks
"""
from dataclasses import dataclass
from enum import Enum
from ..exceptions import ValidationError


class TimeframeUnit(str, Enum):
    """Unidades de tiempo"""
    MINUTE = "m"
    HOUR = "h"
    DAY = "d"
    WEEK = "w"
    MONTH = "M"


@dataclass(frozen=True)
class Timeframe:
    """
    Value object que representa un timeframe (intervalo temporal).
    
    Examples:
        >>> tf = Timeframe.from_string("1h")
        >>> tf.value
        1
        >>> tf.unit
        <TimeframeUnit.HOUR: 'h'>
        >>> tf.to_seconds()
        3600
    """
    
    value: int
    unit: TimeframeUnit
    
    def __post_init__(self):
        """Validación"""
        if self.value <= 0:
            raise ValidationError("value", self.value, "Timeframe value must be positive")
    
    def __str__(self) -> str:
        return f"{self.value}{self.unit.value}"
    
    def __repr__(self) -> str:
        return f"Timeframe({self.value}, {self.unit})"
    
    @classmethod
    def from_string(cls, timeframe_str: str) -> 'Timeframe':
        """
        Crea un Timeframe desde un string.
        
        Args:
            timeframe_str: String del timeframe (ej: "1m", "5m", "1h", "1d")
        
        Returns:
            Timeframe instance
        
        Examples:
            >>> Timeframe.from_string("1h")
            Timeframe(1, <TimeframeUnit.HOUR: 'h'>)
            >>> Timeframe.from_string("15m")
            Timeframe(15, <TimeframeUnit.MINUTE: 'm'>)
        """
        if not timeframe_str:
            raise ValidationError("timeframe", timeframe_str, "Timeframe cannot be empty")
        
        # Extraer número y unidad
        unit_char = timeframe_str[-1]
        value_str = timeframe_str[:-1]
        
        try:
            value = int(value_str)
        except ValueError:
            raise ValidationError("timeframe", timeframe_str, "Invalid timeframe format")
        
        # Mapear unidad
        unit_map = {
            'm': TimeframeUnit.MINUTE,
            'h': TimeframeUnit.HOUR,
            'd': TimeframeUnit.DAY,
            'w': TimeframeUnit.WEEK,
            'M': TimeframeUnit.MONTH,
        }
        
        unit = unit_map.get(unit_char)
        if not unit:
            raise ValidationError("timeframe", timeframe_str, f"Invalid unit: {unit_char}")
        
        return cls(value, unit)
    
    def to_seconds(self) -> int:
        """
        Convierte el timeframe a segundos.
        
        Returns:
            Número de segundos
        
        Examples:
            >>> Timeframe.from_string("1m").to_seconds()
            60
            >>> Timeframe.from_string("1h").to_seconds()
            3600
        """
        multipliers = {
            TimeframeUnit.MINUTE: 60,
            TimeframeUnit.HOUR: 3600,
            TimeframeUnit.DAY: 86400,
            TimeframeUnit.WEEK: 604800,
            TimeframeUnit.MONTH: 2592000,  # Aproximado: 30 días
        }
        return self.value * multipliers[self.unit]
    
    def to_minutes(self) -> int:
        """Convierte el timeframe a minutos"""
        return self.to_seconds() // 60
    
    def exchange_format(self, exchange: str = "binance") -> str:
        """
        Retorna el timeframe en el formato del exchange.
        
        Args:
            exchange: Nombre del exchange
        
        Returns:
            Timeframe formateado
        """
        # La mayoría de exchanges usan el mismo formato
        return str(self)
    
    # Timeframes comunes predefinidos
    @classmethod
    def M1(cls) -> 'Timeframe':
        """1 minuto"""
        return cls(1, TimeframeUnit.MINUTE)
    
    @classmethod
    def M5(cls) -> 'Timeframe':
        """5 minutos"""
        return cls(5, TimeframeUnit.MINUTE)
    
    @classmethod
    def M15(cls) -> 'Timeframe':
        """15 minutos"""
        return cls(15, TimeframeUnit.MINUTE)
    
    @classmethod
    def M30(cls) -> 'Timeframe':
        """30 minutos"""
        return cls(30, TimeframeUnit.MINUTE)
    
    @classmethod
    def H1(cls) -> 'Timeframe':
        """1 hora"""
        return cls(1, TimeframeUnit.HOUR)
    
    @classmethod
    def H4(cls) -> 'Timeframe':
        """4 horas"""
        return cls(4, TimeframeUnit.HOUR)
    
    @classmethod
    def D1(cls) -> 'Timeframe':
        """1 día"""
        return cls(1, TimeframeUnit.DAY)
    
    @classmethod
    def W1(cls) -> 'Timeframe':
        """1 semana"""
        return cls(1, TimeframeUnit.WEEK)
