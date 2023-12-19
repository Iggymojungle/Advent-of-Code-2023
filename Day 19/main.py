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
        input_data = get_input.get_input(2023, 19)
        with open(DATA, "w") as f:
            f.write(input_data.strip("\n"))
    with open(DATA, "r") as f:
        data = f.read()
    return data


def run_workflow(workflow, part):
    for rule in workflow:
        rule = str(rule)
        if ":" not in rule:
            return rule
        rule = rule.split(":")
        if "<" in rule[0]:
            rule[0] = rule[0].split("<")
            if part[rule[0][0]] < int(rule[0][1]):
                return rule[1]
        if ">" in rule[0]:
            rule[0] = rule[0].split(">")
            if part[rule[0][0]] > int(rule[0][1]):
                return rule[1]


def part1(data):
    workflows, parts = [i.split("\n") for i in data.split("\n\n")]
    workflows = [i.replace("}", "").split("{") for i in workflows]
    workflows = {i[0]:i[1].split(",") for i in workflows}
    parts = [{i.split("=")[0]:int(i.split("=")[1]) for i in part.replace("{", "").replace("}", "").split(",")} for part in parts]
    total = 0
    for part in parts:
        current_workflow = "in"
        while current_workflow not in ["A", "R"]:
            current_workflow = run_workflow(workflows[current_workflow], part)
        if current_workflow == "A":
            total += sum(list(part.values()))
    return total


def depth_first(workflows, current_workflow, final_possibilities, current_conditions):
    for rule in current_workflow:
        rule = str(rule)
        if ":" not in rule:
            if rule in ["A", "R"]:
                final_possibilities[rule].append(current_conditions)
            else:
                final_possibilities = depth_first(workflows, workflows[rule], final_possibilities, str(current_conditions))
        rule = rule.split(":")
        if "<" in rule[0]:
            if rule[1] in ["A", "R"]:
                final_possibilities[rule[1]].append(str(current_conditions) + "," + rule[0])
            else:
                final_possibilities = depth_first(workflows, workflows[rule[1]], final_possibilities, str(current_conditions) + "," + rule[0])
            rule[0] = rule[0].split("<")
            rule[0][1] = str(int(rule[0][1]) - 1)
            rule[0] = ">".join(rule[0])
            current_conditions += "," + rule[0]
        elif ">" in rule[0]:
            if rule[1] in ["A", "R"]:
                final_possibilities[rule[1]].append(str(current_conditions) + "," + rule[0])
            else:
                final_possibilities = depth_first(workflows, workflows[rule[1]], final_possibilities, str(current_conditions) + "," + rule[0])
            rule[0] = rule[0].split(">")
            rule[0][1] = str(int(rule[0][1]) + 1)
            rule[0] = "<".join(rule[0])
            current_conditions += "," + rule[0]
    return final_possibilities


def range_intersect(r1, r2):
    return range(max(r1.start,r2.start), min(r1.stop,r2.stop)) or None


def part2(data):
    workflows = data.split("\n\n")[0].split("\n")
    workflows = [i.replace("}", "").split("{") for i in workflows]
    workflows = {i[0]:i[1].split(",") for i in workflows}
    # depth first search through each condition to find all possibilities for A or R
    final_possibilities = {"A":[], "R":[]}
    final_possibilities = depth_first(workflows, workflows["in"], final_possibilities, "")
    final_possibilities = {i:[j.strip(",").split(",") for j in final_possibilities[i]] for i in final_possibilities}
    total = 0
    final_ranges = []
    for possibility in final_possibilities["A"]:
        ranges = {"x":[], "m":[], "a":[], "s":[]}
        for condition in possibility:
            if ">" in condition:
                condition = condition.split(">")
                ranges[condition[0]].append(range(int(condition[1]) + 1, 4001))
            elif "<" in condition:
                condition = condition.split("<")
                ranges[condition[0]].append(range(1, int(condition[1])))
        for rating in ranges:
            while len(ranges[rating]) > 1:
                new_range = range_intersect(ranges[rating][0], ranges[rating][1])
                if new_range is None:
                    ranges[rating] = "stop"
                    break
                else:
                    ranges[rating].pop(0)
                    ranges[rating].pop(0)
                    ranges[rating].append(new_range)
        if "stop" not in ranges.values():
            for rating in ranges:
                if ranges[rating] == []:
                    ranges[rating] = range(1, 4001)
                else:
                    ranges[rating] = ranges[rating][0]
            final_ranges.append(ranges)
    for situation in final_ranges:
        temp_total = 1
        for rating in situation:
            temp_total *= situation[rating].stop - situation[rating].start
        total += temp_total
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

