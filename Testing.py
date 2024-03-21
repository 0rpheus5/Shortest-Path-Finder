import random
import time
import matplotlib.pyplot as plt
from main import find_shortest_path


def generate_random_graph(num_nodes):
    graph = {chr(i): {} for i in range(ord('A'), ord('A') + num_nodes)}
    for i in graph:
        if num_nodes <= 2:
            neighbors = graph.keys() - {i}
        else:
            neighbors = random.sample(graph.keys(), random.randint(1, num_nodes // 2))
            neighbors = set(neighbors) - {i}
        for j in neighbors:
            weight = random.randint(1, 10)
            graph[i][j] = weight
            graph[j][i] = weight
    return graph

def measure_runtime(random_graph, start, end):
    start_time = time.time()
    dijkstra(random_graph, start, end)
    end_time = time.time()
    return end_time - start_time


def run_tests(min_nodes, max_nodes, step):
    runtimes = []
    for num_nodes in range(min_nodes, max_nodes + 1, step):
        random_graph = generate_random_graph(num_nodes)
        start_node = random.choice(list(random_graph.keys()))
        end_node = random.choice(list(random_graph.keys() - {start_node}))

        start_time = time.time()
        shortest_distance, path = find_shortest_path(random_graph, start_node, end_node)
        end_time = time.time()

        runtimes.append((num_nodes, end_time - start_time))
        print(f"{num_nodes} nodes: {end_time - start_time} seconds")
    return runtimes


def plot_results(runtimes):
    plt.figure()
    plt.plot([x[0] for x in runtimes], [x[1] for x in runtimes], 'o-')
    plt.xlabel("Number of Nodes")
    plt.ylabel("Runtime (s)")
    plt.title("Dijkstra's Algorithm Runtime vs. Number of Nodes")
    plt.show()


if __name__ == "__main__":
    min_nodes = 10
    max_nodes = 2000
    step = 10

    runtimes = run_tests(min_nodes, max_nodes, step)
    plot_results(runtimes)
