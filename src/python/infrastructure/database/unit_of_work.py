"""
Unit of Work Pattern Implementation
Manages transactions across multiple repositories
"""
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from src.python.infrastructure.database.repositories.order_repository import OrderRepository
from src.python.infrastructure.database.repositories.position_repository import PositionRepository


class UnitOfWork:
    """
    Unit of Work pattern for managing database transactions.
    
    Usage:
        async with UnitOfWork(session) as uow:
            order = await uow.orders.save(order)
            position = await uow.positions.save(position)
            await uow.commit()
    """
    
    def __init__(self, session: AsyncSession):
        """
        Initialize Unit of Work with database session.
        
        Args:
            session: Async SQLAlchemy session
        """
        self.session = session
        self._orders: Optional[OrderRepository] = None
        self._positions: Optional[PositionRepository] = None
    
    @property
    def orders(self) -> OrderRepository:
        """Get Order repository"""
        if self._orders is None:
            self._orders = OrderRepository(self.session)
        return self._orders
    
    @property
    def positions(self) -> PositionRepository:
        """Get Position repository"""
        if self._positions is None:
            self._positions = PositionRepository(self.session)
        return self._positions
    
    async def commit(self) -> None:
        """Commit the transaction"""
        await self.session.commit()
    
    async def rollback(self) -> None:
        """Rollback the transaction"""
        await self.session.rollback()
    
    async def __aenter__(self):
        """Enter async context manager"""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Exit async context manager.
        Auto-rollback on exception.
        """
        if exc_type is not None:
            await self.rollback()
        await self.session.close()
