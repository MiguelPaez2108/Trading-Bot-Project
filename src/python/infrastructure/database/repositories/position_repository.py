"""
Position Repository Implementation
"""
from typing import List, Optional
from uuid import UUID
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.python.application.ports.repositories import IPositionRepository
from src.python.domain.entities import Position
from src.python.domain.value_objects import Symbol, Price
from src.python.infrastructure.database.orm_models import PositionModel
from src.python.infrastructure.database.mappers import PositionMapper


class PositionRepository(IPositionRepository):
    """Concrete implementation of Position repository"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self.mapper = PositionMapper()
    
    async def save(self, position: Position) -> Position:
        """Save or update a position"""
        # Try to find existing position
        stmt = select(PositionModel).where(
            PositionModel.symbol == str(position.symbol),
            PositionModel.closed_at.is_(None)
        )
        result = await self.session.execute(stmt)
        existing = result.scalar_one_or_none()
        
        if existing:
            model = self.mapper.to_model(position, existing)
        else:
            model = self.mapper.to_model(position)
            self.session.add(model)
        
        await self.session.flush()
        await self.session.refresh(model)
        
        return self.mapper.to_entity(model)
    
    async def find_by_id(self, position_id: UUID) -> Optional[Position]:
        """Find position by ID"""
        model = await self.session.get(PositionModel, position_id)
        return self.mapper.to_entity(model) if model else None
    
    async def find_by_symbol(self, symbol: Symbol) -> Optional[Position]:
        """Find open position by symbol"""
        stmt = select(PositionModel).where(
            PositionModel.symbol == str(symbol),
            PositionModel.closed_at.is_(None)
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return self.mapper.to_entity(model) if model else None
    
    async def find_all_open(self) -> List[Position]:
        """Find all open positions"""
        stmt = select(PositionModel).where(
            PositionModel.closed_at.is_(None)
        ).order_by(PositionModel.opened_at.desc())
        
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self.mapper.to_entity(model) for model in models]
    
    async def find_by_strategy(self, strategy_id: str) -> List[Position]:
        """Find positions by strategy ID"""
        stmt = select(PositionModel).where(
            PositionModel.strategy_id == strategy_id
        ).order_by(PositionModel.opened_at.desc())
        
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self.mapper.to_entity(model) for model in models]
    
    async def update_current_price(self, position_id: UUID, current_price: Price) -> Position:
        """Update current price and recalculate unrealized PnL"""
        position = await self.find_by_id(position_id)
        if not position:
            raise ValueError(f"Position {position_id} not found")
        
        # Update price (this will recalculate unrealized PnL in domain entity)
        position.update_price(current_price)
        
        # Save updated position
        return await self.save(position)
    
    async def close_position(self, position_id: UUID) -> Position:
        """Mark position as closed"""
        position = await self.find_by_id(position_id)
        if not position:
            raise ValueError(f"Position {position_id} not found")
        
        # Close position (domain logic)
        position.close()
        
        # Save closed position
        return await self.save(position)
    
    async def delete(self, position_id: UUID) -> bool:
        """Delete a position"""
        model = await self.session.get(PositionModel, position_id)
        if model:
            await self.session.delete(model)
            await self.session.flush()
            return True
        return False
