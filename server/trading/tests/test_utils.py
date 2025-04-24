#!/usr/bin/env python3
"""
Tests for utility functions in the trading system.
"""
import os
import unittest
import tempfile
import json
from pathlib import Path
from unittest.mock import patch, mock_open

# Import the module to test
from utils import (
    generate_id, format_money, load_json_file, 
    save_json_file, get_env_var
)


class TestUtils(unittest.TestCase):
    """Test cases for utility functions."""
    
    def setUp(self):
        """Set up test environment."""
        # Create a temp directory for file operations
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)
        
        # Save original environment
        self.original_env = os.environ.copy()
    
    def tearDown(self):
        """Clean up the test environment."""
        # Remove temp directory
        self.temp_dir.cleanup()
        
        # Restore original environment
        os.environ.clear()
        os.environ.update(self.original_env)
    
    def test_generate_id(self):
        """Test the generate_id function."""
        # Generate IDs with different prefixes
        order_id = generate_id("order")
        trade_id = generate_id("trade")
        
        # Assertions
        self.assertTrue(order_id.startswith("order-"))
        self.assertTrue(trade_id.startswith("trade-"))
        self.assertEqual(len(order_id), 14)  # prefix(5) + dash(1) + uuid(8)
        self.assertEqual(len(trade_id), 14)  # prefix(5) + dash(1) + uuid(8)
        self.assertNotEqual(order_id, trade_id)
        
        # Generate multiple IDs with same prefix to check uniqueness
        ids = [generate_id("test") for _ in range(10)]
        self.assertEqual(len(set(ids)), 10)  # All IDs should be unique
    
    def test_format_money(self):
        """Test the format_money function."""
        test_cases = [
            (0, "$0.00"),
            (10, "$10.00"),
            (10.5, "$10.50"),
            (10.567, "$10.57"),  # Should round to 2 decimal places
            (1000, "$1000.00"),
            (-50.25, "-$50.25"),  # Negative value
            (0.01, "$0.01")
        ]
        
        for value, expected in test_cases:
            self.assertEqual(format_money(value), expected)
    
    @patch('pathlib.Path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_load_json_file_existing(self, mock_file, mock_exists):
        """Test loading an existing JSON file."""
        # Configure mocks
        mock_exists.return_value = True
        mock_data = {'key': 'value', 'number': 42}
        mock_file.return_value.__enter__.return_value.read.return_value = json.dumps(mock_data)
        
        # Call the function
        result = load_json_file(Path('/tmp/test.json'))
        
        # Assertions
        self.assertEqual(result, mock_data)
        mock_exists.assert_called_once()
        mock_file.assert_called_once_with(Path('/tmp/test.json'), 'r')
    
    @patch('pathlib.Path.exists')
    def test_load_json_file_non_existing(self, mock_exists):
        """Test loading a non-existent JSON file."""
        # Configure mock
        mock_exists.return_value = False
        default_value = {'default': True}
        
        # Call the function
        result = load_json_file(Path('/tmp/not-exists.json'), default=default_value)
        
        # Assertions
        self.assertEqual(result, default_value)
        mock_exists.assert_called_once()
    
    @patch('builtins.open', side_effect=Exception("Test error"))
    def test_load_json_file_error(self, mock_file):
        """Test error handling when loading a JSON file."""
        # Configure mock to raise an exception
        mock_data = {'default': True}
        
        # Call the function
        result = load_json_file(Path('/tmp/error.json'), default=mock_data)
        
        # Assertions
        self.assertEqual(result, mock_data)  # Should return the default value
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_json_file_success(self, mock_dump, mock_file):
        """Test successfully saving a JSON file."""
        # Call the function
        data = {'key': 'value', 'nested': {'data': [1, 2, 3]}}
        result = save_json_file(Path('/tmp/save.json'), data)
        
        # Assertions
        self.assertTrue(result)
        mock_file.assert_called_once_with(Path('/tmp/save.json'), 'w')
        mock_dump.assert_called_once()
    
    @patch('builtins.open', side_effect=Exception("Test error"))
    def test_save_json_file_error(self, mock_file):
        """Test error handling when saving a JSON file."""
        # Call the function with mock raising an exception
        result = save_json_file(Path('/tmp/error.json'), {'data': 'test'})
        
        # Assertions
        self.assertFalse(result)
    
    def test_get_env_var_string(self):
        """Test getting string environment variables."""
        # Set environment variables for testing
        os.environ['TEST_STRING'] = 'test_value'
        
        # Call the function
        result = get_env_var('TEST_STRING', default='default')
        
        # Assertions
        self.assertEqual(result, 'test_value')
        
        # Test with non-existent variable
        result = get_env_var('NON_EXISTENT', default='default')
        self.assertEqual(result, 'default')
    
    def test_get_env_var_int(self):
        """Test getting integer environment variables."""
        # Set environment variables for testing
        os.environ['TEST_INT'] = '42'
        
        # Call the function
        result = get_env_var('TEST_INT', default=0)
        
        # Assertions
        self.assertEqual(result, 42)
        self.assertIsInstance(result, int)
    
    def test_get_env_var_float(self):
        """Test getting float environment variables."""
        # Set environment variables for testing
        os.environ['TEST_FLOAT'] = '3.14'
        
        # Call the function
        result = get_env_var('TEST_FLOAT', default=0.0)
        
        # Assertions
        self.assertEqual(result, 3.14)
        self.assertIsInstance(result, float)
    
    def test_get_env_var_bool(self):
        """Test getting boolean environment variables."""
        # Set environment variables for testing
        os.environ['TEST_BOOL_TRUE'] = 'TRUE'
        os.environ['TEST_BOOL_YES'] = 'yes'
        os.environ['TEST_BOOL_1'] = '1'
        os.environ['TEST_BOOL_FALSE'] = 'false'
        
        # Call the function
        result_true = get_env_var('TEST_BOOL_TRUE', default=False)
        result_yes = get_env_var('TEST_BOOL_YES', default=False)
        result_1 = get_env_var('TEST_BOOL_1', default=False)
        result_false = get_env_var('TEST_BOOL_FALSE', default=True)
        
        # Assertions
        self.assertTrue(result_true)
        self.assertTrue(result_yes)
        self.assertTrue(result_1)
        self.assertFalse(result_false)
    
    def test_get_env_var_required(self):
        """Test required environment variables."""
        # Test with a non-existent required variable
        with self.assertRaises(ValueError):
            get_env_var('REQUIRED_VAR', required=True)
        
        # Set the variable and test again
        os.environ['REQUIRED_VAR'] = 'exists'
        value = get_env_var('REQUIRED_VAR', required=True)
        self.assertEqual(value, 'exists')


if __name__ == '__main__':
    unittest.main()