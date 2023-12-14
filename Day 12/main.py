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
        input_data = get_input.get_input(2023, 12)
        with open(DATA, "w") as f:
            f.write(input_data.strip("\n"))
    with open(DATA, "r") as f:
        data = f.read()
    return data
            

def line_count(line):
    current = 0
    count = []
    for character in line:
        if character == "#":
            current += 1
        elif current != 0:
            count.append(current)
            current = 0
    if current != 0:
        count.append(current)
    return count


def brute_force(line):
    total = 0
    picross_bit = list(line[0])
    for num in range(2**picross_bit.count("?")):
        binary_num = str(bin(num))[2:].zfill(picross_bit.count("?"))
        q_num = 0
        new_ver = list(picross_bit)
        for chr_num, character in enumerate(picross_bit):
            if character == "?":
                if binary_num[q_num] == "1":
                    new_ver[chr_num] = "#"
                else:
                    new_ver[chr_num] = "."
                q_num += 1
        if line_count(new_ver) == line[1]:
            total += 1
    return total
                    

def part1(data):
    data = [[line.split(" ")[0],[int(i) for i in line.split(" ")[1].split(",")]] for line in data.split("\n")]
    total = 0
    for line in data:
        total += brute_force(line)
    return total



def part2(data):
    return None


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

