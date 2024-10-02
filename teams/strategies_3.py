import random
import numpy as np


def playing(player, deck):
    """
    Max First strategy
    """
    if not player.hand:
        return None

    played_cards = sum(list(player.exposed_cards.values()), [])
    possible_cards = set()

    for card in player.hand:
        if card not in played_cards:
            possible_cards.add(card)

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
            list(possible_cards), (13 - len(player.played_cards)), replace=False
        )
        score = 0
        for c in combination:
            if c in player.hand:
                score += 1
        if score > highest_score:
            highest_score = score
            card_to_play = card

    if card_to_play:
        print(f"Highest score: {highest_score}")
        print(f"Card to play: {str(card_to_play)}")
        return player.hand.index(card_to_play)

    return 0


def guessing(player, cards, round):
    return random.sample(cards, 13 - round)
