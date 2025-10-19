# NetworkX MCP Server - Architecture

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Claude Desktop                           │
│                                                              │
│  User: "Find shortest path from A to B in my network"      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ MCP Protocol (stdio)
                         │
┌────────────────────────▼────────────────────────────────────┐
│              NetworkX MCP Server (Node.js)                   │
│                                                              │
│  ┌────────────────────────────────────────────────────┐   │
│  │  Tool Router                                        │   │
│  │  - Receives MCP requests                           │   │
│  │  - Validates parameters                            │   │
│  │  - Routes to appropriate handler                   │   │
│  └────────────────┬───────────────────────────────────┘   │
│                   │                                          │
│  ┌────────────────▼───────────────────────────────────┐   │
│  │  Tool Handlers (13 tools)                          │   │
│  │  - create_graph                                    │   │
│  │  - shortest_path                                   │   │
│  │  - centrality                                      │   │
│  │  - communities                                     │   │
│  │  - ... and 9 more                                  │   │
│  └────────────────┬───────────────────────────────────┘   │
│                   │                                          │
│                   │ Python Script Generation                 │
│                   │                                          │
└───────────────────┼──────────────────────────────────────────┘
                    │
                    │ spawn python3 process
                    │
┌───────────────────▼──────────────────────────────────────────┐
│                  Python 3 Runtime                             │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  NetworkX Library                                    │   │
│  │  - Graph data structures                            │   │
│  │  - Algorithms (paths, centrality, communities)      │   │
│  │  - Graph generation                                 │   │
│  │  - Analysis functions                               │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Matplotlib (optional)                               │   │
│  │  - Visualization layout algorithms                   │   │
│  │  - Drawing functions                                 │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                               │
└───────────────────┬──────────────────────────────────────────┘
                    │
                    │ JSON output (stdout)
                    │
┌───────────────────▼──────────────────────────────────────────┐
│              Results Processing                               │
│              - Parse JSON output                              │
│              - Format for Claude                              │
│              - Handle errors                                  │
└───────────────────┬──────────────────────────────────────────┘
                    │
                    │ MCP Response
                    │
┌───────────────────▼──────────────────────────────────────────┐
│                     Claude Desktop                            │
│                                                               │
│  "The shortest path from A to B is: A → C → B                │
│   Length: 2"                                                  │
└───────────────────────────────────────────────────────────────┘
```

## Data Flow

### Example: Finding Shortest Path

1. **User Input** (Natural Language)
   ```
   "Find shortest path from SF to NYC in this network:
   SF-LA, LA-Phoenix, Phoenix-Denver, Denver-Chicago, Chicago-NYC"
   ```

2. **Claude Processing**
   - Understands intent: shortest path calculation
   - Identifies tool: `networkx:shortest_path`
   - Extracts parameters:
     - edges: [["SF","LA"], ["LA","Phoenix"], ...]
     - source: "SF"
     - target: "NYC"

3. **MCP Request** (JSON-RPC)
   ```json
   {
     "method": "tools/call",
     "params": {
       "name": "networkx:shortest_path",
       "arguments": {
         "edges": [["SF","LA"], ["LA","Phoenix"], ...],
         "source": "SF",
         "target": "NYC",
         "directed": false
       }
     }
   }
   ```

4. **Server Processing**
   - Validates parameters
   - Generates Python script:
     ```python
     import networkx as nx
     import json
     
     G = nx.Graph()
     G.add_edges_from([["SF","LA"], ["LA","Phoenix"], ...])
     
     path = nx.shortest_path(G, 'SF', 'NYC')
     length = nx.shortest_path_length(G, 'SF', 'NYC')
     
     result = {'path': path, 'length': length}
     print(json.dumps(result))
     ```

5. **Python Execution**
   - Spawns python3 process
   - Executes script
   - NetworkX calculates shortest path
   - Returns JSON to stdout

6. **Result Processing**
   ```json
   {
     "path": ["SF", "LA", "Phoenix", "Denver", "Chicago", "NYC"],
     "length": 5
   }
   ```

7. **MCP Response**
   ```json
   {
     "content": [{
       "type": "text",
       "text": "Shortest path from SF to NYC:\nSF → LA → Phoenix → Denver → Chicago → NYC\nLength: 5"
     }]
   }
   ```

8. **Claude Response** (Natural Language)
   ```
   The shortest path from San Francisco to New York City is:
   SF → LA → Phoenix → Denver → Chicago → NYC
   
   This route requires 5 connections (or hops).
   ```

## Component Details

### Node.js Server
- **Runtime**: Node.js 18+
- **Framework**: @modelcontextprotocol/sdk
- **Communication**: stdio transport
- **Responsibilities**:
  - MCP protocol handling
  - Tool registration
  - Parameter validation
  - Python script generation
  - Process management
  - Error handling

### Python Environment
- **Runtime**: Python 3.7+
- **Libraries**: NetworkX 3.0+, Matplotlib 3.5+
- **Execution**: Spawned child processes
- **Responsibilities**:
  - Graph operations
  - Algorithm execution
  - Data processing
  - Result formatting

### Tool Categories

```
┌─────────────────────────────────────────────────┐
│           NetworkX MCP Tools                     │
├─────────────────────────────────────────────────┤
│                                                  │
│  📊 Creation & Manipulation                      │
│     • create_graph                              │
│     • add_nodes                                 │
│     • add_edges                                 │
│     • generate_graph                            │
│                                                  │
│  🔍 Analysis                                     │
│     • graph_info                                │
│     • shortest_path                             │
│     • centrality                                │
│     • clustering                                │
│     • communities                               │
│     • is_connected                              │
│                                                  │
│  🚀 Advanced                                     │
│     • minimum_spanning_tree                     │
│     • execute_custom                            │
│                                                  │
│  🎨 Visualization                                │
│     • visualize                                 │
│                                                  │
└─────────────────────────────────────────────────┘
```

## Error Handling Flow

```
User Request
     │
     ▼
Parameter Validation ──✗──▶ Return validation error
     │ ✓
     ▼
Python Script Generation
     │
     ▼
Process Spawn ──────────✗──▶ Return spawn error
     │ ✓
     ▼
Script Execution ───────✗──▶ Capture stderr, return error
     │ ✓
     ▼
JSON Parsing ───────────✗──▶ Return parsing error
     │ ✓
     ▼
Format Response
     │
     ▼
Return to Claude
```

## Tool Execution Patterns

### Pattern 1: Direct Graph Operations
```
User Query → Tool Handler → Python Script → NetworkX → Result
```
Examples: graph_info, is_connected, clustering

### Pattern 2: Algorithm Execution
```
User Query → Tool Handler → Python Script → NetworkX Algorithm → Result
```
Examples: shortest_path, centrality, communities, MST

### Pattern 3: Code Generation
```
User Query → Tool Handler → Code Template → Return Code String
```
Examples: visualize

### Pattern 4: Custom Execution
```
User Query → Tool Handler → User Python Code → NetworkX → Result
```
Examples: execute_custom

## Configuration Flow

```
1. User edits config file:
   ~/Library/Application Support/Claude/claude_desktop_config.json

2. Claude Desktop reads config on startup

3. Claude Desktop spawns MCP server:
   node /path/to/networkx-mcp/index.js

4. Server starts stdio transport

5. Server registers 13 tools via MCP protocol

6. Claude Desktop now has access to all NetworkX tools

7. User can start using tools in conversation
```

## Security Considerations

### Sandboxing
- Python processes are spawned per-request
- No persistent state between requests
- No file system access (except temp for execution)
- No network access from Python scripts

### Input Validation
- Parameter type checking
- Graph size limits (configurable)
- Edge/node count validation
- Timeout protection on Python execution

### Error Isolation
- Python errors don't crash Node.js server
- Failed requests don't affect other requests
- Graceful error messages to user

## Performance Optimization

### Caching (Future Enhancement)
```
Request → Check Cache → Hit: Return cached result
                     → Miss: Execute & cache result
```

### Batch Operations (Current)
- Multiple edges/nodes added in single operation
- Bulk graph generation

### Async Processing
- Non-blocking Python execution
- Promise-based architecture
- Concurrent request handling

## Extensibility

### Adding New Tools

1. **Define Tool Schema**
   ```javascript
   {
     name: 'networkx:new_tool',
     description: '...',
     inputSchema: { ... }
   }
   ```

2. **Implement Handler**
   ```javascript
   case 'networkx:new_tool': {
     // Generate Python script
     // Execute
     // Return results
   }
   ```

3. **Document in README**

### Supporting New NetworkX Features
- Update Python requirements
- Add new tool definitions
- Test and document

## Monitoring & Debugging

### Logs
```
Node.js Server: console.error() → stderr
Python Output: print() → stdout (captured)
Python Errors: stderr → captured and returned
```

### Testing
```bash
# Test Python dependencies
python3 test_dependencies.py

# Test Node.js server (manual)
node index.js

# Send test MCP request
echo '{"method":"tools/list"}' | node index.js
```

## Deployment

### Development
```
Local filesystem → Direct node execution → stdio
```

### Production (Claude Desktop)
```
Config file → Claude spawns server → stdio transport → User interaction
```

This architecture provides:
- ✅ Clean separation of concerns
- ✅ Language-appropriate implementations
- ✅ Error resilience
- ✅ Easy extensibility
- ✅ Good performance
- ✅ User-friendly interface
