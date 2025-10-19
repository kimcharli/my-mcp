#!/usr/bin/env node

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import { spawn } from 'child_process';
import { promisify } from 'util';
import { exec as execCallback } from 'child_process';

const exec = promisify(execCallback);

// Initialize MCP server
const server = new Server(
  {
    name: 'networkx-mcp-server',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Helper function to execute Python code
async function executePython(code) {
  try {
    const { stdout, stderr } = await exec(`python3 -c "${code.replace(/"/g, '\\"')}"`);
    if (stderr && !stderr.includes('FutureWarning')) {
      return { success: false, error: stderr };
    }
    return { success: true, output: stdout.trim() };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

// Helper function to run Python script from file
async function runPythonScript(script) {
  return new Promise((resolve, reject) => {
    const python = spawn('python3', ['-c', script]);
    
    let stdout = '';
    let stderr = '';
    
    python.stdout.on('data', (data) => {
      stdout += data.toString();
    });
    
    python.stderr.on('data', (data) => {
      stderr += data.toString();
    });
    
    python.on('close', (code) => {
      if (code !== 0 && stderr) {
        resolve({ success: false, error: stderr });
      } else {
        resolve({ success: true, output: stdout.trim() });
      }
    });
  });
}

// Define available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: 'networkx:create_graph',
        description: 'Create a new NetworkX graph (Graph, DiGraph, MultiGraph, or MultiDiGraph)',
        inputSchema: {
          type: 'object',
          properties: {
            graph_type: {
              type: 'string',
              enum: ['Graph', 'DiGraph', 'MultiGraph', 'MultiDiGraph'],
              description: 'Type of graph to create',
              default: 'Graph'
            },
            nodes: {
              type: 'array',
              items: { type: 'string' },
              description: 'List of nodes to add',
              default: []
            },
            edges: {
              type: 'array',
              items: {
                type: 'array',
                items: { type: 'string' }
              },
              description: 'List of edges as [source, target] pairs',
              default: []
            }
          }
        }
      },
      {
        name: 'networkx:add_nodes',
        description: 'Add nodes to a graph with optional attributes',
        inputSchema: {
          type: 'object',
          properties: {
            nodes: {
              type: 'array',
              items: { type: 'string' },
              description: 'List of nodes to add'
            },
            attributes: {
              type: 'object',
              description: 'Optional attributes for nodes (as JSON object)',
              default: {}
            }
          },
          required: ['nodes']
        }
      },
      {
        name: 'networkx:add_edges',
        description: 'Add edges to a graph with optional weights',
        inputSchema: {
          type: 'object',
          properties: {
            edges: {
              type: 'array',
              items: {
                type: 'array',
                items: { type: 'string' }
              },
              description: 'List of edges as [source, target] pairs'
            },
            weights: {
              type: 'array',
              items: { type: 'number' },
              description: 'Optional weights for edges',
              default: []
            }
          },
          required: ['edges']
        }
      },
      {
        name: 'networkx:graph_info',
        description: 'Get basic information about a graph (nodes, edges, density)',
        inputSchema: {
          type: 'object',
          properties: {
            nodes: {
              type: 'array',
              items: { type: 'string' },
              description: 'List of nodes in the graph'
            },
            edges: {
              type: 'array',
              items: {
                type: 'array',
                items: { type: 'string' }
              },
              description: 'List of edges'
            },
            directed: {
              type: 'boolean',
              description: 'Whether graph is directed',
              default: false
            }
          },
          required: ['nodes', 'edges']
        }
      },
      {
        name: 'networkx:shortest_path',
        description: 'Find shortest path between two nodes',
        inputSchema: {
          type: 'object',
          properties: {
            edges: {
              type: 'array',
              items: {
                type: 'array',
                items: { type: 'string' }
              },
              description: 'List of edges'
            },
            source: {
              type: 'string',
              description: 'Source node'
            },
            target: {
              type: 'string',
              description: 'Target node'
            },
            weighted: {
              type: 'boolean',
              description: 'Whether to use edge weights',
              default: false
            },
            weights: {
              type: 'array',
              items: { type: 'number' },
              description: 'Edge weights (if weighted=true)',
              default: []
            },
            directed: {
              type: 'boolean',
              description: 'Whether graph is directed',
              default: false
            }
          },
          required: ['edges', 'source', 'target']
        }
      },
      {
        name: 'networkx:centrality',
        description: 'Calculate centrality measures (degree, betweenness, closeness, eigenvector)',
        inputSchema: {
          type: 'object',
          properties: {
            edges: {
              type: 'array',
              items: {
                type: 'array',
                items: { type: 'string' }
              },
              description: 'List of edges'
            },
            measure: {
              type: 'string',
              enum: ['degree', 'betweenness', 'closeness', 'eigenvector'],
              description: 'Type of centrality to calculate'
            },
            directed: {
              type: 'boolean',
              description: 'Whether graph is directed',
              default: false
            }
          },
          required: ['edges', 'measure']
        }
      },
      {
        name: 'networkx:clustering',
        description: 'Calculate clustering coefficient',
        inputSchema: {
          type: 'object',
          properties: {
            edges: {
              type: 'array',
              items: {
                type: 'array',
                items: { type: 'string' }
              },
              description: 'List of edges'
            },
            node: {
              type: 'string',
              description: 'Specific node (optional - calculates for all if omitted)'
            }
          },
          required: ['edges']
        }
      },
      {
        name: 'networkx:communities',
        description: 'Detect communities using Louvain algorithm',
        inputSchema: {
          type: 'object',
          properties: {
            edges: {
              type: 'array',
              items: {
                type: 'array',
                items: { type: 'string' }
              },
              description: 'List of edges'
            }
          },
          required: ['edges']
        }
      },
      {
        name: 'networkx:generate_graph',
        description: 'Generate common graph types (random, complete, cycle, path, star, etc.)',
        inputSchema: {
          type: 'object',
          properties: {
            graph_type: {
              type: 'string',
              enum: ['random', 'complete', 'cycle', 'path', 'star', 'wheel', 'ladder', 'grid'],
              description: 'Type of graph to generate'
            },
            n: {
              type: 'number',
              description: 'Number of nodes'
            },
            p: {
              type: 'number',
              description: 'Probability for random graphs (0-1)',
              default: 0.5
            },
            m: {
              type: 'number',
              description: 'Second dimension for grid graphs',
              default: null
            }
          },
          required: ['graph_type', 'n']
        }
      },
      {
        name: 'networkx:visualize',
        description: 'Generate Python code to visualize a graph using matplotlib',
        inputSchema: {
          type: 'object',
          properties: {
            edges: {
              type: 'array',
              items: {
                type: 'array',
                items: { type: 'string' }
              },
              description: 'List of edges'
            },
            layout: {
              type: 'string',
              enum: ['spring', 'circular', 'kamada_kawai', 'random', 'shell', 'spectral'],
              description: 'Layout algorithm',
              default: 'spring'
            },
            directed: {
              type: 'boolean',
              description: 'Whether graph is directed',
              default: false
            },
            node_labels: {
              type: 'boolean',
              description: 'Show node labels',
              default: true
            }
          },
          required: ['edges']
        }
      },
      {
        name: 'networkx:is_connected',
        description: 'Check if graph is connected',
        inputSchema: {
          type: 'object',
          properties: {
            edges: {
              type: 'array',
              items: {
                type: 'array',
                items: { type: 'string' }
              },
              description: 'List of edges'
            },
            directed: {
              type: 'boolean',
              description: 'Whether graph is directed',
              default: false
            }
          },
          required: ['edges']
        }
      },
      {
        name: 'networkx:minimum_spanning_tree',
        description: 'Find minimum spanning tree',
        inputSchema: {
          type: 'object',
          properties: {
            edges: {
              type: 'array',
              items: {
                type: 'array',
                items: { type: 'string' }
              },
              description: 'List of edges'
            },
            weights: {
              type: 'array',
              items: { type: 'number' },
              description: 'Edge weights'
            }
          },
          required: ['edges', 'weights']
        }
      },
      {
        name: 'networkx:execute_custom',
        description: 'Execute custom NetworkX Python code',
        inputSchema: {
          type: 'object',
          properties: {
            code: {
              type: 'string',
              description: 'Python code to execute (NetworkX is imported as nx)'
            }
          },
          required: ['code']
        }
      }
    ]
  };
});

// Handle tool execution
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case 'networkx:create_graph': {
        const { graph_type = 'Graph', nodes = [], edges = [] } = args;
        const script = `
import networkx as nx
import json

G = nx.${graph_type}()
G.add_nodes_from(${JSON.stringify(nodes)})
G.add_edges_from(${JSON.stringify(edges)})

result = {
    'type': '${graph_type}',
    'nodes': list(G.nodes()),
    'edges': list(G.edges()),
    'num_nodes': G.number_of_nodes(),
    'num_edges': G.number_of_edges()
}
print(json.dumps(result))
`;
        const result = await runPythonScript(script);
        if (!result.success) {
          return { content: [{ type: 'text', text: `Error: ${result.error}` }] };
        }
        const data = JSON.parse(result.output);
        return {
          content: [{
            type: 'text',
            text: `Created ${data.type} with ${data.num_nodes} nodes and ${data.num_edges} edges.\nNodes: ${data.nodes.join(', ')}\nEdges: ${JSON.stringify(data.edges)}`
          }]
        };
      }

      case 'networkx:graph_info': {
        const { nodes, edges, directed = false } = args;
        const graphType = directed ? 'DiGraph' : 'Graph';
        const script = `
import networkx as nx
import json

G = nx.${graphType}()
G.add_nodes_from(${JSON.stringify(nodes)})
G.add_edges_from(${JSON.stringify(edges)})

result = {
    'num_nodes': G.number_of_nodes(),
    'num_edges': G.number_of_edges(),
    'density': nx.density(G),
    'is_directed': G.is_directed()
}
print(json.dumps(result))
`;
        const result = await runPythonScript(script);
        if (!result.success) {
          return { content: [{ type: 'text', text: `Error: ${result.error}` }] };
        }
        const data = JSON.parse(result.output);
        return {
          content: [{
            type: 'text',
            text: `Graph Information:\n- Nodes: ${data.num_nodes}\n- Edges: ${data.num_edges}\n- Density: ${data.density.toFixed(4)}\n- Directed: ${data.is_directed}`
          }]
        };
      }

      case 'networkx:shortest_path': {
        const { edges, source, target, weighted = false, weights = [], directed = false } = args;
        const graphType = directed ? 'DiGraph' : 'Graph';
        
        let edgeList = edges;
        if (weighted && weights.length === edges.length) {
          edgeList = edges.map((edge, i) => [...edge, weights[i]]);
        }
        
        const script = `
import networkx as nx
import json

G = nx.${graphType}()
G.add_${weighted ? 'weighted_' : ''}edges_from(${JSON.stringify(edgeList)})

try:
    path = nx.shortest_path(G, '${source}', '${target}'${weighted ? ", weight='weight'" : ''})
    length = nx.shortest_path_length(G, '${source}', '${target}'${weighted ? ", weight='weight'" : ''})
    result = {'path': path, 'length': length}
    print(json.dumps(result))
except nx.NetworkXNoPath:
    print(json.dumps({'error': 'No path exists'}))
`;
        const result = await runPythonScript(script);
        if (!result.success) {
          return { content: [{ type: 'text', text: `Error: ${result.error}` }] };
        }
        const data = JSON.parse(result.output);
        if (data.error) {
          return { content: [{ type: 'text', text: data.error }] };
        }
        return {
          content: [{
            type: 'text',
            text: `Shortest path from ${source} to ${target}:\n${data.path.join(' → ')}\nLength: ${data.length}`
          }]
        };
      }

      case 'networkx:centrality': {
        const { edges, measure, directed = false } = args;
        const graphType = directed ? 'DiGraph' : 'Graph';
        const centralityFuncs = {
          degree: 'degree_centrality',
          betweenness: 'betweenness_centrality',
          closeness: 'closeness_centrality',
          eigenvector: 'eigenvector_centrality'
        };
        
        const script = `
import networkx as nx
import json

G = nx.${graphType}()
G.add_edges_from(${JSON.stringify(edges)})

centrality = nx.${centralityFuncs[measure]}(G)
sorted_centrality = dict(sorted(centrality.items(), key=lambda x: x[1], reverse=True))
print(json.dumps(sorted_centrality))
`;
        const result = await runPythonScript(script);
        if (!result.success) {
          return { content: [{ type: 'text', text: `Error: ${result.error}` }] };
        }
        const data = JSON.parse(result.output);
        const output = Object.entries(data)
          .map(([node, value]) => `${node}: ${value.toFixed(4)}`)
          .join('\n');
        return {
          content: [{
            type: 'text',
            text: `${measure.charAt(0).toUpperCase() + measure.slice(1)} Centrality:\n${output}`
          }]
        };
      }

      case 'networkx:clustering': {
        const { edges, node } = args;
        const script = `
import networkx as nx
import json

G = nx.Graph()
G.add_edges_from(${JSON.stringify(edges)})

${node 
  ? `clustering = nx.clustering(G, '${node}')
result = {'node': '${node}', 'clustering': clustering}`
  : `clustering = nx.clustering(G)
avg_clustering = nx.average_clustering(G)
result = {'clustering': clustering, 'average': avg_clustering}`
}
print(json.dumps(result))
`;
        const result = await runPythonScript(script);
        if (!result.success) {
          return { content: [{ type: 'text', text: `Error: ${result.error}` }] };
        }
        const data = JSON.parse(result.output);
        if (node) {
          return {
            content: [{
              type: 'text',
              text: `Clustering coefficient for ${data.node}: ${data.clustering.toFixed(4)}`
            }]
          };
        } else {
          const output = Object.entries(data.clustering)
            .map(([n, value]) => `${n}: ${value.toFixed(4)}`)
            .join('\n');
          return {
            content: [{
              type: 'text',
              text: `Clustering Coefficients:\n${output}\n\nAverage: ${data.average.toFixed(4)}`
            }]
          };
        }
      }

      case 'networkx:communities': {
        const { edges } = args;
        const script = `
import networkx as nx
import json

G = nx.Graph()
G.add_edges_from(${JSON.stringify(edges)})

# Using greedy modularity communities as it's built into NetworkX
from networkx.algorithms import community
communities = list(community.greedy_modularity_communities(G))
result = [list(c) for c in communities]
print(json.dumps(result))
`;
        const result = await runPythonScript(script);
        if (!result.success) {
          return { content: [{ type: 'text', text: `Error: ${result.error}` }] };
        }
        const data = JSON.parse(result.output);
        const output = data
          .map((comm, i) => `Community ${i + 1}: ${comm.join(', ')}`)
          .join('\n');
        return {
          content: [{
            type: 'text',
            text: `Detected ${data.length} communities:\n${output}`
          }]
        };
      }

      case 'networkx:generate_graph': {
        const { graph_type, n, p = 0.5, m = null } = args;
        let genFunc = '';
        
        switch (graph_type) {
          case 'random':
            genFunc = `nx.erdos_renyi_graph(${n}, ${p})`;
            break;
          case 'complete':
            genFunc = `nx.complete_graph(${n})`;
            break;
          case 'cycle':
            genFunc = `nx.cycle_graph(${n})`;
            break;
          case 'path':
            genFunc = `nx.path_graph(${n})`;
            break;
          case 'star':
            genFunc = `nx.star_graph(${n - 1})`;
            break;
          case 'wheel':
            genFunc = `nx.wheel_graph(${n})`;
            break;
          case 'ladder':
            genFunc = `nx.ladder_graph(${n})`;
            break;
          case 'grid':
            genFunc = `nx.grid_2d_graph(${n}, ${m || n})`;
            break;
        }
        
        const script = `
import networkx as nx
import json

G = ${genFunc}
result = {
    'nodes': [str(n) for n in G.nodes()],
    'edges': [[str(u), str(v)] for u, v in G.edges()],
    'num_nodes': G.number_of_nodes(),
    'num_edges': G.number_of_edges()
}
print(json.dumps(result))
`;
        const result = await runPythonScript(script);
        if (!result.success) {
          return { content: [{ type: 'text', text: `Error: ${result.error}` }] };
        }
        const data = JSON.parse(result.output);
        return {
          content: [{
            type: 'text',
            text: `Generated ${graph_type} graph with ${data.num_nodes} nodes and ${data.num_edges} edges.\nEdges: ${JSON.stringify(data.edges.slice(0, 10))}${data.edges.length > 10 ? '...' : ''}`
          }]
        };
      }

      case 'networkx:visualize': {
        const { edges, layout = 'spring', directed = false, node_labels = true } = args;
        const graphType = directed ? 'DiGraph' : 'Graph';
        
        const code = `import networkx as nx
import matplotlib.pyplot as plt

# Create graph
G = nx.${graphType}()
G.add_edges_from(${JSON.stringify(edges)})

# Set up the plot
plt.figure(figsize=(10, 8))

# Choose layout
pos = nx.${layout}_layout(G)

# Draw the graph
nx.draw(G, pos, 
        with_labels=${node_labels},
        node_color='lightblue',
        node_size=500,
        font_size=10,
        font_weight='bold',
        arrows=${directed},
        edge_color='gray',
        width=2)

plt.title('${graphType} Visualization (${layout} layout)')
plt.axis('off')
plt.tight_layout()
plt.show()
`;
        
        return {
          content: [{
            type: 'text',
            text: `Python code to visualize the graph:\n\n\`\`\`python\n${code}\n\`\`\``
          }]
        };
      }

      case 'networkx:is_connected': {
        const { edges, directed = false } = args;
        const graphType = directed ? 'DiGraph' : 'Graph';
        const connectFunc = directed ? 'is_strongly_connected' : 'is_connected';
        
        const script = `
import networkx as nx
import json

G = nx.${graphType}()
G.add_edges_from(${JSON.stringify(edges)})

connected = nx.${connectFunc}(G)
num_components = nx.number_${directed ? 'strongly' : 'weakly'}_connected_components(G) if ${directed} else nx.number_connected_components(G)
result = {'connected': connected, 'num_components': num_components}
print(json.dumps(result))
`;
        const result = await runPythonScript(script);
        if (!result.success) {
          return { content: [{ type: 'text', text: `Error: ${result.error}` }] };
        }
        const data = JSON.parse(result.output);
        return {
          content: [{
            type: 'text',
            text: `Graph is ${data.connected ? '' : 'not '}connected.\nNumber of components: ${data.num_components}`
          }]
        };
      }

      case 'networkx:minimum_spanning_tree': {
        const { edges, weights } = args;
        const edgeList = edges.map((edge, i) => [...edge, weights[i]]);
        
        const script = `
import networkx as nx
import json

G = nx.Graph()
G.add_weighted_edges_from(${JSON.stringify(edgeList)})

mst = nx.minimum_spanning_tree(G)
result = {
    'edges': [[u, v, d['weight']] for u, v, d in mst.edges(data=True)],
    'total_weight': sum(d['weight'] for u, v, d in mst.edges(data=True))
}
print(json.dumps(result))
`;
        const result = await runPythonScript(script);
        if (!result.success) {
          return { content: [{ type: 'text', text: `Error: ${result.error}` }] };
        }
        const data = JSON.parse(result.output);
        const edgeStr = data.edges
          .map(([u, v, w]) => `${u} - ${v} (weight: ${w})`)
          .join('\n');
        return {
          content: [{
            type: 'text',
            text: `Minimum Spanning Tree:\n${edgeStr}\n\nTotal weight: ${data.total_weight}`
          }]
        };
      }

      case 'networkx:execute_custom': {
        const { code } = args;
        const script = `
import networkx as nx
import json

${code}
`;
        const result = await runPythonScript(script);
        if (!result.success) {
          return { content: [{ type: 'text', text: `Error: ${result.error}` }] };
        }
        return {
          content: [{
            type: 'text',
            text: result.output || 'Code executed successfully (no output)'
          }]
        };
      }

      default:
        return {
          content: [{ type: 'text', text: `Unknown tool: ${name}` }],
          isError: true
        };
    }
  } catch (error) {
    return {
      content: [{ type: 'text', text: `Error: ${error.message}` }],
      isError: true
    };
  }
});

// Start the server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('NetworkX MCP Server running on stdio');
}

main().catch((error) => {
  console.error('Fatal error:', error);
  process.exit(1);
});
