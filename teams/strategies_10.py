import random
from copy import copy

def group_cards(deck, n, seed):
    # Set random seed for reproducibility
    random.seed(seed)

    cards = copy(deck.copyCards)

    # Shuffle the deck to ensure randomness
    random.shuffle(cards)
    
    # Calculate the size of each group
    group_size = 52 // n
    
    # Create groups
    groups = {i: [] for i in range(1, n+1)}
    cards_to_groups = {}
    
    # Distribute cards into groups
    for i in range(n):
        group_cards = cards[i * group_size: (i + 1) * group_size]
        groups[i + 1] = group_cards
        
        # Populate the reverse dictionary
        for card in group_cards:
            cards_to_groups[card] = i + 1
    
    return groups, cards_to_groups


def playing(player, deck):
    
    random_seeds = random.sample(range(100), 13)

    if player.name == "North" or player.name == "South":
        return NorthSouthStrategy(player, deck, random_seeds)
    else:
        return EastWestStrategy(player, deck, random_seeds)
    

def guessing(player, cards, round):
    return random.sample(cards, 13 - round)


def NorthSouthStrategy(player, deck, random_seeds):
    """
    Max First strategy
    """
    if not player.hand:
        return None
    
    value_order = deck.values
    max_index = 0
    max_value = -1
    
    for i, card in enumerate(player.hand):
        value = value_order.index(card.value)
        if value > max_value:
            max_value = value
            max_index = i
    
    groups, cards_to_groups = group_cards(deck, 4, random_seeds[0])

    present_groups = {i: [] for i in range(1, len(groups) + 1 )}

    for i, card in enumerate(player.hand):
        present_groups[cards_to_groups[card]].append(card)

    largest_group_index = -1
    largest_group_size = -1
    smallest_opposite_group_size = 52

    for group_index, group in present_groups.items():
        if len(groups[opposite(group_index)]) > 0 and (len(group) > largest_group_size or (len(group) == largest_group_size and len(groups[opposite(group_index)]) < smallest_opposite_group_size)):
            largest_group_size = len(group)
            largest_group_index = group_index
            smallest_opposite_group_size = len(groups[opposite(group_index)])

    assert(cards_to_groups[present_groups[largest_group_index][0]] == largest_group_index)

    return player.hand.index(present_groups[largest_group_index][0])

def opposite(group_index):
    if group_index % 2 == 0:
        return group_index - 1
    else:
        return group_index + 1
    

def EastWestStrategy(player, deck):
    return NorthSouthStrategy(player, deck)