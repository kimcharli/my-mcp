#!/usr/bin/env python3
"""
Tests for the PaperTradingService class functionality.
"""
import os
import json
import unittest
import asyncio
from unittest.mock import patch, MagicMock, mock_open
from datetime import datetime
from typing import Dict, Any
from pathlib import Path
import pytest

# Import the modules to test
from paper_trading import PaperTradingService
import paper_trading
from models import OrderAction, OrderType, PaperAccount, Position, Order

# Change this line at the top of the file
DEFAULT_TIMEOUT = float(os.getenv("DATA_REQUEST_TIMEOUT", "5.0"))  # seconds

class TestPaperTradingService(unittest.TestCase):
    """Test cases for the PaperTradingService class."""
    
    def setUp(self):
        """Set up test environment."""
        # Create a temp path for test account data
        self.temp_account_path = "/tmp/test_paper_account.json"
        self.original_account_path = paper_trading.PAPER_ACCOUNT_FILE
        paper_trading.PAPER_ACCOUNT_FILE = self.temp_account_path
        
        # Create a test account
        self.test_account = PaperAccount(
            cash=100000.0,
            positions={},
            orders={},
            trades=[],
            daily_pl={}
        )
    
    def tearDown(self):
        """Clean up the test environment."""
        # Restore original path
        paper_trading.PAPER_ACCOUNT_FILE = self.original_account_path
        
        # Remove test file if it exists
        if os.path.exists(self.temp_account_path):
            os.remove(self.temp_account_path)
    
    @patch('json.dump')
    @patch('builtins.open', new_callable=mock_open)
    def test_setup_account(self, mock_file, mock_dump):
        """Test the setup_account method."""
        # Call the method
        account = PaperTradingService.setup_account(cash=50000.0)
        
        # Assertions
        self.assertEqual(account.cash, 50000.0)
        self.assertEqual(account.positions, {})
        self.assertEqual(account.orders, {})
        self.assertEqual(account.trades, [])
        self.assertIsNotNone(account)
        
        # Verify file operations
        mock_file.assert_called_with(self.temp_account_path, 'w')
        mock_dump.assert_called_once()
    
    @patch('json.load')
    @patch('builtins.open', new_callable=mock_open)
    @patch('pathlib.Path.exists', return_value=True)
    def test_load_account_existing(self, mock_exists, mock_file, mock_load):
        """Test loading an existing account."""
        # Configure mocks
        mock_load.return_value = {
            'cash': 50000.0,
            'positions': {
                'AAPL': {
                    'symbol': 'AAPL',
                    'quantity': 10,
                    'cost_basis': 150.0,
                    'current_price': 155.0,
                    'market_value': 1550.0,
                    'unrealized_pl': 50.0,
                    'unrealized_pl_percent': 3.33
                }
            },
            'orders': {},
            'trades': [
                {
                    'trade_id': 'trade-123',
                    'order_id': 'order-456',
                    'symbol': 'AAPL',
                    'action': 'BUY',
                    'quantity': 10,
                    'price': 150.0,
                    'timestamp': datetime.now().isoformat(),
                    'commission': 0.0
                }
            ],
            'daily_pl': {}
        }
        
        # Call the method
        account = PaperTradingService.load_account()
        
        # Assertions
        self.assertEqual(account.cash, 50000.0)
        self.assertEqual(len(account.positions), 1)
        self.assertEqual(account.positions['AAPL'].quantity, 10)
        self.assertEqual(len(account.trades), 1)
    
    @patch('os.path.exists', return_value=False)
    def test_load_account_not_existing(self, mock_exists):
        """Test loading a non-existing account."""
        # Mock the setup_account method
        original_setup = PaperTradingService.setup_account
        PaperTradingService.setup_account = MagicMock(return_value=self.test_account)
        
        # Call the method
        account = PaperTradingService.load_account()
        
        # Assertions
        self.assertEqual(account, self.test_account)
        PaperTradingService.setup_account.assert_called_once()
        
        # Restore original method
        PaperTradingService.setup_account = original_setup
    
    @patch('paper_trading.PaperTradingService.load_account')
    @patch('paper_trading.PaperTradingService.save_account')
    @pytest.mark.asyncio
    async def test_create_order(self, mock_save, mock_load):
        """Test creating a new order."""
        # Configure mock
        mock_load.return_value = self.test_account
        
        # Call the method
        order = await PaperTradingService.create_order(
            symbol='AAPL',
            action=OrderAction.BUY,
            quantity=10,
            order_type=OrderType.MARKET.value,
            current_price=150.0
        )
        
        # Assertions
        self.assertEqual(order.symbol, 'AAPL')
        self.assertEqual(order.action, OrderAction.BUY)
        self.assertEqual(order.quantity, 10)
        self.assertEqual(order.price, 150.0)
        self.assertEqual(order.total, 1500.0)
    
    @patch('paper_trading.PaperTradingService.load_account')
    @patch('paper_trading.PaperTradingService.save_account')
    @pytest.mark.asyncio
    async def test_submit_buy_order(self, mock_save, mock_load):
        """Test submitting a buy order."""
        # Configure mocks
        mock_load.return_value = self.test_account
        
        # Create a test order
        order = Order(
            id='123',
            timestamp=datetime.now().isoformat(),
            symbol='AAPL',
            action=OrderAction.BUY,
            quantity=10,
            order_type=OrderType.MARKET,
            price=150.0,
            total=1500.0
        )
        
        # Call the method
        result = await PaperTradingService.submit_order(
            order=order,
            account=self.test_account,
            execution_price=150.0
        )
        
        # Assertions
        self.assertTrue(result['success'])
        self.assertEqual(self.test_account.cash, 100000.0 - 1500.0)
        self.assertIn('AAPL', self.test_account.positions)
        self.assertEqual(self.test_account.positions['AAPL'].quantity, 10)
        self.assertEqual(len(self.test_account.trades), 1)
        mock_save.assert_called_once()
    
    @patch('paper_trading.PaperTradingService.load_account')
    @patch('paper_trading.PaperTradingService.save_account')
    @pytest.mark.asyncio
    async def test_submit_sell_order(self, mock_save, mock_load):
        """Test submitting a sell order."""
        # Set up an account with an existing position
        account = PaperAccount(
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
                )
            },
            orders={},
            trades=[],
            daily_pl={}
        )
        mock_load.return_value = account
        
        # Create a test order
        order = Order(
            id='123',
            timestamp=datetime.now().isoformat(),
            symbol='AAPL',
            action=OrderAction.SELL,
            quantity=5,
            order_type=OrderType.MARKET,
            price=160.0,
            total=800.0
        )
        
        # Call the method
        result = await PaperTradingService.submit_order(
            order=order,
            account=account,
            execution_price=160.0
        )
        
        # Assertions
        self.assertTrue(result['success'])
        self.assertEqual(account.cash, 100000.0 + 800.0)
        self.assertEqual(account.positions['AAPL'].quantity, 5)
        self.assertEqual(len(account.trades), 1)
        mock_save.assert_called_once()
    
    @patch('paper_trading.PaperTradingService.load_account')
    @patch('paper_trading.PaperTradingService.save_account')
    @pytest.mark.asyncio
    async def test_insufficient_funds(self, mock_save, mock_load):
        """Test order failure due to insufficient funds."""
        # Configure mock with low cash balance
        account = PaperAccount(
            cash=1000.0,  # Not enough for the order
            positions={},
            orders={},
            trades=[],
            daily_pl={}
        )
        mock_load.return_value = account
        
        # Create a test order that exceeds available cash
        order = Order(
            id='123',
            timestamp=datetime.now().isoformat(),
            symbol='AAPL',
            action=OrderAction.BUY,
            quantity=10,
            order_type=OrderType.MARKET,
            price=150.0,
            total=1500.0
        )
        
        # Call the method
        result = await PaperTradingService.submit_order(
            order=order,
            account=account,
            execution_price=150.0
        )
        
        # Assertions
        self.assertFalse(result['success'])
        self.assertIn('insufficient funds', result['message'].lower())
        self.assertEqual(account.cash, 1000.0)  # Cash unchanged
        self.assertEqual(len(account.positions), 0)
        self.assertEqual(len(account.trades), 0)
        mock_save.assert_not_called()
    
    @patch('paper_trading.PaperTradingService.load_account')
    @patch('paper_trading.PaperTradingService.save_account')
    @pytest.mark.asyncio
    async def test_insufficient_shares(self, mock_save, mock_load):
        """Test order failure due to insufficient shares for selling."""
        # Configure mock with a position that has fewer shares than the sell order
        account = PaperAccount(
            cash=100000.0,
            positions={
                'AAPL': Position(
                    symbol='AAPL',
                    quantity=5,  # Not enough for the order
                    cost_basis=150.0,
                    current_price=160.0,
                    market_value=800.0,
                    unrealized_pl=50.0,
                    unrealized_pl_percent=6.67
                )
            },
            orders={},
            trades=[],
            daily_pl={}
        )
        mock_load.return_value = account
        
        # Create a test order
        order = Order(
            id='123',
            timestamp=datetime.now().isoformat(),
            symbol='AAPL',
            action=OrderAction.SELL,
            quantity=10,  # More than available
            order_type=OrderType.MARKET,
            price=160.0,
            total=1600.0
        )
        
        # Call the method
        result = await PaperTradingService.submit_order(
            order=order,
            account=account,
            execution_price=160.0
        )
        
        # Assertions
        self.assertFalse(result['success'])
        self.assertIn('insufficient shares', result['message'].lower())
        self.assertEqual(account.cash, 100000.0)  # Cash unchanged
        self.assertEqual(account.positions['AAPL'].quantity, 5)  # Position unchanged
        self.assertEqual(len(account.trades), 0)
        mock_save.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_update_positions(self):
        """Test updating positions with current prices."""
        # Create an account with positions
        account = PaperAccount(
            cash=100000.0,
            positions={
                'AAPL': Position(
                    symbol='AAPL',
                    quantity=10,
                    cost_basis=150.0,
                    current_price=150.0,
                    market_value=1500.0,
                    unrealized_pl=0.0,
                    unrealized_pl_percent=0.0
                ),
                'MSFT': Position(
                    symbol='MSFT',
                    quantity=5,
                    cost_basis=200.0,
                    current_price=200.0,
                    market_value=1000.0,
                    unrealized_pl=0.0,
                    unrealized_pl_percent=0.0
                )
            },
            orders={},
            trades=[],
            daily_pl={}
        )
        
        # Current prices to update
        current_prices = {
            'AAPL': 160.0,
            'MSFT': 220.0
        }
        
        # Call the method
        updated_account = await PaperTradingService.update_positions(account, current_prices)
        
        # Assertions for AAPL
        aapl_pos = updated_account.positions['AAPL']
        self.assertEqual(aapl_pos.current_price, 160.0)
        self.assertEqual(aapl_pos.market_value, 1600.0)
        self.assertEqual(aapl_pos.unrealized_pl, 100.0)
        self.assertAlmostEqual(aapl_pos.unrealized_pl_percent, 6.67, places=2)
        
        # Assertions for MSFT
        msft_pos = updated_account.positions['MSFT']
        self.assertEqual(msft_pos.current_price, 220.0)
        self.assertEqual(msft_pos.market_value, 1100.0)
        self.assertEqual(msft_pos.unrealized_pl, 100.0)
        self.assertAlmostEqual(msft_pos.unrealized_pl_percent, 10.0, places=2)
    
    @patch('paper_trading.PaperTradingService.load_account')
    @patch('paper_trading.PaperTradingService.save_account')
    @pytest.mark.asyncio
    async def test_analyze_portfolio(self, mock_save, mock_load):
        """Test portfolio analysis."""
        # Create an account with positions
        account = PaperAccount(
            cash=50000.0,
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
            orders={},
            trades=[],
            daily_pl={}
        )
        mock_load.return_value = account
        
        # Call the method
        analysis = await PaperTradingService.analyze_portfolio(account)
        
        # Assertions
        self.assertEqual(analysis['total_value'], 52700.0)  # 50000 + 1600 + 1100
        self.assertEqual(analysis['cash'], 50000.0)
        self.assertEqual(analysis['invested'], 2700.0)  # 1600 + 1100
        self.assertEqual(analysis['total_unrealized_pl'], 200.0)  # 100 + 100
        self.assertAlmostEqual(analysis['cash_percent'], (50000.0 / 52700.0) * 100, places=2)
        self.assertAlmostEqual(analysis['invested_percent'], (2700.0 / 52700.0) * 100, places=2)
        
        # Check position details
        self.assertEqual(len(analysis['positions']), 2)
        pos_symbols = [p[0] for p in analysis['positions']]
        self.assertIn('AAPL', pos_symbols)
        self.assertIn('MSFT', pos_symbols)


# Helper function to run async tests
def run_async_test(coroutine):
    """Run an async test coroutine."""
    return asyncio.run(coroutine)


if __name__ == '__main__':
    unittest.main()