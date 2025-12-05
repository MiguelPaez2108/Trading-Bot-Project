"""
Abstract Repository Interface - Order Repository
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from src.python.domain.entities import Order
from src.python.domain.enums import OrderStatus
from src.python.domain.value_objects import Symbol


class IOrderRepository(ABC):
    """
    Abstract interface for Order repository.
    All methods are async and return domain entities.
    """
    
    @abstractmethod
    async def save(self, order: Order) -> Order:
        """
        Save or update an order.
        
        Args:
            order: Order entity to save
        
        Returns:
            Saved order entity
        """
        pass
    
    @abstractmethod
    async def find_by_id(self, order_id: UUID) -> Optional[Order]:
        """
        Find order by ID.
        
        Args:
            order_id: Order UUID
        
        Returns:
            Order if found, None otherwise
        """
        pass
    
    @abstractmethod
    async def find_by_symbol(self, symbol: Symbol, limit: int = 100) -> List[Order]:
        """
        Find orders by symbol.
        
        Args:
            symbol: Trading symbol
            limit: Maximum number of results
        
        Returns:
            List of orders
        """
        pass
    
    @abstractmethod
    async def find_by_status(self, status: OrderStatus, limit: int = 100) -> List[Order]:
        """
        Find orders by status.
        
        Args:
            status: Order status
            limit: Maximum number of results
        
        Returns:
            List of orders
        """
        pass
    
    @abstractmethod
    async def find_active_orders(self) -> List[Order]:
        """
        Find all active orders (PENDING, SUBMITTED, PARTIALLY_FILLED).
        
        Returns:
            List of active orders
        """
        pass
    
    @abstractmethod
    async def find_by_strategy(self, strategy_id: str, limit: int = 100) -> List[Order]:
        """
        Find orders by strategy ID.
        
        Args:
            strategy_id: Strategy identifier
            limit: Maximum number of results
        
        Returns:
            List of orders
        """
        pass
    
    @abstractmethod
    async def update_status(self, order_id: UUID, status: OrderStatus) -> Order:
        """
        Update order status.
        
        Args:
            order_id: Order UUID
            status: New status
        
        Returns:
            Updated order
        """
        pass
    
    @abstractmethod
    async def delete(self, order_id: UUID) -> bool:
        """
        Delete an order.
        
        Args:
            order_id: Order UUID
        
        Returns:
            True if deleted, False otherwise
        """
        pass
