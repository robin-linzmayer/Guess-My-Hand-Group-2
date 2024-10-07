import random
import numpy as np

from CardGame import Card, Deck, Player


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
    """
    Update available guesses and probabilities and return the top guesses by probability
    """
    # Initialize available guesses and probabilities
    available_guesses = np.ones(52, dtype=bool)
    probabilities = np.full(52, 1/3, dtype=float)

    # Update available guesses and probabilities
    update_available_guesses(player, available_guesses)
    update_probabilities(player, round, available_guesses, probabilities)
    
    # Update probabilities based on partner cards
    # [PROBABILITY NOT THE SPIRIT OF THE GAME :)]
    get_partner_cards(player, round, probabilities)
    probabilities[~available_guesses] = 0

    # Debug print
    # print(f'probabilities: {probabilities}')
    
    # Return top guesses by probability
    candidate_guesses = probabilities.argsort()[::-1][:13-round]
    guesses = [card for card in cards if convert_card_to_index(card) in candidate_guesses]
    return guesses


def update_available_guesses(player, available_guesses):
    """
    Update available guesses by removing cards in hand, played and exposed cards
    """
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


def update_probabilities(player, round, available_guesses, probabilities):
    """
    Update probabilities by various strategies
    """
    # Set unavailable cards to zero probability
    probabilities[~available_guesses] = 0

    # Update probabilities based on previous rounds' guesses and cVals
    for i in range(round - 1):
        accuracy = player.cVals[i] / (12-i)
        for card in player.guesses[i]:
            card_idx = convert_card_to_index(card)
            if available_guesses[card_idx]:
                probabilities[card_idx] = accuracy


def get_partner_cards(player, round, probabilities):
    """
    Update probabilities based on partner cards
    [THIS IS PROBABILITY NOT THE SPIRIT OF THE GAME :)]
    """
    if np.sum(partner_cards) > 0:
        probabilities[~partner_cards] = 0
        probabilities[partner_cards] = 1

    for my_card in player.hand:
        card_idx = convert_card_to_index(my_card)
        partner_cards[card_idx] = True

    print(f'partner_cards: {partner_cards}')


def convert_card_to_index(card):
    """
    Convert Card object to an index ranking by value then suit
    """
    suit_idx = suit_to_idx[card.suit]
    value_idx = value_to_idx[card.value]
    return value_idx * 4 + suit_idx


"""
Global variables
"""
partner_cards = np.zeros(52, dtype=bool)

suit_to_idx = {"Clubs": 0, "Diamonds": 1, "Hearts": 2, "Spades": 3}
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
