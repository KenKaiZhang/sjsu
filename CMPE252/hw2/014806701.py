import json
import argparse

def build_graph(file):
    graph = {}

    with open(file, "r") as f:
        file_data = f.readlines()
        for line in file_data[3:]:
            node1, node2, weight = line.split()
            if node1 not in graph:
                graph[node1] = {}
            graph[node1][node2] = float(weight)

    return graph


def compute_output(graph, start, goal):

    # Initialize V(x) for all nodes in graph
    Vs = {node: float("inf") for node in graph}

    # V(G) is 0
    Vs[goal] = 0

    # Get all nodes in graph
    nodes = list(graph.keys())

    # Run |V| - 1 times
    for _ in range(len(nodes) - 1):
        # Fill in V(node) proper values
        for node in nodes:
            # Skip goal node since it will always be 0
            if node == goal:
                continue
            # If node exists, calculate V() for its neighbors
            if graph[node]:
                neighbors = [graph[node][neighbor] + Vs[neighbor] for neighbor in graph[node]]
                Vs[node] = min(neighbors)
            else:
                Vs[node] = float("inf")

    for node in nodes:
        if not graph[node]:
            continue
        for neighbor, weight in graph[node].items():
            if Vs[node] != float("inf") and Vs[node] + weight < Vs[neighbor]:
                raise ValueError("Graph contains negative-weight cycle")

    # Building the shortest path
    path = []
    path_cost = []
    current = start
    while current != goal:
        path.append(str(current))
        # The next best node will be the one with the smallest V()
        next = min(graph[current], key=lambda x: graph[current][x] + Vs[x])
        path_cost.append(str(round(graph[current][next] + Vs[next], 4)))
        current = next

    path.append(str(goal))
    path_cost.append("0")

    with open("014806701.txt", "w") as f:
        format_path = " -> ".join(path)
        f.write(f"{format_path}\n")
        f.write(f"{path_cost}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run cost-to-go algorithm to calculate the shortest path.")
    parser.add_argument("-i", "--input", required=True, help="Path to the input file")
    parser.add_argument("-s", "--start", required=True, help="Start node")
    parser.add_argument("-g", "--goal", required=True, help="Goal node")
    args = parser.parse_args()

    try:
        graph = build_graph(args.input)
        compute_output(graph, args.start, args.goal)
    except Exception as e:
        print(f"Failed to find shortest path: {e}")