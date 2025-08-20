# Installation Guide

This guide provides detailed installation instructions for all MCP servers in the my-mcp collection.

## Prerequisites

### System Requirements
- **Operating System**: macOS, Linux, or Windows
- **Python**: 3.10 or higher
- **Node.js**: 18 or higher (for third-party servers)
- **Git**: For cloning repositories

### Required Tools

#### UV Package Manager
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Alternative: via pip
pip install uv

# Verify installation
uv --version
```

#### Claude Code CLI
```bash
# Install Claude Code
# Visit https://claude.ai/code for platform-specific instructions

# Verify installation
claude --version
```

## Custom Server Installation

### Trading Server

```bash
cd server/trading

# Install dependencies
uv add -e .

# Set up environment
cp .env.sample .env
# Edit .env with your API credentials

# Initialize paper trading account
uv run cli.py setup --cash 100000

# Test installation
uv run cli.py quote AAPL
```

### Filesystem Server

```bash
cd server/filesystem

# Install dependencies
uv add -e .

# Test installation
uv run filesystem.py disk-usage
```

### Weather Server

```bash
cd server/weather

# Install dependencies
uv add -e .

# Test installation (via Claude after MCP registration)
```

## Third-Party Server Installation

### Context7 (Documentation Lookup)
```bash
# No installation required - NPX handles it
# Test: npx -y @upstash/context7-mcp
```

### Gemini Integration
```bash
# Requires API key setup
export GEMINI_API_KEY="your_api_key_here"

# Test: npx -y github:kimcharli/mcp-server-gemini
```

### Browser MCP
```bash
# Test: npx @browsermcp/mcp@latest
```

### Memory Server
```bash
# Test: npx -y @modelcontextprotocol/server-memory
```

### IDE Integration
```bash
# Test: npx @modelcontextprotocol/server-ide
```

### Apify (Web Scraping)
```bash
# Requires Apify token
export APIFY_TOKEN="your_apify_token"

# Test: npx -y @apify/actors-mcp-server --actors apify/web-scraper
```

## MCP Server Registration

### Claude Code Registration

```bash
# Custom servers
claude mcp add trading -- uv --directory /path/to/my-mcp/server/trading run trading.py
claude mcp add filesystem -- uv --directory /path/to/my-mcp/server/filesystem run filesystem.py
claude mcp add weather -- uv --directory /path/to/my-mcp/server/weather run weather.py

# Third-party servers
claude mcp add context7 -- npx -y @upstash/context7-mcp
claude mcp add gemini -e GEMINI_API_KEY=$GEMINI_API_KEY -- npx -y github:kimcharli/mcp-server-gemini
claude mcp add memory -s user -- npx -y @modelcontextprotocol/server-memory
claude mcp add browsermcp -- npx @browsermcp/mcp@latest
claude mcp add ide -s user -- npx @modelcontextprotocol/server-ide

# Verify registration
claude mcp list
```

### Claude Desktop Configuration

Add to `~/.config/claude-desktop/claude_desktop_config.json`:

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

## Environment Configuration

### Trading Server Environment

Create `server/trading/.env`:

```bash
# E*TRADE API Credentials
ETRADE_CONSUMER_KEY=your_consumer_key
ETRADE_CONSUMER_SECRET=your_consumer_secret
ETRADE_SANDBOX=TRUE

# Trading Configuration
TRADING_MODE=paper
RISK_MAX_POSITION_SIZE=5000
RISK_MAX_DAILY_LOSS=1000
DATA_REQUEST_TIMEOUT=10.0

# Market Data Settings
DEFAULT_MARKET_SESSION=REGULAR
ENABLE_EXTENDED_HOURS=FALSE
```

### Global Environment Variables

Add to your shell profile (`.bashrc`, `.zshrc`, etc.):

```bash
# API Keys
export GEMINI_API_KEY="your_gemini_api_key"
export APIFY_TOKEN="your_apify_token"

# MCP Configuration
export MCP_CONFIG_PATH="$HOME/.config/mcp"
export UV_CACHE_DIR="$HOME/.cache/uv"
```

## Verification

### Test Individual Servers

```bash
# Trading server
cd server/trading
uv run cli.py quote AAPL
uv run cli.py account

# Filesystem server
cd server/filesystem
uv run filesystem.py disk-usage

# Test third-party servers
npx -y @upstash/context7-mcp --version
```

### Test MCP Integration

```bash
# List registered servers
claude mcp list

# Test connection
claude mcp test trading
claude mcp test context7
```

### Test with Claude

Ask Claude:
- "Get me a quote for Apple stock" (Trading server)
- "Show me my disk usage" (Filesystem server)
- "What's the weather forecast?" (Weather server)
- "Find documentation for React hooks" (Context7)

## Troubleshooting Installation

### Common Issues

#### UV Installation Failed
```bash
# Clear cache and retry
rm -rf ~/.cache/uv
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Python Version Issues
```bash
# Check Python version
python3 --version

# Install specific Python version (macOS with Homebrew)
brew install python@3.11
```

#### Permission Errors
```bash
# Fix UV permissions
chmod +x ~/.local/bin/uv

# Fix server permissions
chmod +x server/*/[server-name].py
```

#### Network/Firewall Issues
```bash
# Test connectivity
curl -I https://pypi.org/
curl -I https://registry.npmjs.org/

# Try different network if corporate firewall blocks
```

#### MCP Registration Issues
```bash
# Remove and re-add server
claude mcp remove problematic-server
claude mcp add problematic-server -- [command]

# Check Claude Code logs
claude mcp logs problematic-server
```

### Getting Help

1. Check server-specific README files
2. Review [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
3. Test servers individually before MCP registration
4. Verify environment variables are set correctly
5. Check network connectivity for API-dependent servers

## Next Steps

After successful installation:

1. Review [Advanced Usage Guide](ADVANCED.md)
2. Explore [Usage Examples](../README.md#key-usage-examples)
3. Set up [Testing Environment](DEVELOPMENT.md#testing)
4. Configure [SuperClaude Framework](ADVANCED.md#claude-code-superClaude-framework)
