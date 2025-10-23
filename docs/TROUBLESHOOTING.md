# Troubleshooting Guide

Common issues and solutions for the my-mcp server collection.

## Server Connection Issues

### MCP Server Not Responding

**Symptoms:**

- Claude can't connect to server

- "Server unavailable" errors

- Timeout errors

**Solutions:**


1. **Test server directly:**
   ```bash
   # Trading server
   cd server/trading
   uv run cli.py quote AAPL

   # Filesystem server
   cd server/filesystem
   uv run filesystem.py disk-usage
   ```


2. **Check MCP registration:**
   ```bash
   claude mcp list
   claude mcp test [server-name]
   ```


3. **Re-register server:**
   ```bash
   claude mcp remove [server-name]
   claude mcp add [server-name] -- [command]
   ```


4. **Check server logs:**
   ```bash
   claude mcp logs [server-name]
   ```

### Python/UV Issues

#### UV Command Not Found

```bash

# Reinstall UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add to PATH (add to ~/.bashrc or ~/.zshrc)
export PATH="$HOME/.local/bin:$PATH"

# Reload shell
source ~/.bashrc  # or ~/.zshrc

```

#### Python Version Conflicts

```bash

# Check Python version in server directory
cd server/trading
uv run python --version

# Force specific Python version
uv python install 3.11
uv python pin 3.11

```

#### Dependency Installation Failed

```bash

# Clear UV cache
uv cache clean

# Reinstall dependencies
uv sync --reinstall

# Force refresh lock file
uv lock --refresh

```

## Network and API Issues

### SSL Certificate Errors

**Common with corporate networks/firewalls:**

```bash

# Test basic connectivity
curl -I https://pypi.org/
curl -I https://finance.yahoo.com/

# Try different network

# - Mobile hotspot

# - Home Wi-Fi vs corporate network

```

**Solutions:**

1. Try from different network location

2. Contact IT about firewall restrictions

3. Use VPN if permitted

4. Check for zScaler or similar security appliances

### API Rate Limiting

**Trading Server:**

```bash

# Check rate limit status
uv run cli.py status

# Wait and retry (most APIs reset limits hourly)

# Reduce request frequency

```

**Third-party Services:**

```bash

# Check API key validity
echo $GEMINI_API_KEY
echo $APIFY_TOKEN

# Verify quota/limits in provider dashboard

```

### API Authentication Failures

**Trading Server (.env issues):**

```bash

# Verify .env file exists and is readable
ls -la server/trading/.env
cat server/trading/.env

# Check environment variables are loaded
cd server/trading
uv run python -c "import os; print(os.getenv('ETRADE_CONSUMER_KEY'))"

```

**Gemini Integration:**

```bash

# Test API key
export GEMINI_API_KEY="your_key"
npx -y github:kimcharli/mcp-server-gemini --test

```

## Server-Specific Issues

### Trading Server

#### E*TRADE API Issues

```bash

# Test API connectivity
uv run cli.py test-connection

# Check sandbox vs production mode
grep ETRADE_SANDBOX server/trading/.env

# Verify API credentials in E*TRADE developer portal

```

#### Market Data Unavailable

```bash

# Check market hours
uv run cli.py market-status

# Try different symbols
uv run cli.py quote SPY  # ETF, more reliable
uv run cli.py quote AAPL # Individual stock

```

#### Paper Trading Account Issues

```bash

# Reset paper account
uv run cli.py setup --cash 100000 --reset

# Check account status
uv run cli.py account
uv run cli.py portfolio

```

### Filesystem Server

#### Permission Denied Errors

```bash

# Check file permissions
ls -la server/filesystem/filesystem.py

# Fix permissions
chmod +x server/filesystem/filesystem.py

# macOS security prompt

# Allow "Terminal" or "Claude Code" in System Preferences > Security & Privacy

```

#### Disk Analysis Fails

```bash

# Test with specific directory
uv run filesystem.py disk-usage --path ~/Downloads

# Check available disk space
df -h

# Verify no corrupted filesystem
sudo fsck -fy  # macOS/Linux

```

### Weather Server

#### No Weather Data

```bash

# Check if server responds
cd server/weather
uv run python -c "import weather; print('Weather server loaded')"

# Test with Claude after ensuring MCP registration

```

### Third-Party Servers

#### NPX Package Issues

```bash

# Clear NPX cache
npm cache clean --force

# Update Node.js
nvm install node  # if using nvm

# or via package manager

# Test NPX directly
npx -y @upstash/context7-mcp --version

```

#### Context7 Connection Failed

```bash

# Test directly
npx -y @upstash/context7-mcp

# Check network access to Upstash services
curl -I https://console.upstash.com

```

#### Apify Integration Issues (Recently Fixed)

```bash

# Verify token setup
echo $APIFY_TOKEN

# Test Apify server
npx -y @apify/actors-mcp-server --actors apify/web-scraper

# Re-register with proper environment
claude mcp remove apify-web-scraper
claude mcp add apify-web-scraper -e APIFY_TOKEN=$APIFY_TOKEN -- npx -y @apify/actors-mcp-server --actors misceres/indeed-scraper,apify/google-search-scraper

```

## Claude Code Specific Issues

### Claude Code Not Recognizing Servers

```bash

# Check Claude Code version
claude --version

# Update Claude Code

# Follow instructions at https://claude.ai/code

# Reset MCP configuration
claude mcp reset

# Re-add servers one by one

```

### SuperClaude Framework Issues

```bash

# Check framework files
ls -la .claude/commands/ck/

# Fix permissions
chmod +x .claude/commands/ck/*

# Test custom command
claude /ck:update-docs --dry-run

```

### Memory/Performance Issues

```bash

# Check system resources
top -p $(pgrep -f "uv\|claude\|node")

# Restart Claude Code
pkill -f claude
claude [your-command]

# Clear temporary files
rm -rf /tmp/claude-*
rm -rf ~/.cache/claude/

```

## Configuration Issues

### Environment Variables Not Loading

```bash

# Check shell profile
echo $SHELL
cat ~/.bashrc  # or ~/.zshrc

# Reload environment
source ~/.bashrc  # or ~/.zshrc

# Test environment variable
echo $GEMINI_API_KEY

```

### MCP Configuration Conflicts

```bash

# Check for conflicting configurations
cat ~/.config/claude-desktop/claude_desktop_config.json
cat mcp.json

# Validate JSON syntax
python -m json.tool mcp.json

```

### Path Issues

```bash

# Check PATH includes UV
echo $PATH | grep -o '[^:]*\.local/bin[^:]*'

# Find UV installation
which uv
ls -la ~/.local/bin/uv

# Fix PATH in shell profile
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc

```

## Testing and Validation

### Comprehensive System Test

```bash

# Run all tests
python run_all_tests.py

# Test individual components
cd server/trading && uv run pytest -v
cd server/filesystem && uv run pytest -v

# Test MCP integration
python tests/test_mcp_integration.py

```

### Diagnostic Commands

```bash

# System info
uv --version
python3 --version
node --version
claude --version

# Network tests
ping 8.8.8.8
curl -I https://pypi.org/
curl -I https://finance.yahoo.com/

# MCP status
claude mcp list
claude mcp test --all

```

## Performance Optimization

### Slow Server Response

```bash

# Check server resource usage
cd server/trading
uv run python -c "import psutil; print(f'CPU: {psutil.cpu_percent()}%, RAM: {psutil.virtual_memory().percent}%')"

# Optimize UV cache
uv cache clean
uv cache prune

# Restart services
pkill -f "uv.*trading"

```

### Network Timeouts

```bash

# Increase timeout in .env
echo "DATA_REQUEST_TIMEOUT=30.0" >> server/trading/.env

# Test with longer timeout
uv run cli.py quote AAPL --timeout 30

```

## Getting Help

### Diagnostic Information to Collect

When reporting issues, include:

```bash

# System information
uname -a
python3 --version
uv --version
claude --version

# Server status
claude mcp list
ls -la server/*/

# Error logs
claude mcp logs [server-name]
tail -n 50 ~/.cache/claude/logs/latest.log

```

### Support Resources


1. **Server-specific README files**: Check individual server documentation

2. **MCP Protocol Documentation**: [modelcontextprotocol.io](https://modelcontextprotocol.io/)

3. **Claude Code Documentation**: [docs.anthropic.com](https://docs.anthropic.com/en/docs/claude-code)

4. **GitHub Issues**: Report bugs and request features

5. **Community Forums**: Discuss with other users

### Escalation Path


1. **Self-diagnosis**: Use this troubleshooting guide

2. **Test isolation**: Run servers individually

3. **Check dependencies**: Verify all prerequisites

4. **Network testing**: Try different network environments

5. **Clean reinstall**: Remove and reinstall problematic components

6. **Report issue**: Provide diagnostic information and steps to reproduce

## Prevention

### Regular Maintenance

```bash

# Weekly maintenance script
#!/bin/bash

# Update dependencies
cd server/trading && uv sync
cd server/filesystem && uv sync
cd server/weather && uv sync

# Clean caches
uv cache clean
npm cache clean --force

# Test all servers
python run_all_tests.py

# Update MCP servers
claude mcp update --all

```

### Monitoring

```bash

# Check server health
claude mcp status

# Monitor logs
tail -f ~/.cache/claude/logs/latest.log

# Resource monitoring
watch -n 60 'ps aux | grep -E "(uv|claude|node)" | grep -v grep'

```
