import random
import numpy as np
from CardGame import Card, Deck, Player


def playing(player, deck):
    """
    Max First strategy
    """
    if not player.hand:
        return None

    played_cards = sum(list(player.exposed_cards.values()), [])
    possible_cards = []

    all_suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
    all_values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

    for card in [Card(suit, value) for suit in all_suits for value in all_values]:
        if str(card) not in [str(c) for c in possible_cards]:
            possible_cards.append(card)

    card_to_play = None
    highest_score = 0

    card_value = {
        "A": 1,
        "J": 11,
        "Q": 12,
        "K": 13,
    }

    for card in player.hand:
        seed = int(card_value.get(card.value, card.value)) + 13 * (
            list(card.map.keys()).index(card.suit)
        )
        np.random.seed(seed)
        combination = np.random.choice(
            possible_cards, (13 - len(player.played_cards)), replace=False
        )
        score = 0
        for c in combination:
            if str(c) in [str(c) for c in player.hand]:
                score += 1
        if score > highest_score:
            highest_score = score
            card_to_play = card

    if card_to_play:
        print(f"Highest score: {highest_score}")
        return player.hand.index(card_to_play)

    return 0


def guessing(player, cards, round):

    teammate_name = {
        "North": "South",
        "East": "West",
        "South": "North",
        "West": "East",
    }

    teammate_last_card = None
    if len(player.exposed_cards[teammate_name[player.name]]) > 0:
        teammate_last_card = player.exposed_cards[teammate_name[player.name]][-1]

    if not teammate_last_card:
        return random.sample(cards, 13 - round)

    card_value = {
        "A": 1,
        "J": 11,
        "Q": 12,
        "K": 13,
    }

    played_cards = sum(list(player.exposed_cards.values()), [])
    possible_cards = []

    all_suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
    all_values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

    for card in [Card(suit, value) for suit in all_suits for value in all_values]:
        if str(card) not in [str(c) for c in possible_cards]:
            possible_cards.append(card)

    seed = int(
        card_value.get(teammate_last_card.value, teammate_last_card.value)
    ) + 13 * (list(teammate_last_card.map.keys()).index(teammate_last_card.suit))
    np.random.seed(seed)
    combination = np.random.choice(possible_cards, (13 - round), replace=False)

    return combination
