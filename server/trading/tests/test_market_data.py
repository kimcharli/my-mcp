#!/usr/bin/env python3
"""
Tests for the MarketData class functionality.
"""
import os
import unittest
import asyncio
import pandas as pd
from unittest.mock import patch, MagicMock
from typing import Dict, Any

# Import the module to test
from market_data import MarketData


class TestMarketData(unittest.TestCase):
    """Test cases for the MarketData class."""
    
    def setUp(self):
        """Set up test environment."""
        # Save original environment
        self.original_env = os.environ.copy()
        os.environ["DATA_REQUEST_TIMEOUT"] = "5.0"  # Shorter timeout for tests
    
    def tearDown(self):
        """Clean up the test environment."""
        # Restore original environment
        os.environ.clear()
        os.environ.update(self.original_env)
    
    def test_constants(self):
        """Test that constants are properly initialized."""
        # Should reflect the value set in setUp
        from market_data import DEFAULT_TIMEOUT
        self.assertEqual(DEFAULT_TIMEOUT, 5.0)
    
    @patch('yfinance.Ticker')
    async def test_get_quote_mock(self, mock_ticker):
        """Test the get_quote method with mock data."""
        # Configure mock
        mock_ticker_instance = MagicMock()
        mock_ticker.return_value = mock_ticker_instance
        
        # Create mock info and history data
        mock_ticker_instance.info = {
            'shortName': 'Apple Inc.',
            'regularMarketPrice': 150.0,
            'regularMarketPreviousClose': 148.0,
            'regularMarketVolume': 1000000,
            'marketCap': 2500000000000,
            'trailingPE': 25.5
        }
        
        # Test with mock mode
        quote = await MarketData.get_quote('AAPL', use_mock=True)
        
        # Assertions for mock mode
        self.assertIn('price', quote)
        self.assertIn('change', quote)
        self.assertIn('change_percent', quote)
        
    @patch('yfinance.Ticker')
    async def test_get_quote_real(self, mock_ticker):
        """Test the get_quote method with simulated real data."""
        # Configure mock for yfinance.Ticker
        mock_ticker_instance = MagicMock()
        mock_ticker.return_value = mock_ticker_instance
        
        # Create mock info data
        mock_ticker_instance.info = {
            'shortName': 'Apple Inc.',
            'regularMarketPrice': 150.0,
            'regularMarketPreviousClose': 148.0,
            'regularMarketVolume': 1000000,
            'marketCap': 2500000000000,
            'trailingPE': 25.5
        }
        
        # Test with regular mode
        quote = await MarketData.get_quote('AAPL', use_mock=False)
        
        # Assertions
        self.assertEqual(quote['price'], 150.0)
        self.assertEqual(quote['change'], 2.0)
        self.assertAlmostEqual(quote['change_percent'], 1.3513513513513513)
        self.assertEqual(quote['volume'], 1000000)
        self.assertEqual(quote['name'], 'Apple Inc.')
        self.assertEqual(quote['market_cap'], 2500000000000)
        self.assertEqual(quote['pe_ratio'], 25.5)
    
    @patch('yfinance.Ticker')
    async def test_get_quote_error(self, mock_ticker):
        """Test error handling in get_quote."""
        # Configure mock to raise an exception
        mock_ticker.side_effect = Exception("API error")
        
        # Test exception handling
        with self.assertRaises(Exception):
            await MarketData.get_quote('AAPL')
    
    @patch('yfinance.Ticker')
    async def test_get_historical_data(self, mock_ticker):
        """Test the get_historical_data method."""
        # Configure mock
        mock_ticker_instance = MagicMock()
        mock_ticker.return_value = mock_ticker_instance
        
        # Create mock history data
        index = pd.date_range(start='2023-01-01', periods=30)
        mock_history = pd.DataFrame({
            'Open': range(100, 130),
            'High': range(105, 135),
            'Low': range(95, 125),
            'Close': range(102, 132),
            'Volume': [1000000] * 30
        }, index=index)
        mock_ticker_instance.history.return_value = mock_history
        
        # Test with regular parameters
        data = await MarketData.get_historical_data('AAPL', period='1mo', interval='1d')
        
        # Assertions
        self.assertIn('start_date', data)
        self.assertIn('end_date', data)
        self.assertIn('start_price', data)
        self.assertIn('end_price', data)
        self.assertIn('high', data)
        self.assertIn('low', data)
        self.assertIn('change', data)
        self.assertIn('change_percent', data)
        self.assertIn('avg_volume', data)
        
        # Verify correct calculations
        self.assertEqual(data['start_price'], 102)
        self.assertEqual(data['end_price'], 131)
        self.assertEqual(data['high'], 134)
        self.assertEqual(data['low'], 95)
        self.assertEqual(data['change'], 29)
        self.assertAlmostEqual(data['change_percent'], (29 / 102) * 100)
    
    @patch('yfinance.Ticker')
    async def test_get_historical_data_mock(self, mock_ticker):
        """Test the get_historical_data method with mock data."""
        # Test with mock mode
        data = await MarketData.get_historical_data('AAPL', use_mock=True)
        
        # Basic assertions for mock data
        self.assertIn('start_date', data)
        self.assertIn('end_date', data)
        self.assertIn('start_price', data)
        self.assertIn('end_price', data)
        self.assertIn('high', data)
        self.assertIn('low', data)
        self.assertIn('change', data)
        self.assertIn('change_percent', data)
        self.assertIn('avg_volume', data)


# Helper function to run async tests
def run_async_test(coroutine):
    """Run an async test coroutine."""
    return asyncio.run(coroutine)


if __name__ == '__main__':
    unittest.main()