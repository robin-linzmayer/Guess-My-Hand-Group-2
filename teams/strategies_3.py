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


TEAMMATE_NAME = {
    "North": "South",
    "East": "West",
    "South": "North",
    "West": "East",
}

def get_seed(card: Card):
    return int(CARD_VALUE.get(card.value, card.value)) + 13 * (
        list(card.map.keys()).index(card.suit)
    )

def get_possible_cards():
    possible_cards = []
    for card in [Card(suit, value) for suit in ALL_SUITS for value in ALL_VALUES]:
        if card not in possible_cards:
            possible_cards.append(card)
    
    return possible_cards


def find_best_card(player: Player) -> Card:
    played_cards = sum(list(player.exposed_cards.values()), [])
    possible_cards = get_possible_cards()
    highest_score = 0
    card_to_play = None

    for card in player.hand:
        seed = get_seed(card)
        np.random.seed(seed)

        shuffled_cards = possible_cards.copy()
        np.random.shuffle(shuffled_cards)

        for c in shuffled_cards:
            if c in played_cards:
                shuffled_cards.remove(c)

        combination = shuffled_cards[: 12 - len(player.played_cards)]

        score = 0
        for c in combination:
            if c in player.hand:
                score += 1
        if score > highest_score:
            highest_score = score
            card_to_play = card
    
    # TODO: plays random card - we can optimize this
    return card_to_play or player.hand[0]



def get_teammate_shuffle(player, teammate_last_card):
    played_cards = sum(list(player.exposed_cards.values()), [])
    possible_cards = get_possible_cards()

    seed = get_seed(teammate_last_card)
    np.random.seed(seed)
    shuffled_cards = possible_cards.copy()
    np.random.shuffle(shuffled_cards)

    for c in shuffled_cards:
        if c in played_cards + player.hand:
            shuffled_cards.remove(c)
    
    return shuffled_cards


def get_teammate_last_card(player):
    teammate_last_card = None
    if len(player.exposed_cards[TEAMMATE_NAME[player.name]]) > 0:
        teammate_last_card = player.exposed_cards[TEAMMATE_NAME[player.name]][-1]

    if not teammate_last_card:
        raise Exception("should not happen")
        return random.sample(cards, 13 - round)

    return teammate_last_card

def get_exposed_cards(player) -> set:
    """Returns a set of all exposed cards"""
    exposed_cards = set()
    for player_cards in player.exposed_cards.values():
        for card in player_cards:
            exposed_cards.add(card)

    return exposed_cards


def remove_impossible_cards(player, combination: list[Card]) -> list[Card]:
    """Receives teammate's combination
    Removes impossible cards from the combination
    Impossible cards are cards that have been dealt or are in my hand"""
    cards_to_guess = []
    exposed_cards = get_exposed_cards(player)

    for c in combination:
        if c not in player.hand and c not in exposed_cards:
            cards_to_guess.append(c)

    return cards_to_guess

def corrected_cVal(player, idx):
    """Calculate the corrected cVal out of a specific guess
    The corrected cVal deducts one point for every correct card our player guessed that has since been played"""
    original = player.cVals[idx]

    teammates_exposed = player.exposed_cards[TEAMMATE_NAME[player.name]]

    # how many of our teammate's cards we guessed in that round
    # have since been played (exposed)
    exposed_guesses = set(player.guesses[idx]).intersection(set(teammates_exposed))

    # original cVal - correct but exposed cards
    return original - len(exposed_guesses)


def get_most_likely_cards(player, cards):
    """
    Returns a list of tuple(Card, probability: float), 
    with the cards that are most likely in the hands of our teammate first
    """

    likelyhood = dict()
    seen = dict()

    # keep track of how many times we've seen each card
    for card in cards:
        seen[card] = 0

    for idx, guess in enumerate(player.guesses):
        valid_cards = remove_impossible_cards(player, guess)
        cVal = corrected_cVal(player, idx)

        # calculate average probability of each guessed card being in our teammate's hand
        for valid_card in valid_cards:
            seen_count = seen[valid_card]
            if seen_count ==  0:
                # first time we're seeing this card
                # its probability is the cVal from our guess divided 
                # by the number of all possible cards from that guess
                likelyhood[valid_card] = cVal / len(valid_cards)
            else:
                prob = likelyhood[valid_card]
                # calculate the average probability out of all our guesses
                likelyhood[valid_card] = prob * (seen_count / (seen_count + 1)) + cVal / len(valid_cards)

            seen[valid_card] = seen_count + 1

    return sorted([(k, v) for k, v in likelyhood.items()], key=lambda x: x[1], reverse=True)

def add_likely_cards(player, combination, cards):
    most_likely = get_most_likely_cards(player, cards)

    likelies = []

    while len(combination) + len(likelies) < 13 - len(player.played_cards):
        if len(most_likely) > 0:
            best_card = most_likely.pop(0)[0]
            likelies.append(best_card)
        # if we don't have any likely cards
        # just add a random card to the list
        else:
            random_card = remove_impossible_cards(player, cards)[0]
            likelies.append(random_card)
            

    return combination + likelies


def playing(player, deck):
    """
    Player 3 strategy
    """
    if player.name == "North":
        pass
    else: 
        print(f"{player.name}: {player.hand}")

    if not player.hand:
        return None

    card_to_play = find_best_card(player)

    return player.hand.index(card_to_play)

    # raise Exception("This should never happen")

def guessing(player, cards, round):
    """
    Player 3 Guess
    """

    if player.name == "North":
        pass

    teammate_last_card = get_teammate_last_card(player)

    shuffled_cards = get_teammate_shuffle(player, teammate_last_card)

    combination = shuffled_cards[: 13 - len(player.played_cards)]

    combination = remove_impossible_cards(player, combination)
    combination = add_likely_cards(player, combination, cards)

    return combination
