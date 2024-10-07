import random
from itertools import chain
from CardGame import Player, Deck, Card

random.seed(41)

PARTNERS = {
    "North": "South",
    "East": "West",
    "South": "North",
    "West": "East",
}

SUIT_TO_NUM = {"Hearts": 0, "Spades": 13, "Diamonds": 26, "Clubs": 39}

VAL_TO_NUM = {
    "A": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
}

NUM_TO_SUIT = {v: k for k, v in SUIT_TO_NUM.items()}
NUM_TO_VAL = {v: k for k, v in VAL_TO_NUM.items()}


def generate_permutation(perm_size):
    """Generates a permutation dictionary, each card points to one permutation"""
    numbers = list(range(1, 53))
    perms = {}

    for i in range(1, 53):
        perms[i] = random.sample(numbers, perm_size)
    return perms


def initialize_probabilities():
    """Initilize probability dictionary"""
    return {card: 1 / 52 for card in range(1, 53)}


def initilize_permutations():
    """Generates a dictionary with keys 1 to 12, values are permutations of decreasing size"""
    result = {}
    for key in range(1, 13):
        perm_size = 13 - key
        perms = generate_permutation(perm_size)
        result[key] = perms
    return result


PERMUTATIONS = initilize_permutations()


def card_to_val(card: Card):
    """Converts suit and value into a number from 1-52"""
    return SUIT_TO_NUM[card.suit] + VAL_TO_NUM[card.value]


def val_to_card(val: int) -> Card:
    """Converts a number from 1-52 into a Card object"""
    if val < 1 or val > 52:
        raise ValueError("Value must be between 1 and 52")

    for base in [39, 26, 13, 0]:  # Clubs, Diamonds, Spades, Hearts
        if val > base:
            suit = NUM_TO_SUIT[base]
            break

    # Determine the value
    card_val = val - base
    value = NUM_TO_VAL[card_val]

    return Card(suit, value)


def update_probabilities(
    probs: dict[int, float],
    guess: list[Card],
    seen: list[Card],
    correct: int,
    hand_size: int,
) -> dict[int, float]:
    """Update probability dictionary"""
    pass


def playing(player: Player, deck: Deck):
    game_round = len(player.played_cards) + 1
    my_cards = [card_to_val(card) for card in player.hand]

    # Find most similar permutations to players cards
    card_index = 0
    max_sim = 0
    for i, k in enumerate(my_cards):
        perms = PERMUTATIONS[game_round][k]
        sim = len((set(my_cards) & set(perms)) - {k})
        if sim > max_sim:
            card_index = i
            max_sim = sim

    return card_index


def guessing(player: Player, cards, round):

    perm_index = card_to_val(player.exposed_cards[PARTNERS[player.name]][-1])

    educated_guess = (
        set(PERMUTATIONS[round][perm_index])
        - set(card_to_val(card) for card in player.hand)
        - set(chain.from_iterable(player.exposed_cards.values()))
    )

    guess_deck = list(
        set(i for i in range(1, 53))
        - set(card_to_val(card) for card in player.hand)
        - set(
            card_to_val(card)
            for card in chain.from_iterable(player.exposed_cards.values())
        )
        - educated_guess
    )

    guess = random.sample(guess_deck, 13 - round - len(educated_guess))
    educated_guess = list(educated_guess) + guess

    card_guesses = [val_to_card(i) for i in educated_guess]
    return card_guesses
