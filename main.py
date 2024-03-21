import heapq
import tkinter as tk


# Dijkstra's algorithm function
def dijkstra(graph, start, end):
    # Initialize a dictionary to store the minimum distance of each vertex from the starting vertex
    distances = {vertex: float('infinity') for vertex in graph}
    # Set the distance of the starting vertex to itself as 0
    distances[start] = 0

    # Initialize a dictionary to store the previous vertex in the shortest path for each vertex
    previous_vertices = {vertex: None for vertex in graph}

    # Initialize a priority queue with the starting vertex and its distance (0)
    pq = [(0, start)]
    # Loop until the priority queue is empty
    while pq:
        # Pop the vertex with the smallest distance from the priority queue
        current_distance, current_vertex = heapq.heappop(pq)

        # If the current vertex is the end vertex, construct the shortest path
        if current_vertex == end:
            path = []
            # Trace back the path from the end vertex to the start vertex using the previous_vertices dictionary
            while current_vertex is not None:
                path.append(current_vertex)
                current_vertex = previous_vertices[current_vertex]
            # Reverse the path to get the correct order from start to end
            return current_distance, path[::-1]

        # If the current distance is greater than the already recorded distance for the current vertex, skip this vertex
        if current_distance > distances[current_vertex]:
            continue

        # Iterate through the neighboring vertices and their weights
        for neighbor, weight in graph[current_vertex].items():
            # Calculate the distance to the neighboring vertex through the current vertex
            distance = current_distance + weight

            # If the calculated distance is less than the already recorded distance for the neighboring vertex
            if distance < distances[neighbor]:
                # Update the distance for the neighboring vertex
                distances[neighbor] = distance
                # Update the previous vertex for the neighboring vertex to be the current vertex
                previous_vertices[neighbor] = current_vertex
                # Add the neighboring vertex and its distance to the priority queue
                heapq.heappush(pq, (distance, neighbor))

    # If no path is found, return infinity and an empty list
    return float('infinity'), []


def find_shortest_path(input_graph, start, end):
    return dijkstra(input_graph, start, end)


# Draw the initial graph on the canvas
def draw_graph(gui):
    for node, pos in node_positions.items():
        x, y = pos
        shape = gui.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="black", width=4)
        gui.canvas.create_text(x, y, text=node, font=('Arial', 32, 'bold'))
        gui.node_shapes[node] = shape

    drawn_edge_labels = set()
    for node, neighbors in graph.items():
        for neighbor, weight in neighbors.items():
            node_x, node_y = node_positions[node]
            neighbor_x, neighbor_y = node_positions[neighbor]
            shape = gui.canvas.create_line(node_x, node_y, neighbor_x, neighbor_y, width=4)
            gui.edge_shapes[(node, neighbor)] = shape

            # Draw the edge label only if the edge is not a duplicate
            if (node, neighbor) not in drawn_edge_labels and (neighbor, node) not in drawn_edge_labels:
                draw_edge_label(gui, node, neighbor, weight)
                drawn_edge_labels.add((node, neighbor))


# Reset the graph colors to their initial state
def reset_graph(gui):
    for node, shape in gui.node_shapes.items():
        gui.canvas.itemconfig(shape, fill="black")

    for edge, shape in gui.edge_shapes.items():
        gui.canvas.itemconfig(shape, fill="black")


# Color the path according to the given rules
def color_path(gui, path):
    # Color the nodes and edges in the path
    for i, node in enumerate(path):
        x, y = node_positions[node]
        if i == 0:  # Starting node
            color = "green"
        elif i == len(path) - 1:  # Ending node
            color = "red"
        else:  # Intermediate nodes
            color = "yellow"

        gui.node_shapes[node] = draw_node(gui, node, x, y, )

        if i > 0:
            # Color the edge between the current node and the previous node
            edge_key = (path[i - 1], node)
            gui.edge_shapes[edge_key] = draw_edge(gui, path[i - 1], node, )
            node_shape = gui.node_shapes[node]
            gui.canvas.itemconfig(node_shape, fill="orange")

    start_node_shape = gui.node_shapes[path[0]]
    gui.canvas.itemconfig(start_node_shape, fill="green")

    end_node_shape = gui.node_shapes[path[-1]]
    gui.canvas.itemconfig(end_node_shape, fill="red")


class DijkstraGUI:
    def __init__(self, master):
        self.master = master
        master.title("Dijkstra's Algorithm")

        # Set canvas size to width=1200 and height=600
        self.canvas = tk.Canvas(master, width=1500, height=600)
        self.canvas.pack()

        self.node_shapes = {}
        self.edge_shapes = {}

        # Draw the initial graph
        draw_graph(self)

        # Create and pack the starting point label and entry
        self.start_label = tk.Label(master, text="Starting point:")
        self.start_label.pack(side="left", padx=10, pady=10)
        self.start_entry = tk.Entry(master, width=5)
        self.start_entry.pack(side="left", padx=5, pady=10)

        # Create and pack the ending point label and entry
        self.end_label = tk.Label(master, text="Ending point:")
        self.end_label.pack(side="left", padx=10, pady=10)
        self.end_entry = tk.Entry(master, width=5)
        self.end_entry.pack(side="left", padx=5, pady=10)

        # Create and pack the submit button
        self.submit_button = tk.Button(master, text="Submit", command=self.run_algorithm)
        self.submit_button.pack(side="left", padx=10, pady=10)

        # Create and pack the result label
        self.result_label = tk.Label(master, text="")
        self.result_label.pack(side="bottom", padx=10, pady=10)

    # Run Dijkstra's algorithm, color the path, and display the result
    def run_algorithm(self):
        start = self.start_entry.get()
        end = self.end_entry.get()

        if start in graph and end in graph:
            reset_graph(self)
            shortest_distance, path = dijkstra(graph, start, end)
            print(f"Path: {path}")
            color_path(self, path)

            # Update the result label with the shortest distance and path
            self.result_label.config(text=f"Shortest distance: {shortest_distance}\nPath: {' -> '.join(path)}")
        else:
            self.result_label.config(text="Invalid start or end node.")


# graph database
graph = {
    'A': {'B': 3, 'C': 2, 'D': 1},
    'B': {'A': 3, 'C': 4, 'E': 2},
    'C': {'A': 2, 'B': 4, 'D': 2, 'E': 3, 'F': 6},
    'D': {'A': 1, 'C': 2, 'F': 7, 'G': 8},
    'E': {'B': 2, 'C': 3, 'F': 1, 'H': 5},
    'F': {'C': 6, 'D': 7, 'E': 1, 'G': 9, 'H': 2, 'I': 3},
    'G': {'D': 8, 'F': 9, 'I': 4},
    'H': {'E': 5, 'F': 2, 'I': 1, 'J': 2},
    'I': {'F': 3, 'G': 4, 'H': 1, 'J': 3},
    'J': {'H': 2, 'I': 3}
}

# Updated node positions
node_positions = {
    'A': (100, 300),
    'B': (300, 100),
    'C': (300, 500),
    'D': (500, 200),
    'E': (700, 100),
    'F': (700, 500),
    'G': (900, 200),
    'H': (1100, 100),
    'I': (1100, 500),
    'J': (1300, 300)
}


# Update draw_edge function to create thicker edges
def draw_edge(gui, node1, node2):
    x1, y1 = node_positions[node1]
    x2, y2 = node_positions[node2]
    return gui.canvas.create_line(x1, y1, x2, y2, fill="white", width=4)


# Update draw_node function to create larger nodes
def draw_node(gui, node, x, y):
    shape = gui.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="black", width=4)
    gui.canvas.create_text(x, y, text=node, font=('Arial', 32, 'bold'))
    return shape


# Function to draw edge labels
def draw_edge_label(gui, node1, node2, weight):
    x1, y1 = node_positions[node1]
    x2, y2 = node_positions[node2]
    x = (x1 + x2) / 2
    y = (y1 + y2) / 2

    # Calculate the vector from node1 to node2
    dx, dy = x2 - x1, y2 - y1
    # Normalize the vector and scale it by the desired offset
    length = (dx ** 2 + dy ** 2) ** 0.5
    offset = 10
    dx, dy = dx / length * offset, dy / length * offset

    # Calculate the new label position by adding the offset vector
    x, y = x - dy, y + dx

    return gui.canvas.create_text(x, y, text=str(weight), font=('Arial', 16, 'bold'), fill="white")


if __name__ == "__main__":
    # Create the main Tkinter window and pass it to the DijkstraGUI class
    root = tk.Tk()
    my_gui = DijkstraGUI(root)

    # Run the main
    root.mainloop()
