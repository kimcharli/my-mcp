# Python NetworkX Skill - Prompt Guide

## How to Get the Best Code from Claude

This guide helps you ask effective questions to get high-quality NetworkX Python code.

## Basic Prompt Structure

A good prompt includes:
1. **What you want to do** (the goal)
2. **Your data structure** (nodes, edges, attributes)
3. **Expected output** (analysis, visualization, etc.)
4. **Any constraints** (performance, specific algorithms)

## Prompt Templates

### Template 1: Create a Graph
```
"Write Python code to create a [directed/undirected] graph with:
- Nodes: [list or description]
- Edges: [list or connection rules]
- [Optional] Edge weights: [how weights are determined]
- [Optional] Node attributes: [what attributes nodes have]"
```

**Example:**
```
"Write Python code to create an undirected social network with 20 people,
where each person is randomly connected to 3-5 others."
```

### Template 2: Analyze a Graph
```
"I have a [graph type] with [description of structure].
Please write code to:
- Calculate [specific metric]
- Find [specific pattern]
- Analyze [specific property]"
```

**Example:**
```
"I have a transportation network of 30 cities connected by roads.
Write code to find the 5 most central cities using betweenness centrality
and identify any isolated regions."
```

### Template 3: Load and Process Data
```
"Write code to:
1. Load a graph from [file format: CSV/JSON/etc.]
2. The data has [describe structure]
3. Then [what analysis to perform]
4. Output [what you want to see]"
```

**Example:**
```
"Write code to:
1. Load a graph from a CSV with columns: person1, person2, interaction_count
2. Create a weighted graph where edge weights are interaction counts
3. Find the most influential person using PageRank
4. Save the top 10 people to a new CSV file"
```

### Template 4: Visualization
```
"Create a visualization of [graph description] with:
- Layout: [spring/circular/hierarchical/etc.]
- Highlight: [specific nodes or edges]
- Style: [colors, sizes, labels]
- [Optional] Save as: [file format]"
```

**Example:**
```
"Create a visualization of a citation network with:
- Layout: hierarchical (papers cited at top)
- Node size: proportional to citation count
- Node color: by publication year
- Show edge direction with arrows
- Save as PNG with high resolution"
```

### Template 5: Compare Approaches
```
"Show me [number] different ways to [task] and explain
the pros/cons of each approach."
```

**Example:**
```
"Show me 3 different centrality measures for finding influential nodes
in a social network and explain when to use each one."
```

## Specific Task Prompts

### Shortest Path Problems
```
"Write code to find the shortest path in a weighted graph where:
- Graph structure: [describe]
- Start node: [name]
- End node: [name]
- Weight represents: [distance/cost/time/etc.]
- Handle the case where no path exists"
```

### Community Detection
```
"Write code to detect communities in a social network with [N] nodes.
Use [specific algorithm or 'best algorithm'] and visualize the result
with different colors for each community."
```

### Network Generation
```
"Generate a [type] network with [N] nodes that simulates [scenario].
Include code to verify the network has expected properties like
[specific properties]."
```

### Performance Optimization
```
"Write efficient code to [task] on a large graph with approximately
[number] nodes and [number] edges. Focus on memory efficiency and
speed."
```

### Data Import/Export
```
"Write code to:
1. Import a graph from [format/source]
2. Convert it to [NetworkX format]
3. Validate the data (check for [issues])
4. Export to [format] for use in [tool]"
```

## Advanced Prompts

### Multi-Step Analysis
```
"Create a complete analysis pipeline that:
1. Loads data from [source]
2. Cleans the data by [specific cleaning steps]
3. Creates a [graph type]
4. Calculates [metrics 1, 2, 3]
5. Generates [number] visualizations
6. Exports results to [format]

Include progress messages and error handling."
```

### Custom Algorithm
```
"Implement [specific algorithm or approach] for [task].
The algorithm should:
- Input: [describe input]
- Process: [describe steps]
- Output: [describe output]
- Handle edge cases like [list cases]"
```

### Comparative Analysis
```
"Write code to compare [N] different [graphs/algorithms/approaches]:
- [Option 1 description]
- [Option 2 description]
- [Option 3 description]

Create a summary table showing [metrics to compare]."
```

## Common Scenarios

### Scenario 1: Working with Real Data
```
"I have a CSV file with columns [col1, col2, col3, ...].
Each row represents [what it represents].
Write code to load this data and create a graph where [describe graph structure].
Then analyze [what to analyze]."
```

### Scenario 2: Debugging Help
```
"I have this NetworkX code [paste code] but I'm getting [error/unexpected result].
Can you help me fix it and explain what was wrong?"
```

### Scenario 3: Learning a Concept
```
"Explain [concept] in NetworkX and provide a simple working example
that demonstrates the concept with clear comments."
```

### Scenario 4: Optimization
```
"This code [paste code] works but is slow for large graphs.
Can you optimize it and explain the improvements?"
```

### Scenario 5: Adding Features
```
"I have this working code [paste code].
Can you extend it to also:
- [Feature 1]
- [Feature 2]
- [Feature 3]

Keep the existing functionality intact."
```

## Tips for Better Results

### DO:
✅ Be specific about graph properties (directed, weighted, etc.)
✅ Provide example data when possible
✅ Mention the size of your graph (helps with algorithm choice)
✅ State your experience level if you want explanations
✅ Ask for comments in the code
✅ Request error handling
✅ Specify visualization requirements early

### DON'T:
❌ Be vague ("make a network")
❌ Assume Claude knows your data format
❌ Forget to mention performance constraints
❌ Skip validation requirements
❌ Omit the desired output format

## Example Progression

### Beginner Request:
```
"Show me how to create a simple graph and draw it."
```

### Better Request:
```
"Write Python code to create an undirected graph with 5 nodes (A-E)
and 7 edges connecting them. Then visualize it with node labels."
```

### Best Request:
```
"Write Python code to:
1. Create an undirected graph with nodes: ['A', 'B', 'C', 'D', 'E']
2. Add edges: A-B, A-C, B-C, B-D, C-D, C-E, D-E
3. Visualize using spring layout with:
   - Blue nodes (size 1500)
   - Gray edges
   - Bold node labels
   - Figure size 10x8 inches
4. Save as 'graph.png' with 300 DPI
5. Print the number of nodes and edges

Include error handling and comments explaining each step."
```

## Follow-Up Prompts

After getting initial code, you can ask:

- "Add [feature] to this code"
- "Optimize this for graphs with 10,000+ nodes"
- "Explain why you chose [algorithm/approach]"
- "Show an alternative way to do this"
- "Add visualization of [specific aspect]"
- "What are the time and space complexities?"
- "How would this scale to [larger size]?"
- "Add unit tests for this code"

## Domain-Specific Prompts

### Social Networks
```
"Model a social media platform where users can follow others (directed)
and have attributes like follower_count and post_count. Find the top
influencers using appropriate centrality measures."
```

### Biological Networks
```
"Create a protein-protein interaction network from this data [data].
Calculate clustering to identify protein complexes and visualize
the network with proteins colored by their functional category."
```

### Transportation
```
"Build a city transportation network with [N] stops and [M] routes.
Each route has a travel time. Find the optimal route from [start] to [end]
that minimizes total travel time. Show all routes within 10% of optimal."
```

### Supply Chain
```
"Model a supply chain with suppliers, manufacturers, distributors, and retailers.
Identify bottlenecks using betweenness centrality and suggest alternative
routes if a critical node fails."
```

## Getting Help with Errors

```
"This NetworkX code raises [error type]:
[paste error message]

Here's my code:
[paste code]

What's wrong and how do I fix it?"
```

## Asking for Explanations

```
"Explain this NetworkX code line by line:
[paste code]

I particularly don't understand [specific part]."
```

## Remember

The more context you provide, the better code you'll get!

- Clear goal
- Data structure
- Expected output
- Constraints
- Error handling needs
- Visualization preferences

Happy coding! 🐍📊
