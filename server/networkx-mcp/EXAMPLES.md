# NetworkX MCP Server - Examples

## Basic Graph Operations

### Example 1: Create a Simple Social Network

**Prompt**: "Create a social network graph with these friendships: Alice-Bob, Bob-Charlie, Charlie-David, David-Alice, Alice-Charlie, Bob-David. Then calculate who has the most connections."

The server will:

1. Use `create_graph` to build the network

2. Use `centrality` with measure="degree" to find the most connected person

### Example 2: Find Shortest Path

**Prompt**: "I have cities connected by roads: SF-LA, LA-Phoenix, Phoenix-Denver, Denver-Chicago, Chicago-NYC, SF-Denver. What's the shortest path from SF to NYC?"

The server will use `shortest_path` to find the minimum number of hops.

## Network Analysis

### Example 3: Weighted Shortest Path

**Prompt**: "Given these routes with distances in miles:

- SF to LA: 380

- LA to Phoenix: 370

- Phoenix to Denver: 600

- SF to Denver: 950

- Denver to Chicago: 920

- Chicago to NYC: 790

What's the shortest route by distance from SF to NYC?"

### Example 4: Community Detection

**Prompt**: "Analyze this social network and find friend groups:
Alice-Bob, Alice-Charlie, Bob-Charlie, David-Eve, David-Frank, Eve-Frank, Charlie-David"

The server will use `communities` to identify clusters.

### Example 5: Network Centrality Analysis

**Prompt**: "Calculate betweenness centrality for a network with edges: A-B, B-C, C-D, D-E, B-D, A-C. Who are the key connectors?"

Betweenness centrality identifies nodes that act as bridges between other nodes.

## Graph Generation

### Example 6: Random Network

**Prompt**: "Generate a random network with 20 nodes and 30% connection probability. Then check if it's connected."

Uses `generate_graph` with type="random" and `is_connected` to analyze.

### Example 7: Standard Graph Types

**Prompt**: "Create a wheel graph with 8 nodes and visualize it with spring layout."

Creates a wheel graph (hub with spokes) and generates matplotlib code.

## Advanced Operations

### Example 8: Minimum Spanning Tree

**Prompt**: "I need to connect 5 offices with fiber cable. Here are the costs between locations:
A-B: $1200, A-C: $1800, B-C: $900, B-D: $2100, C-D: $1500, C-E: $1100, D-E: $800

What's the cheapest way to connect all offices?"

Uses `minimum_spanning_tree` to find the optimal solution.

### Example 9: Clustering Coefficient

**Prompt**: "Calculate the clustering coefficient for this friendship network:
A-B, A-C, A-D, B-C, B-D, C-D, D-E, D-F, E-F

How tightly knit are the friend groups?"

### Example 10: Path Analysis

**Prompt**: "Given this transportation network:
NYC-Boston, Boston-Portland, NYC-Philadelphia, Philadelphia-DC, DC-Richmond, NYC-Pittsburgh, Pittsburgh-Cleveland, Cleveland-Detroit

Find all paths from NYC to Detroit that are 5 hops or less."

## Visualization

### Example 11: Network Diagram

**Prompt**: "Create a visualization of a star network with 7 nodes using circular layout. Show me the Python code."

Generates complete matplotlib visualization code.

### Example 12: Directed Graph Visualization

**Prompt**: "Visualize a food chain: Grass→Rabbit, Rabbit→Fox, Rabbit→Hawk, Fox→Decomposer, Hawk→Decomposer. Use hierarchical layout."

Creates a directed graph with arrows showing relationships.

## Complex Queries

### Example 13: Multi-Step Analysis

**Prompt**: "Create a random social network with 30 people and 20% connection probability. Then:

1. Check if it's connected

2. Find the person with highest betweenness centrality

3. Identify communities

4. Calculate average clustering coefficient"

### Example 14: Comparison Analysis

**Prompt**: "Compare these two network structures:
Network A: Complete graph with 5 nodes
Network B: Star graph with 5 nodes

Calculate density, average clustering, and degree centrality for both."

### Example 15: Network Growth Simulation

**Prompt**: "Start with a triangle (A-B-C). Then add nodes D, E, F where each new node connects to 2 random existing nodes. Show the final network properties."

Uses `execute_custom` for complex operations.

## Real-World Applications

### Example 16: Analyzing a Citation Network

**Prompt**: "I have a citation network where papers cite each other:
Paper1→Paper5, Paper2→Paper1, Paper2→Paper5, Paper3→Paper1, Paper3→Paper2, Paper4→Paper3

Which papers are most influential (highest PageRank-like centrality)?"

### Example 17: Transportation Network Optimization

**Prompt**: "Design an efficient bus route network for 10 neighborhoods. Create a connected network with minimum total distance where each neighborhood has 2-3 connections."

### Example 18: Collaboration Network

**Prompt**: "Analyze this co-authorship network:
Alice-Bob-Paper1, Bob-Charlie-Paper2, Alice-Charlie-Paper3, David-Eve-Paper4, Eve-Charlie-Paper5

Who are the key collaborators bridging different research groups?"

## Custom Python Code

### Example 19: Advanced NetworkX Operations

**Prompt**: "Use custom Python code to create a scale-free network with 100 nodes using Barabási-Albert model (m=2), then calculate the degree distribution."

Uses `execute_custom` with custom NetworkX code.

### Example 20: Graph Metrics Suite

**Prompt**: "Calculate a complete metrics report for this network including: density, average path length, diameter, assortativity, and transitivity."

## Tips for Best Results


1. **Be specific about graph type**: Mention if directed/undirected, weighted/unweighted

2. **Provide complete data**: Include all nodes and edges

3. **State your goal clearly**: Analysis, visualization, or generation

4. **Use node names consistently**: Keep naming simple (A, B, C or names)

5. **Ask for comparisons**: Compare multiple networks or metrics

6. **Request explanations**: Ask what metrics mean in your context

## Common NetworkX Concepts


- **Degree**: Number of connections a node has

- **Path**: Sequence of edges connecting two nodes

- **Centrality**: Measures of node importance

- **Clustering**: How interconnected a node's neighbors are

- **Community**: Dense groups of nodes with sparse connections between groups

- **Connected**: All nodes can reach each other through paths

- **Spanning Tree**: Subset of edges connecting all nodes without cycles
