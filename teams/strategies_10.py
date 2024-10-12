import random
from CardGame import Card
from copy import copy
import numpy as np


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


def playing(player, deck):
    global seeds
    # Determine the random seed to use based on the number of cards already played
    random_seed_index = len(player.played_cards)
    print(f"Random seed index in playing is {random_seed_index}.")
    random_seed = seeds[random_seed_index]
    print(f"Random seed in playing is {random_seed}.")

    # Get the random mapping for the entire deck
    card_mapping = randomize_card_mapping(deck.copyCards, random_seed)

    # Find the card in the player's hand that has the maximum random mapping value
    max_card = max(player.hand, key=lambda card: card_mapping[card])
    print(f"Max card mapping for the card {player.name}: {card_mapping[max_card]}")

    return player.hand.index(max_card)

    
def guessing(player, cards, round):
    """
    Update available guesses and probabilities and return the top guesses by probability
    """
    
    # Initialize available guesses and probabilities
    available_guesses = np.ones(DECK_SIZE, dtype=bool)
    probabilities = np.full(DECK_SIZE, PAR_PROBABILITY, dtype=float)

    # Update available guesses and probabilities
    available_guesses = update_available_guesses(player, available_guesses, cards, round)
    probabilities = update_probabilities(player, round, available_guesses, probabilities)
    
    # Return top guesses by probability
    candidate_guesses = probabilities.argsort()[::-1][:13-round]
    guesses = [card for card in cards if convert_card_to_index(card) in candidate_guesses]
    return guesses


def update_available_guesses(player, available_guesses, cards, round):
    """
    Update available guesses by removing cards in hand, played and exposed cards,
    as well as cards outside of partner's min/max
    """
    global seeds

    for my_card in player.hand:
        card_idx = convert_card_to_index(my_card)
        available_guesses[card_idx] = False

    for played_card in player.played_cards:
        card_idx = convert_card_to_index(played_card)
        available_guesses[card_idx] = False

    for exposed_card_lst in player.exposed_cards.values():
        for exposed_card in exposed_card_lst:
            card_idx = convert_card_to_index(exposed_card)
            available_guesses[card_idx] = False
    
    for i, guess in enumerate(player.guesses):
        if player.cVals[i] == 0:
            for card in guess:
                if card in cards:
                    cards.remove(card)

    for i in range(1, round+1):
        random_seed_index = i - 1
        print(f"Random seed index in guessing is {random_seed_index}.")
        random_seed = seeds[random_seed_index]
        print(f"Random seed in guessing is {random_seed}.")
        card_mapping = randomize_card_mapping(copy(cards), random_seed)
        partner_card = player.exposed_cards[PARTNERS[player.name]][i-1]
        removed_cards = [card for card in copy(cards) if card_mapping[card] > card_mapping[partner_card]]
        for removed_card in removed_cards:
            card_idx = convert_card_to_index(removed_card)
            available_guesses[card_idx] = False
    
    return available_guesses


def update_probabilities(player, round, available_guesses, probabilities):
    """
    Update probabilities by various strategies
    """
    # Set unavailable cards to zero probability
    probabilities[~available_guesses] = 0

    # Update probabilities based on previous rounds' guesses and cVals
    partner_name = partner[player.name]
    opponents_names = opponents[player.name]
    
    for i in range(round - 1):
        numerator = player.cVals[i]
        denominator = OPENING_HAND_SIZE - 1 - i
        for card in player.guesses[i]:
            if card in player.exposed_cards[partner_name]:
                numerator -= 1
                denominator -= 1
            if card in player.exposed_cards[opponents_names[0]] or \
                card in player.exposed_cards[opponents_names[1]]:
                denominator -= 1
            card_idx = convert_card_to_index(card)
            accuracy = numerator / denominator if denominator > 0 else 0
            if available_guesses[card_idx]:
                probabilities[card_idx] = accuracy
    return probabilities


def convert_card_to_index(card):
    """
    Convert Card object to an index ranking by value then suit
    """
    suit_idx = suit_to_idx[card.suit]
    value_idx = value_to_idx[card.value]
    return value_idx * 4 + suit_idx


def convert_index_to_card(index):
    """
    Convert index to Card object
    """
    suit_idx = index % 4
    value_idx = index // 4
    suit = list(suit_to_idx.keys())[suit_idx]
    value = list(value_to_idx.keys())[value_idx]
    return Card(suit, value)


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

"""
Static global variables
"""
seeds = list(range(13))     
DECK_SIZE = 52
OPENING_HAND_SIZE = 13
PAR_PROBABILITY = 1/3

suit_to_idx = {"Diamonds": 0, "Clubs": 1, "Hearts": 2, "Spades": 3}
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
partner = {"North": "South", "East": "West", "South": "North", "West": "East"}
opponents = {
    "North": ["East", "West"],
    "East": ["South", "North"],
    "South": ["West", "East"],
    "West": ["North", "South"]
}

PARTNERS = {
    'North': 'South',
    'East': 'West',
    'South': 'North',
    'West': 'East',
}