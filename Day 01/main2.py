import os
import time
import sys

DATA = "data.txt"

def get_data():
    os.chdir(os.path.dirname(__file__))
    if DATA not in os.listdir():
        test_dir = os.path.dirname(__file__)
        module_dir = os.path.dirname(test_dir)
        src_dir = os.path.join(module_dir, "get_input")
        sys.path.insert(0, src_dir)
        import get_input
        input_data = get_input.get_input(2023, 1)
        with open(DATA, "w") as f:
            f.write(input_data.strip("\n"))
    with open(DATA, "r") as f:
        data = f.read()
    return data

def part1():
    data = [d for d in get_data().split("\n")]
    removablecharacters = "abcdefghijklmnopqrstuvwxyz"
    for i, d in enumerate(data):
        #print(d)
        for char in removablecharacters:
            d = d.replace(char, '')
        #print(d)
        data[i] = int(d[0] + d[-1])
    #print(data)
    print(sum(data))

def part2():
    data = [d for d in get_data().split("\n")]
    removablecharacters = "abcdefghijklmnopqrstuvwxyz"
    numbers = ['1', 'one', '2', 'two', '3', 'three', '4', 'four', '5', 'five', '6', 'six', '7', 'seven', '8', 'eight', '9', 'nine']
    decode = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9
    }
    for i, d in enumerate(data):
        foundnumbers = []
        for j in range(len(d)):
            for k in range(j+1):
                segment = d[k:j+1]
                if segment in numbers:
                    foundnumbers.append(segment)
        decodefunc = lambda x: x if x.isnumeric() else decode[x]
        output = int(str(decodefunc(foundnumbers[0])) + str(decodefunc(foundnumbers[-1])))
        data[i] = output
    print(sum(data))

def main():
    start = time.perf_counter()
    part1()
    part2()
    end = time.perf_counter()
    print(f"Time to run: {end-start:.3f}")  
    
    
if __name__ == "__main__":
    main()