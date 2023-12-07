import os
import sys
import time
import math


DATA = "data.txt"


def get_data():
    os.chdir(os.path.dirname(__file__))
    if DATA not in os.listdir():
        test_dir = os.path.dirname(__file__)
        module_dir = os.path.dirname(test_dir)
        src_dir = os.path.join(module_dir, "get_input")
        sys.path.insert(0, src_dir)
        import get_input
        input_data = get_input.get_input(2023, 6)
        with open(DATA, "w") as f:
            f.write(input_data.strip("\n"))
    with open(DATA, "r") as f:
        data = f.read()
    return data
            

def prepare_data_p1(data):
    return [[int(j) for j in i.split(" ") if j.isnumeric()] for i in data.split("\n")]


def prepare_data_p2(data):
    return [int("".join([j for j in i.split(" ") if j.isnumeric()])) for i in data.split("\n")]


def quadratic_calculate(time, distance):
    higher = (time + (time ** 2 - 4 * distance)**(1/2))/2
    lower = (time - (time ** 2 - 4 * distance)**(1/2))/2
    if higher//1 == higher:
        higher -= 1
    if lower//1 == lower:
        lower += 1
    return math.floor(higher) - math.ceil(lower) + 1


def part1(data):
    data = prepare_data_p1(data)
    times = data[0]
    distances = data[1]
    total = 1
    for timenum, time in enumerate(times):
        total *= quadratic_calculate(time, distances[timenum])
    return int(total)


def part2(data):
    data = prepare_data_p2(data)
    time = data[0]
    distance = data[1]
    return int(quadratic_calculate(time, distance))


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

