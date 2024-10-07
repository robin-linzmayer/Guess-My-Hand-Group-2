import random
from CardGame import Card
from copy import copy

# random_seeds = random.sample(range(100), 13)
random_seeds = list(range(13))
number_of_groups = 4
PARTNERS = {
    'North': 'South',
    'East': 'West',
    'South': 'North',
    'West': 'East',
}
all_cards = None
remaining_cards_south = None
remaining_cards_north = None


# Original mappings
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

def randomize_mappings(seed):
    # Set the random seed for reproducibility
    random.seed(seed)
    
    # Randomize suits
    suits = list(suit_to_idx.keys())
    random.shuffle(suits)
    randomized_suit_to_idx = {suit: idx for idx, suit in enumerate(suits)}
    
    # Randomize values
    values = list(value_to_idx.keys())
    random.shuffle(values)
    randomized_value_to_idx = {value: idx for idx, value in enumerate(values)}
    
    return randomized_suit_to_idx, randomized_value_to_idx

def convert_card_to_index(card, seed):
    """
    Convert Card object to an index using a random seed to randomize the suit and value mappings.
    """
    # Get randomized mappings based on the seed
    suit_to_idx_random, value_to_idx_random = randomize_mappings(seed)
    
    # Use randomized mappings to get the indices
    suit_idx = suit_to_idx_random[card.suit]
    value_idx = value_to_idx_random[card.value]
    
    return value_idx * 4 + suit_idx

def convert_list_of_cards_to_list_of_indices(list_of_cards, seed):
    """
    Convert a list of Card objects to a list of indices using a random seed for randomization.
    """
    return [convert_card_to_index(card, seed) for card in list_of_cards]

def convert_index_to_card(index, seed):
    """
    Convert an index to a Card object using a random seed for randomization.
    """
    # Get randomized mappings based on the seed
    suit_to_idx_random, value_to_idx_random = randomize_mappings(seed)
    
    # Invert the mappings to retrieve suits and values
    suits = list(suit_to_idx_random.keys())
    values = list(value_to_idx_random.keys())
    
    suit_idx = index % 4
    value_idx = index // 4
    
    # Find suit and value based on randomized indices
    suit = suits[list(suit_to_idx_random.values()).index(suit_idx)]
    value = values[list(value_to_idx_random.values()).index(value_idx)]
    
    return Card(suit, value)

def update_remaining_cards(player, remove=[]):
    if player.name == "North":
        global remaining_cards_north
        cards = remaining_cards_north
    elif player.name == "South":
        global remaining_cards_south
        cards = remaining_cards_south

    to_remove = player.hand + player.played_cards + player.exposed_cards['North'] + player.exposed_cards['East'] + player.exposed_cards['South'] + player.exposed_cards['West']
    
    if remove:
        to_remove += remove

    for card in to_remove:
        if card in cards:
            cards.remove(card)
    
    for i, guess in enumerate(player.guesses):
        if player.cVals[i] == 0:
            print(f"ALL GUESSES AT ROUND {i+1} WERE INCORRECT!!!")
            for card in guess:
                if card in cards:
                    cards.remove(card)
    if player.name == "North":
        remaining_cards_north = cards
        #print(f"Remaining cards for north: {remaining_cards_north}")
    elif player.name == "South":
        remaining_cards_south = cards
        #print(f"Remaining cards for south: {remaining_cards_south}")
    return list(cards)
    
def set_of_remaining_cards(player, cards, remove=[]):
    copy_of_cards = copy(cards)
    previous_guesses = [card for guess in player.guesses for card in guess]
    to_remove = player.hand + player.played_cards + player.exposed_cards['North'] + player.exposed_cards['East'] + player.exposed_cards['South'] + player.exposed_cards['West']
    
    if remove:
        to_remove += remove

    for card in to_remove:
        if card in copy_of_cards:
            copy_of_cards.remove(card)
    
    for i, guess in enumerate(player.guesses):
        if player.cVals[i] == 0:
            print(f"ALL GUESSES AT ROUND {i+1} WERE INCORRECT!!!")
            for card in guess:
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
    global all_cards
    global remaining_cards_north
    global remaining_cards_south

    if player.name == "North" or player.name == "South":
        return NorthSouthStrategy(player, deck)
    else:
        return EastWestStrategy(player, deck)

def randomize_card_mapping(deck_cards, seed):
    """
    Randomizes the mapping of the entire deck to indices using the given seed.
    """
    random.seed(seed)
    
    # Shuffle the deck cards using the provided seed
    shuffled_indices = list(range(len(deck_cards)))
    random.shuffle(shuffled_indices)
    
    # Create a mapping of each card in the deck to a random index
    card_to_random_map = {card: shuffled_indices[i] for i, card in enumerate(deck_cards)}
    return card_to_random_map

def NorthSouthStrategy(player, deck):
    """
    Max First strategy: Returns the card in the player's hand that is mapped to the largest number
    based on the random mapping of the entire deck.
    """
    if not player.hand:
        return None
    global random_seeds
    global remaining_cards_south
    global remaining_cards_north

    # Determine the random seed to use based on the number of cards already played
    random_seed_index = len(player.played_cards)
    print(f"Random seed index in playing is {random_seed_index}.")
    random_seed = random_seeds[random_seed_index]
    print(f"Random seed in playing is {random_seed}.")

    # Get the random mapping for the entire deck
    card_mapping = randomize_card_mapping(deck.copyCards, random_seed)

    # Find the card in the player's hand that has the maximum random mapping value
    max_card = max(player.hand, key=lambda card: card_mapping[card])
    min_card = min(player.hand, key=lambda card: card_mapping[card])
    print(f"Max card mapping for the card {player.name}: {card_mapping[max_card]}")

    # if 51 - card_mapping[max_card] > card_mapping[min_card]:
    #     return player.hand.index(max_card)
    # else:
    #     return player.hand.index(min_card)

    return player.hand.index(max_card)

def guessing(player, cards, round):
    global remaining_cards_south
    global remaining_cards_north
    global random_seeds

    print(f"Round {round} for guessing!")

    if len(player.played_cards) == 1:
        global all_cards
        all_cards = copy(cards)
        remaining_cards_north = copy(cards)
        remaining_cards_south = copy(cards)

    random_seed_index = len(player.played_cards) - 1
    print(f"Random seed index in guessing is {random_seed_index}.")
    random_seed = random_seeds[random_seed_index]
    print(f"Random seed in guessing is {random_seed}.")
    assert(round == len(player.played_cards))

    # Randomize the mapping of the deck using the current seed
    card_mapping = randomize_card_mapping(copy(cards), random_seed)

    # Determine the player's card in this round
    partner_card = get_partner_exposed_card(player)
    print(f"Partner's card mapping when {player.name} is guessing: {card_mapping[partner_card]}")

    # if card_mapping[partner_card] <= 25:
    #     remove = [card for card in all_cards if card_mapping[card] < card_mapping[partner_card]]
    # else:
    #     remove = [card for card in all_cards if card_mapping[card] > card_mapping[partner_card]]

    remove = [card for card in all_cards if card_mapping[card] > card_mapping[partner_card]]
    
    # Update remaining cards with the 'remove' list
    remaining_cards = update_remaining_cards(player, remove=remove)

    if player.name == "North":
        remaining_cards_north = remaining_cards
    elif player.name == "South":
        remaining_cards_south = remaining_cards

    # Return a random sample of the specified length from the remaining cards
    number_of_cards_to_guess = 13 - round
    return random.sample(remaining_cards, number_of_cards_to_guess)





def opposite(group_index):
    if group_index % 2 == 0:
        return group_index + 1
    else:
        return group_index - 1



def get_partner_exposed_card(player):
    return player.exposed_cards[PARTNERS[player.name]][-1]




def oldguessing(player, cards, round):
    global remaining_cards_south
    global remaining_cards_north
    print(f"Round {round} for guessing!")

    if len(player.played_cards) == 1:
        global all_cards
        all_cards = copy(cards)
        remaining_cards_north = copy(cards)
        remaining_cards_south = copy(cards)

    remaining_cards = update_remaining_cards(player, remove = None)

    if player.name == "North":
        remaining_cards_north = remaining_cards
    elif player.name == "South":
        remaining_cards_south = remaining_cards

    random_seed_index = len(player.played_cards) - 1
    number_of_cards_to_guess = 13 - round
    partner_card = get_partner_exposed_card(player)
    assert(round == len(player.played_cards))


    # remaining_cards = update_remaining_cards(player, remove = None)
    # remaining_cards = set_of_remaining_cards(player, cards, remove = None)
    
    groups, cards_to_group_indices = group_cards(random_seeds[random_seed_index], cards)
    group_index_to_guess = opposite(cards_to_group_indices[partner_card])
    guessed_group = groups[group_index_to_guess]
    #print({card for card in guessed_group if card in remaining_cards})
    cards_to_guess = list({card for card in guessed_group if card in remaining_cards})
    #print(convert_list_of_cards_to_list_of_indices(cards_to_guess))
    #print(f"The number of cards of the predicted group to be guessed is {len(cards_to_guess)}")
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

def oldNorthSouthStrategy(player, deck, random_seeds):
    """
    Max First strategy
    """
    if not player.hand:
        return None
    
    random_seed_index = len(player.played_cards)
    
    # print(f"Random seed index in playing is {random_seed_index}.")

    groups, cards_to_group_indices = group_cards(random_seeds[random_seed_index], deck.copyCards)

    present_groups = {i: [] for i in range(0, len(groups) )}

    for i, card in enumerate(player.hand):
        present_groups[cards_to_group_indices[card]].append(card)

    largest_group_index = -1
    largest_group_size = 1
    smallest_opposite_group_size = 52

    for group_index, group in present_groups.items():
        # print(f"Group {group_index}: {len(group)}")
        if len(present_groups[opposite(group_index)]) > 0 and (len(group) >= largest_group_size or (len(group) == largest_group_size and len(present_groups[opposite(group_index)]) < smallest_opposite_group_size)):
            largest_group_size = len(group)
            largest_group_index = group_index
            smallest_opposite_group_size = len(present_groups[opposite(group_index)])

    if largest_group_index == -1:
        # If there is no group that has a partner group, play a random card
        return random.randint(0, len(player.hand) - 1)
    
    # print(f"Largest group index: {largest_group_index}")
    # print(f"Opposite group index: {opposite(largest_group_index)}")
    # print(f"Size of largest group: {len(present_groups[largest_group_index])}")
    # print(f"Size of smallest opposite group: {len(present_groups[opposite(largest_group_index)])}")

    assert(cards_to_group_indices[present_groups[largest_group_index][0]] == largest_group_index)


    return player.hand.index(present_groups[opposite(largest_group_index)][0])

def EastWestStrategy(player, deck):
    return NorthSouthStrategy(player, deck)