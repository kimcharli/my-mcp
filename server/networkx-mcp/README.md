# NetworkX MCP Server

A Model Context Protocol (MCP) server that provides tools for working with Python NetworkX graph library.

## Features

This MCP server provides comprehensive NetworkX functionality including:

### Graph Creation & Manipulation
- **create_graph**: Create graphs (Graph, DiGraph, MultiGraph, MultiDiGraph)
- **add_nodes**: Add nodes with optional attributes
- **add_edges**: Add edges with optional weights
- **generate_graph**: Generate common graph types (random, complete, cycle, path, star, wheel, ladder, grid)

### Graph Analysis
- **graph_info**: Get basic information (nodes, edges, density)
- **shortest_path**: Find shortest paths between nodes
- **centrality**: Calculate centrality measures (degree, betweenness, closeness, eigenvector)
- **clustering**: Calculate clustering coefficients
- **communities**: Detect communities using greedy modularity
- **is_connected**: Check if graph is connected

### Advanced Operations
- **minimum_spanning_tree**: Find minimum spanning tree
- **visualize**: Generate matplotlib visualization code
- **execute_custom**: Execute custom NetworkX Python code

## Installation

1. Clone or create this directory:
```bash
mkdir networkx-mcp
cd networkx-mcp
```

2. Install dependencies:
```bash
npm install
```

3. Ensure Python 3 and NetworkX are installed:
```bash
pip3 install networkx matplotlib
```

## Configuration

Add to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "networkx": {
      "command": "node",
      "args": ["/absolute/path/to/networkx-mcp/index.js"]
    }
  }
}
```

## Usage Examples

### Create a Simple Graph
```
Create a graph with nodes A, B, C, D and edges connecting A-B, B-C, C-D, D-A
```

### Analyze a Social Network
```
I have a social network with edges: [["Alice", "Bob"], ["Bob", "Charlie"], ["Charlie", "David"], ["David", "Alice"], ["Alice", "Charlie"]]. 
Calculate the betweenness centrality and find communities.
```

### Generate Random Graph
```
Generate a random graph with 20 nodes and edge probability 0.3, then check if it's connected
```

### Find Shortest Path
```
Given edges [["A","B"], ["B","C"], ["C","D"], ["A","D"]], find the shortest path from A to D
```

### Minimum Spanning Tree
```
Find the minimum spanning tree for edges [["A","B"], ["B","C"], ["C","D"], ["A","D"], ["B","D"]] 
with weights [1, 2, 3, 4, 1]
```

### Visualize Graph
```
Create visualization code for a star graph with 6 nodes using circular layout
```

## Tools Reference

### networkx:create_graph
Creates a new graph with specified type, nodes, and edges.

**Parameters**:
- `graph_type`: "Graph", "DiGraph", "MultiGraph", or "MultiDiGraph"
- `nodes`: Array of node names
- `edges`: Array of [source, target] pairs

### networkx:shortest_path
Finds shortest path between two nodes.

**Parameters**:
- `edges`: Array of edges
- `source`: Source node
- `target`: Target node
- `weighted`: Use edge weights (default: false)
- `weights`: Array of edge weights
- `directed`: Is directed graph (default: false)

### networkx:centrality
Calculates centrality measures.

**Parameters**:
- `edges`: Array of edges
- `measure`: "degree", "betweenness", "closeness", or "eigenvector"
- `directed`: Is directed graph (default: false)

### networkx:communities
Detects communities using greedy modularity algorithm.

**Parameters**:
- `edges`: Array of edges

### networkx:generate_graph
Generates common graph types.

**Parameters**:
- `graph_type`: "random", "complete", "cycle", "path", "star", "wheel", "ladder", or "grid"
- `n`: Number of nodes
- `p`: Probability for random graphs (0-1)
- `m`: Second dimension for grid graphs

### networkx:execute_custom
Executes custom NetworkX Python code.

**Parameters**:
- `code`: Python code to execute (NetworkX imported as `nx`)

## Requirements

- Node.js 18+
- Python 3.7+
- NetworkX (`pip3 install networkx`)
- Matplotlib (`pip3 install matplotlib`) - for visualization

## License

MIT
