import os
import sys
import time
from collections import defaultdict

DATA = "data.txt"


def get_data():
    os.chdir(os.path.dirname(__file__))
    if DATA not in os.listdir():
        test_dir = os.path.dirname(__file__)
        module_dir = os.path.dirname(test_dir)
        src_dir = os.path.join(module_dir, "get_input")
        sys.path.insert(0, src_dir)
        import get_input
        input_data = get_input.get_input(2023, 3)
        with open(DATA, "w") as f:
            f.write(input_data.strip("\n"))
    with open(DATA, "r") as f:
        data = f.read()
    return data
            

DIRECTIONS = [
    [0, -1],
    [0, 1],
    [-1, 0],
    [1, 0],
    [-1, -1],
    [-1, 1],
    [1, -1],
    [1, 1],
]

NOT_SYMBOL = ".1234567890"


def part1(data):
    total = 0
    data = data.split("\n")
    current_num = None
    part_num = False
    for linenum, line in enumerate(data):
        for chrnum, character in enumerate(line):
            if character.isnumeric():
                if current_num is None:
                    current_num = character
                    part_num = False
                else:
                    current_num += character
                
                for direction in DIRECTIONS:
                    if 0 <= linenum + direction[0] < len(data) and 0 <= chrnum + direction[1] < len(line):
                        if data[linenum+direction[0]][chrnum+direction[1]] not in NOT_SYMBOL:
                            part_num = True
            elif current_num is not None:
                if part_num:
                    total += int(current_num)
                current_num = None
                part_num = False
        if part_num:
            total += int(current_num)
        current_num = None
        part_num = False
    return total
            

def part2(data):
    total = 0
    data = data.split("\n")
    current_num = None
    index = None
    gears = defaultdict(int)
    for linenum, line in enumerate(data):
        for chrnum, character in enumerate(line):
            if character.isnumeric():
                if current_num is None:
                    current_num = character
                else:
                    current_num += character
                
                for direction in DIRECTIONS:
                    if 0 <= linenum + direction[0] < len(data) and 0 <= chrnum + direction[1] < len(line):
                        if data[linenum+direction[0]][chrnum+direction[1]] == "*":
                            index = str(linenum+direction[0]) + "," + str(chrnum+direction[1])
                            
            elif current_num is not None:
                if index:
                    if gears[index]:
                        gears[index].append(int(current_num))
                    else:
                        gears[index] = [int(current_num)]
                current_num = None
                index = None
        if index:
            if gears[index]:
                gears[index].append(int(current_num))
            else:
                gears[index] = [int(current_num)]
        current_num = None
        index = None
    for gear in gears.values():
        if len(gear) == 2:
            total += gear[0] * gear[1]
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

