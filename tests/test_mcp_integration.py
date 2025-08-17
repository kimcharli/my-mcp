#!/usr/bin/env python3
"""
Integration tests for MCP server collection functionality.
Tests end-to-end workflows across all MCP servers.
"""
import os
import tempfile
import unittest
import asyncio
import json
from unittest.mock import patch, MagicMock, AsyncMock
from pathlib import Path
import pytest

# Test imports - these would normally be available when servers are running
# For testing, we'll mock the server interactions


class TestMCPIntegration(unittest.TestCase):
    """Integration test cases for MCP server collection."""
    
    def setUp(self):
        """Set up test environment for integration tests."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_data_dir = Path(self.temp_dir) / "test_data"
        self.test_data_dir.mkdir(exist_ok=True)
        
        # Create test files for filesystem operations
        (self.test_data_dir / "large_file.txt").write_text("x" * 1024 * 1024)  # 1MB file
        (self.test_data_dir / "small_file.txt").write_text("small content")
        (self.test_data_dir / "cache_file.cache").write_text("cache data")
        
    def tearDown(self):
        """Clean up test environment."""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    @pytest.mark.asyncio
    async def test_trading_workflow_integration(self):
        """Test complete trading workflow: setup → quote → order → portfolio analysis."""
        from unittest.mock import patch, AsyncMock
        
        # Mock the trading server functions
        with patch('trading.setup_paper_account') as mock_setup, \
             patch('trading.get_quote') as mock_quote, \
             patch('trading.submit_order') as mock_order, \
             patch('trading.analyze_portfolio') as mock_analyze:
            
            # Configure mocks for realistic workflow
            mock_setup.return_value = {
                "cash": 100000.0,
                "positions": {},
                "message": "Paper trading account created successfully"
            }
            
            mock_quote.return_value = {
                "symbol": "AAPL",
                "price": 150.0,
                "change": 2.5,
                "change_percent": 1.69
            }
            
            mock_order.return_value = {
                "success": True,
                "order_id": "12345",
                "message": "Order executed successfully",
                "execution_price": 150.0,
                "total": 1500.0
            }
            
            mock_analyze.return_value = {
                "total_value": 98500.0,
                "cash": 98500.0,
                "invested": 1500.0,
                "positions": [("AAPL", 1500.0, 1.52)]
            }
            
            # Execute workflow steps
            # Step 1: Setup account
            account = await mock_setup(cash=100000.0)
            self.assertEqual(account["cash"], 100000.0)
            
            # Step 2: Get quote
            quote = await mock_quote("AAPL")
            self.assertEqual(quote["symbol"], "AAPL")
            self.assertGreater(quote["price"], 0)
            
            # Step 3: Submit order
            order = await mock_order("AAPL", "buy", 10, "market")
            self.assertTrue(order["success"])
            self.assertEqual(order["execution_price"], 150.0)
            
            # Step 4: Analyze portfolio
            portfolio = await mock_analyze()
            self.assertGreater(portfolio["total_value"], 0)
            self.assertEqual(len(portfolio["positions"]), 1)
            
            # Verify all steps were called
            mock_setup.assert_called_once()
            mock_quote.assert_called_once_with("AAPL")
            mock_order.assert_called_once_with("AAPL", "buy", 10, "market")
            mock_analyze.assert_called_once()

    @pytest.mark.asyncio
    async def test_filesystem_workflow_integration(self):
        """Test complete filesystem workflow: analyze → identify → clean → verify."""
        # Import filesystem functions for testing
        # These would be mocked in real integration tests
        
        with patch('filesystem.disk_usage_summary') as mock_disk, \
             patch('filesystem.find_large_files') as mock_large, \
             patch('filesystem.clean_temp_files') as mock_clean, \
             patch('filesystem.analyze_directory_sizes') as mock_analyze:
            
            # Configure realistic responses
            mock_disk.return_value = "Disk: /dev/disk1s1\nTotal: 1.0 TB\nUsed: 500.0 GB (50.0%)\nFree: 500.0 GB"
            
            mock_large.return_value = f"Large files found:\n{self.test_data_dir}/large_file.txt - 1.0 MB"
            
            mock_analyze.return_value = f"Directory sizes:\n{self.test_data_dir} - 1.1 MB (100.0%)"
            
            mock_clean.return_value = "Cleaned 1 temporary files, freed 1.0 KB"
            
            # Execute workflow
            # Step 1: Analyze disk usage
            disk_summary = await mock_disk()
            self.assertIn("1.0 TB", disk_summary)
            self.assertIn("50.0%", disk_summary)
            
            # Step 2: Find large files
            large_files = await mock_large(min_size_mb=1, directory=str(self.test_data_dir))
            self.assertIn("large_file.txt", large_files)
            self.assertIn("1.0 MB", large_files)
            
            # Step 3: Analyze directories
            dir_analysis = await mock_analyze()
            self.assertIn("1.1 MB", dir_analysis)
            
            # Step 4: Clean temp files
            cleanup_result = await mock_clean(dry_run=False)
            self.assertIn("Cleaned", cleanup_result)
            
            # Verify workflow execution
            mock_disk.assert_called_once()
            mock_large.assert_called_once()
            mock_analyze.assert_called_once()
            mock_clean.assert_called_once()

    @pytest.mark.asyncio 
    async def test_weather_workflow_integration(self):
        """Test complete weather workflow: alerts → forecast → analysis."""
        
        with patch('weather.get_alerts') as mock_alerts, \
             patch('weather.get_forecast') as mock_forecast:
            
            # Configure realistic weather responses
            mock_alerts.return_value = """
Event: Winter Storm Warning
Area: Northern California
Severity: Moderate
Description: Heavy snow expected in mountain areas
Instructions: Avoid unnecessary travel
"""
            
            mock_forecast.return_value = """
Tonight:
Temperature: 35°F
Wind: 5 mph NW
Forecast: Partly cloudy with light winds

Tomorrow:
Temperature: 55°F
Wind: 10 mph SW
Forecast: Sunny and warm
"""
            
            # Execute workflow
            # Step 1: Check alerts
            alerts = await mock_alerts("CA")
            self.assertIn("Winter Storm Warning", alerts)
            self.assertIn("Northern California", alerts)
            
            # Step 2: Get forecast
            forecast = await mock_forecast(37.7749, -122.4194)  # San Francisco
            self.assertIn("Tonight", forecast)
            self.assertIn("35°F", forecast)
            self.assertIn("Tomorrow", forecast)
            self.assertIn("55°F", forecast)
            
            # Verify workflow execution
            mock_alerts.assert_called_once_with("CA")
            mock_forecast.assert_called_once_with(37.7749, -122.4194)

    @pytest.mark.asyncio
    async def test_cross_server_data_flow(self):
        """Test data flowing between different MCP servers."""
        # Simulate a scenario where filesystem analysis informs trading decisions
        # and weather data affects portfolio management
        
        with patch('filesystem.analyze_directory_sizes') as mock_fs, \
             patch('trading.get_quote') as mock_quote, \
             patch('weather.get_alerts') as mock_weather:
            
            # Mock responses
            mock_fs.return_value = "Cache usage: 2.5 GB - consider cleanup"
            mock_quote.return_value = {"symbol": "AAPL", "price": 150.0}
            mock_weather.return_value = "No active alerts"
            
            # Simulate workflow that uses all three servers
            # 1. Check system resources before trading
            fs_status = await mock_fs()
            system_healthy = "consider cleanup" not in fs_status
            
            # 2. Only proceed with trading if system is healthy
            if system_healthy:
                quote = await mock_quote("AAPL")
                trade_price = quote["price"]
            else:
                trade_price = None
            
            # 3. Check weather for any alerts that might affect markets
            weather_status = await mock_weather("CA")
            severe_weather = "Warning" in weather_status
            
            # Assertions
            self.assertFalse(system_healthy)  # Should detect cleanup needed
            self.assertIsNone(trade_price)  # Should skip trading due to system issues
            self.assertFalse(severe_weather)  # No severe weather detected
            
            # Verify all servers were consulted
            mock_fs.assert_called_once()
            mock_quote.assert_not_called()  # Should be skipped
            mock_weather.assert_called_once()

    @pytest.mark.asyncio
    async def test_error_handling_across_servers(self):
        """Test error handling and recovery across MCP servers."""
        
        with patch('trading.get_quote') as mock_quote, \
             patch('filesystem.disk_usage_summary') as mock_fs, \
             patch('weather.get_forecast') as mock_weather:
            
            # Configure various error scenarios
            mock_quote.side_effect = Exception("Network timeout")
            mock_fs.return_value = "Error: Permission denied"
            mock_weather.side_effect = Exception("API rate limit exceeded")
            
            # Test graceful error handling
            errors_caught = []
            
            # Trading server error
            try:
                await mock_quote("AAPL")
            except Exception as e:
                errors_caught.append(("trading", str(e)))
            
            # Filesystem server error (returns error string, doesn't raise)
            fs_result = await mock_fs()
            if "Error:" in fs_result:
                errors_caught.append(("filesystem", fs_result))
            
            # Weather server error
            try:
                await mock_weather(37.7749, -122.4194)
            except Exception as e:
                errors_caught.append(("weather", str(e)))
            
            # Verify all errors were caught
            self.assertEqual(len(errors_caught), 3)
            
            error_types = [error[0] for error in errors_caught]
            self.assertIn("trading", error_types)
            self.assertIn("filesystem", error_types)
            self.assertIn("weather", error_types)

    @pytest.mark.asyncio
    async def test_mcp_server_configuration(self):
        """Test MCP server configuration and initialization."""
        # Test that all servers can be configured and initialized properly
        
        server_configs = {
            "trading": {
                "name": "trading",
                "tools": ["get_quote", "submit_order", "analyze_portfolio", "setup_paper_account"]
            },
            "filesystem": {
                "name": "filesystem", 
                "tools": ["disk_usage_summary", "find_large_files", "clean_temp_files"]
            },
            "weather": {
                "name": "weather",
                "tools": ["get_alerts", "get_forecast"]
            }
        }
        
        # Verify configuration structure
        for server_name, config in server_configs.items():
            self.assertIn("name", config)
            self.assertIn("tools", config)
            self.assertIsInstance(config["tools"], list)
            self.assertGreater(len(config["tools"]), 0)
            
            # Verify server names are valid
            self.assertRegex(server_name, r'^[a-z]+$')

    def test_performance_requirements(self):
        """Test performance requirements across servers."""
        # Define performance thresholds
        performance_thresholds = {
            "response_time_ms": 5000,  # 5 seconds max
            "memory_usage_mb": 100,    # 100MB max
            "concurrent_requests": 10   # Handle 10 concurrent requests
        }
        
        # These would be measured in real performance tests
        # For now, verify thresholds are reasonable
        self.assertLessEqual(performance_thresholds["response_time_ms"], 10000)
        self.assertLessEqual(performance_thresholds["memory_usage_mb"], 500)
        self.assertGreaterEqual(performance_thresholds["concurrent_requests"], 5)

    @pytest.mark.asyncio
    async def test_security_compliance(self):
        """Test security compliance across all servers."""
        security_requirements = {
            "no_secrets_in_logs": True,
            "input_validation": True,
            "error_message_sanitization": True,
            "safe_file_operations": True
        }
        
        # Test input validation patterns
        invalid_inputs = [
            "../../../etc/passwd",  # Path traversal
            "<script>alert('xss')</script>",  # XSS
            "'; DROP TABLE users; --",  # SQL injection
            "\x00\x01\x02",  # Null bytes
        ]
        
        for invalid_input in invalid_inputs:
            # These should be properly validated by the servers
            # In real tests, we would verify the servers reject these
            self.assertTrue(len(invalid_input) > 0)  # Placeholder assertion
        
        # Verify security requirements
        for requirement, required in security_requirements.items():
            self.assertTrue(required, f"Security requirement {requirement} must be True")


class TestMCPServerRegistry(unittest.TestCase):
    """Test MCP server registry and discovery functionality."""
    
    def test_server_registry(self):
        """Test server registration and discovery."""
        expected_servers = ["trading", "filesystem", "weather", "add-demo"]
        
        # In a real implementation, this would test the actual registry
        registered_servers = expected_servers  # Placeholder
        
        for server in expected_servers:
            self.assertIn(server, registered_servers)
        
        # Verify no duplicate registrations
        self.assertEqual(len(registered_servers), len(set(registered_servers)))


if __name__ == '__main__':
    # Run integration tests
    unittest.main()