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
        input_data = get_input.get_input(2023, 10)
        with open(DATA, "w") as f:
            f.write(input_data.strip("\n"))
    with open(DATA, "r") as f:
        data = f.read()
    return data
            

PIPES = {
    "|" : [0, 2],
    "-" : [1, 3],
    "L" : [0, 1],
    "J" : [0, 3],
    "7" : [2, 3],
    "F" : [1, 2],
}


DIRECTIONS = [
    [-1, 0],
    [0, 1],
    [1, 0],
    [0, -1],
]


s_directions = []


def part1(data):
    data = data.split("\n")
    start = None
    for linenum, line in enumerate(data):
        for chrnum, character in enumerate(line):
            if character == "S":
                start = [linenum, chrnum]
                break
        if start:
            break
    current_pos = []
    #print(start)
    # May be error if S at 0, thus -1
    if start[1] - 1 >= 0:
        if data[start[0]][start[1]-1] in ["-", "L", "F"]:
            s_directions.append("left")
            current_pos.append([start[0],start[1]-1])
    if start[1] + 1 < len(data[0]):
        if data[start[0]][start[1]+1] in ["-", "J", "7"]:
            s_directions.append("right")
            current_pos.append([start[0],start[1]+1])
    if start[0] + 1 < len(data):
        if data[start[0]+1][start[1]] in ["|", "J", "L"]:
            s_directions.append("down")
            current_pos.append([start[0]+1,start[1]])
    if start[0] - 1 >= 0:
        if data[start[0]-1][start[1]] in ["|", "F", "7"]:
            s_directions.append("up")
            current_pos.append([start[0]-1,start[1]])
    #print(f"{current_pos=}")
    if len(current_pos) != 2:
        raise Exception("Not the right amount of starting positions")


    visited = [list(start), current_pos[0], current_pos[1]]
    done = False
    steps = 0
    while not done:
        steps += 1
        for pos_num, pos in enumerate(current_pos):
            pipe_type = data[pos[0]][pos[1]]
            some_visited = False
            for directions in PIPES[pipe_type]:
                new_location = [pos[0] + DIRECTIONS[directions][0], pos[1] + DIRECTIONS[directions][1]]
                if new_location not in visited:
                    visited.append(new_location)
                    current_pos[pos_num] = new_location
                    some_visited = True
            if not some_visited:
                done = True
    return steps + 1, visited


def extendright(index, grid):
    for line in grid:
        if line[index] in "7-J" or (line[index] == "S" and "left" in s_directions):
            line.insert(index, "-")
        else:
            line.insert(index, ".")
    return grid


def rightshift(grid):
    for i in range(len(grid[0])-1,0,-1):
        grid = extendright(i, grid)
    return grid


def extenddown(index, grid):
    grid = [list(line) for line in list(zip(*grid))]
    for line in grid:
        if line[index] in "L|J"  or (line[index] == "S" and "up" in s_directions):
            line.insert(index, "|")
        else:
            line.insert(index, ".")
    return [list(line) for line in list(zip(*grid))]


def downshift(grid):
    for i in range(len(grid)-1,0,-1):
        grid = extenddown(i, grid)
    return grid


def collapse(grid):
    original_len = (len(grid)+1)/2
    current_pos = 0
    while len(grid) > original_len:
        current_pos += 1
        grid.pop(current_pos)
    return grid


def floodfill(grid, start_pos):
    visited = [start_pos]
    queue = [start_pos]
    edge = False
    while queue:
        current = queue.pop(0)
        for direction in DIRECTIONS:
            cell = [current[0] + direction[0], current[1] + direction[1]] 
            if not (cell[0] < 0 or cell[0] >= len(grid) or cell[1] < 0 or cell[1] >= len(grid[0])):
                if cell not in visited:
                    if grid[cell[0]][cell[1]] == ".":
                        visited.append(cell)
                        queue.append(cell)
                        if cell[0] in [0, len(grid)-1] or cell[1] in [0, len(grid[0])-1]:
                            edge = True
    for position in visited:
        if edge:
            grid[position[0]][position[1]] = "O"
        else:
            grid[position[0]][position[1]] = "I"
    return grid



def part2(data, visited):
    grid = list(map(list, data.split("\n")))
    for linenum, line in enumerate(grid):
        for chrnum, character in enumerate(line):
            if [linenum, chrnum] not in visited:
                grid[linenum][chrnum] = "."

    grid = rightshift(grid)
    grid = downshift(grid)

    filled = False
    while not filled:
        filled = True
        for linenum, line in enumerate(grid):
            if "." in line:
                filled = False
                grid = floodfill(grid, [linenum, line.index(".")])
    
    grid = collapse(grid)
    grid = list(zip(*collapse(list(zip(*grid)))))
    total = 0
    for line in grid:
        for letter in line:
            if letter == "I":
                total += 1
    return total


def main():
    start = time.perf_counter()

    data = get_data()
    part1_answer, visited = part1(data)
    print("Part 1:", part1_answer)

    data = get_data()
    print("Part 2:", part2(data, visited))
    
    end = time.perf_counter()
    print(f"Time to run: {end-start:.3f}")    

    
if __name__ == "__main__":
    main()

