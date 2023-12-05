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
        input_data = get_input.get_input(2023, 5)
        with open(DATA, "w") as f:
            f.write(input_data.strip("\n"))
    with open(DATA, "r") as f:
        data = f.read()
    return data
            

def prepare_data(data):
    data = data.split("\n\n")
    seeds = list(map(int, data.pop(0).split(" ")[1:]))
    maps = [[list(map(int, j.split(" "))) for j in i.split("\n")[1:]] for i in data]
    return seeds, maps


def map_seed(to_map, seed):
    for line in to_map:
        if line[1] <= seed < line[1] + line[2]:
            return seed + line[0] - line[1]
    return seed


def part1(data):
    seeds, maps = prepare_data(data)
    for seednum, seed in enumerate(seeds):
        for to_map in maps:
            seed = map_seed(to_map, seed)
            seeds[seednum] = seed
    return min(seeds)
            

def range_intersect(r1, r2):
    return range(max(r1.start,r2.start), min(r1.stop,r2.stop)) or None


def map_seed_p2(to_map, seed):
    new_seeds = []
    unchanged_seeds = []
    intersections = []
    for line in to_map:
        line_range = range(line[1], line[1] + line[2])
        intersection = range_intersect(line_range, seed)
        if intersection is not None:
            intersections.append(intersection)
            new_seeds.append(range(intersection.start + line[0] - line[1], intersection.stop + line[0] - line[1]))
    new_seed_mins = sorted(list(map(min, intersections)))
    new_seed_maxs = sorted(list(map(max, intersections)))
    if intersections:
        if new_seed_mins[0] != seed.start:
            unchanged_seeds.append(range(seed.start, new_seed_mins[0]))
        for new_seed_num in range(len(new_seeds)-1):
            if new_seed_maxs[new_seed_num] + 1 != new_seed_mins[new_seed_num + 1]:
                unchanged_seeds.append(range(new_seed_maxs[new_seed_num] + 1, new_seed_mins[new_seed_num + 1]))
        if new_seed_maxs[-1] + 1 != seed.stop:
            unchanged_seeds.append(range(new_seed_maxs[0], seed.stop))
        new_seeds += unchanged_seeds
        return new_seeds
    return [seed]
    



def part2(data):
    seeds, maps = prepare_data(data)
    new_seeds = []
    for seednum in range(0, len(seeds), 2):
        new_seeds.append(range(seeds[seednum], seeds[seednum] + seeds[seednum+1]))
    seeds = new_seeds
    for map_num, to_map in enumerate(maps):
        print(f"Map number {map_num+1} of 7")
        new_seeds = []
        for seed in seeds:
            new_seeds += map_seed_p2(to_map, seed)
        seeds = new_seeds
    return min(map(min, seeds))


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

