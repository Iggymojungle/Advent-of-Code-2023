import os
import sys
import time


DATA = "data.txt"

words_to_numbers = {"one":"1",
                    "two":"2",
                    "three":"3",
                    "four":"4",
                    "five":"5",
                    "six":"6",
                    "seven":"7",
                    "eight":"8",
                    "nine":"9",}


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
            

def convert(line, direction):
    in_line = []
    for word in words_to_numbers:
        if word in line:
            in_line.append(word)
    if direction:
        in_line = sorted(in_line, key=lambda word:line.index(word))
    if not direction:
        in_line = sorted(in_line, key=lambda word:line[::-1].index(word[::-1]))
    for word in in_line:
        line = line.replace(word, words_to_numbers[word])
    return line


def part1(data):
    data = [[j for j in i if j.isnumeric()] for i in data.split("\n")]
    data = [[i[0],i[-1]] for i in data]
    return str(sum([int("".join(i)) for i in data]))


def part2(data):
    data = data.split("\n")
    data_forward = [[j for j in convert(i, True) if j.isnumeric()] for i in data]
    data_backward = [[j for j in convert(i, False) if j.isnumeric()] for i in data]
    data_end = [[data_forward[i][0],data_backward[i][-1]] for i in range(len(data))]
    return str(sum([int("".join(i)) for i in data_end]))


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
