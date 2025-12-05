"""
Order Repository Implementation
Concrete implementation using async SQLAlchemy
"""
from typing import List, Optional
from uuid import UUID
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.python.application.ports.repositories import IOrderRepository
from src.python.domain.entities import Order
from src.python.domain.enums import OrderStatus
from src.python.domain.value_objects import Symbol
from src.python.infrastructure.database.orm_models import OrderModel
from src.python.infrastructure.database.mappers import OrderMapper


class OrderRepository(IOrderRepository):
    """
    Concrete implementation of Order repository.
    Uses async SQLAlchemy for database operations.
    """
    
    def __init__(self, session: AsyncSession):
        """
        Initialize repository with database session.
        
        Args:
            session: Async SQLAlchemy session
        """
        self.session = session
        self.mapper = OrderMapper()
    
    async def save(self, order: Order) -> Order:
        """Save or update an order"""
        # Check if order exists
        existing = await self.session.get(OrderModel, UUID(order.order_id))
        
        if existing:
            # Update existing
            model = self.mapper.update_model_from_entity(order, existing)
        else:
            # Create new
            model = self.mapper.to_model(order)
            self.session.add(model)
        
        await self.session.flush()
        await self.session.refresh(model)
        
        return self.mapper.to_entity(model)
    
    async def find_by_id(self, order_id: UUID) -> Optional[Order]:
        """Find order by ID"""
        model = await self.session.get(OrderModel, order_id)
        return self.mapper.to_entity(model) if model else None
    
    async def find_by_symbol(self, symbol: Symbol, limit: int = 100) -> List[Order]:
        """Find orders by symbol"""
        stmt = (
            select(OrderModel)
            .where(OrderModel.symbol == str(symbol))
            .order_by(OrderModel.created_at.desc())
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self.mapper.to_entity(model) for model in models]
    
    async def find_by_status(self, status: OrderStatus, limit: int = 100) -> List[Order]:
        """Find orders by status"""
        stmt = (
            select(OrderModel)
            .where(OrderModel.status == status.value)
            .order_by(OrderModel.created_at.desc())
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self.mapper.to_entity(model) for model in models]
    
    async def find_active_orders(self) -> List[Order]:
        """Find all active orders"""
        active_statuses = [
            OrderStatus.PENDING.value,
            OrderStatus.SUBMITTED.value,
            OrderStatus.PARTIALLY_FILLED.value,
        ]
        
        stmt = (
            select(OrderModel)
            .where(OrderModel.status.in_(active_statuses))
            .order_by(OrderModel.created_at.desc())
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self.mapper.to_entity(model) for model in models]
    
    async def find_by_strategy(self, strategy_id: str, limit: int = 100) -> List[Order]:
        """Find orders by strategy ID"""
        stmt = (
            select(OrderModel)
            .where(OrderModel.strategy_id == strategy_id)
            .order_by(OrderModel.created_at.desc())
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self.mapper.to_entity(model) for model in models]
    
    async def update_status(self, order_id: UUID, status: OrderStatus) -> Order:
        """Update order status"""
        stmt = (
            update(OrderModel)
            .where(OrderModel.id == order_id)
            .values(status=status.value)
            .returning(OrderModel)
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one()
        await self.session.flush()
        return self.mapper.to_entity(model)
    
    async def delete(self, order_id: UUID) -> bool:
        """Delete an order"""
        model = await self.session.get(OrderModel, order_id)
        if model:
            await self.session.delete(model)
            await self.session.flush()
            return True
        return False
