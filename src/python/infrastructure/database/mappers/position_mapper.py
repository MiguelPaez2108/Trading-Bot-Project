"""
Mapper - Position Domain Entity ↔ ORM Model
"""
from typing import Optional
from uuid import UUID

from src.python.domain.entities import Position, PositionSide
from src.python.domain.value_objects import Symbol, Price, Quantity, Money
from src.python.infrastructure.database.orm_models import PositionModel


class PositionMapper:
    """Mapper for Position entity ↔ PositionModel ORM"""
    
    @staticmethod
    def to_entity(model: PositionModel) -> Position:
        """Convert ORM model to domain entity"""
        symbol = Symbol.from_string(model.symbol)
        side = PositionSide(model.side)
        entry_price = Price(model.entry_price)
        quantity = Quantity(model.quantity)
        current_price = Price(model.current_price) if model.current_price else entry_price
        
        # Create position
        position = Position(
            symbol=symbol,
            side=side,
            quantity=quantity,
            entry_price=entry_price,
            current_price=current_price,
            realized_pnl=Money(model.realized_pnl, symbol.quote),
            unrealized_pnl=Money(model.unrealized_pnl, symbol.quote),
            total_fees=Money(model.total_fees, symbol.quote),
            opened_at=model.opened_at,
            updated_at=model.updated_at,
            closed_at=model.closed_at,
            is_open=model.closed_at is None,
        )
        
        return position
    
    @staticmethod
    def to_model(entity: Position, model: Optional[PositionModel] = None) -> PositionModel:
        """Convert domain entity to ORM model"""
        if model is None:
            model = PositionModel()
        
        model.symbol = str(entity.symbol)
        model.exchange = "BINANCE"  # TODO: Get from entity when added
        model.side = entity.side.value
        model.entry_price = entity.entry_price.value
        model.quantity = entity.quantity.value
        model.current_price = entity.current_price.value if entity.current_price else None
        model.realized_pnl = entity.realized_pnl.amount
        model.unrealized_pnl = entity.unrealized_pnl.amount
        model.total_fees = entity.total_fees.amount
        model.opened_at = entity.opened_at
        model.updated_at = entity.updated_at
        model.closed_at = entity.closed_at
        
        return model
