import os
import sys
import time
import copy


DATA = "data.txt"


def get_data():
    os.chdir(os.path.dirname(__file__))
    if DATA not in os.listdir():
        test_dir = os.path.dirname(__file__)
        module_dir = os.path.dirname(test_dir)
        src_dir = os.path.join(module_dir, "get_input")
        sys.path.insert(0, src_dir)
        import get_input
        input_data = get_input.get_input(2023, 13)
        with open(DATA, "w") as f:
            f.write(input_data.strip("\n"))
    with open(DATA, "r") as f:
        data = f.read()
    return data


def check_horizontal(maze):
    for row_num in range(len(maze[:-1])):
        row1 = row_num
        row2 = row_num+1
        symmetrical = False
        while maze[row1] == maze[row2]:
            if row1 == 0 or row2 == len(maze) - 1:
                symmetrical = True
                break
            row1 -= 1
            row2 += 1
        if symmetrical:
            return row_num + 1
    return 0


def check_horizontal_p2(maze, avoid_row):
    for row_num in range(len(maze[:-1])):
        row1 = row_num
        row2 = row_num+1
        symmetrical = False
        while maze[row1] == maze[row2]:
            if (row1 == 0 or row2 == len(maze) - 1) and row_num + 1 != avoid_row:
                symmetrical = True
                break
            elif row1 == 0 or row2 == len(maze) - 1:
                break
            row1 -= 1
            row2 += 1
        if symmetrical:
            return row_num + 1
    return 0


def part1(data):
    data = [[list(j) for j in i.split("\n")] for i in data.split("\n\n")]
    total = 0
    for maze in data:
        horizontal_result = check_horizontal(maze)
        if horizontal_result:
            total += 100 * horizontal_result
        else:
            total += check_horizontal(list(zip(*maze)))
    return total


def part2(data):
    data = [[list(j) for j in i.split("\n")] for i in data.split("\n\n")]
    total = 0
    for maze in data:
        horizontal_result = check_horizontal(maze)
        if horizontal_result:
            original = check_horizontal(maze)
            original_direction = "H"
        else:
            original = check_horizontal(list(zip(*maze)))
            original_direction = "V"
        found = False
        for linenum, line in enumerate(maze):
            for symbolnum, symbol in enumerate(line):
                new_maze = copy.deepcopy(maze)
                if symbol == "#":
                    new_maze[linenum][symbolnum] = "."
                elif symbol == ".":
                    new_maze[linenum][symbolnum] = "#"
                else:
                    raise Exception("Unexpected symbol")
                
                if original_direction == "V":
                    horizontal_result = check_horizontal(new_maze)
                else:
                    horizontal_result = check_horizontal_p2(new_maze, original)
                if horizontal_result and not (original == horizontal_result and original_direction == "H"):
                    total += 100 * horizontal_result
                    found = True 
                    break
                else:
                    if original_direction == "H":
                        vertical_result = check_horizontal(list(zip(*new_maze)))
                    else:
                        vertical_result = check_horizontal_p2(list(zip(*new_maze)), original)
                    if vertical_result and not (original == vertical_result and original_direction == "V"):
                        total += vertical_result
                        found = True
                        break
            if found:
                break
                
    return total


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

