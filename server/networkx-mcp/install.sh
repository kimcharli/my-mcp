#!/bin/bash

# NetworkX MCP Server Installation Script

echo "================================================"
echo "NetworkX MCP Server - Installation"
echo "================================================"
echo ""

# Check if Python 3 is installed
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi
echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Check if Node.js is installed
echo "Checking Node.js installation..."
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi
echo "✓ Node.js found: $(node --version)"
echo ""

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install Python dependencies"
    exit 1
fi
echo "✓ Python dependencies installed"
echo ""

# Test Python dependencies
echo "Testing Python dependencies..."
python3 test_dependencies.py
if [ $? -ne 0 ]; then
    echo "❌ Python dependency test failed"
    exit 1
fi
echo ""

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
npm install
if [ $? -ne 0 ]; then
    echo "❌ Failed to install Node.js dependencies"
    exit 1
fi
echo "✓ Node.js dependencies installed"
echo ""

# Get absolute path
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "================================================"
echo "✓ Installation Complete!"
echo "================================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Add this to your Claude Desktop config:"
echo ""
echo "   macOS: ~/Library/Application Support/Claude/claude_desktop_config.json"
echo "   Windows: %APPDATA%/Claude/claude_desktop_config.json"
echo ""
echo "   {"
echo "     \"mcpServers\": {"
echo "       \"networkx\": {"
echo "         \"command\": \"node\","
echo "         \"args\": [\"$SCRIPT_DIR/index.js\"]"
echo "       }"
echo "     }"
echo "   }"
echo ""
echo "2. Restart Claude Desktop completely"
echo ""
echo "3. Try asking Claude to create and analyze graphs!"
echo ""
echo "See EXAMPLES.md for usage examples."
echo ""
