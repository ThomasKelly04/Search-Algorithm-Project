import csv
import time
import heapq
from collections import deque

# Function to load city data (name, latitude, longitude)
def load_cities(filename):
    cities = {}
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip header if present
        for row in reader:
            if len(row) != 3:
                print(f"Skipping invalid row in {filename}: {row}")
                continue
            city, lat, lon = row
            cities[city] = (float(lat), float(lon))
    return cities

# Function to load adjacency list from whitespace-separated file
def load_adjacencies(filename):
    graph = {}
    with open(filename, 'r') as file:
        for line in file:
            row = line.strip().split()  # Split by any whitespace
            if len(row) != 2:
                print(f"Skipping invalid row in {filename}: {row}")
                continue
            city1, city2 = row
            graph.setdefault(city1, []).append(city2)
            graph.setdefault(city2, []).append(city1)  # Ensure bidirectional connection
    return graph

# Function to measure execution time of search algorithms
def measure_time(search_function, *args):
    start = time.perf_counter()  # High-precision timer
    result = search_function(*args)
    end = time.perf_counter()
    
    elapsed_time = end - start
    print(f"Time taken: {elapsed_time:.6f} seconds")  # Display time with 6 decimals
    
    return result  # Return the found path

# Breadth-First Search (BFS)
def bfs(graph, start, goal):
    queue = deque([(start, [start])])  # (Current city, Path)
    visited = set()

    while queue:
        current, path = queue.popleft()
        if current == goal:
            return path  # Goal reached
        if current not in visited:
            visited.add(current)
            for neighbor in graph.get(current, []):
                queue.append((neighbor, path + [neighbor]))

    return None  # No path found

# Depth-First Search (DFS)
def dfs(graph, start, goal):
    stack = [(start, [start])]
    visited = set()

    while stack:
        current, path = stack.pop()
        if current == goal:
            return path
        if current not in visited:
            visited.add(current)
            for neighbor in graph.get(current, []):
                stack.append((neighbor, path + [neighbor]))

    return None

# Iterative Deepening Depth-First Search (ID-DFS)
def iddfs(graph, start, goal, max_depth=20):
    def dls(node, path, depth):
        if depth == 0:
            return None
        if node == goal:
            return path
        for neighbor in graph.get(node, []):
            if neighbor not in path:
                new_path = dls(neighbor, path + [neighbor], depth - 1)
                if new_path:
                    return new_path
        return None

    for depth in range(max_depth):
        result = dls(start, [start], depth)
        if result:
            return result
    return None

# Best-First Search (Greedy)
def best_first_search(graph, cities, start, goal):
    def heuristic(city):
        lat1, lon1 = cities[city]
        lat2, lon2 = cities[goal]
        return ((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2) ** 0.5  # Straight-line distance

    pq = [(heuristic(start), start, [start])]  # (Priority, Current city, Path)
    visited = set()

    while pq:
        _, current, path = heapq.heappop(pq)
        if current == goal:
            return path
        if current not in visited:
            visited.add(current)
            for neighbor in graph.get(current, []):
                heapq.heappush(pq, (heuristic(neighbor), neighbor, path + [neighbor]))

    return None

# A* Search
def a_star(graph, cities, start, goal):
    def heuristic(city):
        lat1, lon1 = cities[city]
        lat2, lon2 = cities[goal]
        return ((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2) ** 0.5  # Straight-line distance

    open_set = [(0, start, [start], 0)]  # (Priority, Current city, Path, Cost so far)
    g_score = {start: 0}
    visited = set()

    while open_set:
        _, current, path, cost = heapq.heappop(open_set)
        if current == goal:
            return path
        if current not in visited:
            visited.add(current)
            for neighbor in graph.get(current, []):
                new_cost = cost + heuristic(neighbor)  # Assume cost is heuristic for simplicity
                if neighbor not in g_score or new_cost < g_score[neighbor]:
                    g_score[neighbor] = new_cost
                    heapq.heappush(open_set, (new_cost + heuristic(neighbor), neighbor, path + [neighbor], new_cost))

    return None

# Main function
def main():
    cities = load_cities("coordinates.csv")  # Load city data
    graph = load_adjacencies("adjacencies.txt")  # Load adjacency data

    while True:
        start_city = input("Enter the starting city: ").strip()
        goal_city = input("Enter the destination city: ").strip()

        if start_city not in cities or goal_city not in cities:
            print("Invalid cities. Please enter valid city names.")
            continue

        print("\nChoose a search method:")
        print("1. Breadth-First Search (BFS)")
        print("2. Depth-First Search (DFS)")
        print("3. Iterative Deepening DFS (ID-DFS)")
        print("4. Best-First Search (Greedy)")
        print("5. A* Search")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            path = measure_time(bfs, graph, start_city, goal_city)
        elif choice == "2":
            path = measure_time(dfs, graph, start_city, goal_city)
        elif choice == "3":
            path = measure_time(iddfs, graph, start_city, goal_city)
        elif choice == "4":
            path = measure_time(best_first_search, graph, cities, start_city, goal_city)
        elif choice == "5":
            path = measure_time(a_star, graph, cities, start_city, goal_city)
        elif choice == "6":
            print("Exiting program.")
            break
        else:
            print("Invalid choice, try again.")
            continue

        if path:
            print(f"Path found: {' → '.join(path)}")
        else:
            print("No path found between the selected cities.")

if __name__ == "__main__":
    main()

