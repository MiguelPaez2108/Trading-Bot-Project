"""
Abstract Repository Interface - Position Repository
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.python.domain.entities import Position
from src.python.domain.value_objects import Symbol, Price


class IPositionRepository(ABC):
    """Abstract interface for Position repository"""
    
    @abstractmethod
    async def save(self, position: Position) -> Position:
        """Save or update a position"""
        pass
    
    @abstractmethod
    async def find_by_id(self, position_id: UUID) -> Optional[Position]:
        """Find position by ID"""
        pass
    
    @abstractmethod
    async def find_by_symbol(self, symbol: Symbol) -> Optional[Position]:
        """Find open position by symbol"""
        pass
    
    @abstractmethod
    async def find_all_open(self) -> List[Position]:
        """Find all open positions"""
        pass
    
    @abstractmethod
    async def find_by_strategy(self, strategy_id: str) -> List[Position]:
        """Find positions by strategy ID"""
        pass
    
    @abstractmethod
    async def update_current_price(self, position_id: UUID, current_price: Price) -> Position:
        """Update current price and recalculate unrealized PnL"""
        pass
    
    @abstractmethod
    async def close_position(self, position_id: UUID) -> Position:
        """Mark position as closed"""
        pass
    
    @abstractmethod
    async def delete(self, position_id: UUID) -> bool:
        """Delete a position"""
        pass
