import random
import numpy as np
from CardGame import Card, Deck, Player

ALL_SUITS = ["Hearts", "Diamonds", "Clubs", "Spades"]
ALL_VALUES = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
CARD_VALUE = {
    "A": 1,
    "J": 11,
    "Q": 12,
    "K": 13,
}

def get_seed(card: Card):
    return int(CARD_VALUE.get(card.value, card.value)) + 13 * (
        list(card.map.keys()).index(card.suit)
    )

def get_possible_cards():
    possible_cards = []
    for card in [Card(suit, value) for suit in ALL_SUITS for value in ALL_VALUES]:
        if str(card) not in [str(c) for c in possible_cards]:
            possible_cards.append(card)
    
    return possible_cards



def playing(player, deck):
    """
    Player 3 strategy
    """
    if not player.hand:
        return None

    played_cards = sum(list(player.exposed_cards.values()), [])
    possible_cards = get_possible_cards()


    card_to_play = None
    highest_score = 0

    for card in player.hand:
        seed = get_seed(card)
        # print(f"P-{player.name} seed: {seed}")
        np.random.seed(seed)

        shuffled_cards = possible_cards.copy()
        np.random.shuffle(shuffled_cards)

        for c in shuffled_cards:
            if str(c) in [str(c) for c in played_cards]:
                shuffled_cards.remove(c)

        combination = shuffled_cards[: 13 - len(player.played_cards)]

        score = 0
        for c in combination:
            if str(c) in [str(c) for c in player.hand]:
                score += 1
        if score > highest_score:
            highest_score = score
            card_to_play = card

    # print("C: {}")

    if card_to_play:
        return player.hand.index(card_to_play)

    # raise Exception("This should never happen")

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

    played_cards = sum(list(player.exposed_cards.values()), [])
    possible_cards = get_possible_cards()

    seed = get_seed(teammate_last_card)
    np.random.seed(seed)
    shuffled_cards = possible_cards.copy()
    np.random.shuffle(shuffled_cards)

    for c in shuffled_cards:
        if str(c) in [str(c) for c in played_cards + player.hand]:
            shuffled_cards.remove(c)

    combination = shuffled_cards[: 13 - len(player.played_cards)]

    cards_to_guess = []
    for c in cards:
        if str(c) in [str(c) for c in combination]:
            cards_to_guess.append(c)

    return cards_to_guess
