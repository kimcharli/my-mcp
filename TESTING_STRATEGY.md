# MCP Server Collection - Testing Strategy & Documentation

## Overview

This document provides comprehensive testing guidance for the MCP (Model Context Protocol) server collection, including 4 custom servers and integration testing strategies.

## Test Architecture

### 1. Unit Tests

**Purpose**: Test individual functions and methods in isolation
**Framework**: pytest with pytest-asyncio for async support
**Coverage Target**: >80% for new code, >60% overall

### 2. Integration Tests

**Purpose**: Test server interactions and end-to-end workflows
**Scope**: Cross-server functionality and MCP protocol compliance
**Location**: `/tests/test_mcp_integration.py`

### 3. Performance Tests

**Purpose**: Validate response times and resource usage
**Targets**: <5s response time, <100MB memory usage

## Server-Specific Testing

### 🏦 Trading Server (`server/trading/`)

**Status**: ✅ Comprehensive unit tests (34 tests)
**Coverage**: 42% overall, models.py at 100%
**Test Files**:


- `test_trading.py` - Main API functions

- `test_paper_trading.py` - Paper trading service

- `test_market_data.py` - Market data retrieval

- `test_utils.py` - Utility functions (99% coverage)

**Key Test Areas**:


- Paper trading account management

- Market data retrieval (real and mock)

- Order submission and validation

- Portfolio analysis and reporting

- Error handling and edge cases

**Run Tests**:

```bash
cd server/trading
uv run pytest tests/ --cov=. --cov-report=html -v

```

### 🗂️ Filesystem Server (`server/filesystem/`)

**Status**: ✅ Comprehensive unit tests created
**Test Files**:


- `test_filesystem.py` - All filesystem operations

**Key Test Areas**:


- Disk usage analysis

- Large file detection

- Directory size calculation

- Temporary file cleanup

- Application cache management

- Duplicate file detection

- System file protection

**Run Tests**:

```bash
cd server/filesystem
uv run pytest tests/ --cov=. --cov-report=html -v

```

### 🌤️ Weather Server (`server/weather/`)

**Status**: ✅ Comprehensive unit tests created
**Test Files**:


- `test_weather.py` - Weather API interactions

**Key Test Areas**:


- Weather alert retrieval

- Forecast data processing

- API error handling

- Response formatting

- Input validation

**Run Tests**:

```bash
cd server/weather
uv run pytest tests/ --cov=. --cov-report=html -v

```

### 🛠️ Add-Demo Server (`add-demo/`)

**Status**: ⚠️ Tests needed
**Recommendation**: Create tests for MCP tool implementations and image processing

## Integration Testing

### Cross-Server Workflows

**File**: `/tests/test_mcp_integration.py`

**Test Scenarios**:


1. **Trading Workflow**: Setup → Quote → Order → Portfolio Analysis

2. **Filesystem Workflow**: Analyze → Identify → Clean → Verify

3. **Weather Workflow**: Alerts → Forecast → Analysis

4. **Cross-Server Data Flow**: System health informing trading decisions

5. **Error Handling**: Graceful failure across servers

6. **Security Compliance**: Input validation and sanitization

**Run Integration Tests**:

```bash
python -m pytest tests/test_mcp_integration.py -v

```

## Testing Best Practices

### 1. Test Structure

```python
class TestServerName(unittest.TestCase):
    def setUp(self):
        """Set up test environment and mocks"""

    def tearDown(self):
        """Clean up test resources"""

    @pytest.mark.asyncio
    async def test_function_name(self):
        """Test description with expected behavior"""

```

### 2. Mocking Strategy


- **External APIs**: Mock HTTP calls and API responses

- **File System**: Use temporary directories and files

- **Time-dependent**: Mock datetime and time functions

- **Environment**: Mock environment variables and configuration

### 3. Test Data Management


- Use factories for generating test data

- Separate test data from production data

- Clean up test artifacts in tearDown methods

### 4. Async Testing


- Use `@pytest.mark.asyncio` decorator

- Mock async functions with `AsyncMock`

- Test timeout scenarios and cancellation

## Coverage Analysis

### Current Coverage Status


- **Trading Server**: 42% overall

  - High: models.py (100%), utils.py (99%)

  - Low: cli.py (0%), market_data.py (18%), trading.py (23%)

- **Other Servers**: Tests created but not yet executed

### Coverage Improvement Plan


1. **Priority 1**: Increase trading server core logic coverage (trading.py, market_data.py)

2. **Priority 2**: Add filesystem and weather server test execution

3. **Priority 3**: Add CLI interface testing

4. **Priority 4**: Integration test coverage expansion

## Test Execution

### Individual Server Testing

Each server has its own test suite that can be run independently:

```bash

# Trading server (working)
cd server/trading && uv run pytest tests/ --cov=. --cov-report=html

# Filesystem server (tests created)
cd server/filesystem && uv run pytest tests/ --cov=. --cov-report=html

# Weather server (tests created)
cd server/weather && uv run pytest tests/ --cov=. --cov-report=html

```

### Comprehensive Test Suite

Use the project test runner for full validation:

```bash
python run_all_tests.py

```

**Output**:


- Test results summary

- Coverage percentages

- Error identification

- Recommendations for improvement

### Continuous Integration

For CI/CD integration, use this command:

```bash
pytest --cov=. --cov-report=xml --cov-fail-under=60

```

## Test Development Guidelines

### 1. Writing New Tests


- **Test Naming**: Use descriptive names (`test_submit_buy_order_with_insufficient_funds`)

- **Test Coverage**: Aim for happy path, edge cases, and error conditions

- **Assertions**: Use specific assertions with clear error messages

- **Test Isolation**: Each test should be independent and repeatable

### 2. Mock Usage


- Mock external dependencies (APIs, file system, network)

- Use realistic test data that reflects production scenarios

- Validate mock calls to ensure correct API usage

### 3. Error Testing


- Test all error conditions and edge cases

- Verify error messages are user-friendly

- Test recovery mechanisms and fallback behavior

## Quality Gates

### Pre-Commit Checks


1. **Syntax**: All tests must pass

2. **Coverage**: New code must have >80% test coverage

3. **Style**: Follow PEP 8 and project conventions

4. **Security**: No hardcoded secrets or unsafe operations

### Release Criteria


1. **Unit Tests**: >95% pass rate

2. **Integration Tests**: All critical workflows pass

3. **Coverage**: >60% overall, >80% for new features

4. **Performance**: Response times within defined limits

## Troubleshooting

### Common Issues

**Import Errors**:

```bash

# Install test dependencies
uv add --dev pytest pytest-asyncio pytest-cov

```

**Async Test Warnings**:

```python

# Use proper async test structure
@pytest.mark.asyncio
async def test_async_function(self):
    result = await async_function()
    self.assertEqual(result, expected)

```

**Coverage Not Recording**:

```bash

# Run with coverage explicitly
pytest --cov=. --cov-report=term-missing

```

**Mock Issues**:

```python

# Patch at the right location
@patch('module.function')  # Where function is imported
async def test_with_mock(self, mock_func):
    mock_func.return_value = test_data

```

## Future Enhancements

### 1. Performance Testing


- Add benchmark tests for response times

- Memory usage profiling

- Concurrent request handling

### 2. Security Testing


- Input validation tests

- Authentication/authorization tests

- Data sanitization verification

### 3. End-to-End Testing


- Real MCP protocol testing

- Multi-server workflow testing

- Client integration testing

### 4. Test Automation


- GitHub Actions integration

- Automated coverage reporting

- Performance regression detection

## Resources


- **pytest Documentation**: <https://docs.pytest.org/>

- **pytest-asyncio**: <https://pytest-asyncio.readthedocs.io/>

- **MCP Specification**: <https://modelcontextprotocol.io/>

- **Test Coverage**: Use `htmlcov/index.html` for detailed coverage reports

---

**Last Updated**: August 17, 2025
**Maintainer**: MCP Development Team
