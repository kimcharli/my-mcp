# Development Guide

Guidelines for developing and contributing to the my-mcp server collection.

## Development Environment Setup

### Prerequisites

```bash
# Install development tools
pip install pre-commit black flake8 mypy pytest pytest-cov

# Set up pre-commit hooks
pre-commit install

# Create development environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# or .venv\Scripts\activate  # Windows
```

### Project Structure

```
my-mcp/
├── server/              # Core MCP servers
│   ├── trading/         # Stock trading server
│   ├── filesystem/      # Filesystem management
│   └── weather/         # Weather data server
├── .claude/             # Claude Code framework
├── .gemini/             # Gemini integration
├── tests/               # Integration tests
├── docs/                # Documentation
└── scripts/             # Utility scripts
```

## Creating New MCP Servers

### 1. Server Scaffolding

```bash
# Create new server directory
mkdir server/new-server
cd server/new-server

# Initialize UV project
uv init
uv add mcp
```

### 2. Basic Server Implementation

```python
# server/new-server/server.py
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Resource, Tool, TextContent

app = Server("new-server")

@app.list_resources()
async def list_resources() -> list[Resource]:
    """List available resources."""
    return [
        Resource(
            uri="example://resource",
            name="Example Resource",
            mimeType="text/plain"
        )
    ]

@app.read_resource()
async def read_resource(uri: str) -> str:
    """Read a specific resource."""
    if uri == "example://resource":
        return "Example resource content"
    raise ValueError(f"Unknown resource: {uri}")

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="example_tool",
            description="An example tool",
            inputSchema={
                "type": "object",
                "properties": {
                    "message": {"type": "string"}
                },
                "required": ["message"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Execute a tool."""
    if name == "example_tool":
        message = arguments.get("message", "")
        return [TextContent(type="text", text=f"Processed: {message}")]
    raise ValueError(f"Unknown tool: {name}")

if __name__ == "__main__":
    asyncio.run(stdio_server(app))
```

### 3. Configuration and Testing

```python
# pyproject.toml
[project]
name = "new-server"
version = "0.1.0"
dependencies = [
    "mcp>=0.4.0",
    "httpx>=0.24.0",
    "pydantic>=2.0.0"
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.0.0"
]

# tests/test_server.py
import pytest
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client

@pytest.mark.asyncio
async def test_server_connection():
    """Test basic server connectivity."""
    # Implementation depends on specific server
    pass
```

## Code Standards

### Python Style Guide

```python
# Use type hints
from typing import Optional, List, Dict, Any

async def process_data(
    data: Dict[str, Any],
    options: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Process data with optional configuration.
    
    Args:
        data: Input data dictionary
        options: Optional processing options
        
    Returns:
        Processed data dictionary
        
    Raises:
        ValueError: If data format is invalid
    """
    if options is None:
        options = []
    
    # Implementation
    return processed_data
```

### Error Handling

```python
# Custom exceptions
class ServerError(Exception):
    """Base exception for server errors."""
    pass

class ConfigurationError(ServerError):
    """Configuration-related errors."""
    pass

# Graceful error handling
async def safe_operation():
    try:
        result = await risky_operation()
        return result
    except SpecificException as e:
        logger.error(f"Operation failed: {e}")
        return default_value
    except Exception as e:
        logger.exception("Unexpected error occurred")
        raise ServerError(f"Internal error: {e}")
```

### Logging

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Use structured logging
logger.info("Processing request", extra={
    "user_id": user_id,
    "operation": "get_quote",
    "symbol": symbol
})
```

## Testing Strategy

### Test Structure

```
server/new-server/
├── tests/
│   ├── __init__.py
│   ├── test_server.py      # Server functionality
│   ├── test_tools.py       # Tool implementations
│   ├── test_resources.py   # Resource handling
│   └── conftest.py         # Test configuration
```

### Unit Tests

```python
# tests/test_tools.py
import pytest
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_example_tool():
    """Test example tool functionality."""
    # Arrange
    server = NewServer()
    arguments = {"message": "test input"}
    
    # Act
    result = await server.call_tool("example_tool", arguments)
    
    # Assert
    assert len(result) == 1
    assert result[0].text == "Processed: test input"

@pytest.mark.asyncio
async def test_tool_error_handling():
    """Test tool error handling."""
    server = NewServer()
    
    with pytest.raises(ValueError, match="Unknown tool"):
        await server.call_tool("nonexistent_tool", {})
```

### Integration Tests

```python
# tests/test_integration.py
@pytest.mark.asyncio
async def test_mcp_protocol_compliance():
    """Test MCP protocol compliance."""
    # Start server process
    # Connect MCP client
    # Test resource listing
    # Test tool execution
    # Verify responses
    pass
```

### Test Configuration

```python
# conftest.py
import pytest
import asyncio
from unittest.mock import AsyncMock

@pytest.fixture
def mock_api_client():
    """Mock external API client."""
    client = AsyncMock()
    client.get_data.return_value = {"status": "success"}
    return client

@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()
```

## Performance Optimization

### Async Best Practices

```python
import asyncio
import aiohttp
from typing import List

# Use connection pooling
async def fetch_multiple_urls(urls: List[str]) -> List[dict]:
    """Fetch multiple URLs concurrently."""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return [r for r in results if not isinstance(r, Exception)]

# Implement caching
from functools import lru_cache
import time

class CacheManager:
    def __init__(self, ttl: int = 300):
        self.cache = {}
        self.ttl = ttl
    
    def get(self, key: str):
        if key in self.cache:
            value, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return value
            else:
                del self.cache[key]
        return None
    
    def set(self, key: str, value):
        self.cache[key] = (value, time.time())
```

### Resource Management

```python
# Context managers for resource cleanup
from contextlib import asynccontextmanager

@asynccontextmanager
async def database_connection():
    """Manage database connection lifecycle."""
    conn = await create_connection()
    try:
        yield conn
    finally:
        await conn.close()

# Usage
async def get_data():
    async with database_connection() as conn:
        return await conn.fetch("SELECT * FROM table")
```

## Security Guidelines

### Input Validation

```python
from pydantic import BaseModel, validator

class RequestModel(BaseModel):
    symbol: str
    quantity: int
    
    @validator('symbol')
    def validate_symbol(cls, v):
        if not v.isalpha() or len(v) > 10:
            raise ValueError('Invalid symbol format')
        return v.upper()
    
    @validator('quantity')
    def validate_quantity(cls, v):
        if v <= 0 or v > 10000:
            raise ValueError('Quantity must be between 1 and 10000')
        return v
```

### Secrets Management

```python
import os
from pathlib import Path

def load_config():
    """Load configuration from environment or file."""
    config = {}
    
    # Load from environment first
    config['api_key'] = os.getenv('API_KEY')
    
    # Fallback to encrypted file
    if not config['api_key']:
        config_file = Path('.env.encrypted')
        if config_file.exists():
            config['api_key'] = decrypt_file(config_file)
    
    # Validate required config
    if not config['api_key']:
        raise ConfigurationError("API key not found")
    
    return config
```

## Documentation Standards

### Code Documentation

```python
def complex_function(
    data: Dict[str, Any],
    options: Optional[ProcessingOptions] = None
) -> ProcessingResult:
    """Process complex data with various options.
    
    This function performs multi-step processing on input data,
    applying various transformations based on the provided options.
    
    Args:
        data: Input data dictionary containing:
            - 'values': List of numeric values to process
            - 'metadata': Dictionary of processing metadata
        options: Optional processing configuration including:
            - normalize: Whether to normalize values (default: False)
            - filter_outliers: Whether to remove outliers (default: True)
    
    Returns:
        ProcessingResult containing:
            - processed_data: Transformed data dictionary
            - statistics: Processing statistics
            - warnings: List of warning messages
    
    Raises:
        ValueError: If data format is invalid
        ProcessingError: If processing fails
    
    Example:
        >>> data = {'values': [1, 2, 3], 'metadata': {'source': 'api'}}
        >>> options = ProcessingOptions(normalize=True)
        >>> result = complex_function(data, options)
        >>> print(result.statistics.mean)
        2.0
    """
    # Implementation
    pass
```

### API Documentation

```markdown
# Server API Reference

## Tools

### `get_quote`

Get real-time stock quote.

**Parameters:**
- `symbol` (string, required): Stock symbol (e.g., "AAPL")
- `extended_hours` (boolean, optional): Include extended hours data

**Returns:**
```json
{
  "symbol": "AAPL",
  "price": 150.25,
  "change": 2.15,
  "change_percent": 1.45,
  "timestamp": "2024-01-15T16:00:00Z"
}
```

**Errors:**
- `400`: Invalid symbol format
- `404`: Symbol not found
- `429`: Rate limit exceeded
```

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/test.yml
name: Test Suite
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install UV
      run: curl -LsSf https://astral.sh/uv/install.sh | sh
    
    - name: Install dependencies
      run: |
        cd server/trading
        uv sync
    
    - name: Run tests
      run: |
        cd server/trading
        uv run pytest --cov=. --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
    -   id: trailing-whitespace
    -   id: end-of-file-fixer
    -   id: check-yaml
    -   id: check-added-large-files

-   repo: https://github.com/psf/black
    rev: 23.1.0
    hooks:
    -   id: black

-   repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
    -   id: flake8

-   repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.0.1
    hooks:
    -   id: mypy
```

## Release Process

### Version Management

```bash
# Update version
uv version patch  # or minor, major

# Tag release
git tag -a v1.2.3 -m "Release version 1.2.3"
git push origin v1.2.3

# Generate changelog
python scripts/generate_changelog.py --version v1.2.3

# Create GitHub release
gh release create v1.2.3 --title "Version 1.2.3" --notes-file CHANGELOG.md
```

### Deployment Checklist

- [ ] All tests passing
- [ ] Documentation updated
- [ ] Version bumped
- [ ] Changelog generated
- [ ] Security scan completed
- [ ] Performance benchmarks passed
- [ ] Breaking changes documented
- [ ] Migration guide provided (if needed)

## Contribution Guidelines

### Pull Request Process

1. **Fork and Clone**
   ```bash
   git clone https://github.com/yourusername/my-mcp.git
   cd my-mcp
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/new-server-implementation
   ```

3. **Develop and Test**
   ```bash
   # Make changes
   # Add tests
   # Update documentation
   
   # Run tests
   python run_all_tests.py
   
   # Run linting
   pre-commit run --all-files
   ```

4. **Commit Changes**
   ```bash
   # Use conventional commits
   git commit -m "feat(trading): add options trading support"
   git commit -m "fix(filesystem): handle permission errors gracefully"
   git commit -m "docs(api): update trading server documentation"
   ```

5. **Submit Pull Request**
   - Provide clear description
   - Link related issues
   - Include test results
   - Update documentation

### Code Review Guidelines

**For Reviewers:**
- Focus on correctness, security, and performance
- Check test coverage and quality
- Verify documentation is updated
- Ensure code follows style guidelines
- Test the changes locally

**For Contributors:**
- Respond to feedback constructively
- Make requested changes promptly
- Keep commits focused and atomic
- Rebase on main before merging

## Debugging and Development Tools

### Local Development Setup

```bash
# Set up development environment
export MCP_DEBUG=1
export LOG_LEVEL=DEBUG

# Start server in debug mode
cd server/trading
uv run python -m debugpy --listen 5678 --wait-for-client trading.py

# Connect debugger (VS Code, PyCharm, etc.)
```

### Testing Tools

```bash
# Run specific test suite
uv run pytest tests/test_trading.py -v

# Run with coverage
uv run pytest --cov=. --cov-report=html

# Run performance tests
uv run pytest tests/test_performance.py --benchmark-only

# Integration testing
python tests/test_mcp_integration.py
```

### Monitoring and Profiling

```python
# Performance monitoring
import cProfile
import pstats

def profile_function():
    profiler = cProfile.Profile()
    profiler.enable()
    
    # Your code here
    
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats()
```

## Best Practices Summary

### Development
- Use type hints for all function parameters and return values
- Write comprehensive tests with good coverage
- Follow async/await patterns for I/O operations
- Implement proper error handling and logging
- Use dependency injection for testability

### Security
- Validate all inputs using Pydantic models
- Use environment variables for secrets
- Implement rate limiting for API endpoints
- Audit dependencies regularly
- Follow principle of least privilege

### Performance
- Use connection pooling for external APIs
- Implement caching where appropriate
- Profile performance-critical code paths
- Monitor resource usage in production
- Optimize database queries

### Documentation
- Keep README files updated
- Document all public APIs
- Provide usage examples
- Maintain changelogs
- Write clear commit messages

## Getting Help

### Resources
- [MCP Protocol Documentation](https://modelcontextprotocol.io/)
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Python asyncio Documentation](https://docs.python.org/3/library/asyncio.html)
- [UV Documentation](https://docs.astral.sh/uv/)

### Support Channels
- GitHub Issues for bug reports and feature requests
- GitHub Discussions for questions and ideas
- Code review for implementation guidance
- Documentation for usage questions

### Contributing Areas
- **New Servers**: Database, social media, IoT integrations
- **Enhanced Features**: Advanced analytics, visualization, automation
- **Performance**: Optimization, caching, load balancing
- **Security**: Authentication, encryption, audit logging
- **Documentation**: Tutorials, examples, API documentation
- **Testing**: Test coverage, integration tests, performance tests
