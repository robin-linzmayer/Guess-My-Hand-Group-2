import random
from itertools import chain
from collections import defaultdict
from CardGame import Player, Deck, Card
import numpy as np

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
MIN_SUIT = {"North": -1, "South": -1, "East": -1, "West": -1}


def generate_permutation(perm_size, cards, seed):
    """Generates a permutation dictionary, each card points to one permutation"""
    perms = {}
    for i in cards:
        random.seed(seed)
        perms[i] = random.sample(cards, perm_size)
    return perms


def get_unguessed_cards(player):
    """Get all cards that have not been guessed by player"""
    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
    values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    allcards = [Card(suit, value) for suit in suits for value in values]

    # All possible cards except exposed cards
    unguessed_cards = []
    for card in allcards:
        if card not in set(
            chain.from_iterable(player.exposed_cards.values())
        ) and card not in set(player.played_cards):
            unguessed_cards.append(card)

    # Add cards exposed in this round as partner might not have had that information during exposing
    for p in player.exposed_cards:
        if player.exposed_cards[p]:
            unguessed_cards.append(player.exposed_cards[p][-1])
    return unguessed_cards


def playing(player: Player, deck: Deck):
    game_round = len(player.played_cards) + 1
    unguessed_cards = get_unguessed_cards(player)
    permutations = generate_permutation(13 - game_round, unguessed_cards, 7)

    # Play min suit
    freq = defaultdict(int)
    for card in player.hand:
        freq[card.suit] += 1

    min_suit = min(freq, key=freq.get)
    # The only cases where this will throw us off 13-0-0-0 [Veryyy unlikely]
    # Other cases where player will lose points > 3 [5-4-4-0, 9-4-0-0, 8-5-0-0, 7-6-0-0]
    # Or always we just sacrifice 1,2 or 3 max points but we get to eliminate 13 cards entirely

    if game_round == 1:
        min_suit_cards = [card for card in player.hand if card.suit == min_suit]
        max_card = max(min_suit_cards, key=lambda card: VAL_TO_NUM[card.value])
        return player.hand.index(max_card)

    # Find most similar permutations to players cards
    card_index = 0
    max_sim = 0
    for i, k in enumerate(player.hand):
        perms = permutations[k]
        sim = len((set(player.hand) & set(perms)) - {k})
        if sim > max_sim:
            card_index = i
            max_sim = sim

    return card_index


def guessing(player: Player, cards, round):
    print("\n Player: ", player.name)
    unguessed_cards = get_unguessed_cards(player)
    permutations = generate_permutation(13 - round, unguessed_cards, 7)
    remaining_cards = []
    for card in cards:
        if (
            card not in set(chain.from_iterable(player.exposed_cards.values()))
            and card not in set(player.hand)
            and card not in set(player.played_cards)
        ):
            remaining_cards.append(card)
    print("Remaining cards for player ", player.name, " : ", remaining_cards)

    if not remaining_cards:
        print("0 remaining at round", round)
        return random.sample(cards, 13 - round)

    if round == 1:
        suit = player.exposed_cards[PARTNERS[player.name]][-1].suit
        MIN_SUIT[player.name] = suit
        # Eliminate suit of card played
        remaining_cards = [card for card in remaining_cards if card.suit != suit]

        # Now we have total max of 26 cards, the most likely suit distribution is 4432
        # Guess 4,4,4 from remaining cards - [TODO: Can I improve using my suit distribution?]
        suit_groups = defaultdict(list)
        for card in remaining_cards:
            suit_groups[card.suit].append(card)

        # Select up to 4 cards. I think there will always be atleast 4 left
        selected_cards = [
            card
            for _, cards in suit_groups.items()
            for card in random.sample(cards, min(4, len(cards)))
        ]
        selected_cards = selected_cards[:12]
        return selected_cards

    remaining_cards = [
        card for card in remaining_cards if card.suit != MIN_SUIT[player.name]
    ]
    prob = {card: (1 / len(remaining_cards)) for card in remaining_cards}

    for i in range(round - 1):
        guess = player.guesses[i]
        c = player.cVals[i]
        remove_prob = []
        for card in prob:
            if card in guess:
                if c == 0:
                    remove_prob.append(card)
                else:
                    prob[card] *= c / len(guess)
            else:
                if len(guess) - c != 0:
                    prob[card] *= (len(guess) - c) / len(guess)
        for card in remove_prob:
            del prob[card]
    most_sim_p = permutations[player.exposed_cards[PARTNERS[player.name]][-1]]
    print("Most Similar Permutation", most_sim_p)

    boost_factor = 2
    for val in most_sim_p:
        if val in prob:
            prob[val] *= boost_factor

    total_weight = sum(prob.values())
    normalized_weights = [val / total_weight for val in prob.values()]
    np.random.seed(7)
    random_indices = np.random.choice(
        np.arange(len(prob.keys())),
        size=13 - round,
        replace=False,
        p=normalized_weights,
    )
    sampled_cards = [list(prob.keys())[i] for i in random_indices]
    return sampled_cards
