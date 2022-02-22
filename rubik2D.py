"""
Name of the author(s):
- Louis Navarre <louis.navarre@uclouvain.be>
"""
import time
import sys
from search import *


#################
# Problem class #
#################
class Rubik2D(Problem):

    def actions(self, state):
        next_actions = []

        for i in range(0, state.shape[0]):
            next_actions.append(
                ("go_right", i)
            )

        for i in range(0, state.shape[1]):
            next_actions.append(
                ("go_down", i)
            )

        return next_actions

    def result(self, state, action):

        if action[0] == "go_right":
            grid = list(state.grid)
            row_id = action[1]
            row = list(state.grid[row_id])
            row_len = state.shape[0]
            last = row[row_len-1]

            for i in range(row_len-1, -1, -1):
                row[i] = row[i-1]
            row[0] = last

            grid[row_id] = tuple(row)

            return State(state.shape, tuple(grid), state.answer, move="go_right")

        elif action[0] == "go_down":
            grid = list(state.grid)
            column_id = action[1]
            column_len = state.shape[1]

            last = grid[column_len-1][column_id]

            for i in range(column_len-1, -1, -1):
                grid[i] = list(grid[i])
                grid[i][column_id] = grid[i][column_id-1]
                grid[i] = tuple(grid[i])

            grid[0] = list(grid[0])
            grid[0][column_id] = last
            grid[0] = tuple(grid[0])

            return State(state.shape, tuple(grid), state.answer, move="go_down")

    def goal_test(self, state):
        return state.grid == state.answer


###############
# State class #
###############
class State:

    def __init__(self, shape, grid, answer=None, move="Init"):
        self.shape = shape
        self.answer = answer
        self.grid = grid
        self.move = move

    def __str__(self):
        s = self.move + "\n"
        for line in self.grid:
            s += "".join(line) + "\n"
        return s


def read_instance_file(filepath):
    with open(filepath) as fd:
        lines = fd.read().splitlines()

    shape_x, shape_y = tuple([int(i) for i in lines[0].split(" ")])
    initial_grid = list()
    for row in lines[1:1 + shape_x]:
        initial_grid.append(tuple([i for i in row]))

    goal_grid = list()
    for row in lines[1 + shape_x + 1:]:
        goal_grid.append(tuple([i for i in row]))

    return (shape_x, shape_y), initial_grid, goal_grid


def main():
    if len(sys.argv) != 2:
        print(f"Usage: ./rubik2D.py <path_to_instance_file>", file=sys.stderr)
        return
    filepath = sys.argv[1]

    shape, initial_grid, goal_grid = read_instance_file(filepath)

    init_state = State(shape, tuple(initial_grid), tuple(goal_grid), "Init")
    problem = Rubik2D(init_state)

    # Example of search
    start_timer = time.perf_counter()
    node, nb_explored, remaining_nodes = breadth_first_graph_search(problem)
    end_timer = time.perf_counter()

    # Example of print
    path = node.path()

    for n in path:
        # assuming that the __str__ function of state outputs the correct format
        print(n.state)

    print("* Execution time:\t", str(end_timer - start_timer))
    print("* Path cost to goal:\t", node.depth, "moves")
    print("* #Nodes explored:\t", nb_explored)
    print("* Queue size at goal:\t",  remaining_nodes)


if __name__ == "__main__":
    main()
