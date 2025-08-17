# My MCP Server Collection

A comprehensive collection of Model Context Protocol (MCP) servers for Claude Code and other AI assistants, featuring custom-built servers for filesystem management, trading operations, weather data, and integration with various third-party services.

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [MCP Servers](#mcp-servers)
- [Installation](#installation)
- [Configuration](#configuration)
- [Client Configuration](#client-configuration)
- [Usage Examples](#usage-examples)
- [Development](#development)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## Overview

This repository contains a curated collection of MCP servers designed to extend AI assistant capabilities with real-world integrations:

### Custom Servers (Local Development)
- **Trading Server** - Stock market data and paper trading capabilities
- **Filesystem Server** - macOS disk analysis and cleanup tools
- **Weather Server** - Weather data and forecasting
- **Add Demo Server** - MCP server development templates and examples

### Third-Party Integrations
- **Context7** - Documentation and code pattern lookup
- **Gemini** - Google Gemini AI integration with specialized command tooling
- **Browser MCP** - Web automation and scraping
- **Memory Server** - Persistent context and memory
- **Sequential Thinking** - Enhanced reasoning capabilities
- **Apify** - Web scraping and data extraction (recently fixed)
- **Apstra** - Network automation and infrastructure management

### Advanced Features
- **Claude Code SuperClaude Framework** - Intelligent task orchestration and custom commands
- **Multi-AI Coordination** - Claude + Gemini integration with context sharing
- **Layered Architecture** - Base servers → Services → Framework → AI coordination

## Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd my-mcp
   ```

2. **Set up a server** (e.g., Trading Server)
   ```bash
   cd server/trading
   uv add -e .
   uv run cli.py setup --cash 100000
   ```

3. **Configure Claude Code**
   ```bash
   # Add trading server
   claude mcp add trading -- uv --directory /path/to/my-mcp/server/trading run trading.py
   
   # Add filesystem server
   claude mcp add filesystem -- uv --directory /path/to/my-mcp/server/filesystem run filesystem.py
   ```

4. **Test the integration**
   ```bash
   # Test trading server
   uv run cli.py quote AAPL
   
   # Test filesystem server
   uv run filesystem.py disk-usage
   ```

## MCP Servers

### 🏦 Trading Server

Professional-grade stock trading and market data server with paper trading simulation.

**Key Features:**
- Real-time and historical market data
- Paper trading with portfolio simulation
- Multiple order types (market, limit, stop)
- Risk management and position tracking
- E*TRADE API integration
- Comprehensive CLI interface

**Location:** `server/trading/`
**Documentation:** [Trading Server README](server/trading/README.md)

**Quick Commands:**
```bash
# Set up paper account with $100K
uv run cli.py setup --cash 100000

# Get real-time quote
uv run cli.py quote AAPL

# Place a buy order
uv run cli.py order AAPL buy 10

# View portfolio
uv run cli.py portfolio
```

### 🗂️ Filesystem Server

macOS disk analysis and cleanup automation server.

**Key Features:**
- Disk usage analysis and reporting
- Large file detection and directory analysis
- Automated cleanup of temporary files
- Application cache management
- Duplicate file detection
- Safe file operations (trash, not delete)

**Location:** `server/filesystem/`
**Documentation:** [Filesystem Server README](server/filesystem/README.md)

**Quick Commands:**
```bash
# Analyze disk usage
uv run filesystem.py disk-usage

# Find large files (>500MB)
uv run filesystem.py large-files --min-size 500

# Clean temporary files (dry-run)
uv run filesystem.py clean-temp

# Clean with execution
uv run filesystem.py clean-temp --execute
```

### 🌤️ Weather Server

Weather data and forecasting integration server.

**Location:** `server/weather/`
**Documentation:** [Weather Server README](server/weather/README.md)

### 🛠️ Add Demo Server

Template and example server for MCP development learning.

**Key Features:**
- Complete MCP server implementation examples
- Authentication patterns
- Resource and tool patterns
- Image processing examples
- Development templates

**Location:** `add-demo/`
**Documentation:** [Add Demo README](add-demo/README.md)

## Installation

### Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- [Claude Code](https://claude.ai/code) CLI
- Node.js (for third-party NPM servers)

### Install UV Package Manager

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or via pip
pip install uv
```

### Install Individual Servers

Each server has its own dependencies managed by uv:

```bash
# Trading server
cd server/trading
uv add -e .

# Filesystem server  
cd server/filesystem
uv add -e .

# Weather server
cd server/weather
uv add -e .
```

## Configuration

### Environment Variables

Create `.env` files in each server directory as needed:

**Trading Server** (`server/trading/.env`):
```bash
# API Credentials
ETRADE_CONSUMER_KEY=your_consumer_key
ETRADE_CONSUMER_SECRET=your_consumer_secret
ETRADE_SANDBOX=TRUE

# Trading Configuration
TRADING_MODE=paper
RISK_MAX_POSITION_SIZE=5000
RISK_MAX_DAILY_LOSS=1000
DATA_REQUEST_TIMEOUT=10.0
```

**Third-party Integrations**:
```bash
# Gemini integration
GEMINI_API_KEY=your_gemini_api_key

# Apify integration
APIFY_TOKEN=your_apify_token
```

### MCP Configuration Files

The repository includes pre-configured MCP server definitions:

- `mcp.json` - Main MCP servers (weather, context7, memory, sequential-thinking, browsermcp, gemini, apstra)
- `apify.json` - Apify-specific configuration with web scraping actors (recently fixed)

**Recent Configuration Updates:**
- **Enhanced mcp.json**: Added comprehensive server descriptions and usage comments
- **Fixed Apify Integration**: Resolved connection issues with detailed setup guidance
- **New Server Additions**: Apstra network automation and enhanced Gemini integration
- **Improved Documentation**: Each configuration includes setup instructions and usage examples

## Client Configuration

### Claude Code CLI

```bash
# Add individual servers
claude mcp add trading -- uv --directory /path/to/my-mcp/server/trading run trading.py
claude mcp add filesystem -- uv --directory /path/to/my-mcp/server/filesystem run filesystem.py
claude mcp add weather -- uv --directory /path/to/my-mcp/server/weather run weather.py

# Add third-party servers
claude mcp add context7 -- npx -y @upstash/context7-mcp
claude mcp add gemini -e GEMINI_API_KEY=your_key -- npx -y github:kimcharli/mcp-server-gemini
claude mcp add browsermcp -- npx @browsermcp/mcp@latest

# Add with user scope
claude mcp add memory -s user -- npx -y @modelcontextprotocol/server-memory
```

### Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "trading": {
      "command": "/Users/yourusername/.local/bin/uv",
      "args": [
        "--directory", "/path/to/my-mcp/server/trading",
        "run", "trading.py"
      ]
    },
    "filesystem": {
      "command": "/Users/yourusername/.local/bin/uv", 
      "args": [
        "--directory", "/path/to/my-mcp/server/filesystem",
        "run", "filesystem.py"
      ]
    },
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    },
    "gemini": {
      "command": "npx",
      "args": ["-y", "github:kimcharli/mcp-server-gemini"],
      "env": {
        "GEMINI_API_KEY": "your_api_key"
      }
    }
  }
}
```

### Gemini Integration

For `~/.gemini/settings.json`:

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    }
  }
}
```

## Advanced Usage

### Claude Code SuperClaude Framework Commands

This project includes specialized commands for enhanced AI assistant capabilities:

```bash
# Security analysis and recommendations
claude /ck:security-review --comprehensive --include-dependencies

# Automated issue resolution
claude /ck:fix-issue --auto-fix --validate

# Smart git operations with conventional commits
claude /ck:git-commit-push --conventional --auto-push

# Test case generation and validation
claude /ck:testcases --coverage-target 80 --include-edge-cases

# Documentation synchronization
claude /ck:update-docs --sync-all --validate-links

# Business rule analysis
claude /ck:rule-engine --analyze-patterns --suggest-optimizations
```

### Gemini Integration Commands

```bash
# Domain expertise analysis
gemini area-of "network automation patterns"

# Automated changelog generation  
gemini changelog --version 2.1.0 --include-breaking-changes

# Smart commit message generation
gemini commit --conventional --scope "mcp-integration"

# Code refactoring recommendations
gemini refactor --target performance --suggest-patterns
```

## Usage Examples

### Trading Workflow

```bash
# Set up paper trading
cd server/trading
uv run cli.py setup --cash 100000

# Research a stock
uv run cli.py quote AAPL
uv run cli.py history AAPL --period 3mo --interval 1d

# Place orders
uv run cli.py order AAPL buy 10
uv run cli.py order MSFT buy 5

# Monitor portfolio
uv run cli.py account
uv run cli.py portfolio
uv run cli.py watch AAPL MSFT --interval 30
```

### Filesystem Maintenance

```bash
# Analyze system
cd server/filesystem
uv run filesystem.py disk-usage
uv run filesystem.py large-files --min-size 1000
uv run filesystem.py dir-sizes --top 20

# Clean up (dry-run first)
uv run filesystem.py clean-temp
uv run filesystem.py clean-downloads --days 60
uv run filesystem.py clear-app-cache --app Chrome

# Execute cleanup
uv run filesystem.py clean-temp --execute
uv run filesystem.py clean-downloads --days 60 --execute
```

### AI Assistant Integration

Use with Claude Code or other AI assistants:

```
# Trading examples
"Get me the current price of Apple stock and Tesla"
"Show me my portfolio performance and suggest rebalancing"
"Place a buy order for 50 shares of Microsoft"

# Filesystem examples  
"Analyze my disk usage and find the largest files"
"Clean up my Downloads folder of files older than 30 days"
"Find duplicate files in my Documents folder"

# Weather examples
"What's the weather forecast for San Francisco this week?"
"Show me historical weather data for the last month"
```

## 📊 Testing & Quality Assurance

### Comprehensive Test Suite

The project includes a robust testing framework with multiple layers:

**Test Coverage:**
- **Trading Server**: 42% coverage with 34+ unit tests
- **Filesystem Server**: Complete unit test suite with safety validation  
- **Weather Server**: Comprehensive test coverage for all API interactions
- **Integration Tests**: Cross-server workflow validation
- **Command Validation**: Bash command permission testing (recently added)

**Testing Features:**
- **Multi-language Support**: Python (pytest), JavaScript (npm test), Java (maven/gradle)
- **Safety Testing**: Dry-run validation for destructive operations
- **Permission Validation**: Claude Code command compatibility testing
- **Performance Testing**: Response time and resource usage validation

**Run Tests:**
```bash
# Individual server testing
cd server/trading && uv run pytest tests/ --cov=. --cov-report=html -v
cd server/filesystem && uv run pytest tests/ --cov=. --cov-report=html -v  
cd server/weather && uv run pytest tests/ --cov=. --cov-report=html -v

# Comprehensive test suite
python run_all_tests.py

# Command validation testing
python tests/test_command_bash_validation.py
```

**Recent Enhancements:**
- **Bash Command Validation**: New test framework for Claude Code command compatibility
- **Permission Testing**: Validates complex command patterns before deployment
- **Integration Testing**: Enhanced MCP protocol compliance testing
- **Coverage Reporting**: HTML reports with detailed analysis

## Development

### Project Structure

```
my-mcp/
├── .claude/             # Claude Code SuperClaude framework
│   └── commands/ck/     # Custom commands (security, git, docs, etc.)
├── .gemini/             # Gemini AI integration
│   └── commands/ck/     # Gemini-specific command tooling
├── server/              # Core MCP servers
│   ├── trading/         # Stock trading MCP server
│   ├── filesystem/      # macOS filesystem tools
│   └── weather/         # Weather data server
├── add-demo/           # MCP development examples and templates
├── mcp.json           # Main MCP configuration (enhanced)
├── apify.json         # Apify-specific configuration (fixed)
├── CLAUDE.md          # AI assistant integration guide (updated)
├── CHANGELOG.md       # Version history and changes (new)
└── README.md          # Project overview (this file)
```

### Adding New Servers

1. **Create server directory**
   ```bash
   mkdir server/new-server
   cd server/new-server
   ```

2. **Set up Python project**
   ```bash
   uv init
   uv add mcp
   ```

3. **Implement MCP server** following the examples in `add-demo/`

4. **Add to configuration**
   ```bash
   claude mcp add new-server -- uv --directory /path/to/server/new-server run main.py
   ```

### Testing

Each server includes comprehensive testing:

```bash
# Trading server tests
cd server/trading
uv run pytest

# Run specific tests
uv run pytest tests/test_market_data.py -v

# Filesystem server tests
cd server/filesystem
uv run filesystem.py --help
```

## Troubleshooting

### Common Issues

1. **Network Connectivity**
   - Corporate firewalls may block financial data APIs
   - Try different networks if experiencing SSL errors
   - Check for zScaler or similar security appliances

2. **UV Installation**
   ```bash
   # Reinstall uv
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Check version
   uv --version
   ```

3. **Python Dependencies**
   ```bash
   # Clear cache and reinstall
   cd server/trading
   uv cache clean
   uv lock --refresh
   uv add -e .
   ```

4. **MCP Connection Issues**
   ```bash
   # Test server directly
   cd server/trading
   uv run trading.py get-quote --symbol AAPL
   
   # Check Claude Code MCP status
   claude mcp list
   claude mcp remove problematic-server
   claude mcp add problematic-server -- [command]
   ```

5. **Apify Integration Issues** (Recently Fixed)

   ```bash
   # Verify Apify token setup
   echo $APIFY_TOKEN
   
   # Test Apify server connection
   npx -y @apify/actors-mcp-server --actors apify/web-scraper
   
   # Common fixes
   export APIFY_TOKEN="your_actual_token"
   claude mcp remove apify-web-scraper
   claude mcp add apify-web-scraper -e APIFY_TOKEN=$APIFY_TOKEN -- npx -y @apify/actors-mcp-server --actors misceres/indeed-scraper,apify/google-search-scraper
   ```

6. **Claude Code SuperClaude Framework Issues**

   ```bash
   # Verify framework installation
   ls -la .claude/commands/ck/
   
   # Test custom commands
   claude /ck:update-docs --dry-run
   
   # Check command permissions
   chmod +x .claude/commands/ck/*
   ```

### Network and Security Warnings

> **Warning:** Access to financial data providers (Yahoo Finance, etc.) may be blocked by corporate networks, zScaler, or other security appliances. If encountering SSL errors or connection issues:
>
> - Try from a different network (home Wi-Fi, mobile hotspot)
> - Contact IT administrator about firewall restrictions  
> - Check for rate limiting (temporary blocks)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-server`)
3. Make your changes and add tests
4. Update documentation
5. Submit a pull request

### Development Guidelines

- Follow existing code structure and patterns
- Add comprehensive tests for new features
- Update documentation for any changes
- Use type hints and proper error handling
- Follow the MCP protocol specifications

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Related Resources

### Official MCP Resources
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [MCP Server Examples](https://github.com/modelcontextprotocol)

### Third-Party Integrations
- [Context7 Documentation](https://github.com/upstash/context7)
- [Browser MCP Documentation](https://docs.browsermcp.io/welcome)
- [Supabase MCP Guide](https://supabase.com/docs/guides/getting-started/mcp)
- [VS Code MCP Extension](https://code.visualstudio.com/mcp)

