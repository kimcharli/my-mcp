#!/usr/bin/env python3
"""
Tests for the weather MCP server functionality.
"""
import unittest
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock
import pytest

# Import the modules to test
from weather import (
    get_alerts, get_forecast, make_nws_request, format_alert,
    NWS_API_BASE, USER_AGENT
)


class TestWeatherServer(unittest.TestCase):
    """Test cases for the weather server functions."""
    
    def setUp(self):
        """Set up test environment."""
        self.sample_alert_feature = {
            "properties": {
                "event": "Winter Storm Warning",
                "areaDesc": "Northern California",
                "severity": "Moderate",
                "description": "Heavy snow expected in mountain areas",
                "instruction": "Avoid unnecessary travel"
            }
        }
        
        self.sample_forecast_period = {
            "name": "Tonight",
            "temperature": 35,
            "temperatureUnit": "F",
            "windSpeed": "5 mph",
            "windDirection": "NW",
            "detailedForecast": "Partly cloudy with light winds"
        }

    def test_format_alert(self):
        """Test alert formatting function."""
        result = format_alert(self.sample_alert_feature)
        
        self.assertIn("Winter Storm Warning", result)
        self.assertIn("Northern California", result)
        self.assertIn("Moderate", result)
        self.assertIn("Heavy snow expected", result)
        self.assertIn("Avoid unnecessary travel", result)

    @patch('weather.httpx.AsyncClient')
    @pytest.mark.asyncio
    async def test_make_nws_request_success(self, mock_client_class):
        """Test successful NWS API request."""
        # Mock the client and response
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {"test": "data"}
        mock_response.raise_for_status.return_value = None
        
        mock_client.get = AsyncMock(return_value=mock_response)
        mock_client_class.return_value.__aenter__.return_value = mock_client
        
        result = await make_nws_request("http://test.com/api")
        
        self.assertEqual(result, {"test": "data"})
        mock_client.get.assert_called_once()
        
        # Check that proper headers were used
        call_args = mock_client.get.call_args
        headers = call_args[1]['headers']
        self.assertEqual(headers['User-Agent'], USER_AGENT)
        self.assertEqual(headers['Accept'], "application/geo+json")

    @patch('weather.httpx.AsyncClient')
    @pytest.mark.asyncio
    async def test_make_nws_request_failure(self, mock_client_class):
        """Test failed NWS API request."""
        # Mock client that raises an exception
        mock_client = MagicMock()
        mock_client.get = AsyncMock(side_effect=Exception("Network error"))
        mock_client_class.return_value.__aenter__.return_value = mock_client
        
        result = await make_nws_request("http://test.com/api")
        
        self.assertIsNone(result)

    @patch('weather.make_nws_request')
    @pytest.mark.asyncio
    async def test_get_alerts_success(self, mock_request):
        """Test successful alert retrieval."""
        # Mock API response with alerts
        mock_response = {
            "features": [
                self.sample_alert_feature,
                {
                    "properties": {
                        "event": "Flood Warning",
                        "areaDesc": "San Francisco Bay Area",
                        "severity": "Minor",
                        "description": "Urban flooding possible",
                        "instruction": "Turn around, don't drown"
                    }
                }
            ]
        }
        mock_request.return_value = mock_response
        
        result = await get_alerts("CA")
        
        self.assertIn("Winter Storm Warning", result)
        self.assertIn("Flood Warning", result)
        self.assertIn("Northern California", result)
        self.assertIn("San Francisco Bay Area", result)
        
        # Check API was called with correct URL
        expected_url = f"{NWS_API_BASE}/alerts/active/area/CA"
        mock_request.assert_called_once_with(expected_url)

    @patch('weather.make_nws_request')
    @pytest.mark.asyncio
    async def test_get_alerts_no_alerts(self, mock_request):
        """Test alert retrieval when no alerts are active."""
        # Mock API response with no alerts
        mock_response = {"features": []}
        mock_request.return_value = mock_response
        
        result = await get_alerts("CA")
        
        self.assertIn("No active alerts", result)

    @patch('weather.make_nws_request')
    @pytest.mark.asyncio
    async def test_get_alerts_api_failure(self, mock_request):
        """Test alert retrieval when API fails."""
        mock_request.return_value = None
        
        result = await get_alerts("CA")
        
        self.assertIn("Unable to fetch alerts", result)

    @patch('weather.make_nws_request')
    @pytest.mark.asyncio
    async def test_get_alerts_invalid_response(self, mock_request):
        """Test alert retrieval with invalid API response."""
        # Mock API response without features
        mock_response = {"invalid": "data"}
        mock_request.return_value = mock_response
        
        result = await get_alerts("CA")
        
        self.assertIn("Unable to fetch alerts", result)

    @patch('weather.make_nws_request')
    @pytest.mark.asyncio
    async def test_get_forecast_success(self, mock_request):
        """Test successful forecast retrieval."""
        # Mock the two API calls needed for forecast
        def mock_request_side_effect(url):
            if "points" in url:
                return {
                    "properties": {
                        "forecast": "https://api.weather.gov/gridpoints/MTR/85,105/forecast"
                    }
                }
            elif "forecast" in url:
                return {
                    "properties": {
                        "periods": [
                            self.sample_forecast_period,
                            {
                                "name": "Tuesday",
                                "temperature": 55,
                                "temperatureUnit": "F",
                                "windSpeed": "10 mph",
                                "windDirection": "SW",
                                "detailedForecast": "Sunny and warm"
                            }
                        ]
                    }
                }
            return None
        
        mock_request.side_effect = mock_request_side_effect
        
        result = await get_forecast(37.7749, -122.4194)  # San Francisco coordinates
        
        self.assertIn("Tonight", result)
        self.assertIn("35°F", result)
        self.assertIn("5 mph NW", result)
        self.assertIn("Partly cloudy", result)
        self.assertIn("Tuesday", result)
        self.assertIn("55°F", result)
        
        # Should make two API calls
        self.assertEqual(mock_request.call_count, 2)
        
        # Check first call was to points API
        first_call_url = mock_request.call_args_list[0][0][0]
        self.assertIn("points/37.7749,-122.4194", first_call_url)

    @patch('weather.make_nws_request')
    @pytest.mark.asyncio
    async def test_get_forecast_points_failure(self, mock_request):
        """Test forecast retrieval when points API fails."""
        mock_request.return_value = None
        
        result = await get_forecast(37.7749, -122.4194)
        
        self.assertIn("Unable to fetch forecast data", result)
        mock_request.assert_called_once()

    @patch('weather.make_nws_request')
    @pytest.mark.asyncio
    async def test_get_forecast_forecast_failure(self, mock_request):
        """Test forecast retrieval when forecast API fails."""
        def mock_request_side_effect(url):
            if "points" in url:
                return {
                    "properties": {
                        "forecast": "https://api.weather.gov/gridpoints/MTR/85,105/forecast"
                    }
                }
            else:
                return None
        
        mock_request.side_effect = mock_request_side_effect
        
        result = await get_forecast(37.7749, -122.4194)
        
        self.assertIn("Unable to fetch detailed forecast", result)
        self.assertEqual(mock_request.call_count, 2)

    @patch('weather.make_nws_request')
    @pytest.mark.asyncio
    async def test_get_forecast_limits_periods(self, mock_request):
        """Test that forecast limits to 5 periods."""
        # Create 10 periods to test limiting
        periods = []
        for i in range(10):
            periods.append({
                "name": f"Period {i}",
                "temperature": 50 + i,
                "temperatureUnit": "F",
                "windSpeed": "5 mph",
                "windDirection": "N",
                "detailedForecast": f"Forecast for period {i}"
            })
        
        def mock_request_side_effect(url):
            if "points" in url:
                return {
                    "properties": {
                        "forecast": "https://api.weather.gov/gridpoints/test"
                    }
                }
            else:
                return {
                    "properties": {
                        "periods": periods
                    }
                }
        
        mock_request.side_effect = mock_request_side_effect
        
        result = await get_forecast(37.7749, -122.4194)
        
        # Should only contain first 5 periods
        self.assertIn("Period 0", result)
        self.assertIn("Period 4", result)
        self.assertNotIn("Period 5", result)
        self.assertNotIn("Period 9", result)

    @pytest.mark.asyncio
    async def test_get_alerts_input_validation(self):
        """Test input validation for get_alerts."""
        # Test with empty state
        with patch('weather.make_nws_request') as mock_request:
            mock_request.return_value = {"features": []}
            
            result = await get_alerts("")
            
            # Should still make API call even with empty string
            self.assertIn("No active alerts", result)

    @pytest.mark.asyncio
    async def test_get_forecast_coordinate_validation(self):
        """Test coordinate handling for get_forecast."""
        # Test with boundary coordinates
        with patch('weather.make_nws_request') as mock_request:
            mock_request.return_value = None
            
            # Test extreme coordinates
            result = await get_forecast(90.0, 180.0)
            self.assertIn("Unable to fetch forecast data", result)
            
            result = await get_forecast(-90.0, -180.0)
            self.assertIn("Unable to fetch forecast data", result)


if __name__ == '__main__':
    unittest.main()