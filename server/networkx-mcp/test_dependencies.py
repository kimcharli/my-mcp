#!/usr/bin/env python3
"""
Test script to verify NetworkX installation and basic functionality
"""

import sys

def test_networkx():
    """Test NetworkX installation"""
    try:
        import networkx as nx
        print("✓ NetworkX installed successfully")
        print(f"  Version: {nx.__version__}")
        
        # Test basic graph creation
        G = nx.Graph()
        G.add_edges_from([('A', 'B'), ('B', 'C'), ('C', 'A')])
        print(f"✓ Graph creation works")
        print(f"  Created graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
        
        # Test shortest path
        path = nx.shortest_path(G, 'A', 'C')
        print(f"✓ Shortest path algorithm works")
        print(f"  Path A→C: {' → '.join(path)}")
        
        # Test centrality
        centrality = nx.degree_centrality(G)
        print(f"✓ Centrality calculations work")
        print(f"  Degree centrality: {centrality}")
        
        return True
    except ImportError as e:
        print(f"✗ NetworkX not installed: {e}")
        print("  Install with: pip3 install networkx")
        return False
    except Exception as e:
        print(f"✗ Error testing NetworkX: {e}")
        return False

def test_matplotlib():
    """Test matplotlib installation"""
    try:
        import matplotlib
        print("✓ Matplotlib installed successfully")
        print(f"  Version: {matplotlib.__version__}")
        return True
    except ImportError:
        print("✗ Matplotlib not installed (optional for visualization)")
        print("  Install with: pip3 install matplotlib")
        return False
    except Exception as e:
        print(f"✗ Error testing matplotlib: {e}")
        return False

def main():
    print("=" * 50)
    print("NetworkX MCP Server - Dependency Test")
    print("=" * 50)
    print()
    
    nx_ok = test_networkx()
    print()
    mpl_ok = test_matplotlib()
    print()
    
    if nx_ok:
        print("✓ All required dependencies are installed!")
        print("  You can now run: npm install")
        print("  Then configure Claude Desktop with this MCP server")
        return 0
    else:
        print("✗ Missing required dependencies")
        print("  Please install NetworkX before proceeding")
        return 1

if __name__ == "__main__":
    sys.exit(main())
