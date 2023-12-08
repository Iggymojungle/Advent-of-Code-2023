import os
import sys
import time
import math

DATA = "data.txt"


def get_data():
    os.chdir(os.path.dirname(__file__))
    if DATA not in os.listdir():
        test_dir = os.path.dirname(__file__)
        module_dir = os.path.dirname(test_dir)
        src_dir = os.path.join(module_dir, "get_input")
        sys.path.insert(0, src_dir)
        import get_input
        input_data = get_input.get_input(2023, 8)
        with open(DATA, "w") as f:
            f.write(input_data.strip("\n"))
    with open(DATA, "r") as f:
        data = f.read()
    return data
            

def part1(data):
    data = data.split("\n\n")
    direction_list = data[0]
    node_graph_str = [[j.split(", ") if len(j) > 1 else j for j in i.replace("(", "").replace(")", "").split(" = ")] for i in data[1].split("\n")]
    node_graph = {}
    for node in node_graph_str:
        node_graph[node[0][0]] = node[1]
    current_node = "AAA"
    step = 0
    while current_node != "ZZZ":
        if direction_list[step % len(direction_list)] == "L":
            current_node = node_graph[current_node][0]
        else:
            current_node = node_graph[current_node][1]
        step += 1
    return step


class Node:
    def __init__(self, starting_node, cycle_list):
        self.starting_node = starting_node
        self.leadup_length = cycle_list.index(cycle_list[-1])
        self.cycle_length = len(cycle_list) - self.leadup_length - 1
        self.z_positions = [pos for pos, i in enumerate(cycle_list) if i[2] == "Z"]
    
    def __repr__(self):
        return f"<{self.starting_node} - Leadup: {self.leadup_length}, Cycle: {self.cycle_length}, Zs: {self.z_positions}>"
        


def part2(data):
    data = data.split("\n\n")
    direction_list = data[0]
    node_graph_str = [[j.split(", ") if len(j) > 1 else j for j in i.replace("(", "").replace(")", "").split(" = ")] for i in data[1].split("\n")]
    node_graph = {}
    for node in node_graph_str:
        node_graph[node[0][0]] = node[1]
    current_nodes = [i for i in node_graph.keys() if i[2] == "A"]
    starting_nodes = list(current_nodes)
    node_cycles = {i:None for i in current_nodes}
    incomplete_cycles = {i:[] for i in current_nodes}
    step = 0
    while not(all([node_cycles[i] is not None for i in starting_nodes])):
        for node_num, current_node in enumerate(current_nodes):
            if node_cycles[starting_nodes[node_num]] is None:
                if direction_list[step % len(direction_list)] == "L": 
                    current_nodes[node_num] = node_graph[current_node][0]
                else:
                    current_nodes[node_num] = node_graph[current_node][1]
                
                if [current_node, step % len(direction_list)] not in incomplete_cycles[starting_nodes[node_num]]:
                    incomplete_cycles[starting_nodes[node_num]].append([current_node, step % len(direction_list)])
                else:
                    node_cycles[starting_nodes[node_num]] = [i[0] for i in incomplete_cycles[starting_nodes[node_num]]] + [current_node]
        step += 1
    node_objects = []
    for node in node_cycles:
        node_objects.append(Node(node, node_cycles[node]))
    z_positions = [node.z_positions[0] for node in node_objects]
    return math.lcm(*z_positions)


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

