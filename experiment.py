import networkx as nx
import random
from topology_generators import random_graph, small_world_graph, preferential_attachment_graph

def generate_failures_graph(graph: nx.Graph, p: float):
    """ Adds failures with probability p to edges of a graph """
    experiment_graph = graph.copy()
    for edge in experiment_graph.edges():
        if random.random() < p:
            experiment_graph.remove_edge(edge[0], edge[1])
    return experiment_graph

def g_prime(graph: nx.Graph, vertex: str | int):
    """ Makes a copy of the graph without a selected vertex, as defined in the MaxFlowRouting Algorithm """
    g_prime = graph.copy()
    g_prime.remove_node(vertex)
    return g_prime

def create_experiment_setup(graph: nx.Graph):
    """ Creates a dict with the list of neighbors for each destination """
    setup = dict()
    for origin in list(graph.nodes()):
        destinations = list(graph.nodes())
        destinations.remove(origin)

        setup[origin] = dict()
        setup[origin]["g_prime"] = g_prime(graph, origin)
        setup[origin]["destinations"] = destinations

        for destination in destinations:
            neighbors = []
            for neighbor in graph.neighbors(origin):
                if nx.has_path(setup[origin]["g_prime"], neighbor, destination) and neighbor != destination:
                    neighbors.append(neighbor)
            setup[origin]["neighbors_" + destination] = neighbors
    
    return setup

def create_experiment_results_object(setup: dict):
    """ Creates a dict to store results """
    results = dict()

    for origin in setup.keys():
        results[origin] = dict()
        for destination in setup[origin]["destinations"]:
            results[origin][destination] = dict()
            for neighbor in setup[origin]["neighbors_" + destination]:
                results[origin][destination][neighbor] = 0

    return results

def save_to_csv(results: dict, epochs: int, name: str):
    filename = name + ".csv"
    with open("results/" + filename, "w") as f:
        print("Origin,Destination,Neighbor,Result", file=f)
        for origin in results.keys():
            for destination in results[origin].keys():
                for neighbor in results[origin][destination]:
                    print(f"{origin},{destination},{neighbor},{results[origin][destination][neighbor] / epochs}", file=f)

def experiment(graph: nx.Graph, p: float, epochs: int, experiment_name: str):
    setup = create_experiment_setup(graph)
    results = create_experiment_results_object(setup)

    print(f"Starting experiment {experiment_name}!")

    step_10_percent = epochs // 10
    for epoch in range(epochs):
        if (epoch + 1) % step_10_percent == 0:
            percentage = ((epoch + 1) // step_10_percent) * 10
            print(f"Progress: {percentage}% - Epoch {epoch + 1}/{epochs}")

        for origin in graph.nodes():
            experiment_graph = generate_failures_graph(setup[origin]["g_prime"], p)
            for destination in setup[origin]["destinations"]:
                for neighbor in setup[origin]["neighbors_" + destination]:
                    if nx.has_path(experiment_graph, neighbor, destination):
                        results[origin][destination][neighbor] += 1

    save_to_csv(results, epochs, experiment_name)
    print(f"Saved results in results/{experiment_name}.csv")

if __name__ == "__main__":
    P = 0.1
    EPOCHS = 1000

    experiments = [
        (nx.read_edgelist("topologies/rnp.txt"), "rnp_topology"),
        (nx.read_edgelist("topologies/chinanet.txt", "chinanet_topology")),
        (nx.read_edgelist("topologies/internet2.txt", "internet2_topology")),
        (nx.read_edgelist("topologies/geant.txt"), "geant_topology"),
        (random_graph(50, 0.3), "random_graph_50_03"),
        (random_graph(100, 0.3), "random_graph_100_03"),
        (random_graph(150, 0.3), "random_graph_150_03"),
        (random_graph(50, 0.5), "random_graph_50_05"),
        (random_graph(100, 0.5), "random_graph_100_05"),
        (random_graph(150, 0.5), "random_graph_150_05"),
        (random_graph(50, 0.3), "random_graph_50_07"),
        (random_graph(100, 0.7), "random_graph_100_07"),
        (random_graph(150, 0.7), "random_graph_150_07"),
        (small_world_graph(50), "small_world_50"),
        (small_world_graph(100), "small_world_100"),
        (small_world_graph(150), "small_world_150"),
        (preferential_attachment_graph(50), "preferential_attachment_50"),
        (preferential_attachment_graph(100), "preferential_attachment_100"),
        (preferential_attachment_graph(150), "preferential_attachment_150")
    ]

    for graph, name in experiments:
        nx.set_edge_attributes(graph, 1, "capacity")
        nx.set_edge_attributes(graph, 1, "weight")
        experiment(graph, P, EPOCHS, name)