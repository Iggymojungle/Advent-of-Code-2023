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
        input_data = get_input.get_input(2023, 4)
        with open(DATA, "w") as f:
            f.write(input_data.strip("\n"))
    with open(DATA, "r") as f:
        data = f.read()
    return data
            

def part1(data):
    return int(sum([2 ** (len(i)-len(set(i)) - 1)//1 for i in [j[j.index(":")+1:].replace(" |", "").replace("  "," ").split(" ") for j in data.split("\n")]]))


def recursive_p2(data, total):
    total += data[0]
    for i in range(data[0]):
        total = recursive_p2(data[i+1:], total)
    return total


def part2(data):
    data = [(len(i)-len(set(i)))//1 for i in [j[j.index(":")+1:].replace(" |", "").replace("  "," ").split(" ") for j in data.split("\n")]]
    data.insert(0, len(data))
    return recursive_p2(data, 0)


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

