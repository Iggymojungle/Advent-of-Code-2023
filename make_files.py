import os
import pathlib

YEAR = "2023"
DAY_PLACEHOLDER = "DAY_GOES_HERE"
TEMPLATE = f'''import os
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
        input_data = get_input.get_input({YEAR}, {DAY_PLACEHOLDER})
        with open(DATA, "w") as f:
            f.write(input_data.strip("\\n"))
    with open(DATA, "r") as f:
        data = f.read()
    return data
            

def part1(data):
    return None


def part2(data):
    return None


def main():
    start = time.perf_counter()

    data = get_data()
    print("Part 1:", part1(data))

    data = get_data()
    print("Part 2:", part2(data))
    
    end = time.perf_counter()
    print(f"Time to run: {{end-start:.3f}}")    

    
if __name__ == "__main__":
    main()

'''
REMAKE_OVERRIDE = False


folders = [i for i in pathlib.Path(os.getcwd()).iterdir() if i.is_dir() and ("Day" in str(i))]


for num, folder in enumerate(folders):
    os.chdir(folder)
    if "main.py" not in os.listdir() or REMAKE_OVERRIDE:
        with open("main.py", "w") as f:
            f.write(TEMPLATE.replace(DAY_PLACEHOLDER, str(num+1)))