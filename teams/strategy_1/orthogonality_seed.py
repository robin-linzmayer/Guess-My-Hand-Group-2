import random


NAIVE_BEST_SEED = 134


def shuffle_and_divide(deck, seed, turn, num_groups=4):
    random.seed(seed*turn)  # needs to be clarified
    random.shuffle(deck)
    groupings = [deck[i::num_groups] for i in range(num_groups)]
    return groupings

def calculate_consecutive_overlap(group_sets):
    total_overlap = 0
    # Compare each corresponding group for overlap between consecutive sets
    for i in range(len(group_sets) - 1):
        current_groups = group_sets[i]
        next_groups = group_sets[i + 1]
        overlap = sum(len(set(current_groups[j]).intersection(next_groups[j])) for j in range(len(current_groups)))
        total_overlap += overlap
    return total_overlap

def find_best_seed(seed_range, turns=100):
    best_seed = None
    best_score = float('inf')  # Aim to minimize overlap
    
    for seed in seed_range:
        deck = list(range(52))
        groups_list = [shuffle_and_divide(deck, seed, turn+1) for turn in range(turns)]
        score = calculate_consecutive_overlap(groups_list)
        
        if score < best_score:
            best_score = score
            best_seed = seed
    
    return best_seed, best_score


if __name__ == "__main__":
    seed_range = range(1, 500)  # Example range of seeds to test
    best_seed, best_score = find_best_seed(seed_range)
    print(f"Best Seed: {best_seed}, Best Score: {best_score}")
