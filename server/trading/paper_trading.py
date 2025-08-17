"""
Paper trading implementation for simulating trades without real money.
"""
import os
import json
import logging
import datetime
from pathlib import Path
from typing import Dict, Optional, List, Any

from models import Position, Order, Trade, PaperAccount, OrderAction, OrderStatus
from utils import generate_id, load_json_file, save_json_file, format_money

logger = logging.getLogger("trading-mcp.paper_trading")

# Constants
PAPER_ACCOUNT_FILE = Path(__file__).parent / "paper_account.json"
RISK_MAX_POSITION_SIZE = float(os.getenv("RISK_MAX_POSITION_SIZE", "5000"))
RISK_MAX_DAILY_LOSS = float(os.getenv("RISK_MAX_DAILY_LOSS", "1000"))

class PaperTradingService:
    """Service for paper trading operations."""
    
    def __init__(self, risk_max_position_size: float = 5000.0, risk_max_daily_loss: float = 1000.0):
        self.RISK_MAX_POSITION_SIZE = float(os.getenv("RISK_MAX_POSITION_SIZE", risk_max_position_size))
        self.RISK_MAX_DAILY_LOSS = float(os.getenv("RISK_MAX_DAILY_LOSS", risk_max_daily_loss))
    
    @staticmethod
    def load_account() -> PaperAccount:
        """Load the paper trading account data."""
        data = load_json_file(PAPER_ACCOUNT_FILE)
        if data:
            return PaperAccount.model_validate(data)
        else:
            logger.info("No paper account found. Creating new account.")
            # Use setup_account to allow test patching and cash customization
            return PaperTradingService.setup_account()
    
    @staticmethod
    def save_account(account: PaperAccount) -> bool:
        """Save the paper trading account data."""
        return save_json_file(PAPER_ACCOUNT_FILE, account.model_dump(mode="json"))
    
    @staticmethod
    def setup_account(cash: float = 100000.0) -> PaperAccount:
        """Initialize or reset the paper trading account."""
        account = PaperAccount(cash=cash)
        PaperTradingService.save_account(account)
        logger.info(f"Paper account initialized with {format_money(cash)}")
        return account
    
    @staticmethod
    async def update_positions(account: PaperAccount, current_prices: Dict[str, float]) -> PaperAccount:
        """Update position values with current market prices."""
        for symbol, position in account.positions.items():
            if symbol in current_prices:
                price = current_prices[symbol]
                position.current_price = price
                position.market_value = position.quantity * price
                position.unrealized_pl = position.market_value - (position.quantity * position.cost_basis)
                position.unrealized_pl_percent = (position.unrealized_pl / (position.quantity * position.cost_basis)) * 100
        
        return account
    
    @staticmethod
    async def create_order(
        symbol: str,
        action: OrderAction,
        quantity: float,
        order_type: str,
        limit_price: Optional[float] = None,
        stop_price: Optional[float] = None,
        current_price: Optional[float] = None
    ) -> Order:
        """Create a new order (does not submit)."""
        order_id = generate_id("order")
        order = Order(
            order_id=order_id,
            symbol=symbol.upper(),
            action=action,
            quantity=quantity,
            order_type=order_type,
            limit_price=limit_price,
            stop_price=stop_price,
            status=OrderStatus.OPEN
        )
        
        # Validate against risk parameters if we have a price estimate
        if current_price:
            estimated_value = quantity * current_price
            if estimated_value > RISK_MAX_POSITION_SIZE:
                logger.warning(f"Order value ${estimated_value:.2f} exceeds maximum position size ${RISK_MAX_POSITION_SIZE:.2f}")
        
        return order
    
    @staticmethod
    async def submit_order(order: Order, account: PaperAccount, execution_price: float) -> Dict[str, Any]:
        """Submit an order and update the account."""
        # For market orders, simulate immediate execution
        if order.order_type == "MARKET":
            order.status = OrderStatus.EXECUTED
            order.executed_at = datetime.datetime.now()
            order.execution_price = execution_price
            
            # Create a trade record
            trade = Trade(
                trade_id=generate_id("trade"),
                order_id=order.order_id,
                symbol=order.symbol,
                action=order.action,
                quantity=order.quantity,
                price=execution_price,
                timestamp=datetime.datetime.now(),
                commission=4.95  # Simulated commission
            )
            
            # Update account based on the trade
            trade_value = order.quantity * execution_price
            commission = trade.commission
            
            result = {
                "success": False,
                "message": "",
                "order": order,
                "trade": trade
            }
            
            if order.action in [OrderAction.BUY, OrderAction.BUY_TO_COVER]:
                # Check if we have enough cash
                if account.cash < trade_value + commission:
                    result["message"] = f"Insufficient funds. Required: ${trade_value + commission:.2f}, Available: ${account.cash:.2f}"
                    return result
                
                # Deduct cash, update or create position
                account.cash -= (trade_value + commission)
                
                if order.symbol in account.positions:
                    position = account.positions[order.symbol]
                    # Calculate new cost basis
                    total_shares = position.quantity + order.quantity
                    total_cost = (position.quantity * position.cost_basis) + trade_value
                    position.quantity = total_shares
                    position.cost_basis = total_cost / total_shares
                else:
                    account.positions[order.symbol] = Position(
                        symbol=order.symbol,
                        quantity=order.quantity,
                        cost_basis=execution_price
                    )
                
                result["success"] = True
                result["message"] = f"Bought {order.quantity} shares of {order.symbol} at {format_money(execution_price)}"
                
            elif order.action in [OrderAction.SELL, OrderAction.SELL_SHORT]:
                # Check if we have the position for a sell
                if order.action == OrderAction.SELL and (
                    order.symbol not in account.positions or 
                    account.positions[order.symbol].quantity < order.quantity
                ):
                    result["message"] = f"Insufficient shares. Required: {order.quantity}, " \
                                       f"Available: {account.positions.get(order.symbol, Position(symbol=order.symbol, quantity=0, cost_basis=0)).quantity}"
                    return result
                
                # Add cash, update position
                account.cash += (trade_value - commission)
                
                # For a regular sell, reduce existing position
                if order.action == OrderAction.SELL:
                    position = account.positions[order.symbol]
                    position.quantity -= order.quantity
                    
                    # If position is now zero, calculate realized P/L and remove it
                    if position.quantity == 0:
                        realized_pl = trade_value - (order.quantity * position.cost_basis)
                        today = datetime.datetime.now().strftime("%Y-%m-%d")
                        if today not in account.daily_pl:
                            account.daily_pl[today] = 0
                        account.daily_pl[today] += realized_pl
                        del account.positions[order.symbol]
                    
                    result["success"] = True
                    result["message"] = f"Sold {order.quantity} shares of {order.symbol} at {format_money(execution_price)}"
                
                # For short-selling, create a negative position
                elif order.action == OrderAction.SELL_SHORT:
                    account.positions[order.symbol] = Position(
                        symbol=order.symbol,
                        quantity=-order.quantity,
                        cost_basis=execution_price
                    )
                    
                    result["success"] = True
                    result["message"] = f"Sold short {order.quantity} shares of {order.symbol} at {format_money(execution_price)}"
            
            # Save the trade and order to the account
            account.orders[order.order_id] = order
            account.trades.append(trade)
            PaperTradingService.save_account(account)
            
            return result
        else:
            # For non-market orders, we just save them for now
            account.orders[order.order_id] = order
            PaperTradingService.save_account(account)
            
            return {
                "success": True,
                "message": f"Order submitted (ID: {order.order_id})",
                "order": order
            }
    
    @staticmethod
    async def cancel_order(order_id: str, account: PaperAccount) -> Dict[str, Any]:
        """Cancel a pending order."""
        if order_id not in account.orders:
            return {
                "success": False,
                "message": f"Order with ID {order_id} not found."
            }
        
        order = account.orders[order_id]
        
        if order.status != OrderStatus.OPEN:
            return {
                "success": False,
                "message": f"Cannot cancel order with status {order.status.value}."
            }
        
        # Cancel the order
        order.status = OrderStatus.CANCELED
        account.orders[order_id] = order
        PaperTradingService.save_account(account)
        
        return {
            "success": True,
            "message": f"Order {order_id} for {order.quantity} shares of {order.symbol} has been canceled."
        }
    
    @staticmethod
    async def get_trading_history(account: PaperAccount, days: int = 30) -> List[Trade]:
        """Get recent trading history."""
        cutoff_date = datetime.datetime.now() - datetime.timedelta(days=days)
        recent_trades = [t for t in account.trades if t.timestamp >= cutoff_date]
        
        # Sort trades by timestamp (newest first)
        return sorted(recent_trades, key=lambda t: t.timestamp, reverse=True)
    
    @staticmethod
    async def analyze_portfolio(account: PaperAccount) -> Dict[str, Any]:
        """Analyze portfolio composition and metrics."""
        if not account.positions:
            return {"message": "No positions in portfolio to analyze."}
        
        # Calculate basic portfolio metrics
        total_value = account.cash
        total_invested = 0
        portfolio_dict = {}
        
        for symbol, pos in account.positions.items():
            market_value = pos.market_value or 0
            cost_basis_total = pos.quantity * pos.cost_basis
            total_value += market_value
            total_invested += cost_basis_total
            portfolio_dict[symbol] = {
                "value": market_value,
                "weight": 0,  # Will calculate after total is known
                "unrealized_pl": pos.unrealized_pl or 0,
                "unrealized_pl_percent": pos.unrealized_pl_percent or 0
            }
        
        # Calculate weights
        for symbol in portfolio_dict:
            portfolio_dict[symbol]["weight"] = (portfolio_dict[symbol]["value"] / total_value) * 100 if total_value > 0 else 0
        
        # Sort positions by weight
        sorted_positions = sorted(
            portfolio_dict.items(),
            key=lambda x: x[1]["value"],
            reverse=True
        )
        
        # Calculate unrealized P/L
        total_unrealized_pl = sum(pos[1]["unrealized_pl"] for pos in sorted_positions)
        total_unrealized_pl_percent = (total_unrealized_pl / total_invested) * 100 if total_invested > 0 else 0
        
        # Prepare result
        result = {
            "total_value": total_value,
            "cash": account.cash,
            "cash_percent": (account.cash / total_value * 100) if total_value > 0 else 0,
            "invested": total_value - account.cash,
            "invested_percent": ((total_value - account.cash) / total_value * 100) if total_value > 0 else 0,
            "total_unrealized_pl": total_unrealized_pl,
            "total_unrealized_pl_percent": total_unrealized_pl_percent,
            "positions": sorted_positions,
            "num_positions": len(sorted_positions)
        }
        
        # Add risk metrics
        if len(sorted_positions) > 0:
            most_concentrated = sorted_positions[0]
            result["most_concentrated"] = {
                "symbol": most_concentrated[0],
                "weight": most_concentrated[1]["weight"]
            }
        
        # Daily P/L history
        if account.daily_pl:
            daily_pl_values = list(account.daily_pl.values())
            result["daily_pl"] = {
                "avg": sum(daily_pl_values) / len(daily_pl_values) if daily_pl_values else 0,
                "best": max(daily_pl_values) if daily_pl_values else 0,
                "worst": min(daily_pl_values) if daily_pl_values else 0
            }
        
        return result