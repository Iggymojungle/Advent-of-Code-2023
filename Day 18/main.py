import os
import sys
import time


DATA = "data.txt"
DIRECTIONS = {
    "U" : [-1, 0],
    "R" : [0, 1],
    "L" : [0, -1],
    "D" : [1, 0]
}
DIRECTION_NUMS = ["R", "D", "L", "U"]


def get_data():
    os.chdir(os.path.dirname(__file__))
    if DATA not in os.listdir():
        test_dir = os.path.dirname(__file__)
        module_dir = os.path.dirname(test_dir)
        src_dir = os.path.join(module_dir, "get_input")
        sys.path.insert(0, src_dir)
        import get_input
        input_data = get_input.get_input(2023, 18)
        with open(DATA, "w") as f:
            f.write(input_data.strip("\n"))
    with open(DATA, "r") as f:
        data = f.read()
    return data


def floodfill(grid, start_pos):
    visited = set([tuple(start_pos)])
    queue = [start_pos]
    edge = False
    while queue:
        current = queue.pop(0)
        for direction in DIRECTIONS.values():
            cell = [current[0] + direction[0], current[1] + direction[1]] 
            if not (cell[0] < 0 or cell[0] >= len(grid) or cell[1] < 0 or cell[1] >= len(grid[0])):
                if tuple(cell) not in visited:
                    if grid[cell[0]][cell[1]] == ".":
                        visited.add(tuple(cell))
                        queue.append(cell)
                        if cell[0] in [0, len(grid)-1] or cell[1] in [0, len(grid[0])-1]:
                            edge = True
    for position in visited:
        if edge:
            grid[position[0]][position[1]] = "O"
        else:
            grid[position[0]][position[1]] = "#"
    return grid


def part1(data):
    data = [[i.split(" ")[0], int(i.split(" ")[1])] for i in data.split("\n")]
    position = [0, 0]
    dug = set([tuple(position)])
    for instruction in data:
        for _ in range(instruction[1]):
            position[0] += DIRECTIONS[instruction[0]][0]
            position[1] += DIRECTIONS[instruction[0]][1]
            dug.add(tuple(position))
    max_height = max([i[0] for i in dug]) + 1
    max_length = max([i[1] for i in dug]) + 1
    min_height = min([i[0] for i in dug])
    min_length = min([i[1] for i in dug])
    grid = [["." for _ in range(max_length - min_length)] for _ in range(max_height - min_height)]
    for long in range(min_height, max_height):
        for down in range(min_length, max_length):
            if tuple([long, down]) in dug:
                grid[long-min_height][down-min_length] = "#"
            else:
                grid[long-min_height][down-min_length] = "."
    while "." in "".join(["".join(line) for line in grid]):
        for linenum, line in enumerate(grid):
            if "." in line:
                grid = floodfill(grid, [linenum, line.index(".")])
                break
    total = 0
    for line in grid:
        total += line.count("#")
    return total
        

def shoelace(vertices):
  #A function to apply the Shoelace algorithm
  numberOfVertices = len(vertices)
  sum1 = 0
  sum2 = 0
  
  for i in range(numberOfVertices-1):
    sum1 = sum1 + vertices[i][0] * vertices[i+1][1]
    sum2 = sum2 + vertices[i][1] * vertices[i+1][0]
  
  #Add xn.y1
  sum1 = sum1 + vertices[numberOfVertices-1][0]*vertices[0][1]   
  #Add x1.yn
  sum2 = sum2 + vertices[0][0]*vertices[numberOfVertices-1][1]   
  
  area = abs(sum1 - sum2) / 2
  return area
   


def part2(data):
    data = [i.split(" ")[2] for i in data.split("\n")]
    data = [[DIRECTION_NUMS[int(i[7])], int(i[2:7], 16)] for i in data]
    position = [0, 0]
    corners = [list(position)]
    for line in data:
        position[0] += line[1] * DIRECTIONS[line[0]][0]
        position[1] += line[1] * DIRECTIONS[line[0]][1]
        corners.append(list(position))
    area = shoelace(corners)
    perimeter = 0
    for corner_num, corner in enumerate(corners[:-1]):
        perimeter += abs(corners[corner_num + 1][0] - corner[0])
        perimeter += abs(corners[corner_num + 1][1] - corner[1])
    area += perimeter / 2
    area += 1
    return int(area)
    


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

