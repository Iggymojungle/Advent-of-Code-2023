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
        input_data = get_input.get_input(2023, 9)
        with open(DATA, "w") as f:
            f.write(input_data.strip("\n"))
    with open(DATA, "r") as f:
        data = f.read()
    return data


def recursive_sequence_p1(line):
    if all([i == 0 for i in line]):
        return 0
    return line[-1] + recursive_sequence_p1([line[i+1]-line[i] for i in range(len(line)-1)])
    

def recursive_sequence_p2(line):
    if all([i == 0 for i in line]):
        return 0
    return line[0] - recursive_sequence_p2([line[i+1]-line[i] for i in range(len(line)-1)])


def part1(data):
    data = [[int(num) for num in line.split(" ")] for line in data.split("\n")]
    total = 0
    for line in data:
        total += recursive_sequence_p1(line)
    return total


def part2(data):
    data = [[int(num) for num in line.split(" ")] for line in data.split("\n")]
    total = 0
    for line in data:
        total += recursive_sequence_p2(line)
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

