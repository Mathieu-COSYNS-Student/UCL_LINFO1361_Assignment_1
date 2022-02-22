"""
Name of the author(s):
- Louis Navarre <louis.navarre@uclouvain.be>
"""
import time
import sys
from search import *
import collections


#################
# Problem class #
#################
class Rubik2D(Problem):

    def actions(self, state):
        for i in range(0, state.shape[0]):
            for j in range(1, state.shape[1]):
                action = ("go_right", i, j)
                yield action

        for i in range(0, state.shape[1]):
            for j in range(1, state.shape[0]):
                action = ("go_down", i, j)
                yield action

    def result(self, state, action):

        if action[0] == "go_right":
            grid = list(state.grid)
            row_id = action[1]
            step = action[2]

            row = collections.deque(state.grid[row_id])
            row.rotate(step)

            grid[row_id] = tuple(row)

            new_state = State(state.shape, tuple(
                grid), move=f"Row #{row_id} right {step}")

            return new_state

        elif action[0] == "go_down":
            grid = list(state.grid)
            column_id = action[1]
            step = action[2]

            column = collections.deque()

            for i in range(0, state.shape[1]):
                column.append(grid[i][column_id])

            column.rotate(step)

            for i in range(0, state.shape[1]):
                row = list(grid[i])
                row[column_id] = column[i]
                grid[i] = tuple(row)

            new_state = State(state.shape, tuple(
                grid), move=f"Col #{column_id} down {step}")

            return new_state

    def goal_test(self, state):
        return state.grid == self.goal


###############
# State class #
###############
class State:

    def __init__(self, shape, grid, move="Init"):
        self.shape = shape
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

    init_state = State(shape, tuple(initial_grid), "Init")
    problem = Rubik2D(init_state, tuple(goal_grid))

    # Example of search
    start_timer = time.perf_counter()
    node, nb_explored, remaining_nodes = depth_limited_search(problem)
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
