"""
Domain Entity - Portfolio
Representa el estado completo del portfolio
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional
from decimal import Decimal

from ..value_objects import Symbol, Money, Price
from ..exceptions import PositionNotFoundError, InsufficientFundsError
from .position import Position, PositionSide


@dataclass
class Portfolio:
    """
    Entidad agregada que representa el portfolio completo.
    
    Mantiene tracking de:
    - Balance total y disponible
    - Posiciones abiertas
    - PnL total
    - Exposure
    
    Examples:
        >>> portfolio = Portfolio.create(initial_balance=Money(10000, "USDT"))
        >>> portfolio.total_balance
        Money(Decimal('10000'), 'USDT')
    """
    
    # Balance
    total_balance: Money
    available_balance: Money
    
    # Posiciones abiertas (key: symbol string)
    positions: Dict[str, Position] = field(default_factory=dict)
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    @classmethod
    def create(cls, initial_balance: Money) -> 'Portfolio':
        """
        Crea un nuevo portfolio.
        
        Args:
            initial_balance: Balance inicial
        
        Returns:
            Nuevo portfolio
        """
        return cls(
            total_balance=initial_balance,
            available_balance=initial_balance
        )
    
    def open_position(self, position: Position):
        """
        Abre una nueva posición.
        
        Args:
            position: Posición a abrir
        
        Raises:
            InsufficientFundsError: Si no hay fondos suficientes
        """
        # Calcular capital requerido
        required_capital = Money(position.notional_value, self.total_balance.currency)
        
        if required_capital > self.available_balance:
            raise InsufficientFundsError(
                float(required_capital.amount),
                float(self.available_balance.amount),
                self.total_balance.currency
            )
        
        # Agregar posición
        symbol_key = str(position.symbol)
        self.positions[symbol_key] = position
        
        # Actualizar balance disponible
        self.available_balance = self.available_balance - required_capital
        self.updated_at = datetime.utcnow()
    
    def close_position(self, symbol: Symbol, exit_price: Price) -> Money:
        """
        Cierra una posición.
        
        Args:
            symbol: Símbolo de la posición a cerrar
            exit_price: Precio de salida
        
        Returns:
            PnL realizado
        
        Raises:
            PositionNotFoundError: Si no existe la posición
        """
        symbol_key = str(symbol)
        
        if symbol_key not in self.positions:
            raise PositionNotFoundError(symbol_key)
        
        position = self.positions[symbol_key]
        
        # Cerrar posición y obtener PnL
        pnl = position.close(exit_price)
        
        # Liberar capital + PnL
        released_capital = Money(position.notional_value, self.total_balance.currency)
        self.available_balance = self.available_balance + released_capital + pnl
        self.total_balance = self.total_balance + pnl
        
        # Remover posición cerrada
        del self.positions[symbol_key]
        
        self.updated_at = datetime.utcnow()
        return pnl
    
    def update_position_price(self, symbol: Symbol, current_price: Price):
        """
        Actualiza el precio de una posición.
        
        Args:
            symbol: Símbolo
            current_price: Precio actual
        """
        symbol_key = str(symbol)
        
        if symbol_key in self.positions:
            self.positions[symbol_key].update_price(current_price)
            self.updated_at = datetime.utcnow()
    
    def get_position(self, symbol: Symbol) -> Optional[Position]:
        """
        Obtiene una posición por símbolo.
        
        Args:
            symbol: Símbolo
        
        Returns:
            Posición si existe, None si no
        """
        return self.positions.get(str(symbol))
    
    def has_position(self, symbol: Symbol) -> bool:
        """Verifica si existe una posición para el símbolo"""
        return str(symbol) in self.positions
    
    # Propiedades calculadas
    
    @property
    def total_unrealized_pnl(self) -> Money:
        """PnL no realizado total de todas las posiciones"""
        if not self.positions:
            return Money(0, self.total_balance.currency)
        
        total = Decimal('0')
        for position in self.positions.values():
            total += position.unrealized_pnl.amount
        
        return Money(total, self.total_balance.currency)
    
    @property
    def total_realized_pnl(self) -> Money:
        """PnL realizado total (desde el balance inicial)"""
        # El PnL realizado está reflejado en el total_balance
        # Necesitaríamos tracking del balance inicial para calcularlo
        # Por ahora retornamos 0
        return Money(0, self.total_balance.currency)
    
    @property
    def equity(self) -> Money:
        """Equity total (balance + unrealized PnL)"""
        return self.total_balance + self.total_unrealized_pnl
    
    @property
    def total_exposure(self) -> Money:
        """Exposure total (suma de valores nocionales de posiciones)"""
        if not self.positions:
            return Money(0, self.total_balance.currency)
        
        total = Decimal('0')
        for position in self.positions.values():
            total += position.notional_value
        
        return Money(total, self.total_balance.currency)
    
    @property
    def exposure_percentage(self) -> Decimal:
        """Exposure como porcentaje del equity"""
        if self.equity.amount == 0:
            return Decimal('0')
        return (self.total_exposure.amount / self.equity.amount) * 100
    
    @property
    def number_of_positions(self) -> int:
        """Número de posiciones abiertas"""
        return len(self.positions)
    
    @property
    def margin_used_percentage(self) -> Decimal:
        """Porcentaje del balance usado como margen"""
        if self.total_balance.amount == 0:
            return Decimal('0')
        
        used = self.total_balance.amount - self.available_balance.amount
        return (used / self.total_balance.amount) * 100
    
    def get_positions_list(self) -> List[Position]:
        """Retorna lista de todas las posiciones"""
        return list(self.positions.values())
    
    def __repr__(self) -> str:
        return (
            f"Portfolio(balance={self.total_balance}, "
            f"equity={self.equity}, "
            f"positions={self.number_of_positions}, "
            f"exposure={self.exposure_percentage:.2f}%)"
        )
