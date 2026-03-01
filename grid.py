import numpy as np
import random


class Grid:

    EMPTY = 0
    WALL = 1
    START = 2
    GOAL = 3

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = self.initialize_grid()
        self.start = None
        self.goal = None

    def initialize_grid(self):
        return np.zeros((self.rows, self.cols))

    def check_valid_position(self, r, c):
        if r < 0 or r >= self.rows or c < 0 or c >= self.cols:
            return False
        return True

    def set_wall(self, r, c):
        if self.check_valid_position(r, c):
            if (r, c) != self.start and (r, c) != self.goal:
                self.grid[r][c] = Grid.WALL

    def remove_wall(self, r, c):
        if self.check_valid_position(r, c):
            self.grid[r][c] = Grid.EMPTY

    def toggle_wall(self, r, c):
        if self.check_valid_position(r, c):

            if (r, c) == self.start or (r, c) == self.goal:
                return

            if self.grid[r][c] == Grid.WALL:
                self.grid[r][c] = Grid.EMPTY
            else:
                self.grid[r][c] = Grid.WALL

    def set_start(self, r, c):
        if self.check_valid_position(r, c):

            if self.grid[r][c] != Grid.WALL:

                if self.start is not None:
                    old_r, old_c = self.start
                    self.grid[old_r][old_c] = Grid.EMPTY

                self.start = (r, c)
                self.grid[r][c] = Grid.START

    def set_goal(self, r, c):
        if self.check_valid_position(r, c):

            if self.grid[r][c] != Grid.WALL:

                if self.goal is not None:
                    old_r, old_c = self.goal
                    self.grid[old_r][old_c] = Grid.EMPTY

                self.goal = (r, c)
                self.grid[r][c] = Grid.GOAL

    def random_obstacles(self, density):

        for r in range(self.rows):
            for c in range(self.cols):

                if (r, c) == self.start or (r, c) == self.goal:
                    continue

                if random.random() < density:
                    self.grid[r][c] = Grid.WALL
                else:
                    self.grid[r][c] = Grid.EMPTY

    def get_neighbors(self, node):

        r, c = node
        neighbors = []

        directions = [
            (-1, 0),  # up
            (1, 0),   # down
            (0, -1),  # left
            (0, 1)    # right
        ]

        for dr, dc in directions:

            nr = r + dr
            nc = c + dc

            if self.check_valid_position(nr, nc):

                if self.grid[nr][nc] != Grid.WALL:
                    neighbors.append((nr, nc))

        return neighbors

    def clear_grid(self):

        self.grid = np.zeros((self.rows, self.cols))
        self.start = None
        self.goal = None


if __name__ == "__main__":

    g = Grid(4, 5)

    g.set_start(0, 0)
    g.set_goal(3, 4)

    g.set_wall(1, 1)
    g.set_wall(2, 2)

    g.random_obstacles(0.2)

    print("Grid:")
    print(g.grid)

    print("Neighbors of (1,2):")
    print(g.get_neighbors((1, 2)))