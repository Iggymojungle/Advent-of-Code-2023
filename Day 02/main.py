import os
import sys
import time
from collections import defaultdict

DATA = "data.txt"
MAX_RED = 12
MAX_GREEN = 13
MAX_BLUE = 14

def get_data():
    os.chdir(os.path.dirname(__file__))
    if DATA not in os.listdir():
        test_dir = os.path.dirname(__file__)
        module_dir = os.path.dirname(test_dir)
        src_dir = os.path.join(module_dir, "get_input")
        sys.path.insert(0, src_dir)
        import get_input
        input_data = get_input.get_input(2023, 2)
        with open(DATA, "w") as f:
            f.write(input_data.strip("\n"))
    with open(DATA, "r") as f:
        data = f.read()
    return data
            

def prepare_data(data):
    return [[defaultdict(int, {k.split(" ")[1]: int(k.split(" ")[0]) for k in j.split(", ")}) for j in i[i.index(":")+2:].split("; ")] for i in data.split("\n")]


def part1(data):
    total = 0
    data = prepare_data(data)
    for linenum, line in enumerate(data):
        good = True
        for part in line:
            if part["red"] > MAX_RED or part["green"] > MAX_GREEN or part["blue"] > MAX_BLUE:
                good = False
        if good:
            total += linenum + 1
    return total




def part2(data):
    total = 0
    data = prepare_data(data)
    for line in data:
        minimums = {"red" : 0, "green" : 0, "blue" : 0}
        for part in line:
            for colour in minimums:
                if minimums[colour] < part[colour]:
                    minimums[colour] = part[colour]
        total += minimums["red"] * minimums["blue"] * minimums["green"]
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

