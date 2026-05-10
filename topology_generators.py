import networkx as nx

def random_graph(size: int, connectivity: float, max_attempts: int = 100) -> nx.Graph:
    # Generates a connected Erdos-Renyi G(n, p) graph        
    for _ in range(max_attempts):
        graph = nx.erdos_renyi_graph(size, connectivity)
        if nx.is_connected(graph):
            return graph
    raise ValueError("Failed to generate a connected Erdos-Renyi graph within the maximum attempts.")

def small_world_graph(size: int) -> nx.Graph:
    # Generates a connected Watts-Strogatz small-world graph
    # k=4 (average degree of 4), p=0.4 (rewiring probability)
    graph = nx.connected_watts_strogatz_graph(size, 4, 0.4)
    return graph

def preferential_attachment_graph(size: int) -> nx.Graph:
    # Generates a Barabasi-Albert graph (preferential attachment)
    # m=3 (number of edges to attach from a new node to existing nodes)
    graph = nx.barabasi_albert_graph(size, 3)
    return graph

def remove_low_connectivity_vertices(graph: nx.Graph) -> nx.Graph:
    # Removes vertices that possess connectivity equal to 1
    to_remove = []
    
    for vertex in list(graph.nodes):
        if graph.degree(vertex) <= 1:
            to_remove.append(vertex)
    
    for vertex in to_remove:
        graph.remove_node(vertex)

    return graph