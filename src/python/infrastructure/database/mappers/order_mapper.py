"""
Mapper - Order Domain Entity ↔ ORM Model
Bidirectional conversion between domain and persistence layers
"""
from typing import Optional
from decimal import Decimal
from uuid import UUID

from src.python.domain.entities import Order
from src.python.domain.enums import OrderSide, OrderType, OrderStatus
from src.python.domain.value_objects import Symbol, Price, Quantity
from src.python.infrastructure.database.orm_models import OrderModel


class OrderMapper:
    """
    Mapper for converting between Order domain entity and OrderModel ORM.
    Ensures clean separation between domain and infrastructure layers.
    """
    
    @staticmethod
    def to_entity(model: OrderModel) -> Order:
        """
        Convert ORM model to domain entity.
        
        Args:
            model: OrderModel from database
        
        Returns:
            Order domain entity
        """
        # Parse symbol
        symbol = Symbol.from_string(model.symbol)
        
        # Convert enums
        side = OrderSide(model.side)
        order_type = OrderType(model.type)
        status = OrderStatus(model.status)
        
        # Convert quantities and prices
        quantity = Quantity(model.quantity)
        filled_quantity = Quantity(model.filled_quantity)
        
        price = Price(model.price) if model.price is not None else None
        stop_price = Price(model.stop_price) if model.stop_price is not None else None
        average_fill_price = Price(model.average_fill_price) if model.average_fill_price is not None else None
        
        # Create Order entity
        order = Order(
            order_id=str(model.id),
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
            stop_price=stop_price,
            status=status,
            filled_quantity=filled_quantity,
            exchange=model.exchange,
            exchange_order_id=model.exchange_order_id,
            client_order_id=model.client_order_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
            filled_at=model.filled_at,
            commission=model.commission,
            commission_asset=model.commission_asset or "USDT",
        )
        
        # Set average fill price if exists
        if average_fill_price:
            object.__setattr__(order, 'average_fill_price', average_fill_price)
        
        return order
    
    @staticmethod
    def to_model(entity: Order, model: Optional[OrderModel] = None) -> OrderModel:
        """
        Convert domain entity to ORM model.
        
        Args:
            entity: Order domain entity
            model: Existing OrderModel to update (optional)
        
        Returns:
            OrderModel for database
        """
        if model is None:
            model = OrderModel()
            model.id = UUID(entity.order_id)
        
        # Basic fields
        model.symbol = str(entity.symbol)
        model.exchange = entity.exchange or "BINANCE"
        model.side = entity.side.value
        model.type = entity.order_type.value
        model.status = entity.status.value
        
        # Quantities and prices
        model.quantity = entity.quantity.value
        model.filled_quantity = entity.filled_quantity.value
        model.price = entity.price.value if entity.price else None
        model.stop_price = entity.stop_price.value if entity.stop_price else None
        
        # Fees
        model.commission = entity.commission
        model.commission_asset = entity.commission_asset
        
        # Exchange IDs
        model.exchange_order_id = entity.exchange_order_id
        model.client_order_id = entity.client_order_id
        
        # Timestamps
        model.created_at = entity.created_at
        model.updated_at = entity.updated_at
        model.filled_at = entity.filled_at
        
        return model
    
    @staticmethod
    def update_model_from_entity(entity: Order, model: OrderModel) -> OrderModel:
        """
        Update existing model with entity data.
        Useful for updates without creating new model.
        
        Args:
            entity: Order domain entity
            model: Existing OrderModel
        
        Returns:
            Updated OrderModel
        """
        return OrderMapper.to_model(entity, model)
