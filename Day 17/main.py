import os
import sys
import time


DATA = "data.txt"
DIRECTIONS = [
    [0, 1],
    [0, -1],
    [1, 0],
    [-1, 0],
]


def get_data():
    os.chdir(os.path.dirname(__file__))
    if DATA not in os.listdir():
        test_dir = os.path.dirname(__file__)
        module_dir = os.path.dirname(test_dir)
        src_dir = os.path.join(module_dir, "get_input")
        sys.path.insert(0, src_dir)
        import get_input
        input_data = get_input.get_input(2023, 17)
        with open(DATA, "w") as f:
            f.write(input_data.strip("\n"))
    with open(DATA, "r") as f:
        data = f.read()
    return data
            

class Node:
    def __init__(self, position, value, direction, grid):
        self.position = position
        self.connections = [[position[0] + direction[0], position[1] + direction[1]] for direction in DIRECTIONS if (0 <= position[0] + direction[0] < len(grid)) and (0 <= position[1] + direction[1] < len(grid[0]))]
        self.value = value
        self.direction_from = None
        self.num_in_direction = 0
        self.last_node = None
        self.distance_to = None
        self.final = False
    
    def __repr__(self) -> str:
        return str(self.direction_from) + str(self.num_in_direction)
        


def part1(data):
    data = data.split("\n")
    node_grid = [[{tuple(direction) : [Node([posy, posx], int(data[posy][posx]), direction, data) for _ in range(3)] for direction in DIRECTIONS} for posx in range(len(data[posy]))] for posy in range(len(data))]
    node_grid[0][0][(0, 1)][0].distance_to = 0
    to_visit = [node_grid[0][0][(0, 1)][0]]
    visited = set()
    while to_visit:
        to_visit = sorted(to_visit, key = lambda i : i.distance_to)
        current_node = to_visit.pop(0)
        current_node.final = True
        visited.add(current_node)
        for connection in current_node.connections:
            dir_from = (connection[0] - current_node.position[0], connection[1] - current_node.position[1])
            #print(dir_from)
            if current_node.direction_from is not None:
                if list(dir_from) == [i*-1 for i in current_node.direction_from]: # No doubling back!
                    continue
            if list(dir_from) == current_node.direction_from:
                new_amount = current_node.num_in_direction + 1
                if new_amount >= 3:
                    continue
            else:
                new_amount = 0
            connecting_node = node_grid[connection[0]][connection[1]][dir_from][new_amount]
            if connecting_node not in visited and connecting_node not in to_visit and not (dir_from == current_node.direction_from and current_node.num_in_direction >= 2):
                connecting_node.distance_to = current_node.distance_to + connecting_node.value
                connecting_node.last_node = current_node
                connecting_node.direction_from = [connecting_node.position[0] - current_node.position[0], connecting_node.position[1] - current_node.position[1]]
                if connecting_node.direction_from == current_node.direction_from:
                    connecting_node.num_in_direction = current_node.num_in_direction + 1
                else:
                    connecting_node.num_in_direction = 0
                to_visit.append(connecting_node)
            
            elif connecting_node in to_visit:
                original = connecting_node.distance_to
                connecting_node.distance_to = min([connecting_node.distance_to, current_node.distance_to + connecting_node.value])
                if connecting_node.distance_to != original:
                    original_direction = current_node.direction_from
                    connecting_node.direction_from = [connecting_node.position[0] - current_node.position[0], connecting_node.position[1] - current_node.position[1]]
                    if connecting_node.direction_from == current_node.direction_from:
                        if current_node.num_in_direction >= 2:
                            connecting_node.distance_to = original
                            current_node.direction_from = original_direction
                        else:
                            connecting_node.num_in_direction = current_node.num_in_direction + 1
                            connecting_node.last_node = current_node
                    else:
                        connecting_node.num_in_direction = 0
                        connecting_node.last_node = current_node
                    
    final_nodes = []
    final_distances = []
    for direction in node_grid[-1][-1]:
        for node in node_grid[-1][-1][direction]:
            if node.distance_to is not None:
                final_nodes.append(node)
                final_distances.append(node.distance_to)
    for current_node in final_nodes:
        final_visited = []
        while current_node is not None:
            final_visited.append(current_node)
            current_node = current_node.last_node
        for line in node_grid:
            for position in line:
                node_in = False
                for direction in position:
                    for node in position[direction]:
                        if node in final_visited:
                            node_in = True
    return min(final_distances)




     


def part2(data):
    data = data.split("\n")
    node_grid = [[{tuple(direction) : [Node([posy, posx], int(data[posy][posx]), direction, data) for _ in range(10)] for direction in DIRECTIONS} for posx in range(len(data[posy]))] for posy in range(len(data))]
    node_grid[0][0][(0, 1)][0].distance_to = 0
    to_visit = [node_grid[0][0][(0, 1)][0]]
    visited = set()
    while to_visit:
        if len(visited) % 1000 == 0:
            print("Progress: " + str(len(visited)))
        to_visit = sorted(to_visit, key = lambda i : i.distance_to) # TODO Implement insertion sort instead of this
        current_node = to_visit.pop(0)
        current_node.final = True
        visited.add(current_node)
        for connection in current_node.connections:
            dir_from = (connection[0] - current_node.position[0], connection[1] - current_node.position[1])
            if current_node.direction_from is not None:
                if list(dir_from) == [i*-1 for i in current_node.direction_from]: # No doubling back!
                    continue
            if list(dir_from) == current_node.direction_from or (current_node.position == [0, 0] and current_node.last_node is None):
                new_amount = current_node.num_in_direction + 1
                if new_amount >= 10:
                    continue
            else:
                if current_node.num_in_direction < 3:
                    continue
                new_amount = 0
            connecting_node = node_grid[connection[0]][connection[1]][dir_from][new_amount]
            if connecting_node not in visited and connecting_node not in to_visit and not (dir_from == current_node.direction_from and current_node.num_in_direction >= 9):
                connecting_node.distance_to = current_node.distance_to + connecting_node.value
                connecting_node.last_node = current_node
                connecting_node.direction_from = [connecting_node.position[0] - current_node.position[0], connecting_node.position[1] - current_node.position[1]]
                if connecting_node.direction_from == current_node.direction_from:
                    connecting_node.num_in_direction = current_node.num_in_direction + 1
                else:
                    connecting_node.num_in_direction = 0
                to_visit.append(connecting_node)
            
            elif connecting_node in to_visit:
                original = connecting_node.distance_to
                connecting_node.distance_to = min([connecting_node.distance_to, current_node.distance_to + connecting_node.value])
                if connecting_node.distance_to != original:
                    original_direction = current_node.direction_from
                    connecting_node.direction_from = [connecting_node.position[0] - current_node.position[0], connecting_node.position[1] - current_node.position[1]]
                    if connecting_node.direction_from == current_node.direction_from:
                        if current_node.num_in_direction >= 9:
                            connecting_node.distance_to = original
                            current_node.direction_from = original_direction
                        else:
                            connecting_node.num_in_direction = current_node.num_in_direction + 1
                            connecting_node.last_node = current_node
                    else:
                        connecting_node.num_in_direction = 0
                        connecting_node.last_node = current_node
                    
    final_nodes = []
    final_distances = []
    for direction in node_grid[-1][-1]:
        for node in node_grid[-1][-1][direction]:
            if node.distance_to is not None:
                final_nodes.append(node)
                final_distances.append(node.distance_to)
    for current_node in final_nodes:
        final_visited = []
        while current_node is not None:
            final_visited.append(current_node)
            current_node = current_node.last_node
        for line in node_grid:
            for position in line:
                node_in = False
                for direction in position:
                    for node in position[direction]:
                        if node in final_visited:
                            node_in = True
    return min(final_distances)


def main():
    start = time.perf_counter()

    data = get_data()
    print("Part 1:", part1(data))

    data = get_data()
    print("Part 2:", part2(data))
    
    end = time.perf_counter()
    print(f"Time to run: {end-start:.3f}")    

    
if __name__ == "__main__":
    main()

