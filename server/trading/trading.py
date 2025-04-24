#!/usr/bin/env python3
"""
Trading MCP Server - A Model Context Protocol server for stock trading.
Supports paper trading (default) and live trading with brokerages like E*TRADE.
"""
import os
import json
import logging
import argparse
import datetime
import ssl
from pathlib import Path
import asyncio
from typing import Dict, Optional, List, Union, Any

# Configure SSL for testing environments
if os.getenv("BYPASS_SSL_VERIFICATION", "FALSE").upper() == "TRUE":
    # Disable SSL verification globally
    ssl._create_default_https_context = ssl._create_unverified_context
    os.environ['PYTHONHTTPSVERIFY'] = '0'

# Third-party imports
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Local imports
from models import OrderAction, OrderType, Position
from utils import format_money, get_env_var
from market_data import MarketData
from paper_trading import PaperTradingService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("trading-mcp")

# Load environment variables
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("trading")

# Constants and configuration
TRADING_MODE = get_env_var("TRADING_MODE", "paper").lower()
DATA_REQUEST_TIMEOUT = get_env_var("DATA_REQUEST_TIMEOUT", 10.0)
USE_MOCK_DATA = get_env_var("USE_MOCK_DATA", False)

# Registry of CLI commands
cli_commands = {}

# Define CLI command decorator
def cli_command(name=None):
    """Decorator to register a function as a CLI command."""
    def decorator(func):
        command_name = name or func.__name__
        cli_commands[command_name] = func
        return func
    return decorator

# Trading MCP Tools

@mcp.tool()
async def get_quote(symbol: str) -> str:
    """Get current price quote for a stock.
    
    Args:
        symbol: The stock ticker symbol (e.g., AAPL, MSFT, GOOGL)
    """
    logger.info(f"Getting quote for {symbol}")
    
    try:
        quote_data = await MarketData.get_quote(symbol, timeout=DATA_REQUEST_TIMEOUT, use_mock=USE_MOCK_DATA)
        
        # Format the quote data into a nice string
        result = [f"Quote for {symbol}:"]
        result.append(f"Price: {format_money(quote_data['price'])}")
        result.append(f"Change: {format_money(quote_data['change'])} ({quote_data['change_percent']:.2f}%)")
        result.append(f"Volume: {int(quote_data['volume']):,}")
        
        if "name" in quote_data and quote_data["name"] != symbol:
            result[0] = f"{quote_data['name']} ({symbol})"
            
        if "market_cap" in quote_data and quote_data["market_cap"]:
            result.append(f"Market Cap: {format_money(quote_data['market_cap'])}")
            
        if "pe_ratio" in quote_data and quote_data["pe_ratio"]:
            result.append(f"P/E Ratio: {quote_data['pe_ratio']:.2f}")
            
        return "\n".join(result)
    except TimeoutError:
        return f"Error: Timed out while retrieving quote for {symbol}. Please try again later."
    except Exception as e:
        logger.error(f"Error getting quote for {symbol}: {e}")
        return f"Error getting quote for {symbol}: {str(e)}"

@mcp.tool()
async def get_account_summary() -> str:
    """Get a summary of your trading account including cash balance and positions."""
    logger.info("Getting account summary")
    
    try:
        # Load paper trading account
        account = PaperTradingService.load_account()
        
        # Get current prices for all positions
        if account.positions:
            symbols = list(account.positions.keys())
            current_prices = {}
            
            for symbol in symbols:
                try:
                    quote = await MarketData.get_quote(symbol, use_mock=USE_MOCK_DATA)
                    current_prices[symbol] = quote["price"]
                except Exception as e:
                    logger.error(f"Error getting price for {symbol}: {e}")
                    # Fall back to cost basis if price lookup fails
                    current_prices[symbol] = account.positions[symbol].cost_basis
            
            # Update positions with current prices
            account = await PaperTradingService.update_positions(account, current_prices)
        
        # Calculate total account value
        total_value = account.cash
        unrealized_pl = 0.0
        
        # Format the result
        result = ["Account Summary (Paper Trading):", f"Cash: {format_money(account.cash)}"]
        
        if account.positions:
            result.append("\nPositions:")
            for symbol, pos in account.positions.items():
                market_value = pos.market_value or 0
                total_value += market_value
                unrealized_pl += pos.unrealized_pl or 0
                
                pl_str = f"{format_money(pos.unrealized_pl or 0)} ({pos.unrealized_pl_percent:.2f}%)" if pos.unrealized_pl is not None else "N/A"
                result.append(f"  {symbol}: {pos.quantity} shares @ {format_money(pos.cost_basis)} | Current: {format_money(pos.current_price or 0)} | Value: {format_money(market_value)} | P/L: {pl_str}")
        
        result.append(f"\nTotal Account Value: {format_money(total_value)}")
        result.append(f"Total Unrealized P/L: {format_money(unrealized_pl)}")
        
        # Daily P/L
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        if today in account.daily_pl:
            result.append(f"Today's P/L: {format_money(account.daily_pl[today])}")
        
        return "\n".join(result)
    except Exception as e:
        logger.error(f"Error getting account summary: {e}")
        return f"Error getting account summary: {str(e)}"

@mcp.tool()
async def submit_order(symbol: str, action: str, quantity: float, order_type: str = "MARKET", limit_price: float = None) -> str:
    """Submit an order to buy or sell a stock.
    
    Args:
        symbol: The stock ticker symbol (e.g., AAPL, MSFT)
        action: Order action (BUY or SELL)
        quantity: Number of shares to trade
        order_type: Order type (MARKET or LIMIT)
        limit_price: Price for limit orders (required for LIMIT orders)
    """
    logger.info(f"Submitting {action} order for {quantity} shares of {symbol}")
    
    try:
        symbol = symbol.upper()
        action = getattr(OrderAction, action.upper())
        order_type = getattr(OrderType, order_type.upper())
        
        # Validate inputs
        if order_type == OrderType.LIMIT and limit_price is None:
            return "Error: Limit price is required for LIMIT orders."
        
        if quantity <= 0:
            return "Error: Quantity must be greater than zero."
        
        # Load account
        account = PaperTradingService.load_account()
        
        # Get current price for execution
        try:
            quote = await MarketData.get_quote(symbol, use_mock=USE_MOCK_DATA)
            current_price = quote["price"]
        except Exception as e:
            logger.error(f"Error getting price for {symbol}: {e}")
            return f"Error: Could not get current price for {symbol}. Please try again later."
        
        # Create order
        order = await PaperTradingService.create_order(
            symbol=symbol,
            action=action,
            quantity=quantity,
            order_type=order_type.value,
            limit_price=limit_price,
            current_price=current_price
        )
        
        # Submit order
        result = await PaperTradingService.submit_order(
            order=order,
            account=account,
            execution_price=current_price
        )
        
        return result["message"]
    except Exception as e:
        logger.error(f"Error submitting order: {e}")
        return f"Error submitting order: {str(e)}"

@mcp.tool()
async def analyze_portfolio() -> str:
    """Analyze your portfolio composition and risk metrics."""
    logger.info("Analyzing portfolio")
    
    try:
        # Load account
        account = PaperTradingService.load_account()
        
        # Get current prices for all positions
        if account.positions:
            symbols = list(account.positions.keys())
            current_prices = {}
            
            for symbol in symbols:
                try:
                    quote = await MarketData.get_quote(symbol, use_mock=USE_MOCK_DATA)
                    current_prices[symbol] = quote["price"]
                except Exception as e:
                    logger.error(f"Error getting price for {symbol}: {e}")
                    # Fall back to cost basis
                    current_prices[symbol] = account.positions[symbol].cost_basis
            
            # Update positions with current prices
            account = await PaperTradingService.update_positions(account, current_prices)
        
        # Run portfolio analysis
        analysis = await PaperTradingService.analyze_portfolio(account)
        
        if "message" in analysis:
            return analysis["message"]
        
        # Format the results
        result = ["Portfolio Analysis:"]
        
        # Overall metrics
        result.append(f"\nTotal Portfolio Value: {format_money(analysis['total_value'])}")
        result.append(f"Cash: {format_money(analysis['cash'])} ({analysis['cash_percent']:.2f}%)")
        result.append(f"Invested: {format_money(analysis['invested'])} ({analysis['invested_percent']:.2f}%)")
        result.append(f"Total Unrealized P/L: {format_money(analysis['total_unrealized_pl'])} ({analysis['total_unrealized_pl_percent']:.2f}%)")
        
        # Portfolio composition
        result.append("\nPortfolio Composition:")
        for symbol, metrics in analysis['positions']:
            result.append(f"  {symbol}: {format_money(metrics['value'])} ({metrics['weight']:.2f}%) | P/L: {format_money(metrics['unrealized_pl'])} ({metrics['unrealized_pl_percent']:.2f}%)")
        
        return "\n".join(result)
    except Exception as e:
        logger.error(f"Error analyzing portfolio: {e}")
        return f"Error analyzing portfolio: {str(e)}"

@mcp.tool()
async def setup_paper_account(cash: float = 100000.0) -> str:
    """Initialize or reset the paper trading account with the specified cash amount.
    
    Args:
        cash: Initial cash balance
    """
    logger.info(f"Setting up paper account with {format_money(cash)}")
    
    try:
        account = PaperTradingService.setup_account(cash=cash)
        return f"Paper trading account initialized with {format_money(cash)}"
    except Exception as e:
        logger.error(f"Error setting up paper account: {e}")
        return f"Error setting up paper account: {str(e)}"

@mcp.tool()
async def get_historical_data(symbol: str, period: str = "1mo", interval: str = "1d") -> str:
    """Get historical price data for a stock.
    
    Args:
        symbol: The stock ticker symbol (e.g., AAPL, MSFT)
        period: Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
        interval: Data interval (1d, 5d, 1wk, 1mo, 3mo)
    """
    logger.info(f"Getting historical data for {symbol}")
    
    try:
        data = await MarketData.get_historical_data(
            symbol=symbol,
            period=period,
            interval=interval,
            use_mock=USE_MOCK_DATA
        )
        
        # Format the results
        result = [f"Historical Data for {symbol} ({period}, {interval} interval):"]
        result.append(f"Period: {data.get('start_date')} to {data.get('end_date')}")
        result.append(f"Starting Price: {format_money(data['start_price'])}")
        result.append(f"Ending Price: {format_money(data['end_price'])}")
        result.append(f"Change: {format_money(data['change'])} ({data['change_percent']:.2f}%)")
        result.append(f"High: {format_money(data['high'])}")
        result.append(f"Low: {format_money(data['low'])}")
        result.append(f"Average Volume: {int(data['avg_volume']):,}")
        
        return "\n".join(result)
    except Exception as e:
        logger.error(f"Error getting historical data: {e}")
        return f"Error getting historical data for {symbol}: {str(e)}"

# Register tools as CLI commands
cli_command("get-quote")(get_quote)
cli_command("get-account-summary")(get_account_summary)
cli_command("submit-order")(submit_order)
cli_command("analyze-portfolio")(analyze_portfolio)
cli_command("setup-paper-account")(setup_paper_account)
cli_command("get-historical-data")(get_historical_data)

def main():
    """Run the CLI commands."""
    parser = argparse.ArgumentParser(description="Stock Trading CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Add each registered command as a subparser
    for cmd_name, cmd_func in cli_commands.items():
        cmd_parser = subparsers.add_parser(cmd_name, help=cmd_func.__doc__.splitlines()[0] if cmd_func.__doc__ else "")
        
        # Add arguments based on function signature
        import inspect
        params = inspect.signature(cmd_func).parameters
        
        for name, param in params.items():
            if name != "self":  # Skip "self" parameter if present
                cmd_parser.add_argument(
                    f"--{name.replace('_', '-')}", 
                    dest=name,
                    type=param.annotation if param.annotation != inspect.Parameter.empty else str,
                    required=param.default == inspect.Parameter.empty,
                    default=None if param.default == inspect.Parameter.empty else param.default,
                    help=f"Parameter: {name}"
                )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command not in cli_commands:
        print(f"Unknown command: {args.command}")
        print(f"Available commands: {', '.join(cli_commands.keys())}")
        return
        
    # Execute the command
    cmd_func = cli_commands[args.command]
    print(f"Executing {args.command}, please wait (timeout: {DATA_REQUEST_TIMEOUT}s)...")
    
    # Extract args for the function and convert to the correct types
    func_args = {}
    for name, param in inspect.signature(cmd_func).parameters.items():
        if name != "self" and hasattr(args, name) and getattr(args, name) is not None:
            value = getattr(args, name)
            if param.annotation != inspect.Parameter.empty:
                try:
                    # Handle type conversions
                    if param.annotation == bool:
                        value = value.lower() in ("yes", "true", "t", "y", "1")
                    else:
                        value = param.annotation(value)
                except ValueError:
                    print(f"Error: Could not convert '{name}' to {param.annotation.__name__}")
                    return
            func_args[name] = value
    
    # Run the command
    try:
        if asyncio.iscoroutinefunction(cmd_func):
            result = asyncio.run(cmd_func(**func_args))
        else:
            result = cmd_func(**func_args)
        print(result)
    except Exception as e:
        print(f"Error executing {args.command}: {str(e)}")

if __name__ == "__main__":
    main()