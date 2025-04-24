"""
Market data retrieval and processing.
"""
import os
import logging
import asyncio
from typing import Dict, Any, Optional
import pandas as pd
import yfinance as yf

logger = logging.getLogger("trading-mcp.market_data")

# Constants
DEFAULT_TIMEOUT = float(os.getenv("DATA_REQUEST_TIMEOUT", "5.0"))  # seconds


class MarketData:
    """Market data service for retrieving stock quotes and historical data."""
    
    @staticmethod
    async def get_quote(symbol: str, timeout: float = DEFAULT_TIMEOUT, use_mock: bool = False) -> Dict[str, Any]:
        """Get current price quote for a stock.
        
        Args:
            symbol: The stock ticker symbol (e.g., AAPL, MSFT, GOOGL)
            timeout: Maximum time to wait for data
            use_mock: Use mock data instead of actual API
            
        Returns:
            Dictionary with quote information
        """
        logger.info(f"Getting quote for {symbol}")
        
        if use_mock:
            return {
                "price": 150.50,  # Mock data for stock
                "change": 2.30,
                "change_percent": 1.55,
                "volume": 65000000,
                "name": f"{symbol} Inc."
            }
        
        try:
            def fetch_quote():
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period="2d")
                info = ticker.info if hasattr(ticker, 'info') else {}
                
                if hist.empty:
                    return None
                
                current = hist.iloc[-1]
                prev = hist.iloc[0] if len(hist) > 1 else current
                
                # Calculate change
                change = current["Close"] - prev["Close"]
                change_percent = (change / prev["Close"]) * 100
                
                return {
                    "price": current["Close"],
                    "change": change,
                    "change_percent": change_percent,
                    "volume": int(current["Volume"]),
                    "name": info.get("longName", f"{symbol}"),
                    "market_cap": info.get("marketCap"),
                    "pe_ratio": info.get("trailingPE")
                }
                
            return await asyncio.wait_for(asyncio.to_thread(fetch_quote), timeout=timeout)
        except asyncio.TimeoutError:
            logger.error(f"Timed out while fetching quote for {symbol}")
            raise TimeoutError(f"Timed out while retrieving quote for {symbol}")
        except Exception as e:
            logger.error(f"Error getting quote for {symbol}: {e}")
            raise

    @staticmethod
    async def get_historical_data(symbol: str, period: str = "1mo", interval: str = "1d", timeout: float = DEFAULT_TIMEOUT, use_mock: bool = False) -> Dict[str, Any]:
        """Get historical price data for a stock.
        
        Args:
            symbol: The stock ticker symbol (e.g., AAPL, MSFT)
            period: Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            interval: Data interval (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)
            timeout: Maximum time to wait for data
            use_mock: Use mock data instead of actual API
            
        Returns:
            Dictionary with historical data
        """
        logger.info(f"Getting historical data for {symbol}")
        
        if use_mock:
            # Create mock historical data
            import numpy as np
            from datetime import datetime, timedelta
            
            end_date = datetime.now()
            dates = []
            prices = []
            volumes = []
            
            # Generate 30 days of mock data
            start_price = 100.0
            price = start_price
            for i in range(30):
                day = end_date - timedelta(days=30-i)
                dates.append(day.strftime("%Y-%m-%d"))
                price = price * (1 + np.random.normal(0, 0.02))  # Random walk with 2% std dev
                prices.append(price)
                volumes.append(int(np.random.uniform(1000000, 10000000)))
            
            return {
                "dates": dates,
                "prices": prices,
                "volumes": volumes,
                "start_price": prices[0],
                "end_price": prices[-1],
                "high": max(prices),
                "low": min(prices),
                "avg_volume": sum(volumes) / len(volumes)
            }
        
        try:
            def fetch_historical():
                data = yf.download(symbol, period=period, interval=interval, progress=False)
                
                if data.empty:
                    return None
                
                # Calculate basic statistics
                latest = data.iloc[-1]
                earliest = data.iloc[0]
                high = data["High"].max()
                low = data["Low"].min()
                change = latest["Close"] - earliest["Close"]
                change_percent = (change / earliest["Close"]) * 100
                
                return {
                    "data": data,
                    "start_date": data.index[0].strftime("%Y-%m-%d"),
                    "end_date": data.index[-1].strftime("%Y-%m-%d"),
                    "start_price": float(earliest["Close"]),
                    "end_price": float(latest["Close"]),
                    "change": float(change),
                    "change_percent": float(change_percent),
                    "high": float(high),
                    "low": float(low),
                    "avg_volume": float(data["Volume"].mean())
                }
                
            return await asyncio.wait_for(asyncio.to_thread(fetch_historical), timeout=timeout)
        except asyncio.TimeoutError:
            logger.error(f"Timed out while fetching historical data for {symbol}")
            raise TimeoutError(f"Timed out while retrieving historical data for {symbol}")
        except Exception as e:
            logger.error(f"Error getting historical data for {symbol}: {e}")
            raise