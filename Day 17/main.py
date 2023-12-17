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
    def __init__(self, position, value, grid):
        self.position = position
        self.connections = [[position[0] + direction[0], position[1] + direction[1]] for direction in DIRECTIONS if (0 <= position[0] + direction[0] < len(grid)) and (0 <= position[1] + direction[1] < len(grid[0]))]
        self.value = value
        #self.last_node = {1:None, 2:None, 3:None}
        #self.distance_to = {1:None, 2:None, 3:None}
        self.direction_from = None
        self.num_in_direction = 0
        self.last_node = None
        self.distance_to = None
        self.final = False
    
    def __repr__(self) -> str:
        #return str(self.position) + " " + str(self.value)
        return str(self.direction_from) + str(self.num_in_direction)
    
    #def __str__(self) -> str:
        #return str(self.position)
        


def part1(data):
    data = data.split("\n")
    node_grid = [[Node([posy, posx], int(data[posy][posx]), data) for posx in range(len(data[posy]))] for posy in range(len(data))]
    node_grid[0][0].distance_to = 0
    to_visit = [node_grid[0][0]]
    visited = []
    while to_visit:
        to_visit = sorted(to_visit, key = lambda i : i.distance_to)
        current_node = to_visit.pop(0)
        current_node.final = True
        visited.append(current_node)
        for connection in current_node.connections:
            
            connecting_node = node_grid[connection[0]][connection[1]]
            dir_from = [connecting_node.position[0] - current_node.position[0], connecting_node.position[1] - current_node.position[1]]
            if connecting_node not in visited and connecting_node not in to_visit and not (dir_from == current_node.direction_from and current_node.num_in_direction > 1):
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
                        if current_node.num_in_direction > 1:
                            connecting_node.distance_to = original
                            current_node.direction_from = original_direction
                        else:
                            connecting_node.num_in_direction = current_node.num_in_direction + 1
                            connecting_node.last_node = current_node
                    else:
                        connecting_node.num_in_direction = 0
                        connecting_node.last_node = current_node
                    
    final_visited = []
    current_node = node_grid[-1][-1]
    while current_node is not None:
        final_visited.append(current_node)
        current_node = current_node.last_node
    for line in node_grid:
        for node in line:
            if node in final_visited:
                print("#",end="")
            else:
                print(".",end="")
        print()
    return node_grid[-1][-1].distance_to




     


def part2(data):
    return None


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

