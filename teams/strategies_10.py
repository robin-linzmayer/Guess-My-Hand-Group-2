import random
import numpy as np


def playing(player, deck):
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
    return max_index


def guessing(player, cards, round):
    # Update available guesses and probabilities
    update_available_guesses(player)
    update_probabilities(player)
    candidate_guesses = available_guesses * probabilities

    # Return the top guesses by probability
    return candidate_guesses.argsort()[::-1][:13-round]


def update_available_guesses(player):
    for my_card in player.hand:
        card_idx = convert_card_to_index(my_card)
        available_guesses[card_idx] = False

    for exposed_card in player.exposed_cards:
        card_idx = convert_card_to_index(exposed_card)
        available_guesses[card_idx] = False


def update_probabilities(player):
    for my_card in player.hand:
        card_idx = convert_card_to_index(my_card)
        probabilities[card_idx] = 0

    for exposed_card in player.exposed_cards:
        card_idx = convert_card_to_index(exposed_card)
        probabilities[card_idx] = 0


def convert_card_to_index(card):
    """
    Convert Card object to an index ranking by value then suit
    """
    suit_idx = suit_to_idx[card.suit]
    value_idx = value_to_idx[card.value]
            
    return value_idx * 4 + suit_idx


"""
Global variables for Player 10
"""
available_guesses = np.ones(52, dtype=bool)
probabilities = np.full(52, 1/3, dtype=float)

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
