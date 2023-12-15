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
        input_data = get_input.get_input(2023, 15)
        with open(DATA, "w") as f:
            f.write(input_data.strip("\n"))
    with open(DATA, "r") as f:
        data = f.read()
    return data
            

def hash(string):
    current = 0
    for letter in string:
        current += ord(letter)
        current *= 17
        current %= 256
    return current


def part1(data):
    data = data.split(",")
    total = 0
    for string in data:
        total += hash(string)
    return total


def part2(data):
    data = data.split(",")
    for thing_num, thing in enumerate(data):
        if "=" in thing:
            data[thing_num] = thing.split("=")
        else:
            data[thing_num] = [thing.split("-")[0]]
            
    boxes = [{} for _ in range(256)]
    for instruction in data:
        position = hash(instruction[0])
        if len(instruction) == 2:
            boxes[position][instruction[0]] = instruction[1]
        elif len(instruction) == 1:
            boxes[position][instruction[0]] = ""
            del boxes[position][instruction[0]]
        
    total = 0
    for box_num, box in enumerate(boxes):
        for lens_num, lens in enumerate(box):
            total += (box_num + 1) * (lens_num + 1) * int(box[lens])
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

