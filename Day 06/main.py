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


def part1(data):
    data = prepare_data_p1(data)
    times = data[0]
    distances = data[1]
    total = 1
    for timenum, time in enumerate(times):
        timetotal = 0
        for i in range(time):
            if i*(time-i) > distances[timenum]:
                timetotal += 1
        total *= timetotal
    return total


def part2(data):
    data = prepare_data_p2(data)
    time = data[0]
    distance = data[1]
    min = None
    max = None
    for i in range(time):
        if i*(time-i) > distance:
            min=i
            break
    for i in range(time,0,-1):
        if i*(time-i) > distance:
            max=i
            break
    return max-min+1


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

