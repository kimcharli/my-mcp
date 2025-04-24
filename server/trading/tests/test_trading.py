#!/usr/bin/env python3
"""
Tests for the trading module functionality.
"""
import os
import unittest
import asyncio
from unittest.mock import patch, MagicMock
from datetime import datetime
from typing import Dict, Any
import pytest

# Import the modules to test
from trading import (
    get_quote, get_account_summary, submit_order, analyze_portfolio,
    setup_paper_account, get_historical_data
)
from models import OrderAction, OrderType, PaperAccount, Position, Order


class TestTrading(unittest.TestCase):
    """Test cases for the trading module functions."""
    
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
    
    @patch('market_data.MarketData.get_quote')
    @pytest.mark.asyncio
    async def test_get_quote(self, mock_get_quote):
        """Test the get_quote function."""
        # Configure mock
        mock_quote = {
            'symbol': 'AAPL',
            'name': 'Apple Inc.',
            'price': 150.0,
            'change': 2.0,
            'change_percent': 1.35,
            'volume': 1000000,
            'market_cap': 2500000000000,
            'pe_ratio': 25.5
        }
        mock_get_quote.return_value = mock_quote
        
        # Call the function
        result = await get_quote('AAPL')
        
        # Assertions
        self.assertEqual(result, mock_quote)
        mock_get_quote.assert_called_once_with('AAPL', use_mock=False)
    
    @patch('paper_trading.PaperTradingService.load_account')
    @pytest.mark.asyncio
    async def test_get_account_summary(self, mock_load_account):
        """Test the get_account_summary function."""
        # Create a mock account
        mock_account = Account(
            cash=100000.0,
            positions={
                'AAPL': Position(
                    symbol='AAPL',
                    quantity=10,
                    cost_basis=150.0,
                    current_price=160.0,
                    market_value=1600.0,
                    unrealized_pl=100.0,
                    unrealized_pl_percent=6.67
                ),
                'MSFT': Position(
                    symbol='MSFT',
                    quantity=5,
                    cost_basis=200.0,
                    current_price=220.0,
                    market_value=1100.0,
                    unrealized_pl=100.0,
                    unrealized_pl_percent=10.0
                )
            },
            transactions=[
                {
                    'id': '123',
                    'timestamp': datetime.now().isoformat(),
                    'symbol': 'AAPL',
                    'action': OrderAction.BUY,
                    'quantity': 10,
                    'price': 150.0,
                    'total': 1500.0
                }
            ],
            daily_pl={},
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        mock_load_account.return_value = mock_account
        
        # Call the function
        result = await get_account_summary()
        
        # Assertions
        self.assertEqual(result['cash'], 100000.0)
        self.assertEqual(len(result['positions']), 2)
        self.assertEqual(len(result['transactions']), 1)
        self.assertIn('created_at', result)
        self.assertIn('updated_at', result)
    
    @patch('paper_trading.PaperTradingService.create_order')
    @patch('paper_trading.PaperTradingService.submit_order')
    @patch('market_data.MarketData.get_quote')
    @patch('paper_trading.PaperTradingService.load_account')
    @pytest.mark.asyncio
    async def test_submit_order(self, mock_load, mock_quote, mock_submit, mock_create):
        """Test the submit_order function."""
        # Configure mocks
        mock_account = MagicMock()
        mock_load.return_value = mock_account
        
        mock_quote_result = {'price': 150.0}
        mock_quote.return_value = mock_quote_result
        
        mock_order = Order(
            id='123',
            timestamp=datetime.now().isoformat(),
            symbol='AAPL',
            action=OrderAction.BUY,
            quantity=10,
            order_type=OrderType.MARKET,
            price=150.0,
            total=1500.0
        )
        mock_create.return_value = mock_order
        
        mock_submission_result = {'success': True, 'message': 'Order executed successfully'}
        mock_submit.return_value = mock_submission_result
        
        # Call the function
        result = await submit_order(
            symbol='AAPL',
            action=OrderAction.BUY.value,
            quantity=10,
            order_type=OrderType.MARKET.value
        )
        
        # Assertions
        self.assertEqual(result, mock_submission_result)
        mock_quote.assert_called_once_with('AAPL')
        mock_create.assert_called_once_with(
            symbol='AAPL',
            action=OrderAction.BUY,
            quantity=10,
            order_type=OrderType.MARKET.value,
            current_price=150.0
        )
        mock_submit.assert_called_once_with(
            order=mock_order, 
            account=mock_account,
            execution_price=150.0
        )
    
    @patch('paper_trading.PaperTradingService.analyze_portfolio')
    @patch('paper_trading.PaperTradingService.load_account')
    @pytest.mark.asyncio
    async def test_analyze_portfolio(self, mock_load, mock_analyze):
        """Test the analyze_portfolio function."""
        # Configure mocks
        mock_account = MagicMock()
        mock_load.return_value = mock_account
        
        mock_analysis = {
            'total_value': 101500.0,
            'cash': 100000.0,
            'invested': 1500.0,
            'total_unrealized_pl': 100.0,
            'cash_percent': 98.52,
            'invested_percent': 1.48,
            'positions': [('AAPL', 1600.0, 1.57)]
        }
        mock_analyze.return_value = mock_analysis
        
        # Call the function
        result = await analyze_portfolio()
        
        # Assertions
        self.assertEqual(result, mock_analysis)
        mock_load.assert_called_once()
        mock_analyze.assert_called_once_with(mock_account)
    
    @patch('market_data.MarketData.get_historical_data')
    @pytest.mark.asyncio
    async def test_get_historical_data(self, mock_get_historical):
        """Test the get_historical_data function."""
        # Configure mock
        mock_data = {
            'start_date': '2023-01-01',
            'end_date': '2023-01-31',
            'start_price': 150.0,
            'end_price': 160.0,
            'high': 165.0,
            'low': 145.0,
            'change': 10.0,
            'change_percent': 6.67,
            'avg_volume': 1000000
        }
        mock_get_historical.return_value = mock_data
        
        # Call the function
        result = await get_historical_data('AAPL', period='1mo', interval='1d')
        
        # Assertions
        self.assertEqual(result, mock_data)
        mock_get_historical.assert_called_once_with(
            'AAPL', 
            period='1mo', 
            interval='1d',
            use_mock=False
        )
    
    @patch('paper_trading.PaperTradingService.setup_account')
    @pytest.mark.asyncio
    async def test_setup_paper_account(self, mock_setup):
        """Test the setup_paper_account function."""
        # Configure mock
        mock_account = MagicMock()
        mock_setup.return_value = mock_account
        
        # Call the function
        result = await setup_paper_account(cash=50000.0)
        
        # Assertions
        self.assertEqual(result, mock_account)
        mock_setup.assert_called_once_with(cash=50000.0)


# Helper function to run async tests
def run_async_test(coroutine):
    """Run an async test coroutine."""
    return asyncio.run(coroutine)


if __name__ == '__main__':
    unittest.main()