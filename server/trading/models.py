"""
Data models for the trading system.
"""
import datetime
from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class OrderType(str, Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP = "STOP"
    STOP_LIMIT = "STOP_LIMIT"
    TRAILING_STOP = "TRAILING_STOP"

class OrderAction(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
    BUY_TO_COVER = "BUY_TO_COVER"
    SELL_SHORT = "SELL_SHORT"

class OrderStatus(str, Enum):
    OPEN = "OPEN"
    EXECUTED = "EXECUTED"
    CANCELED = "CANCELED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"

class Position(BaseModel):
    symbol: str
    quantity: float
    cost_basis: float
    current_price: Optional[float] = None
    market_value: Optional[float] = None
    unrealized_pl: Optional[float] = None
    unrealized_pl_percent: Optional[float] = None

class Order(BaseModel):
    order_id: str
    symbol: str
    action: OrderAction
    quantity: float
    order_type: OrderType
    limit_price: Optional[float] = None
    stop_price: Optional[float] = None
    status: OrderStatus = OrderStatus.OPEN
    submitted_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    executed_at: Optional[datetime.datetime] = None
    execution_price: Optional[float] = None
    
class Trade(BaseModel):
    trade_id: str
    order_id: str
    symbol: str
    action: OrderAction
    quantity: float
    price: float
    timestamp: datetime.datetime
    commission: float = 0.0
    
class PaperAccount(BaseModel):
    cash: float = 100000.0
    positions: Dict[str, Position] = Field(default_factory=dict)
    orders: Dict[str, Order] = Field(default_factory=dict)
    trades: List[Trade] = Field(default_factory=list)
    daily_pl: Dict[str, float] = Field(default_factory=dict)