import os
import sys
import time


DATA = "data.txt"


def get_data():
    os.chdir(os.path.dirname(__file__))
    if DATA not in os.listdir():
        test_dir = os.path.dirname(__file__)
        module_dir = os.path.dirname(test_dir)
        src_dir = os.path.join(module_dir, "get_input")
        sys.path.insert(0, src_dir)
        import get_input
        input_data = get_input.get_input(2023, 16)
        with open(DATA, "w") as f:
            f.write(input_data.strip("\n"))
    with open(DATA, "r") as f:
        data = f.read()
    return data


def find_energised(grid, position, direction):
    positions = [position]
    directions = [direction]
    visited = set()
    visited_before = 1
    while visited != visited_before:
        to_remove = []
        visited_before = set(visited)
        for pos_num, position in enumerate(positions):
            direction = directions[pos_num]
            if tuple(position + direction) in visited:
                to_remove.append(pos_num)
                continue

            visited.add(tuple(position + direction))

            if grid[position[0]][position[1]] == "\\":
                direction = [direction[i-1] for i in range(len(direction))] # Switch spaces
                directions[pos_num] = direction
                if 0 <= position[0] + direction[0] < len(grid) and 0 <= position[1] + direction[1] < len(grid[0]):
                    positions[pos_num] = [position[0] + direction[0], position[1] + direction[1]]
                else:
                    to_remove.append(pos_num)
            
            elif grid[position[0]][position[1]] == "/":
                direction = [direction[i-1] * -1 for i in range(len(direction))] # Switch spaces and negate
                directions[pos_num] = direction
                if 0 <= position[0] + direction[0] < len(grid) and 0 <= position[1] + direction[1] < len(grid[0]):
                    positions[pos_num] = [position[0] + direction[0], position[1] + direction[1]]
                else:
                    to_remove.append(pos_num)
            
            elif grid[position[0]][position[1]] == "|" and direction[1]:
                to_remove.append(pos_num)
                if 0 <= position[0] - 1:
                    positions.append([position[0] - 1, position[1]])
                    directions.append([-1, 0])
                if position[0] + 1 < len(grid):
                    positions.append([position[0] + 1, position[1]])
                    directions.append([1, 0])

            elif grid[position[0]][position[1]] == "-" and direction[0]:
                to_remove.append(pos_num)
                if 0 <= position[1] - 1:
                    positions.append([position[0], position[1] - 1])
                    directions.append([0, -1])
                if position[1] + 1 < len(grid[0]):
                    positions.append([position[0], position[1] + 1])
                    directions.append([0, 1])

            else:
                if 0 <= position[0] + direction[0] < len(grid) and 0 <= position[1] + direction[1] < len(grid[0]):
                    positions[pos_num] = [position[0] + direction[0], position[1] + direction[1]]
                else:
                    to_remove.append(pos_num)
        positions = [thing for i, thing in enumerate(positions) if i not in to_remove]
        directions = [thing for i, thing in enumerate(directions) if i not in to_remove]
    for position in positions:
        visited.add(tuple(position+direction))
    visited_print = set([tuple([i[0], i[1]]) for i in visited])
    return len(visited_print)


def part1(data):
    grid = data.split("\n")
    position = [0, 0]
    direction = [0, 1]
    return find_energised(grid, position, direction)


def part2(data):
    grid = data.split("\n")
    max_energised = 0
    positions = [[0, i] for i in range(len(grid[0]))]
    direction = [1, 0]
    for position in positions:
        max_energised = max([find_energised(grid, position, direction), max_energised])
    positions = [[i, 0] for i in range(len(grid))]
    direction = [0, 1]
    for position in positions:
        max_energised = max([find_energised(grid, position, direction), max_energised])
    positions = [[i, len(grid[0]) - 1] for i in range(len(grid))]
    direction = [0, -1]
    for position in positions:
        max_energised = max([find_energised(grid, position, direction), max_energised])
    positions = [[len(grid)-1, i] for i in range(len(grid[0]))]
    direction = [-1, 0]
    for position in positions:
        max_energised = max([find_energised(grid, position, direction), max_energised])
    return max_energised



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

