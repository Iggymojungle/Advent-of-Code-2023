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
        input_data = get_input.get_input(2023, 7)
        with open(DATA, "w") as f:
            f.write(input_data.strip("\n"))
    with open(DATA, "r") as f:
        data = f.read()
    return data
            

STRENGTH_ORDER = "23456789TJQKA"
STRENGTH_ORDER_P2 = "J23456789TQKA"


def make_count(hand):
    hand_count = defaultdict(int)
    for item in hand:
        hand_count[item] += 1
    return hand_count


def rank_hand(hand):
    hand_count = make_count(hand)
    if 5 in hand_count.values():
        return 0
    if 4 in hand_count.values():
        return 1
    if set(hand_count.values()) == set((2, 3)):
        return 2
    if 3 in hand_count.values():
        return 3
    if 2 in hand_count.values():
        temp = list(hand_count.values())
        temp.pop(temp.index(2))
        if 2 in temp:
            return 4
        return 5
    return 6


def get_in_rank_value(hand):
    total = 0
    for letter_num, letter in enumerate(hand[0]):
        total += len(STRENGTH_ORDER) ** (len(hand[0]) - letter_num) * STRENGTH_ORDER.index(letter)
    return total


def sort_rank(rank):
    rank = sorted(rank, key=get_in_rank_value, reverse=True)
    return rank


def part1(data):
    data = [i.split(" ") for i in data.split("\n")]
    ranks = [[] for _ in range(7)]
    
    for hand in data:
        ranks[rank_hand(hand[0])].append(hand)
    
    for ranknum, rank in enumerate(ranks):
        ranks[ranknum] = sort_rank(rank)
    rank_value = len(data) + 1
    total = 0
    for rank in ranks:
        for hand in rank:
            rank_value -= 1
            total += rank_value * int(hand[1])

    return total


def get_in_rank_value_p2(hand):
    total = 0
    for letter_num, letter in enumerate(hand[0]):
        total += len(STRENGTH_ORDER_P2) ** (len(hand[0]) - letter_num) * STRENGTH_ORDER_P2.index(letter)
    return total


def sort_rank_p2(rank):
    rank = sorted(rank, key=get_in_rank_value_p2, reverse=True)
    return rank

def rank_hand_p2(hand):
    hand_count = make_count(hand)
    joker_hand_count = dict(hand_count)
    joker_hand_count["J"] = 0
    max_cards = max(joker_hand_count.values())

    if max_cards + hand_count["J"] == 5:
        return 0
    if max_cards + hand_count["J"] == 4:
        return 1
    if max_cards + hand_count["J"] == 3:
        temp = list(joker_hand_count.values())
        temp.pop(temp.index(max_cards))
        if 2 in temp:
            return 2
        return 3
    if max_cards + hand_count["J"] == 2:
        temp = list(hand_count.values())
        temp.pop(temp.index(max_cards))
        if 2 in temp:
            return 4
        return 5
    return 6


def part2(data):
    data = [i.split(" ") for i in data.split("\n")]
    ranks = [[] for _ in range(7)]
    
    for hand in data:
        ranks[rank_hand_p2(hand[0])].append(hand)
    
    for ranknum, rank in enumerate(ranks):
        ranks[ranknum] = sort_rank_p2(rank)
    rank_value = len(data) + 1
    total = 0
    for rank in ranks:
        for hand in rank:
            rank_value -= 1
            total += rank_value * int(hand[1])
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

