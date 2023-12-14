import os
import sys
import time
import copy

DATA = "data.txt"
EXPANSION_FACTOR = 1_000_000

def get_data():
    os.chdir(os.path.dirname(__file__))
    if DATA not in os.listdir():
        test_dir = os.path.dirname(__file__)
        module_dir = os.path.dirname(test_dir)
        src_dir = os.path.join(module_dir, "get_input")
        sys.path.insert(0, src_dir)
        import get_input
        input_data = get_input.get_input(2023, 11)
        with open(DATA, "w") as f:
            f.write(input_data.strip("\n"))
    with open(DATA, "r") as f:
        data = f.read()
    return data
            

def expand_p1(grid):
    new_grid = copy.deepcopy(grid)
    extras = 0
    for linenum, line in enumerate(grid):
        if "#" not in line:
            new_grid.insert(linenum + extras, "".join(["." for _ in range(len(line))]))
            extras += 1
    return new_grid


def part1(data):
    grid = data.split("\n")
    grid = expand_p1(grid)
    grid = list(map(list, list(zip(*grid))))
    grid = expand_p1(grid)
    grid = list(map(list, list(zip(*grid))))
    galaxies = []
    for linenum, line in enumerate(grid):
        for posnum, thing in enumerate(line):
            if thing == "#":
                galaxies.append([linenum, posnum])
    total = 0
    for galaxy_num, galaxy in enumerate(galaxies):
        for galaxy2 in galaxies[galaxy_num+1:]:
            total += sum([abs(galaxy2[i]-galaxy[i]) for i in range(len(galaxy))])
    return total


def expand_p2(grid):
    new_grid = copy.deepcopy(grid)
    extras = 0
    expanded = []
    for linenum, line in enumerate(grid):
        if "#" not in line:
            new_grid.insert(linenum + extras, "".join(["." for _ in range(len(line))]))
            expanded.append(linenum + extras)
            extras += 1
    return new_grid, expanded


def part2(data):
    grid = data.split("\n")
    grid, expanded_rows = expand_p2(grid)
    grid = list(map(list, list(zip(*grid))))
    grid, expanded_columns = expand_p2(grid)
    grid = list(map(list, list(zip(*grid))))
    galaxies = []
    for linenum, line in enumerate(grid):
        for posnum, thing in enumerate(line):
            if thing == "#":
                galaxies.append([linenum, posnum])
    total = 0
    for galaxy_num, galaxy in enumerate(galaxies):
        for galaxy2 in galaxies[galaxy_num+1:]:
            total += sum([abs(galaxy2[i]-galaxy[i]) for i in range(len(galaxy))])
            for row in expanded_rows:
                if galaxy[0] < row < galaxy2[0] or galaxy2[0] < row < galaxy[0]:
                    total += EXPANSION_FACTOR - 2
            for column in expanded_columns:
                if galaxy[1] < column < galaxy2[1] or galaxy2[1] < column < galaxy[1]:
                    total += EXPANSION_FACTOR - 2
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

