import os
import sys

def get_data():
    os.chdir(os.path.dirname(__file__))
    if "data.txt" not in os.listdir():
        test_dir = os.path.dirname(__file__)
        module_dir = os.path.dirname(test_dir)
        src_dir = os.path.join(module_dir, "get_input")
        sys.path.insert(0, src_dir)
        import get_input
        input_data = get_input.get_input(2023, 16)
        with open("data.txt", "w") as f:
            f.write(input_data.strip("\n"))
    with open("data.txt", "r") as f:
        data = f.read()
    return data
            

def main():
    data = get_data()
    

if __name__ == "__main__":
    main()
