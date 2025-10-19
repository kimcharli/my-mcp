# NetworkX MCP Server - Setup Guide

## Quick Start

Follow these steps to set up the NetworkX MCP Server:

### 1. Install Python Dependencies

```bash
cd /Users/ckim/Projects/networkx-mcp
pip3 install -r requirements.txt
```

Or install manually:
```bash
pip3 install networkx matplotlib
```

### 2. Test Python Dependencies

Run the test script to verify everything is installed correctly:

```bash
python3 test_dependencies.py
```

You should see checkmarks (✓) for all dependencies.

### 3. Install Node.js Dependencies

```bash
npm install
```

### 4. Configure Claude Desktop

Edit your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

**Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

Add this configuration (update the path to match your system):

```json
{
  "mcpServers": {
    "networkx": {
      "command": "node",
      "args": ["/Users/ckim/Projects/networkx-mcp/index.js"]
    }
  }
}
```

### 5. Restart Claude Desktop

After updating the configuration, completely quit and restart Claude Desktop.

### 6. Verify Installation

In Claude, try asking:
```
Create a simple graph with 4 nodes A, B, C, D and edges A-B, B-C, C-D, D-A. Then calculate the degree centrality.
```

If the tools are working, you should see Claude using the NetworkX tools to create and analyze the graph.

## Troubleshooting

### "NetworkX not found" error

Make sure Python 3 and NetworkX are installed:
```bash
python3 --version
pip3 install networkx
```

### "Module not found" error in Node.js

Install the Node dependencies:
```bash
cd /Users/ckim/Projects/networkx-mcp
npm install
```

### Tools not appearing in Claude

1. Check that the path in `claude_desktop_config.json` is absolute and correct
2. Make sure you completely quit and restarted Claude Desktop (not just closed the window)
3. Check Claude Desktop logs for errors:
   - macOS: `~/Library/Logs/Claude/`
   - Windows: `%APPDATA%/Claude/logs/`

### Python execution errors

The server uses `python3` by default. If your Python installation uses a different name (like `python`), you may need to modify `index.js`.

## Example Uses

Once installed, you can:

1. **Create and analyze graphs**:
   - "Create a directed graph with these connections..."
   - "Find the shortest path between nodes A and B"

2. **Generate standard graphs**:
   - "Generate a random graph with 50 nodes"
   - "Create a complete graph with 10 nodes"

3. **Calculate metrics**:
   - "Calculate betweenness centrality for this network"
   - "Find the clustering coefficient"
   - "Detect communities in this social network"

4. **Visualize**:
   - "Generate visualization code for this graph"
   - "Show me how to plot this network with a circular layout"

5. **Advanced operations**:
   - "Find the minimum spanning tree"
   - "Check if this graph is connected"
   - "Calculate eigenvector centrality"

## Next Steps

Check out the [README.md](README.md) for complete documentation of all available tools and more examples.
