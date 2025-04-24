# Trading MCP Server

An MCP (Model Context Protocol) server that enables AI models to interact with stock trading platforms like E*TRADE. Paper trading (simulation) is enabled by default, with the option to execute real trades when specifically configured.

## Features

- Account management and authentication with brokerages
- Real-time and historical market data access
- Multiple order types (market, limit, stop, etc.)
- Paper trading simulation for risk-free strategy testing
- Risk management and position tracking
- Portfolio analysis and performance reporting
- Support for E*TRADE API (extensible to other brokerages)

## Module Structure

The trading system has been organized into modular components for better maintainability:

- `trading.py` - Main MCP server entry point and tool definitions
- `models.py` - Data structures for positions, orders, accounts, etc.
- `market_data.py` - Market data retrieval for quotes and historical data
- `paper_trading.py` - Paper trading implementation for simulated trades
- `utils.py` - Common utility functions used across modules
- `cli.py` - Command-line interface for direct interaction

This modular design allows for:
- Clear separation of concerns
- Easier maintenance and testing
- Simple extension to support additional brokerages
- Better code organization and readability


## Installation

First, ensure you have uv installed and properly configured:

```bash
# Check uv version
uv --version

# Configure uv (recommended settings)
uv config
```

Then install the dependencies:

```bash
# Install dependencies
uv add mcp httpx pandas numpy pyetrade python-dotenv pydantic
# Or install the package directly
uv add -e .

# Generate requirements.txt (for compatibility)
uv pip compile requirements.in -o requirements.txt
```


## Usage

### Running the Server

```bash
# Run directly
uv run trading.py

# Or if installed as a package
trading-mcp
```

### Using the Command Line Interface

The trading system now includes a dedicated CLI for easier interaction:

```bash
# Get help on available commands
uv run cli.py --help

# Set up a paper trading account
uv run cli.py setup --cash 100000

# Get a stock quote
uv run cli.py quote AAPL

# Submit a market order
uv run cli.py order AAPL buy 10

# View account summary
uv run cli.py account

# Analyze your portfolio
uv run cli.py portfolio

# Get historical data
uv run cli.py history AAPL --period 3mo --interval 1d

# Watch stocks in real-time
uv run cli.py watch AAPL MSFT GOOGL --interval 30
```

### Testing with MCP Tools

The trading server can also be tested directly from the command line using the MCP tool interface:

```bash
# Set up a paper trading account first
uv run trading.py setup-paper-account --cash 100000

# Get a stock quote
uv run trading.py get-quote --symbol AAPL

# Get historical data with custom period and interval
uv run trading.py get-historical-data --symbol MSFT --period 3mo --interval 1wk

# View your account summary
uv run trading.py get-account-summary

# Analyze your portfolio
uv run trading.py analyze-portfolio

# Create a test order (paper trading mode)
uv run trading.py submit-order --symbol AAPL --action BUY --quantity 10
```

#### Timeout Controls

All commands have built-in timeouts to prevent hanging on slow network connections:

```bash
# Set a custom timeout (in seconds) via environment variable
export DATA_REQUEST_TIMEOUT=5
uv run cli.py quote AAPL
```

#### Command Help

Get help for any command:

```bash
# List all available commands
uv run cli.py --help

# Get help for a specific command
uv run cli.py quote --help
```

#### Testing Pipeline

For thorough testing, you can use this sequence of commands:

1. Reset your paper account: `uv run cli.py setup --cash 100000`
2. Check market conditions: `uv run cli.py quote AAPL`
3. Place a buy order: `uv run cli.py order AAPL buy 10`
4. View your positions: `uv run cli.py account`
5. Analyze portfolio: `uv run cli.py portfolio`
6. Watch your stocks: `uv run cli.py watch AAPL MSFT --interval 30`

### Running Automated Tests

To run all unit tests:

```bash
uv run pytest
```

### Configuration

Before using the trading MCP server, you need to set up your configuration:

1. Create a `.env` file in the trading directory with your API credentials:

```
# API Credentials (E*TRADE)
ETRADE_CONSUMER_KEY=your_consumer_key
ETRADE_CONSUMER_SECRET=your_consumer_secret
ETRADE_SANDBOX=TRUE  # Use sandbox/demo environment

# Trading Configuration
TRADING_MODE=paper  # 'paper' or 'live'
RISK_MAX_POSITION_SIZE=5000  # Maximum $ per position
RISK_MAX_DAILY_LOSS=1000  # Maximum daily loss allowed
DATA_REQUEST_TIMEOUT=10.0  # Timeout for market data requests in seconds
USE_MOCK_DATA=FALSE  # Use mock data instead of real market data

UV_CACHE_DIR=.cache/uv  # Custom cache directory for uv
UV_INDEX_URL=https://pypi.org/simple  # PyPI index URL
```

2. Set up your paper trading account with initial values:

```bash
# Initialize paper trading account
uv run cli.py setup --cash 100000
```

### Available MCP Tools

The MCP server exposes the following tools to AI models:

#### Account Management

- `get_account_summary`: Retrieve account balance and positions
- `setup_paper_account`: Initialize or reset the paper trading account

#### Market Data

- `get_quote`: Get current price quote for a stock
- `get_historical_data`: Retrieve historical price data

#### Order Management

- `submit_order`: Submit an order to buy or sell a stock

#### Portfolio Analysis

- `analyze_portfolio`: Get portfolio composition and metrics

### Safety Features

- Paper trading mode is enabled by default
- Clear warnings when switching to live trading
- Order validation before submission
- Risk management limits enforced automatically

## Paper vs. Live Trading

This MCP server supports two modes:

1. **Paper Trading** (default): All orders are simulated with real market data but no actual trades are placed.
2. **Live Trading**: Real orders are submitted to the brokerage.

To enable live trading, set `TRADING_MODE=live` in your `.env` file, but exercise extreme caution as real money will be at risk.

## Requirements

- Python 3.10 or higher
- uv 0.5.24 or higher
- E*TRADE API credentials (or other supported brokerage)
- Internet connection for real-time market data

## Documentation

For detailed requirements and specifications, see [REQUIREMENTS.md](./REQUIREMENTS.md)

## Development Setup

### UV Configuration

For development, we recommend the following uv settings:

```bash
# Set up development environment
uv venv  # Create virtual environment
source .venv/bin/activate

# Configure uv for development
uv pip compile requirements.dev.in -o requirements.dev.txt  # Generate dev requirements
uv pip compile requirements.test.in -o requirements.test.txt  # Generate test requirements

# Install development dependencies
uv pip sync requirements.dev.txt requirements.test.txt
```


## Extending the System

The modular design makes it easy to extend the system:

1. To add support for a new brokerage:
   - Create a new module in a `brokerages/` folder
   - Implement the same interface as `paper_trading.py`
   - Update the trading.py to conditionally use the appropriate service

2. To add new data sources:
   - Extend the `market_data.py` module with additional providers
   - Ensure appropriate fallback mechanisms
