import heapq
import time
import math


class SearchEngine:

    def __init__(self, grid):
        self.grid = grid

    # Heuristic Functions

    def manhattan(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def euclidean(self, a, b):
        return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

    # Path Reconstruction

    def reconstruct_path(self, parent, start, goal):

        path = []
        node = goal

        while node != start:
            path.append(node)
            node = parent[node]

        path.append(start)
        path.reverse()

        return path

    # A* Search

    def astar(self, heuristic="manhattan"):

        start_time = time.time()

        start = self.grid.start
        goal = self.grid.goal

        if start is None or goal is None:
            return None

        if heuristic == "manhattan":
            h = self.manhattan
        else:
            h = self.euclidean

        frontier = []
        heapq.heappush(frontier, (0, start))

        visited = set()
        parent = {}
        g_cost = {start: 0}

        visited_nodes = []
        frontier_nodes = []

        while frontier:

            _, current = heapq.heappop(frontier)

            if current in visited:
                continue

            visited.add(current)
            visited_nodes.append(current)

            if current == goal:

                path = self.reconstruct_path(parent, start, goal)

                end_time = time.time()

                return {
                    "path": path,
                    "visited": visited_nodes,
                    "frontier": frontier_nodes,
                    "path_cost": len(path) - 1,
                    "nodes_visited": len(visited_nodes),
                    "time_ms": (end_time - start_time) * 1000
                }

            for neighbor in self.grid.get_neighbors(current):

                new_cost = g_cost[current] + 1

                if neighbor not in g_cost or new_cost < g_cost[neighbor]:

                    g_cost[neighbor] = new_cost

                    f = new_cost + h(neighbor, goal)

                    heapq.heappush(frontier, (f, neighbor))

                    parent[neighbor] = current

                    frontier_nodes.append(neighbor)

        return None

    # Greedy Best-First Search

    def gbfs(self, heuristic="manhattan"):

        start_time = time.time()

        start = self.grid.start
        goal = self.grid.goal

        if start is None or goal is None:
            return None

        if heuristic == "manhattan":
            h = self.manhattan
        else:
            h = self.euclidean

        frontier = []
        heapq.heappush(frontier, (h(start, goal), start))

        visited = set()
        parent = {}

        visited_nodes = []
        frontier_nodes = []

        while frontier:

            _, current = heapq.heappop(frontier)

            if current in visited:
                continue

            visited.add(current)
            visited_nodes.append(current)

            if current == goal:

                path = self.reconstruct_path(parent, start, goal)

                end_time = time.time()

                return {
                    "path": path,
                    "visited": visited_nodes,
                    "frontier": frontier_nodes,
                    "path_cost": len(path) - 1,
                    "nodes_visited": len(visited_nodes),
                    "time_ms": (end_time - start_time) * 1000
                }

            for neighbor in self.grid.get_neighbors(current):

                if neighbor not in visited:

                    priority = h(neighbor, goal)

                    heapq.heappush(frontier, (priority, neighbor))

                    parent[neighbor] = current

                    frontier_nodes.append(neighbor)

        return None