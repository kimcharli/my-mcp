# My MCP Server Collection

A comprehensive collection of Model Context Protocol (MCP) servers for Claude Code and other AI assistants, featuring custom-built servers for filesystem management, trading operations, weather data, and integration with various third-party services.

## Quick Start (5 minutes)

1. **Prerequisites**: Python 3.10+, [uv](https://github.com/astral-sh/uv), [Claude Code](https://claude.ai/code)

2. **Clone and setup**:
   ```bash
   git clone <repository-url>
   cd my-mcp/server/trading
   uv add -e .
   uv run cli.py setup --cash 100000
   ```

3. **Add to Claude Code**:
   ```bash
   claude mcp add trading -- uv --directory $(pwd) run trading.py
   ```

4. **Test**: Ask Claude "Get me a quote for AAPL stock"

## Available Servers

### Custom Servers (Local Development)

| Server | Purpose | Status | Quick Test |
|--------|---------|--------|------------|
| **🏦 Trading** | Stock market data & paper trading | ✅ Production | `uv run cli.py quote AAPL` |
| **🗂️ Filesystem** | macOS disk analysis & cleanup | ✅ Production | `uv run filesystem.py disk-usage` |
| **🌤️ Weather** | Weather data & forecasting | ✅ Beta | Weather queries via Claude |
| **🛠️ Add Demo** | MCP development templates | ✅ Examples | Development reference |

### Third-Party Integrations

| Server | Purpose | Status | Setup |
|--------|---------|--------|-------|
| **Context7** | Documentation lookup | ✅ Stable | `npx -y @upstash/context7-mcp` |
| **Gemini** | Google AI integration | ✅ Stable | Requires API key |
| **Browser MCP** | Web automation | ✅ Stable | `npx @browsermcp/mcp@latest` |
| **Memory** | Persistent context | ✅ Stable | `npx @modelcontextprotocol/server-memory` |
| **IDE Integration** | VS Code & Jupyter | ✅ Stable | `npx @modelcontextprotocol/server-ide` |
| **Apstra** | Network automation | ✅ Fixed | Network infrastructure management |
| **Apify** | Web scraping | ✅ Recently Fixed | Data extraction automation |

## Installation

### Install UV Package Manager

```bash
# macOS/Linux
curl -LsSf https://astral-sh/uv/install.sh | sh

# Verify installation
uv --version
```

### Install Individual Servers

```bash
# Trading server (recommended first)
cd server/trading && uv add -e .

# Filesystem server
cd server/filesystem && uv add -e .

# Weather server
cd server/weather && uv add -e .
```

## Configuration

### 1. Environment Setup

Create `.env` files for servers requiring API access:

**Trading Server** (`server/trading/.env`):
```bash
ETRADE_CONSUMER_KEY=your_consumer_key
ETRADE_CONSUMER_SECRET=your_consumer_secret
ETRADE_SANDBOX=TRUE
TRADING_MODE=paper
```

**Third-party Services**:
```bash
GEMINI_API_KEY=your_gemini_api_key
APIFY_TOKEN=your_apify_token
```

### 2. Claude Code Registration

```bash
# Custom servers
claude mcp add trading -- uv --directory /path/to/my-mcp/server/trading run trading.py
claude mcp add filesystem -- uv --directory /path/to/my-mcp/server/filesystem run filesystem.py
claude mcp add weather -- uv --directory /path/to/my-mcp/server/weather run weather.py

# Third-party servers
claude mcp add context7 -- npx -y @upstash/context7-mcp
claude mcp add gemini -e GEMINI_API_KEY=your_key -- npx -y github:kimcharli/mcp-server-gemini
claude mcp add memory -s user -- npx -y @modelcontextprotocol/server-memory
```

### 3. Claude Desktop (Alternative)

Add to `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "trading": {
      "command": "/Users/yourusername/.local/bin/uv",
      "args": ["--directory", "/path/to/my-mcp/server/trading", "run", "trading.py"]
    },
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    }
  }
}
```

## Key Usage Examples

### Trading Operations
```bash
# Set up paper account
uv run cli.py setup --cash 100000

# Get stock quotes and place orders
uv run cli.py quote AAPL
uv run cli.py order AAPL buy 10
uv run cli.py portfolio
```

**With Claude**: *"Get me current prices for Apple and Microsoft, then buy 10 shares of Apple"*

### Filesystem Management
```bash
# Analyze disk usage
uv run filesystem.py disk-usage
uv run filesystem.py large-files --min-size 500

# Clean up files (dry-run first)
uv run filesystem.py clean-temp
uv run filesystem.py clean-temp --execute
```

**With Claude**: *"Analyze my disk usage and clean up temporary files older than 30 days"*

### AI Assistant Integration
**Trading**: *"Show me my portfolio performance and suggest rebalancing"*
**Filesystem**: *"Find the largest files on my system and help me free up space"*
**Weather**: *"What's the weather forecast for San Francisco this week?"*
**Documentation**: *"Find examples of React hooks in the codebase"*

## Advanced Features

### Slash Commands
The amp code is using `.agents/commands` for project specific slash command folder and `~/.config/amp/commands` for user specific.

### Claude Code SuperClaude Framework
- **Custom Commands**: `/ck:security-review`, `/ck:fix-issue`, `/ck:git-commit-push`
- **Specialized Agents**: Feature Developer, Bug Fixer, Project Initializer
- **Smart Automation**: Conventional commits, test generation, documentation sync

[📚 Complete Advanced Usage Guide](docs/ADVANCED.md)

### Automated Documentation Review
- **Pre-commit Hooks**: Automatic documentation update triggers for code changes
- **Multi-language Support**: Python, JavaScript/TypeScript, Rust, Go, Java, C#
- **Configurable Patterns**: Project-specific file patterns and documentation targets
- **Claude Code Integration**: Seamless integration with document-reviewer agent

[🔧 Git Hooks Setup Guide](_git/README.md)

### Multi-AI Coordination
- **Claude + Gemini Integration**: Context sharing between AI systems
- **Layered Architecture**: Base servers → Services → Framework → AI coordination
- **Intelligent Task Orchestration**: Automated workflow management

## Testing & Quality Assurance

**Test Coverage**:
- Trading Server: 42% coverage, 34+ unit tests
- Filesystem Server: Complete safety validation
- Integration Tests: Cross-server workflow validation

```bash
# Run comprehensive tests
python run_all_tests.py

# Individual server testing
cd server/trading && uv run pytest tests/ --cov=. --cov-report=html -v
```

## Project Structure

```
my-mcp/
├── server/              # Core MCP servers
│   ├── trading/         # Stock trading & market data
│   ├── filesystem/      # macOS filesystem tools
│   └── weather/         # Weather data service
├── .claude/             # Claude Code SuperClaude framework
├── .gemini/             # Gemini AI integration
├── _git/                # Git hooks for automated documentation review
│   ├── hooks/           # Pre-commit hooks
│   └── README.md        # Setup and configuration guide
├── add-demo/           # MCP development examples
├── mcp.json           # Main MCP configuration
└── docs/              # Detailed documentation
```

## MCP

### chrome-dev-tools
https://github.com/ChromeDevTools/chrome-devtools-mcp

### marckitdown-mcp
https://github.com/microsoft/markitdown/tree/main/packages/markitdown-mcp

### context7
https://github.com/upstash/context7

### sequential thinking mcp
https://github.com/modelcontextprotocol/servers/tree/main/src/sequentialthinking


## Troubleshooting

### Common Issues

1. **Network Connectivity**: Corporate firewalls may block financial APIs
   ```bash
   # Test from different network if SSL errors occur
   ```

2. **UV Installation Problems**:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   uv --version
   ```

3. **MCP Connection Issues**:
   ```bash
   # Test server directly
   cd server/trading && uv run trading.py get-quote --symbol AAPL
   
   # Reset Claude Code MCP
   claude mcp list
   claude mcp remove problematic-server
   ```

4. **Apify Integration** (Recently Fixed):
   ```bash
   export APIFY_TOKEN="your_actual_token"
   claude mcp add apify-web-scraper -e APIFY_TOKEN=$APIFY_TOKEN -- npx -y @apify/actors-mcp-server
   ```

[🔧 Complete Troubleshooting Guide](docs/TROUBLESHOOTING.md)

## Development

### Adding New Servers

1. Create server directory: `mkdir server/new-server`
2. Initialize: `cd server/new-server && uv init && uv add mcp`
3. Implement following patterns in `add-demo/`
4. Register: `claude mcp add new-server -- uv --directory $(pwd) run main.py`

[🛠️ Development Guide](docs/DEVELOPMENT.md)

## Documentation

- **[Installation Guide](docs/INSTALL.md)** - Detailed setup instructions
- **[Advanced Usage](docs/ADVANCED.md)** - SuperClaude framework and multi-AI coordination
- **[API Reference](docs/API.md)** - Server APIs and integration patterns
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues and solutions
- **[Contributing](docs/CONTRIBUTING.md)** - Development guidelines and best practices

## Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-server`
3. Add comprehensive tests
4. Update documentation
5. Submit pull request

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Resources

- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [MCP Server Examples](https://github.com/modelcontextprotocol)
