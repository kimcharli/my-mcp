# Python NetworkX Skill - Code Examples

## Quick Reference Examples

### 1. Basic Graph Creation

```python
import networkx as nx
import matplotlib.pyplot as plt

# Create an undirected graph
G = nx.Graph()

# Add nodes
G.add_nodes_from(['A', 'B', 'C', 'D', 'E'])

# Add edges
G.add_edges_from([
    ('A', 'B'),
    ('B', 'C'),
    ('C', 'D'),
    ('D', 'E'),
    ('E', 'A')
])

print(f"Nodes: {G.number_of_nodes()}")
print(f"Edges: {G.number_of_edges()}")
```

### 2. Directed Graph

```python
import networkx as nx

# Create a directed graph
G = nx.DiGraph()

# Add edges (creates nodes automatically)
G.add_edges_from([
    ('A', 'B'),
    ('B', 'C'),
    ('C', 'A'),
    ('A', 'D')
])

# Check if there's a path
if nx.has_path(G, 'A', 'C'):
    path = nx.shortest_path(G, 'A', 'C')
    print(f"Path from A to C: {' → '.join(path)}")
```

### 3. Weighted Graph and Shortest Path

```python
import networkx as nx

# Create weighted graph
G = nx.Graph()

# Add weighted edges (source, target, weight)
edges = [
    ('SF', 'LA', 380),
    ('LA', 'Phoenix', 370),
    ('Phoenix', 'Denver', 600),
    ('SF', 'Denver', 950),
    ('Denver', 'Chicago', 920),
    ('Chicago', 'NYC', 790)
]

G.add_weighted_edges_from(edges)

# Find shortest path by weight
path = nx.shortest_path(G, 'SF', 'NYC', weight='weight')
distance = nx.shortest_path_length(G, 'SF', 'NYC', weight='weight')

print(f"Shortest route: {' → '.join(path)}")
print(f"Total distance: {distance} miles")
```

### 4. Centrality Analysis

```python
import networkx as nx

# Create a social network
G = nx.Graph()
G.add_edges_from([
    ('Alice', 'Bob'),
    ('Alice', 'Charlie'),
    ('Bob', 'David'),
    ('Charlie', 'David'),
    ('Charlie', 'Eve'),
    ('David', 'Frank'),
    ('Eve', 'Frank')
])

# Calculate different centrality measures
degree_cent = nx.degree_centrality(G)
between_cent = nx.betweenness_centrality(G)
close_cent = nx.closeness_centrality(G)

# Find most central person by betweenness
most_central = max(between_cent, key=between_cent.get)
print(f"Most central person (betweenness): {most_central}")
print(f"Score: {between_cent[most_central]:.3f}")

# Print all centralities
print("\nDegree Centrality:")
for person, score in sorted(degree_cent.items(), key=lambda x: x[1], reverse=True):
    print(f"  {person}: {score:.3f}")
```

### 5. Community Detection

```python
import networkx as nx
from networkx.algorithms import community

# Create a network with clear communities
G = nx.Graph()

# Community 1
G.add_edges_from([('A', 'B'), ('B', 'C'), ('C', 'A')])

# Community 2
G.add_edges_from([('D', 'E'), ('E', 'F'), ('F', 'D')])

# Bridge between communities
G.add_edge('C', 'D')

# Detect communities
communities = list(community.greedy_modularity_communities(G))

print(f"Found {len(communities)} communities:")
for i, comm in enumerate(communities, 1):
    print(f"  Community {i}: {list(comm)}")
```

### 6. Graph from CSV

```python
import networkx as nx
import pandas as pd

# Sample: Read edges from CSV
# CSV format: source,target,weight
df = pd.read_csv('edges.csv')

# Create graph
G = nx.Graph()

# Add edges with weights
for _, row in df.iterrows():
    G.add_edge(row['source'], row['target'], weight=row['weight'])

print(f"Loaded graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

# Or simpler with from_pandas_edgelist
G = nx.from_pandas_edgelist(df, 'source', 'target', edge_attr='weight')
```

### 7. Basic Visualization

```python
import networkx as nx
import matplotlib.pyplot as plt

# Create graph
G = nx.Graph()
G.add_edges_from([
    ('A', 'B'), ('B', 'C'), ('C', 'D'),
    ('D', 'A'), ('A', 'C')
])

# Create layout
pos = nx.spring_layout(G, seed=42)

# Draw
plt.figure(figsize=(8, 6))
nx.draw(G, pos,
        with_labels=True,
        node_color='lightblue',
        node_size=1500,
        font_size=16,
        font_weight='bold',
        edge_color='gray',
        width=2)

plt.title('Simple Graph Visualization')
plt.axis('off')
plt.tight_layout()
plt.show()
```

### 8. Advanced Visualization with Edge Labels

```python
import networkx as nx
import matplotlib.pyplot as plt

# Create weighted graph
G = nx.Graph()
edges = [
    ('A', 'B', 4),
    ('B', 'C', 3),
    ('C', 'D', 2),
    ('D', 'A', 5),
    ('A', 'C', 1)
]
G.add_weighted_edges_from(edges)

# Layout
pos = nx.spring_layout(G, seed=42)

# Draw
plt.figure(figsize=(10, 8))

# Draw nodes
nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=2000)

# Draw edges
nx.draw_networkx_edges(G, pos, width=2, alpha=0.6)

# Draw labels
nx.draw_networkx_labels(G, pos, font_size=16, font_weight='bold')

# Draw edge labels (weights)
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=12)

plt.title('Weighted Graph with Edge Labels', fontsize=18)
plt.axis('off')
plt.tight_layout()
plt.show()
```

### 9. Generate Random Networks

```python
import networkx as nx
import matplotlib.pyplot as plt

# Erdős-Rényi random graph
G_random = nx.erdos_renyi_graph(n=20, p=0.15, seed=42)

# Small-world network (Watts-Strogatz)
G_smallworld = nx.watts_strogatz_graph(n=20, k=4, p=0.3, seed=42)

# Scale-free network (Barabási-Albert)
G_scalefree = nx.barabasi_albert_graph(n=20, m=2, seed=42)

# Visualize all three
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

graphs = [
    (G_random, 'Random (Erdős-Rényi)'),
    (G_smallworld, 'Small-World'),
    (G_scalefree, 'Scale-Free')
]

for ax, (graph, title) in zip(axes, graphs):
    pos = nx.spring_layout(graph, seed=42)
    nx.draw(graph, pos, ax=ax, node_size=200, node_color='lightblue', 
            with_labels=False, edge_color='gray', width=0.5)
    ax.set_title(title)
    ax.axis('off')

plt.tight_layout()
plt.show()
```

### 10. Minimum Spanning Tree

```python
import networkx as nx
import matplotlib.pyplot as plt

# Create weighted graph
G = nx.Graph()
edges = [
    ('A', 'B', 7), ('A', 'D', 5),
    ('B', 'C', 8), ('B', 'D', 9), ('B', 'E', 7),
    ('C', 'E', 5),
    ('D', 'E', 15), ('D', 'F', 6),
    ('E', 'F', 8), ('E', 'G', 9),
    ('F', 'G', 11)
]
G.add_weighted_edges_from(edges)

# Find minimum spanning tree
mst = nx.minimum_spanning_tree(G)

# Calculate total weight
total_weight = sum(d['weight'] for u, v, d in mst.edges(data=True))

print(f"MST edges: {mst.number_of_edges()}")
print(f"Total weight: {total_weight}")
print("\nEdges in MST:")
for u, v, d in mst.edges(data=True):
    print(f"  {u} - {v}: {d['weight']}")

# Visualize original and MST
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

pos = nx.spring_layout(G, seed=42)

# Original graph
ax = axes[0]
nx.draw(G, pos, ax=ax, with_labels=True, node_color='lightblue', 
        node_size=1500, font_size=12, font_weight='bold')
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels, ax=ax)
ax.set_title('Original Weighted Graph')
ax.axis('off')

# MST
ax = axes[1]
nx.draw(mst, pos, ax=ax, with_labels=True, node_color='lightgreen', 
        node_size=1500, font_size=12, font_weight='bold', edge_color='red', width=3)
edge_labels_mst = nx.get_edge_attributes(mst, 'weight')
nx.draw_networkx_edge_labels(mst, pos, edge_labels_mst, ax=ax)
ax.set_title(f'Minimum Spanning Tree (weight={total_weight})')
ax.axis('off')

plt.tight_layout()
plt.show()
```

### 11. PageRank Algorithm

```python
import networkx as nx

# Create a directed graph (e.g., web pages with links)
G = nx.DiGraph()
G.add_edges_from([
    ('Page1', 'Page2'),
    ('Page1', 'Page3'),
    ('Page2', 'Page3'),
    ('Page3', 'Page1'),
    ('Page4', 'Page3'),
    ('Page4', 'Page1')
])

# Calculate PageRank
pagerank = nx.pagerank(G, alpha=0.85)

# Sort by PageRank score
sorted_pages = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)

print("PageRank scores:")
for page, score in sorted_pages:
    print(f"  {page}: {score:.4f}")

# Most important page
print(f"\nMost important page: {sorted_pages[0][0]}")
```

### 12. Clustering Coefficient

```python
import networkx as nx

# Create a graph
G = nx.Graph()
G.add_edges_from([
    ('A', 'B'), ('A', 'C'), ('A', 'D'),
    ('B', 'C'), ('B', 'D'),
    ('C', 'D'),
    ('D', 'E')
])

# Calculate clustering coefficients
clustering = nx.clustering(G)
avg_clustering = nx.average_clustering(G)

print("Clustering coefficients:")
for node, coef in sorted(clustering.items()):
    print(f"  {node}: {coef:.3f}")

print(f"\nAverage clustering: {avg_clustering:.3f}")

# Nodes A, B, C, D form a clique, so they have high clustering
# Node E has only one connection, so clustering is 0
```

### 13. Graph Connectivity

```python
import networkx as nx

# Create a disconnected graph
G = nx.Graph()
G.add_edges_from([
    # Component 1
    ('A', 'B'), ('B', 'C'),
    # Component 2
    ('D', 'E'), ('E', 'F'), ('F', 'D')
])

# Check connectivity
is_connected = nx.is_connected(G)
num_components = nx.number_connected_components(G)
components = list(nx.connected_components(G))

print(f"Is connected: {is_connected}")
print(f"Number of components: {num_components}")
print("\nComponents:")
for i, component in enumerate(components, 1):
    print(f"  Component {i}: {component}")
```

### 14. Directed Acyclic Graph (DAG) - Topological Sort

```python
import networkx as nx

# Create a DAG (e.g., task dependencies)
G = nx.DiGraph()
G.add_edges_from([
    ('Start', 'Task1'),
    ('Start', 'Task2'),
    ('Task1', 'Task3'),
    ('Task2', 'Task3'),
    ('Task3', 'Task4'),
    ('Task4', 'End')
])

# Check if it's a DAG
if nx.is_directed_acyclic_graph(G):
    print("This is a valid DAG")
    
    # Get topological sort (execution order)
    topo_order = list(nx.topological_sort(G))
    print("\nExecution order:")
    for i, task in enumerate(topo_order, 1):
        print(f"  {i}. {task}")
else:
    print("Graph contains cycles!")
```

### 15. Export and Import Graphs

```python
import networkx as nx

# Create a graph
G = nx.Graph()
G.add_weighted_edges_from([
    ('A', 'B', 1.5),
    ('B', 'C', 2.3),
    ('C', 'A', 1.8)
])

# Export to various formats

# GraphML (preserves attributes)
nx.write_graphml(G, 'graph.graphml')

# GML
nx.write_gml(G, 'graph.gml')

# Edge list
nx.write_edgelist(G, 'graph.edgelist', data=['weight'])

# Adjacency list
nx.write_adjlist(G, 'graph.adjlist')

# JSON (node-link format)
from networkx.readwrite import json_graph
import json
data = json_graph.node_link_data(G)
with open('graph.json', 'w') as f:
    json.dump(data, f, indent=2)

# Import back
G_loaded = nx.read_graphml('graph.graphml')
print(f"Loaded graph: {G_loaded.number_of_nodes()} nodes")
```

## Tips for Using These Examples

1. **Copy and modify** - Take these examples as templates
2. **Combine techniques** - Mix different approaches for your needs
3. **Add error handling** - Wrap in try-except for production code
4. **Scale appropriately** - Some algorithms are slow on large graphs
5. **Visualize wisely** - Large graphs (>100 nodes) may need different layouts

## Next Steps

Ask Claude to:
- Modify these examples for your specific use case
- Explain any part you don't understand
- Optimize code for performance
- Add additional features
- Debug your own NetworkX code
