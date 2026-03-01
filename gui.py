import tkinter as tk
from tkinter import messagebox
from grid import Grid
from search import SearchEngine
import time


class PathfindingGUI:

    def __init__(self, root):

        self.root = root
        self.root.title("Pathfinding Visualizer")

        self.cell_size = 30

        self.grid = None
        self.search_engine = None

        self.algorithm = None
        self.heuristic = None
        self.obstacle_type = None

        self.start = None
        self.goal = None

        self.algo_buttons = {}
        self.heur_buttons = {}
        self.obs_buttons = {}

        self.create_controls()

        # -------- MAIN LAYOUT --------

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack()

        self.canvas_frame = tk.Frame(self.main_frame)
        self.canvas_frame.pack(side="left")

        self.metrics_frame = tk.Frame(self.main_frame, padx=25)
        self.metrics_frame.pack(side="right", fill="y")

        self.create_metrics_panel()

    # ------------------------------------------------
    # Metrics Dashboard
    # ------------------------------------------------

    def create_metrics_panel(self):

        tk.Label(
            self.metrics_frame,
            text="Metrics Dashboard",
            font=("Segoe UI", 14, "bold")
        ).pack(pady=10)

        self.nodes_label = tk.Label(
            self.metrics_frame,
            text="Nodes Visited: 0",
            font=("Segoe UI", 11)
        )
        self.nodes_label.pack(anchor="w", pady=5)

        self.cost_label = tk.Label(
            self.metrics_frame,
            text="Path Cost: 0",
            font=("Segoe UI", 11)
        )
        self.cost_label.pack(anchor="w", pady=5)

        self.time_label = tk.Label(
            self.metrics_frame,
            text="Execution Time: 0 ms",
            font=("Segoe UI", 11)
        )
        self.time_label.pack(anchor="w", pady=5)

    # ------------------------------------------------
    # Button styling
    # ------------------------------------------------

    def style_button(self, button):

        button.config(
            width=12,
            height=1,
            font=("Segoe UI", 10),
            bg="white",
            relief="flat",
            bd=1
        )

    def select_button(self, group, selected_key):

        for key, button in group.items():

            if key == selected_key:
                button.config(bg="#4A90E2", fg="white")

            else:
                button.config(bg="white", fg="black")

    # ------------------------------------------------
    # Controls
    # ------------------------------------------------

    def create_controls(self):

        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="Grid Size", font=("Segoe UI", 10)).grid(row=0, column=0)

        self.size_entry = tk.Entry(frame, width=5)
        self.size_entry.insert(0, "20")
        self.size_entry.grid(row=0, column=1)

        create_btn = tk.Button(frame, text="Create Grid", command=self.create_grid)
        self.style_button(create_btn)
        create_btn.grid(row=0, column=2, padx=5)

        # Algorithm

        tk.Label(frame, text="Algorithm", font=("Segoe UI", 10)).grid(row=1, column=0)

        btn_astar = tk.Button(frame, text="A*", command=lambda: self.set_algorithm("astar"))
        btn_gbfs = tk.Button(frame, text="Greedy BFS", command=lambda: self.set_algorithm("gbfs"))

        self.style_button(btn_astar)
        self.style_button(btn_gbfs)

        btn_astar.grid(row=1, column=1, padx=5, pady=3)
        btn_gbfs.grid(row=1, column=2, padx=5, pady=3)

        self.algo_buttons["astar"] = btn_astar
        self.algo_buttons["gbfs"] = btn_gbfs

        # Heuristic

        tk.Label(frame, text="Heuristic", font=("Segoe UI", 10)).grid(row=2, column=0)

        btn_man = tk.Button(frame, text="Manhattan", command=lambda: self.set_heuristic("manhattan"))
        btn_euc = tk.Button(frame, text="Euclidean", command=lambda: self.set_heuristic("euclidean"))

        self.style_button(btn_man)
        self.style_button(btn_euc)

        btn_man.grid(row=2, column=1, padx=5, pady=3)
        btn_euc.grid(row=2, column=2, padx=5, pady=3)

        self.heur_buttons["manhattan"] = btn_man
        self.heur_buttons["euclidean"] = btn_euc

        # Obstacles

        tk.Label(frame, text="Obstacles", font=("Segoe UI", 10)).grid(row=3, column=0)

        btn_static = tk.Button(frame, text="Static", command=lambda: self.set_obstacle("static"))
        btn_dynamic = tk.Button(frame, text="Dynamic", command=lambda: self.set_obstacle("dynamic"))

        self.style_button(btn_static)
        self.style_button(btn_dynamic)

        btn_static.grid(row=3, column=1, padx=5, pady=3)
        btn_dynamic.grid(row=3, column=2, padx=5, pady=3)

        self.obs_buttons["static"] = btn_static
        self.obs_buttons["dynamic"] = btn_dynamic

        # Run / Reset

        run_btn = tk.Button(frame, text="Run Search", command=self.run_search)
        reset_btn = tk.Button(frame, text="Reset Grid", command=self.reset_grid)

        self.style_button(run_btn)
        self.style_button(reset_btn)

        run_btn.grid(row=4, column=1, pady=6)
        reset_btn.grid(row=4, column=2)

    # ------------------------------------------------
    # Grid creation
    # ------------------------------------------------

    def create_grid(self):

        size = int(self.size_entry.get())

        self.grid = Grid(size, size)
        self.search_engine = SearchEngine(self.grid)

        canvas_size = size * self.cell_size

        if hasattr(self, "canvas"):
            self.canvas.destroy()

        self.canvas = tk.Canvas(self.canvas_frame, width=canvas_size, height=canvas_size)
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.handle_click)

        self.start = None
        self.goal = None

        self.draw_grid()

    # ------------------------------------------------
    # Draw grid
    # ------------------------------------------------

    def draw_grid(self):

        self.canvas.delete("all")

        for r in range(self.grid.rows):

            for c in range(self.grid.cols):

                x1 = c * self.cell_size
                y1 = r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                color = "white"

                if self.grid.grid[r][c] == self.grid.WALL:
                    color = "black"

                if self.start == (r, c):
                    color = "green"

                if self.goal == (r, c):
                    color = "red"

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

    # ------------------------------------------------
    # Selection
    # ------------------------------------------------

    def set_algorithm(self, algo):

        self.algorithm = algo
        self.select_button(self.algo_buttons, algo)

    def set_heuristic(self, heuristic):

        self.heuristic = heuristic
        self.select_button(self.heur_buttons, heuristic)

    def set_obstacle(self, type):

        self.obstacle_type = type
        self.select_button(self.obs_buttons, type)

    # ------------------------------------------------
    # Mouse click
    # ------------------------------------------------

    def handle_click(self, event):

        col = event.x // self.cell_size
        row = event.y // self.cell_size

        if not self.start:

            self.start = (row, col)
            self.grid.set_start(row, col)

        elif not self.goal:

            self.goal = (row, col)
            self.grid.set_goal(row, col)

        else:

            self.grid.toggle_wall(row, col)

        self.draw_grid()

    # ------------------------------------------------
    # Run search
    # ------------------------------------------------

    def run_search(self):

        if not self.algorithm or not self.heuristic:
            return

        if not self.start or not self.goal:
            return

        # ---------- STATIC OBSTACLE GENERATION ----------
        if self.obstacle_type == "static":

            # Clear previous walls but keep start/goal
            self.grid.clear_grid()

            # Generate random walls
            self.grid.random_obstacles(0.2)

            # Reapply start and goal so they are not overwritten
            self.grid.set_start(*self.start)
            self.grid.set_goal(*self.goal)

            self.draw_grid()
        # ------------------------------------------------

        start_time = time.time()

        if self.algorithm == "astar":
            result = self.search_engine.astar(self.heuristic)
        else:
            result = self.search_engine.gbfs(self.heuristic)

        if result is None or result["path"] is None:
            messagebox.showinfo("Result", "No path found!")
            return

        exec_time = round((time.time() - start_time) * 1000, 2)

        self.animate_search(result["visited"], result["path"], exec_time)
    # ------------------------------------------------
    # Animation
    # ------------------------------------------------

    def animate_search(self, visited, path, exec_time):

        delay = 20

        for i, node in enumerate(visited):

            self.root.after(
                i * delay,
                lambda n=node, count=i + 1: self.draw_visited_live(n, count)
            )

        for i, node in enumerate(path):

            self.root.after(
                len(visited) * delay + i * 40,
                lambda n=node: self.draw_path(n)
            )

        self.root.after(
            len(visited) * delay + len(path) * 40,
            lambda: self.finish_metrics(path, exec_time)
        )

    def draw_visited_live(self, node, count):

        self.nodes_label.config(text=f"Nodes Visited: {count}")

        r, c = node

        if node != self.start and node != self.goal:

            x1 = c * self.cell_size
            y1 = r * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size

            self.canvas.create_rectangle(
                x1, y1, x2, y2,
                fill="lightblue",
                outline="gray"
            )

    def draw_path(self, node):

        r, c = node

        if node != self.start and node != self.goal:

            x1 = c * self.cell_size
            y1 = r * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size

            self.canvas.create_rectangle(
                x1, y1, x2, y2,
                fill="yellow",
                outline="gray"
            )

    def finish_metrics(self, path, exec_time):

        self.cost_label.config(text=f"Path Cost: {len(path)}")
        self.time_label.config(text=f"Execution Time: {exec_time} ms")

    # ------------------------------------------------
    # Reset
    # ------------------------------------------------

    def reset_grid(self):

        if self.grid:
            self.grid.clear_grid()

        self.start = None
        self.goal = None

        self.nodes_label.config(text="Nodes Visited: 0")
        self.cost_label.config(text="Path Cost: 0")
        self.time_label.config(text="Execution Time: 0 ms")

        self.draw_grid()


# ------------------------------------------------

if __name__ == "__main__":

    root = tk.Tk()

    app = PathfindingGUI(root)

    root.mainloop()