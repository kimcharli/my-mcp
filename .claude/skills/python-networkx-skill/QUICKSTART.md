# Python NetworkX Skill - Quick Start

## What Is This?

This is a **Claude Skill** that helps you write Python code using NetworkX for graph and network analysis. It's not an executable tool - it's a knowledge base and guide for getting great NetworkX code from Claude.

## How to Use

Simply ask Claude to help you with NetworkX tasks!

### Example 1: Simple Request
**You:** "Write Python code to create a graph with 5 nodes and visualize it"

**Claude will provide:** Complete, runnable Python code with NetworkX

### Example 2: Specific Analysis
**You:** "I have a social network with these connections: Alice-Bob, Bob-Charlie, Charlie-David. Find who is most central."

**Claude will provide:** Code to create the graph and calculate centrality measures

### Example 3: Data Processing
**You:** "Load a graph from CSV with columns source,target,weight and find the shortest path between node A and node Z"

**Claude will provide:** Complete data loading and path-finding code

## What You Get

✅ Complete, runnable Python code  
✅ Proper NetworkX imports and setup  
✅ Error handling  
✅ Comments explaining the code  
✅ Visualization code when appropriate  
✅ Best practices and optimization tips  

## Your Resources

### 📖 **README.md**
Overview of what the skill can do and common use cases

### 💡 **EXAMPLES.md**
15 complete code examples you can copy and modify:
- Basic graphs
- Path finding
- Centrality analysis
- Community detection
- Visualization
- And more!

### 🎯 **PROMPTS.md**
Learn how to ask Claude effectively:
- Prompt templates
- Do's and don'ts
- Domain-specific examples
- Follow-up questions

### 📚 **QUICK_REFERENCE.md**
Fast lookup for NetworkX operations:
- Common functions
- Algorithm reference
- Visualization options
- I/O operations

## Installation (For Running the Code)

The code Claude generates requires Python and NetworkX:

```bash
pip install networkx matplotlib numpy pandas
```

## Quick Examples

### Create a Graph
```python
import networkx as nx

G = nx.Graph()
G.add_edges_from([('A', 'B'), ('B', 'C'), ('C', 'D')])
print(f"Nodes: {G.number_of_nodes()}, Edges: {G.number_of_edges()}")
```

### Find Shortest Path
```python
import networkx as nx

G = nx.Graph()
G.add_edges_from([('A', 'B'), ('B', 'C'), ('C', 'D'), ('A', 'D')])
path = nx.shortest_path(G, 'A', 'C')
print(f"Shortest path: {' → '.join(path)}")
```

### Visualize
```python
import networkx as nx
import matplotlib.pyplot as plt

G = nx.karate_club_graph()
nx.draw(G, with_labels=True, node_color='lightblue', node_size=500)
plt.show()
```

## Common Tasks

### 🔍 Analysis
- "Calculate centrality for this network"
- "Find communities in this graph"
- "Compute clustering coefficients"

### 🛣️ Paths
- "Find shortest path between two nodes"
- "Find all paths within N hops"
- "Calculate average path length"

### 📊 Visualization
- "Draw this graph with a circular layout"
- "Visualize communities with different colors"
- "Create a hierarchical tree visualization"

### 📁 Data
- "Load graph from CSV file"
- "Export graph to GraphML format"
- "Convert pandas DataFrame to graph"

### 🎲 Generation
- "Generate a random network"
- "Create a scale-free network"
- "Build a small-world network"

## Tips for Success

### ✅ DO:
- Be specific about what you want
- Mention if your graph is directed or weighted
- Provide sample data when possible
- Ask for explanations if needed

### ❌ DON'T:
- Be vague ("make a network")
- Forget to mention data format
- Skip error handling for production code

## Next Steps

1. **Browse EXAMPLES.md** for code templates
2. **Read PROMPTS.md** to learn effective asking
3. **Use QUICK_REFERENCE.md** as a cheat sheet
4. **Start asking Claude!** Just describe what you need

## Example Conversation

**You:** "I'm new to NetworkX. Show me how to create a simple graph of my friends and find who's most connected."

**Claude:** [Provides complete code with explanations]

**You:** "Now visualize it with names on the nodes"

**Claude:** [Adds visualization code]

**You:** "What if I want to add ages as node attributes?"

**Claude:** [Shows how to add node attributes]

## Remember

This skill helps Claude help YOU write NetworkX code. You still need:
- Python installed on your computer
- NetworkX library installed
- A way to run Python code

But Claude will give you all the code you need!

## Get Started Now!

Just ask Claude something like:

> "Help me create a graph analysis script with NetworkX. I have data about..."

Or

> "Show me how to analyze a social network with NetworkX"

Or

> "I need to find the shortest path in a transportation network. How do I do this with NetworkX?"

Claude will take it from there! 🚀📊🐍
