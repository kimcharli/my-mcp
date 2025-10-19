#!/usr/bin/env python3
"""
NetworkX MCP Server - Integration Tests

This script tests the NetworkX functionality that will be used by the MCP server.
Run this to verify that all required operations work correctly.
"""

import sys
import json

def print_test(name):
    """Print test header"""
    print(f"\n{'='*60}")
    print(f"TEST: {name}")
    print('='*60)

def print_result(success, message=""):
    """Print test result"""
    symbol = "✓" if success else "✗"
    status = "PASS" if success else "FAIL"
    print(f"{symbol} {status}", end="")
    if message:
        print(f": {message}")
    else:
        print()

def test_basic_graph():
    """Test basic graph creation and operations"""
    print_test("Basic Graph Creation")
    try:
        import networkx as nx
        G = nx.Graph()
        G.add_edges_from([('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'A')])
        
        assert G.number_of_nodes() == 4
        assert G.number_of_edges() == 4
        print_result(True, f"{G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
        return True
    except Exception as e:
        print_result(False, str(e))
        return False

def test_directed_graph():
    """Test directed graph"""
    print_test("Directed Graph")
    try:
        import networkx as nx
        G = nx.DiGraph()
        G.add_edges_from([('A', 'B'), ('B', 'C'), ('C', 'A')])
        
        assert G.is_directed() == True
        assert G.number_of_edges() == 3
        print_result(True, "Directed graph with cycles")
        return True
    except Exception as e:
        print_result(False, str(e))
        return False

def test_shortest_path():
    """Test shortest path algorithms"""
    print_test("Shortest Path")
    try:
        import networkx as nx
        G = nx.Graph()
        G.add_edges_from([('A', 'B'), ('B', 'C'), ('C', 'D'), ('A', 'D')])
        
        path = nx.shortest_path(G, 'A', 'C')
        length = nx.shortest_path_length(G, 'A', 'C')
        
        assert length == 2
        print_result(True, f"Path A→C: {' → '.join(path)}, length: {length}")
        return True
    except Exception as e:
        print_result(False, str(e))
        return False

def test_weighted_shortest_path():
    """Test weighted shortest path"""
    print_test("Weighted Shortest Path")
    try:
        import networkx as nx
        G = nx.Graph()
        G.add_weighted_edges_from([
            ('A', 'B', 1),
            ('B', 'C', 2),
            ('C', 'D', 3),
            ('A', 'D', 10)
        ])
        
        path = nx.shortest_path(G, 'A', 'D', weight='weight')
        length = nx.shortest_path_length(G, 'A', 'D', weight='weight')
        
        assert length == 6  # A→B→C→D = 1+2+3
        print_result(True, f"Weighted path A→D: {' → '.join(path)}, weight: {length}")
        return True
    except Exception as e:
        print_result(False, str(e))
        return False

def test_centrality():
    """Test centrality measures"""
    print_test("Centrality Measures")
    try:
        import networkx as nx
        G = nx.Graph()
        G.add_edges_from([
            ('A', 'B'), ('A', 'C'), ('A', 'D'),
            ('B', 'C'), ('C', 'D')
        ])
        
        degree_cent = nx.degree_centrality(G)
        between_cent = nx.betweenness_centrality(G)
        close_cent = nx.closeness_centrality(G)
        
        # Node A has highest degree (connected to all others)
        assert degree_cent['A'] > degree_cent['B']
        print_result(True, f"Degree centrality A: {degree_cent['A']:.3f}")
        return True
    except Exception as e:
        print_result(False, str(e))
        return False

def test_clustering():
    """Test clustering coefficient"""
    print_test("Clustering Coefficient")
    try:
        import networkx as nx
        G = nx.Graph()
        # Triangle
        G.add_edges_from([('A', 'B'), ('B', 'C'), ('C', 'A')])
        
        clustering = nx.clustering(G)
        avg_clustering = nx.average_clustering(G)
        
        # Perfect triangle has clustering coefficient of 1
        assert clustering['A'] == 1.0
        assert avg_clustering == 1.0
        print_result(True, f"Triangle clustering: {avg_clustering:.3f}")
        return True
    except Exception as e:
        print_result(False, str(e))
        return False

def test_communities():
    """Test community detection"""
    print_test("Community Detection")
    try:
        import networkx as nx
        from networkx.algorithms import community
        
        G = nx.Graph()
        # Two distinct communities
        G.add_edges_from([
            ('A', 'B'), ('B', 'C'), ('C', 'A'),  # Community 1
            ('D', 'E'), ('E', 'F'), ('F', 'D'),  # Community 2
            ('C', 'D')  # Bridge
        ])
        
        communities = list(community.greedy_modularity_communities(G))
        
        assert len(communities) >= 1
        print_result(True, f"Found {len(communities)} communities")
        return True
    except Exception as e:
        print_result(False, str(e))
        return False

def test_connectivity():
    """Test connectivity checks"""
    print_test("Connectivity")
    try:
        import networkx as nx
        
        # Connected graph
        G1 = nx.Graph()
        G1.add_edges_from([('A', 'B'), ('B', 'C'), ('C', 'D')])
        
        # Disconnected graph
        G2 = nx.Graph()
        G2.add_edges_from([('A', 'B'), ('C', 'D')])
        
        assert nx.is_connected(G1) == True
        assert nx.is_connected(G2) == False
        print_result(True, "Connected and disconnected graphs detected")
        return True
    except Exception as e:
        print_result(False, str(e))
        return False

def test_minimum_spanning_tree():
    """Test minimum spanning tree"""
    print_test("Minimum Spanning Tree")
    try:
        import networkx as nx
        
        G = nx.Graph()
        G.add_weighted_edges_from([
            ('A', 'B', 1),
            ('A', 'C', 4),
            ('B', 'C', 2),
            ('B', 'D', 5),
            ('C', 'D', 3)
        ])
        
        mst = nx.minimum_spanning_tree(G)
        total_weight = sum(d['weight'] for u, v, d in mst.edges(data=True))
        
        assert mst.number_of_edges() == 3  # n-1 edges for n nodes
        print_result(True, f"MST edges: {mst.number_of_edges()}, total weight: {total_weight}")
        return True
    except Exception as e:
        print_result(False, str(e))
        return False

def test_graph_generation():
    """Test graph generation"""
    print_test("Graph Generation")
    try:
        import networkx as nx
        
        tests_passed = []
        
        # Complete graph
        G = nx.complete_graph(5)
        tests_passed.append(G.number_of_edges() == 10)
        
        # Cycle graph
        G = nx.cycle_graph(6)
        tests_passed.append(G.number_of_edges() == 6)
        
        # Path graph
        G = nx.path_graph(4)
        tests_passed.append(G.number_of_edges() == 3)
        
        # Star graph
        G = nx.star_graph(5)
        tests_passed.append(G.number_of_edges() == 5)
        
        # Random graph
        G = nx.erdos_renyi_graph(10, 0.3)
        tests_passed.append(G.number_of_nodes() == 10)
        
        success = all(tests_passed)
        print_result(success, f"{sum(tests_passed)}/5 graph types generated correctly")
        return success
    except Exception as e:
        print_result(False, str(e))
        return False

def test_graph_info():
    """Test graph information extraction"""
    print_test("Graph Information")
    try:
        import networkx as nx
        
        G = nx.Graph()
        G.add_edges_from([('A', 'B'), ('B', 'C'), ('C', 'A')])
        
        info = {
            'nodes': G.number_of_nodes(),
            'edges': G.number_of_edges(),
            'density': nx.density(G),
            'is_directed': G.is_directed()
        }
        
        assert info['nodes'] == 3
        assert info['edges'] == 3
        assert info['density'] == 1.0  # Complete triangle
        print_result(True, f"Extracted: {info['nodes']} nodes, density: {info['density']:.2f}")
        return True
    except Exception as e:
        print_result(False, str(e))
        return False

def test_json_serialization():
    """Test JSON serialization of results"""
    print_test("JSON Serialization")
    try:
        import networkx as nx
        
        G = nx.Graph()
        G.add_edges_from([('A', 'B'), ('B', 'C')])
        
        result = {
            'nodes': list(G.nodes()),
            'edges': list(G.edges()),
            'num_nodes': G.number_of_nodes()
        }
        
        json_str = json.dumps(result)
        parsed = json.loads(json_str)
        
        assert parsed['num_nodes'] == 2
        print_result(True, "JSON encoding/decoding works")
        return True
    except Exception as e:
        print_result(False, str(e))
        return False

def test_matplotlib_availability():
    """Test matplotlib availability (optional)"""
    print_test("Matplotlib (Optional)")
    try:
        import matplotlib
        import matplotlib.pyplot as plt
        print_result(True, f"Version {matplotlib.__version__}")
        return True
    except ImportError:
        print_result(True, "Not installed (optional for visualization)")
        return True
    except Exception as e:
        print_result(False, str(e))
        return False

def test_eigenvector_centrality():
    """Test eigenvector centrality"""
    print_test("Eigenvector Centrality")
    try:
        import networkx as nx
        
        G = nx.Graph()
        G.add_edges_from([
            ('A', 'B'), ('A', 'C'), ('A', 'D'),
            ('B', 'C'), ('C', 'D')
        ])
        
        centrality = nx.eigenvector_centrality(G)
        
        assert 'A' in centrality
        assert centrality['A'] > 0
        print_result(True, f"Eigenvector centrality A: {centrality['A']:.3f}")
        return True
    except Exception as e:
        print_result(False, str(e))
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("NetworkX MCP Server - Integration Test Suite")
    print("="*60)
    print("\nTesting NetworkX functionality used by the MCP server...")
    
    tests = [
        test_basic_graph,
        test_directed_graph,
        test_shortest_path,
        test_weighted_shortest_path,
        test_centrality,
        test_eigenvector_centrality,
        test_clustering,
        test_communities,
        test_connectivity,
        test_minimum_spanning_tree,
        test_graph_generation,
        test_graph_info,
        test_json_serialization,
        test_matplotlib_availability
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"\n✗ Unexpected error in {test.__name__}: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(results)
    total = len(results)
    percentage = (passed / total) * 100
    
    print(f"\nPassed: {passed}/{total} ({percentage:.1f}%)")
    
    if passed == total:
        print("\n🎉 All tests passed! Your NetworkX setup is ready.")
        print("\nNext steps:")
        print("1. Run: npm install")
        print("2. Configure Claude Desktop")
        print("3. Start using the NetworkX tools!")
        return 0
    else:
        failed = total - passed
        print(f"\n⚠️  {failed} test(s) failed. Please check the errors above.")
        print("\nTroubleshooting:")
        print("- Ensure NetworkX is installed: pip3 install networkx")
        print("- Check Python version: python3 --version (need 3.7+)")
        print("- Try reinstalling: pip3 install --upgrade networkx")
        return 1

if __name__ == "__main__":
    sys.exit(main())
