import os
import sys
import time
import copy


DATA = "data.txt"
CYCLES = 1000000000


def get_data():
    os.chdir(os.path.dirname(__file__))
    if DATA not in os.listdir():
        test_dir = os.path.dirname(__file__)
        module_dir = os.path.dirname(test_dir)
        src_dir = os.path.join(module_dir, "get_input")
        sys.path.insert(0, src_dir)
        import get_input
        input_data = get_input.get_input(2023, 14)
        with open(DATA, "w") as f:
            f.write(input_data.strip("\n"))
    with open(DATA, "r") as f:
        data = f.read()
    return data


def score(data):
    max = len(data)
    total = 0
    for line_num, line in enumerate(data):
        for character in line:
            if character == "O":
                total += max - line_num
    return total


def tilt_up(data):
    for line_num, line in enumerate(data[1:]): # line_num offset by 1
        for character_num, character in enumerate(line):
            if data[line_num][character_num] == "." and character == "O":
                data[line_num + 1][character_num] = "."
                destination = 0
                while line_num - destination > 0 and data[line_num - (destination + 1)][character_num] == ".":
                    destination += 1
                data[line_num - destination][character_num] = "O"
    return data


def part1(data):
    data = [list(i) for i in data.split("\n")]
    data = tilt_up(data)
    return score(data)


def transpose(grid):
    return [list(i) for i in list(zip(*grid))]


def reverse(grid):
    return list(reversed(grid))


def cycle(data):
    data = tilt_up(data)
    data = transpose(tilt_up(transpose(data)))
    data = reverse(tilt_up(reverse(data)))
    return transpose(reverse(tilt_up(reverse(transpose(data)))))


def part2(data):
    data = [list(i) for i in data.split("\n")]
    cache = []
    while data not in cache:
        cache.append(copy.deepcopy(data))
        data = cycle(data)

    cycle_start = cache.index(data)
    cycle_length = len(cache) - cycle_start
    time_in_cycle = CYCLES - cycle_start - 1
    grid_index = time_in_cycle % cycle_length + cycle_start
    exact_grid = cache[grid_index + 1]
    return score(exact_grid)


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

