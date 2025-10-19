# NetworkX Quick Reference for Claude

## Most Common Operations

### Import
```python
import networkx as nx
import matplotlib.pyplot as plt
```

### Graph Types
```python
G = nx.Graph()           # Undirected
G = nx.DiGraph()         # Directed
G = nx.MultiGraph()      # Undirected, multiple edges
G = nx.MultiDiGraph()    # Directed, multiple edges
```

### Adding Elements
```python
# Single node
G.add_node('A')
G.add_node('A', color='red', weight=1.5)  # with attributes

# Multiple nodes
G.add_nodes_from(['A', 'B', 'C'])
G.add_nodes_from([('A', {'color': 'red'}), ('B', {'color': 'blue'})])

# Single edge
G.add_edge('A', 'B')
G.add_edge('A', 'B', weight=4.5)  # with attributes

# Multiple edges
G.add_edges_from([('A', 'B'), ('B', 'C')])
G.add_weighted_edges_from([('A', 'B', 0.5), ('B', 'C', 1.2)])
```

### Accessing Elements
```python
list(G.nodes())                    # All nodes
list(G.edges())                    # All edges
G.number_of_nodes()                # Node count
G.number_of_edges()                # Edge count
G['A']                             # Neighbors of A
G['A']['B']                        # Edge data between A and B
G.nodes['A']                       # Node A attributes
G.edges['A', 'B']                  # Edge attributes
G.degree('A')                      # Degree of node A
list(G.neighbors('A'))             # Neighbors of A
```

### Graph Generators
```python
nx.complete_graph(n)                      # Complete graph
nx.cycle_graph(n)                         # Cycle
nx.path_graph(n)                          # Path
nx.star_graph(n)                          # Star (n+1 nodes)
nx.wheel_graph(n)                         # Wheel
nx.ladder_graph(n)                        # Ladder
nx.grid_2d_graph(m, n)                    # 2D grid
nx.erdos_renyi_graph(n, p)                # Random
nx.watts_strogatz_graph(n, k, p)          # Small-world
nx.barabasi_albert_graph(n, m)            # Scale-free
nx.karate_club_graph()                    # Example graph
```

### Algorithms - Paths
```python
nx.shortest_path(G, source, target)                    # Path
nx.shortest_path_length(G, source, target)             # Length
nx.shortest_path(G, source, target, weight='weight')   # Weighted
nx.all_shortest_paths(G, source, target)               # All shortest
nx.dijkstra_path(G, source, target, weight='weight')   # Dijkstra
nx.has_path(G, source, target)                         # Check if exists
nx.average_shortest_path_length(G)                     # Average
```

### Algorithms - Centrality
```python
nx.degree_centrality(G)                    # Degree
nx.betweenness_centrality(G)              # Betweenness
nx.closeness_centrality(G)                # Closeness
nx.eigenvector_centrality(G)              # Eigenvector
nx.pagerank(G)                            # PageRank
nx.katz_centrality(G)                     # Katz
nx.load_centrality(G)                     # Load
```

### Algorithms - Clustering
```python
nx.clustering(G)                           # Clustering coefficient
nx.clustering(G, nodes)                    # For specific nodes
nx.average_clustering(G)                   # Average
nx.transitivity(G)                         # Transitivity
nx.triangles(G)                            # Triangle count
```

### Algorithms - Communities
```python
from networkx.algorithms import community

community.greedy_modularity_communities(G)       # Greedy modularity
community.label_propagation_communities(G)       # Label propagation
community.asyn_fluidc(G, k)                     # Fluid communities
community.modularity(G, communities)             # Modularity score
```

### Algorithms - Connectivity
```python
nx.is_connected(G)                         # Undirected
nx.is_strongly_connected(G)                # Directed
nx.is_weakly_connected(G)                  # Directed
nx.number_connected_components(G)          # Component count
nx.connected_components(G)                 # All components
nx.node_connectivity(G)                    # Min nodes to disconnect
nx.edge_connectivity(G)                    # Min edges to disconnect
```

### Algorithms - Trees
```python
nx.minimum_spanning_tree(G)                # MST
nx.maximum_spanning_tree(G)                # Maximum ST
nx.is_tree(G)                              # Check if tree
nx.is_forest(G)                            # Check if forest
```

### Algorithms - Cycles
```python
nx.cycle_basis(G)                          # Cycle basis
nx.simple_cycles(G)                        # All simple cycles
nx.find_cycle(G)                           # Find one cycle
nx.is_directed_acyclic_graph(G)           # Check DAG
```

### Algorithms - Matching
```python
nx.max_weight_matching(G)                  # Maximum matching
nx.is_perfect_matching(G, matching)        # Check perfect
```

### Algorithms - Flow
```python
nx.maximum_flow(G, source, target)                    # Max flow
nx.minimum_cut(G, source, target)                     # Min cut
nx.maximum_flow_value(G, source, target)              # Flow value
```

### Algorithms - Topological Sort (DAG)
```python
nx.topological_sort(G)                     # Topological order
nx.is_directed_acyclic_graph(G)           # Check if DAG
nx.dag_longest_path(G)                    # Longest path in DAG
```

### Graph Properties
```python
nx.density(G)                              # Density
nx.diameter(G)                             # Diameter (if connected)
nx.radius(G)                               # Radius
nx.center(G)                               # Center nodes
nx.periphery(G)                            # Periphery nodes
nx.degree_assortativity_coefficient(G)    # Assortativity
```

### Visualization - Basic
```python
nx.draw(G)                                 # Simple draw
nx.draw(G, with_labels=True)              # With labels
nx.draw_networkx(G, pos)                   # Full control

# Layouts
pos = nx.spring_layout(G)                  # Force-directed
pos = nx.circular_layout(G)                # Circular
pos = nx.kamada_kawai_layout(G)           # Kamada-Kawai
pos = nx.shell_layout(G)                   # Concentric shells
pos = nx.spectral_layout(G)                # Spectral
pos = nx.random_layout(G)                  # Random
```

### Visualization - Detailed
```python
nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=500)
nx.draw_networkx_edges(G, pos, edge_color='gray', width=2)
nx.draw_networkx_labels(G, pos, font_size=12)
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels)
```

### File I/O
```python
# Read
nx.read_edgelist('file.txt')
nx.read_adjlist('file.txt')
nx.read_gml('file.gml')
nx.read_graphml('file.graphml')

# Write
nx.write_edgelist(G, 'file.txt')
nx.write_adjlist(G, 'file.txt')
nx.write_gml(G, 'file.gml')
nx.write_graphml(G, 'file.graphml')

# JSON
from networkx.readwrite import json_graph
data = json_graph.node_link_data(G)
G = json_graph.node_link_graph(data)
```

### Convert from Pandas
```python
import pandas as pd

# From edge list
df = pd.DataFrame({'source': [...], 'target': [...], 'weight': [...]})
G = nx.from_pandas_edgelist(df, 'source', 'target', edge_attr='weight')

# From adjacency matrix
G = nx.from_pandas_adjacency(df)
```

### Convert to Pandas
```python
# To edge list
df = nx.to_pandas_edgelist(G)

# To adjacency matrix
df = nx.to_pandas_adjacency(G)
```

### Node/Edge Attributes
```python
# Set
nx.set_node_attributes(G, values, 'attribute_name')
nx.set_edge_attributes(G, values, 'attribute_name')

# Get
nx.get_node_attributes(G, 'attribute_name')
nx.get_edge_attributes(G, 'attribute_name')

# Access
G.nodes['A']['color'] = 'red'
G.edges['A', 'B']['weight'] = 2.5
```

### Subgraphs
```python
H = G.subgraph(['A', 'B', 'C'])           # Induced subgraph
H = G.edge_subgraph([('A', 'B'), ('B', 'C')])  # Edge subgraph
H = G.copy()                               # Full copy
```

### Graph Operations
```python
nx.compose(G1, G2)                         # Union
nx.intersection(G1, G2)                    # Intersection
nx.difference(G1, G2)                      # Difference
nx.symmetric_difference(G1, G2)            # Symmetric difference
nx.complement(G)                           # Complement
```

### Convert Graph Types
```python
G_directed = G.to_directed()               # To directed
G_undirected = G.to_undirected()          # To undirected
```

### Filtering
```python
# Node-induced subgraph
nodes_to_keep = [n for n in G.nodes() if G.degree(n) > 2]
H = G.subgraph(nodes_to_keep)

# Edge-induced subgraph  
edges_to_keep = [(u,v) for u,v in G.edges() if G[u][v].get('weight', 0) > 5]
H = G.edge_subgraph(edges_to_keep)
```

### Common Patterns

#### Check if node exists
```python
if 'A' in G:
    print("Node A exists")
```

#### Check if edge exists
```python
if G.has_edge('A', 'B'):
    print("Edge A-B exists")
```

#### Iterate nodes with attributes
```python
for node, attrs in G.nodes(data=True):
    print(f"{node}: {attrs}")
```

#### Iterate edges with attributes
```python
for u, v, attrs in G.edges(data=True):
    print(f"{u}-{v}: {attrs}")
```

#### Remove nodes/edges
```python
G.remove_node('A')
G.remove_nodes_from(['A', 'B'])
G.remove_edge('A', 'B')
G.remove_edges_from([('A', 'B'), ('C', 'D')])
```

#### Clear graph
```python
G.clear()                  # Remove all nodes and edges
G.clear_edges()           # Remove all edges, keep nodes
```

## Performance Tips

1. **Use views**: `G.nodes()`, `G.edges()` return views (efficient)
2. **Avoid conversion**: Don't convert to list unless needed
3. **Batch operations**: Use `add_nodes_from()`, `add_edges_from()`
4. **Memory**: Use `G.clear()` when done with large graphs
5. **Algorithms**: Some algorithms are O(n²) or O(n³) - be careful with large graphs

## Common Gotchas

1. **Node names**: Can be any hashable type (strings, numbers, tuples)
2. **Graph copies**: `G.subgraph()` returns a view, use `.copy()` for independent copy
3. **Directed vs undirected**: Some algorithms only work on specific types
4. **Weighted graphs**: Must specify `weight='weight'` parameter
5. **Disconnected graphs**: Some algorithms require connected graphs

## Getting Help

```python
# Documentation
help(nx.shortest_path)

# Available functions
dir(nx)

# NetworkX version
nx.__version__
```
