import random
from CardGame import Card
from copy import copy

random_seeds = random.sample(range(100), 13)
number_of_groups = 4
PARTNERS = {
    'North': 'South',
    'East': 'West',
    'South': 'North',
    'West': 'East',
}
cards = None
suit_to_idx = {"Hearts": 0, "Diamonds": 1, "Clubs": 2, "Spades": 3}
value_to_idx = {
    "2": 0,
    "3": 1,
    "4": 2,
    "5": 3,
    "6": 4,
    "7": 5,
    "8": 6,
    "9": 7,
    "10": 8,
    "J": 9,
    "Q": 10,
    "K": 11,
    "A": 12,
}


def convert_card_to_index(card):
    """
    Convert Card object to an index ranking by value then suit
    """
    suit_idx = suit_to_idx[card.suit]
    value_idx = value_to_idx[card.value]
            
    return value_idx * 4 + suit_idx

def convert_list_of_cards_to_list_of_indices(list_of_cards):
    """
    Convert Card object to an index ranking by value then suit
    """
    return [convert_card_to_index(card) for card in list_of_cards]
            

def convert_index_to_card(index):
    """
    Convert index to Card object
    """
    suit_idx = index % 4
    value_idx = index // 4
    
    suit = list(suit_to_idx.keys())[list(suit_to_idx.values()).index(suit_idx)]
    value = list(value_to_idx.keys())[list(value_to_idx.values()).index(value_idx)]
    
    return Card(suit, value)

# we can just use cards instead of copy_of_cards
def set_of_remaining_cards(player, cards):
    copy_of_cards = copy(cards)
    to_remove = player.hand + player.played_cards + player.exposed_cards['North'] + player.exposed_cards['East'] + player.exposed_cards['South'] + player.exposed_cards['West']
    for card in to_remove:
        if card in copy_of_cards:
            copy_of_cards.remove(card)
    return list(copy_of_cards)

def group_cards(seed, cards):
    global number_of_groups
    global suit_to_idx
    copy_of_cards = copy(cards)
    
    # Set random seed for reproducibility
    random.seed(seed)

    # Shuffle the deck to ensure randomness
    random.shuffle(copy_of_cards)
    
    # Calculate the size of each group
    group_size = 52 // number_of_groups
    
    # Create groups
    groups = {i: [] for i in range(0, number_of_groups)}
    cards_to_group_indices = {}
    
    for card in copy_of_cards:
        groups[suit_to_idx[card.suit]].append(card)
        cards_to_group_indices[card] = suit_to_idx[card.suit]

    # # Distribute cards into groups
    # for i in range(number_of_groups):
    #     group_cards = copy_of_cards[i * group_size: (i + 1) * group_size]
    #     groups[i] = group_cards
        
    #     # Populate the reverse dictionary
    #     for card in group_cards:
    #         cards_to_group_indices[card] = i
    
    return groups, cards_to_group_indices


def playing(player, deck):
    global cards
    global random_seeds
    cards = deck.copyCards

    if player.name == "North" or player.name == "South":
        return NorthSouthStrategy(player, deck, random_seeds)
    else:
        return EastWestStrategy(player, deck, random_seeds)
    
def guessing(player, cards, round):
    random_seed_index = len(player.played_cards) - 1
    print(f"Random seed index in guessing is {random_seed_index}.")
    number_of_cards_to_guess = 13 - round
    assert(round == len(player.played_cards))

    remaining_cards = set_of_remaining_cards(player, cards)
    groups, cards_to_group_indices = group_cards(random_seeds[random_seed_index], cards)
    partner_card = get_partner_exposed_card(player)
    group_index_to_guess = opposite(cards_to_group_indices[partner_card])
    guessed_group = groups[group_index_to_guess]
    print({card for card in guessed_group if card in remaining_cards})
    cards_to_guess = list({card for card in guessed_group if card in remaining_cards})
    print(convert_list_of_cards_to_list_of_indices(cards_to_guess))
    print(f"The number of cards of the predicted group to be guessed is {len(cards_to_guess)}")
    if len(cards_to_guess) >= number_of_cards_to_guess:
        return random.sample(cards_to_guess, number_of_cards_to_guess)
    else:
        print(f"The number of cards that can be guessed {len(list(set(remaining_cards) - set(cards_to_guess)))}")
        print(f"len of cards to guess: {len(cards_to_guess)}")
        print(f"len of remaining cards: {len(remaining_cards)}")
        print(f"The number of cards that need to be additionally guessed {number_of_cards_to_guess - len(cards_to_guess)}")
        random_remaining_cards = random.sample(list(set(remaining_cards) - set(cards_to_guess)), number_of_cards_to_guess - len(cards_to_guess))
        union_list_of_cards = cards_to_guess + random_remaining_cards
        return union_list_of_cards

def get_partner_exposed_card(player):
    return player.exposed_cards[PARTNERS[player.name]][-1]

def NorthSouthStrategy(player, deck, random_seeds):
    """
    Max First strategy
    """
    if not player.hand:
        return None
    
    random_seed_index = len(player.played_cards)
    
    print(f"Random seed index in playing is {random_seed_index}.")

    groups, cards_to_group_indices = group_cards(random_seeds[random_seed_index], deck.copyCards)

    present_groups = {i: [] for i in range(0, len(groups) )}

    for i, card in enumerate(player.hand):
        present_groups[cards_to_group_indices[card]].append(card)

    largest_group_index = -1
    largest_group_size = 1
    smallest_opposite_group_size = 52

    for group_index, group in present_groups.items():
        print(f"Group {group_index}: {len(group)}")
        if len(present_groups[opposite(group_index)]) > 0 and (len(group) >= largest_group_size or (len(group) == largest_group_size and len(present_groups[opposite(group_index)]) < smallest_opposite_group_size)):
            largest_group_size = len(group)
            largest_group_index = group_index
            smallest_opposite_group_size = len(present_groups[opposite(group_index)])

    if largest_group_index == -1:
        # If there is no group that has a partner group, play a random card
        return random.randint(0, len(player.hand) - 1)
    
    print(f"Largest group index: {largest_group_index}")
    print(f"Opposite group index: {opposite(largest_group_index)}")
    print(f"Size of largest group: {len(present_groups[largest_group_index])}")
    print(f"Size of smallest opposite group: {len(present_groups[opposite(largest_group_index)])}")

    assert(cards_to_group_indices[present_groups[largest_group_index][0]] == largest_group_index)

    return player.hand.index(present_groups[opposite(largest_group_index)][0])

def opposite(group_index):
    if group_index % 2 == 0:
        return group_index + 1
    else:
        return group_index - 1
    

def EastWestStrategy(player, deck):
    return NorthSouthStrategy(player, deck)