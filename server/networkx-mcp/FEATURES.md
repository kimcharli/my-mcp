# NetworkX MCP Server - Complete Feature List

## 🎯 Overview

This MCP server provides 13 powerful tools for graph theory and network analysis using Python's NetworkX library.

## 📊 Core Tools

### 1. **networkx:create_graph**

Create any type of NetworkX graph

- **Graph Types**: Graph, DiGraph, MultiGraph, MultiDiGraph

- **Features**: Initialize with nodes and edges

- **Use Cases**: Building custom networks from scratch

### 2. **networkx:add_nodes**

Add nodes with optional attributes

- **Attributes**: Custom properties per node

- **Bulk Operations**: Add multiple nodes at once

- **Use Cases**: Expanding existing networks, adding metadata

### 3. **networkx:add_edges**

Add edges with optional weights

- **Weighted Edges**: Support for edge weights

- **Bulk Operations**: Add multiple edges at once

- **Use Cases**: Building connections, weighted networks

## 🔍 Analysis Tools

### 4. **networkx:graph_info**

Get comprehensive graph statistics

- **Metrics**:

  - Number of nodes

  - Number of edges

  - Density

  - Directed/undirected status

- **Use Cases**: Quick overview, initial analysis

### 5. **networkx:shortest_path**

Find optimal paths between nodes

- **Algorithms**:

  - Unweighted shortest path

  - Weighted shortest path (Dijkstra)

- **Outputs**: Path sequence and total length

- **Use Cases**: Navigation, routing, distance analysis

### 6. **networkx:centrality**

Calculate node importance metrics

- **Measures**:  - **Degree Centrality**: Connection count

  - **Betweenness Centrality**: Bridge nodes

  - **Closeness Centrality**: Average distance to all nodes

  - **Eigenvector Centrality**: Influence/prestige

- **Outputs**: Ranked list of nodes by centrality

- **Use Cases**: Finding influencers, key players, bottlenecks

### 7. **networkx:clustering**

Measure local connectedness

- **Metrics**:

  - Individual node clustering

  - Network-wide average clustering

- **Outputs**: Clustering coefficients (0-1)

- **Use Cases**: Community analysis, network cohesion

### 8. **networkx:communities**

Detect community structure

- **Algorithm**: Greedy modularity optimization

- **Outputs**: Groups of tightly connected nodes

- **Use Cases**: Social groups, modules, clusters

### 9. **networkx:is_connected**

Check network connectivity

- **Checks**:

  - Strong connectivity (directed)

  - Weak connectivity (directed)

  - Standard connectivity (undirected)

- **Outputs**: Boolean + component count

- **Use Cases**: Network reliability, fragmentation analysis

## 🏗️ Generation Tools

### 10. **networkx:generate_graph**

Create standard graph structures

- **Types**:

  - **Random**: Erdős-Rényi random graphs

  - **Complete**: All nodes connected

  - **Cycle**: Circular structure

  - **Path**: Linear chain

  - **Star**: Hub and spoke

  - **Wheel**: Star with outer cycle

  - **Ladder**: Two parallel paths

  - **Grid**: 2D lattice

- **Parameters**: Size, probability, dimensions

- **Use Cases**: Testing, modeling, simulations

## 🎨 Visualization

### 11. **networkx:visualize**

Generate matplotlib visualization code

- **Layouts**:

  - **Spring**: Force-directed (default)

  - **Circular**: Nodes on circle

  - **Kamada-Kawai**: Energy-based

  - **Random**: Random placement

  - **Shell**: Concentric circles

  - **Spectral**: Using graph Laplacian

- **Customization**:

  - Node labels on/off

  - Directed arrows

  - Graph type indicators

- **Output**: Complete Python code

- **Use Cases**: Creating visualizations, presentations

## 🚀 Advanced Tools

### 12. **networkx:minimum_spanning_tree**

Find optimal connected subgraph

- **Algorithm**: Kruskal\'s or Prim\'s algorithm

- **Features**:

  - Weighted edges required

  - Minimizes total weight

- **Outputs**: Tree edges and total weight

- **Use Cases**: Network design, infrastructure planning, cost optimization

### 13. **networkx:execute_custom**

Run arbitrary NetworkX code

- **Freedom**: Full Python/NetworkX capabilities

- **Import**: NetworkX pre-imported as `nx`

- **Safety**: Sandboxed execution

- **Use Cases**: Complex analyses, custom algorithms, experimentation

## 🎓 Supported Graph Types

| Type | Description | Directed | Multiple Edges |
|------|-------------|----------|----------------|
| Graph | Simple undirected | ❌ | ❌ |
| DiGraph | Simple directed | ✅ | ❌ |
| MultiGraph | Undirected with parallel edges | ❌ | ✅ |
| MultiDiGraph | Directed with parallel edges | ✅ | ✅ |

## 🔧 Technical Capabilities

### Supported Operations

- ✅ Node/edge creation and manipulation

- ✅ Path finding (shortest, all simple paths)

- ✅ Centrality calculations (4 types)

- ✅ Community detection

- ✅ Clustering analysis

- ✅ Connectivity checks

- ✅ Spanning trees

- ✅ Graph generation (8 types)

- ✅ Visualization code generation

- ✅ Custom Python execution

### Graph Properties Analyzed

- Node count & edge count

- Density

- Degree distribution

- Clustering coefficients

- Centrality measures

- Connected components

- Community structure

- Path lengths

- Network diameter (via custom code)

- Assortativity (via custom code)

## 📈 Use Case Categories

### 1. Social Networks

- Friend connections

- Influence analysis

- Community detection

- Information spread

### 2. Transportation

- Route optimization

- Network coverage

- Critical path identification

- Infrastructure planning

### 3. Biological Networks

- Protein interactions

- Food webs

- Neural networks

- Gene regulatory networks

### 4. Computer Networks

- Internet topology

- Network reliability

- Routing optimization

- Bottleneck identification

### 5. Organizational

- Collaboration networks

- Workflow analysis

- Communication patterns

- Hierarchy visualization

### 6. Academic

- Citation networks

- Co-authorship analysis

- Knowledge graphs

- Concept relationships

## 🎯 Key Features

### Performance

- Efficient Python execution

- Handles large graphs (1000s of nodes)

- Fast centrality calculations

- Optimized algorithms

### Flexibility

- Multiple graph types

- Custom code execution

- Weighted/unweighted edges

- Directed/undirected support

### Ease of Use

- Natural language queries

- Clear output formatting

- Helpful error messages

- Example-rich documentation

### Integration

- Seamless Claude integration

- JSON-based data exchange

- Extensible architecture

- Standard MCP protocol

## 🔮 Advanced Features

### What You Can Do


1. **Multi-Step Analysis**

   - Create → Analyze → Visualize in one conversation

   - Compare multiple networks

   - Iterative refinement


2. **Data Import**

   - Build graphs from data files

   - Parse edge lists

   - Convert formats


3. **Algorithmic Exploration**

   - Test different centrality measures

   - Compare community detection methods

   - Experiment with layouts


4. **Educational Use**

   - Learn graph theory concepts

   - Visualize algorithms

   - Interactive exploration


5. **Research Applications**

   - Network science research

   - Data analysis

   - Model validation

   - Hypothesis testing

## 📚 Learning Resources

Each tool includes:

- Clear parameter descriptions

- Input/output examples

- Common use cases

- Best practices

See **EXAMPLES.md** for 20+ practical examples!

## 🎨 Visualization Examples

The visualization tool generates production-ready matplotlib code for:

- Publication-quality figures

- Interactive exploration

- Custom styling

- Multiple layout algorithms

## 🔒 Security & Reliability


- Sandboxed Python execution

- Error handling for all operations

- Input validation

- Safe graph operations

- No file system access (execution only)

## 📦 Dependencies

### Required

- **Python 3.7+**: Core runtime

- **NetworkX 3.0+**: Graph library

- **Node.js 18+**: MCP server runtime

### Optional

- **Matplotlib 3.5+**: For visualization (recommended)

## 🚀 Performance Notes

Typical performance (on modern hardware):

- Small graphs (<100 nodes): Instant

- Medium graphs (100-1000 nodes): <1 second

- Large graphs (1000-10000 nodes): 1-5 seconds

- Very large graphs (>10000 nodes): Varies by operation

## 🌟 What Makes This Special


1. **Comprehensive**: 13 tools covering major graph operations

2. **Flexible**: Supports all NetworkX graph types

3. **Powerful**: Execute custom Python for unlimited possibilities

4. **Intuitive**: Natural language interface via Claude

5. **Practical**: Real-world examples and use cases

6. **Educational**: Learn graph theory while using it

7. **Production-Ready**: Robust error handling and validation

## 🎯 Perfect For


- Data scientists analyzing networks

- Researchers studying graph theory

- Students learning algorithms

- Engineers designing systems

- Analysts exploring connections

- Anyone working with connected data!
