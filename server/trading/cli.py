#!/usr/bin/env python3
"""
Command line interface for the trading system.
Provides a more user-friendly way to interact with the trading functionality.
"""
import os
import sys
import asyncio
import argparse
import logging
from typing import Dict, Any, Optional

# Local imports - make sure this is at the top level
from trading import (
    get_quote, get_account_summary, submit_order, analyze_portfolio,
    setup_paper_account, get_historical_data
)
from utils import format_money, get_env_var
from market_data import MarketData
from paper_trading import PaperTradingService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("trading-cli")

# Constants
DATA_REQUEST_TIMEOUT = float(os.getenv("DATA_REQUEST_TIMEOUT", "10.0"))  # seconds
USE_MOCK_DATA = os.getenv("USE_MOCK_DATA", "FALSE").upper() == "TRUE"

def setup_command_arguments() -> argparse.ArgumentParser:
    """Set up the command line arguments parser."""
    parser = argparse.ArgumentParser(description="Stock Trading CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Quote command
    quote_parser = subparsers.add_parser("quote", help="Get stock quote")
    quote_parser.add_argument("symbol", help="Stock ticker symbol (e.g., AAPL)")
    
    # Account summary command
    subparsers.add_parser("account", help="Get account summary")
    
    # Order command
    order_parser = subparsers.add_parser("order", help="Submit a trading order")
    order_parser.add_argument("symbol", help="Stock ticker symbol (e.g., AAPL)")
    order_parser.add_argument("action", choices=["buy", "sell"], help="Order action")
    order_parser.add_argument("quantity", type=float, help="Number of shares")
    order_parser.add_argument("--type", choices=["market", "limit"], default="market", help="Order type")
    order_parser.add_argument("--limit-price", type=float, help="Price for limit orders")
    
    # Portfolio command
    subparsers.add_parser("portfolio", help="Analyze portfolio")
    
    # Setup command
    setup_parser = subparsers.add_parser("setup", help="Setup or reset paper trading account")
    setup_parser.add_argument("--cash", type=float, default=100000.0, help="Initial cash balance")
    
    # History command
    history_parser = subparsers.add_parser("history", help="Get historical price data")
    history_parser.add_argument("symbol", help="Stock ticker symbol (e.g., AAPL)")
    history_parser.add_argument("--period", default="1mo", help="Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)")
    history_parser.add_argument("--interval", default="1d", help="Data interval (1d, 5d, 1wk, 1mo, 3mo)")
    
    # Watch command
    watch_parser = subparsers.add_parser("watch", help="Watch stock prices in real-time")
    watch_parser.add_argument("symbols", nargs="+", help="Stock ticker symbols to watch")
    watch_parser.add_argument("--interval", type=int, default=60, help="Refresh interval in seconds")
    
    return parser

async def watch_stocks(symbols: list, interval: int = 60) -> None:
    """Watch stock prices in real-time with periodic updates."""
    try:
        print(f"Watching {', '.join(symbols)} (Press Ctrl+C to stop)")
        print("-" * 80)
        
        while True:
            data = {}
            # Get quotes for all symbols
            for symbol in symbols:
                try:
                    quote = await MarketData.get_quote(symbol, use_mock=USE_MOCK_DATA)
                    data[symbol] = quote
                except Exception as e:
                    logger.error(f"Error getting quote for {symbol}: {e}")
                    data[symbol] = {"error": str(e)}
            
            # Clear screen and print header
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"Stock Watch - {len(symbols)} symbols - Updated at: {asyncio.get_event_loop().time():.0f}")
            print("-" * 80)
            
            # Print data for each symbol
            for symbol in symbols:
                if "error" in data[symbol]:
                    print(f"{symbol}: Error - {data[symbol]['error']}")
                else:
                    quote = data[symbol]
                    change_color = "\033[92m" if quote["change"] >= 0 else "\033[91m"  # Green/Red
                    reset_color = "\033[0m"
                    print(f"{symbol}: {format_money(quote['price'])} | {change_color}{format_money(quote['change'])} ({quote['change_percent']:.2f}%){reset_color} | Vol: {int(quote['volume']):,}")
            
            print("-" * 80)
            print(f"Refreshing in {interval} seconds... (Press Ctrl+C to stop)")
            
            # Wait for next update
            await asyncio.sleep(interval)
    except KeyboardInterrupt:
        print("\nStopping watch mode...")
        return

async def run_command(args: argparse.Namespace) -> Optional[str]:
    """Run the specified command."""
    if not args.command:
        return None
    
    try:
        if args.command == "quote":
            result = await get_quote(args.symbol)
        elif args.command == "account":
            result = await get_account_summary()
        elif args.command == "order":
            order_type = args.type.upper()
            result = await submit_order(
                symbol=args.symbol,
                action=args.action.upper(),
                quantity=args.quantity,
                order_type=order_type,
                limit_price=args.limit_price
            )
        elif args.command == "portfolio":
            result = await analyze_portfolio()
        elif args.command == "setup":
            result = await setup_paper_account(args.cash)
        elif args.command == "history":
            result = await get_historical_data(
                symbol=args.symbol,
                period=args.period,
                interval=args.interval
            )
        elif args.command == "watch":
            await watch_stocks(args.symbols, args.interval)
            return None
        else:
            return f"Unknown command: {args.command}"
        
        return result
    except Exception as e:
        logger.error(f"Error running command {args.command}: {e}")
        return f"Error: {str(e)}"

def main() -> None:
    """Main entry point for the CLI."""
    parser = setup_command_arguments()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    print(f"Executing {args.command}...")
    
    try:
        result = asyncio.run(run_command(args))
        if result:
            print(result)
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()