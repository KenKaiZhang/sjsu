import argparse
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FFMpegWriter
from matplotlib.patches import Rectangle

class Dijkstra():

    def __init__(self, graph, node_coords):
        self.graph = graph
        self.node_coords = node_coords
        self.G = nx.Graph()
        for node, neighbors in graph.items():
            for neighbor, weight in neighbors.items():
                self.G.add_edge(node, neighbor, weight=weight)

    def compute(self, start, end):
        distances = {node: float("infinity") for node in self.graph}
        visited = set()
        previous = {node: None for node in self.graph}

        distances[start] = 0

        while len(visited) < len(self.graph):
            min_distance = float("infinity")
            current = None

            for node in self.graph:
                if node not in visited and distances[node] < min_distance:
                    min_distance = distances[node]
                    current = node

            if current is None:
                break
            
            if current == end:
                break

            visited.add(current)

            for neighbor, weight in self.graph[current].items():
                if neighbor not in visited:
                    new_distance = distances[current] + weight
                    if new_distance < distances[neighbor]:
                        distances[neighbor] = new_distance
                        previous[neighbor] = current
        
        path = []
        path_cost = []
        current = end

        while current is not None:
            path.append(current)
            path_cost.append((current, round(distances[current],2)))
            current = previous[current]
            
        return path[::-1], path_cost[::-1]

    def visualize(self, start, end):
            fig, ax = plt.subplots(figsize=(8, 8))
            pos = self.node_coords
            
            def draw_graph(explored_edges=[], explored_nodes=set(), path_edges=[], path_nodes=[], highlight_nodes=[]):
                ax.clear()
                nx.draw(self.G, pos, with_labels=True, node_color='lightgray', edge_color='gray', node_size=500, font_size=10)
                
                if explored_edges:
                    nx.draw_networkx_edges(self.G, pos, edgelist=explored_edges, edge_color='cyan', width=2)
                if explored_nodes:
                    nx.draw_networkx_nodes(self.G, pos, nodelist=list(explored_nodes), node_color='cyan', node_size=500)
                
                if path_edges:
                    nx.draw_networkx_edges(self.G, pos, edgelist=path_edges, edge_color='lightgreen', width=3)
                if path_nodes:
                    nx.draw_networkx_nodes(self.G, pos, nodelist=path_nodes, node_color='lightgreen', node_size=500)

                border = Rectangle(
                    (-1.5, -1.5), 
                    23, 
                    23,
                    linewidth=1, 
                    edgecolor='black', 
                    facecolor='none', 
                    joinstyle='round', 
                    capstyle='round'
                )
                ax.add_patch(border)
                ax.set_title(f"Shortest Path From {start} to {end}", fontsize=14, fontweight="bold")
                    
            
            distances = {node: float("infinity") for node in self.graph}
            previous = {node: None for node in self.graph}
            visited = set()
            distances[start] = 0
            frames = []
            
            while len(visited) < len(self.graph):
                min_distance = float("infinity")
                current = None
                
                for node in self.graph:
                    if node not in visited and distances[node] < min_distance:
                        min_distance = distances[node]
                        current = node
                
                visited.add(current)
                explored_edges = [(previous[node], node) for node in visited if previous[node] is not None]
                frames.append((explored_edges, visited.copy(), [], [], []))

                if current is None or current == end:
                    break
                
                for neighbor, weight in self.graph[current].items():
                    if neighbor not in visited:
                        new_distance = distances[current] + weight
                        if new_distance < distances[neighbor]:
                            distances[neighbor] = new_distance
                            previous[neighbor] = current
            
            path = []
            current = end
            while current is not None:
                path.append(current)
                current = previous[current]
            path.reverse()
            
            path_edges = []
            for i in range(len(path) - 1):
                path_edges.append((path[i], path[i+1]))
                path_nodes = path[:i+2]  # Include all nodes discovered so far in the shortest path
                frames.append(([], visited, path_edges.copy(), path_nodes, []))
            
            def update(frame):
                draw_graph(*frame)
            
            ani = animation.FuncAnimation(fig, update, frames=frames, interval=100, repeat=False)
            
            writer = FFMpegWriter(fps=30, metadata=dict(artist='DijkstraVisualizer'), bitrate=1800)
            ani.save("014806701.mp4", writer=writer)

    def save(self, path, path_cost):
        with open("014806701.txt", "w") as f:
            f.write(f"{path}\n")
            f.write(f"{path_cost}\n")

def load_graph(input_file):
    graph = {}
    with open(input_file, "r") as f:
        file_data = f.readlines()

        for line in file_data[3:]:
            node1, node2, weight = line.split()
            
            if node1 not in graph:
                graph[node1] = {}
            
            graph[node1][node2] = float(weight)
    return graph

def load_coordinates(coords_file):
    node_coords = {}
    with open(coords_file, "r") as f:
        file_data = f.readlines()

        for node, line in enumerate(file_data):
            x, y = map(float, line.split())
            node_coords[str(node + 1)] = (int(x), int(y))
    return node_coords

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Run Dijkstra's Algorithm with given input and coordinate files")
    parser.add_argument("-i", "--input", required=True, help="Path to the input file")
    parser.add_argument("-c", "--coords", required=True, help="Path to the coordinates file")
    parser.add_argument("-s", "--start", required=True, help="Start node")
    parser.add_argument("-e", "--end", required=True, help="End node")
    parser.add_argument("-v", "--visualize", nargs="?", const=True, default=None, help="Run visualization and save as mp4")
    args = parser.parse_args()

    try:
        graph = load_graph(args.input)
        node_coords = load_coordinates(args.coords)
        
        dijkstra = Dijkstra(graph, node_coords)
        path, path_cost = dijkstra.compute(args.start, args.end)
        dijkstra.save(path, path_cost)

        if (args.visualize):
            dijkstra.visualize(args.start, args.end)
            
    except Exception as e:
        print(f"Failed to run Dijksta's algorithm: {e}")