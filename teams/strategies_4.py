import random
from itertools import chain
from collections import defaultdict
import numpy as np
from CardGame import Card, Player, Deck

PLAYERS = {"North", "South", "East", "West"}

PARTNERS = {
    "North": "South",
    "East": "West",
    "South": "North",
    "West": "East",
}

OPPONENTS = {
    "North": ["East", "West"],
    "South": ["East", "West"],
    "East": ["North", "South"],
    "West": ["North", "South"],
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

MIN_SUIT = {player: -1 for player in PLAYERS}

DECK = [Card(suit, value) for suit in SUIT_TO_NUM.keys() for value in VAL_TO_NUM.keys()]


def generate_permutation(perm_size, cards, seed):
    """Generates a permutation dictionary, each card points to one permutation"""
    perms = {}
    for i in cards:
        random.seed(seed)
        perms[i] = random.sample(cards, perm_size)
    return perms


def get_unguessed_cards(player):
    """Get all cards that have not been guessed by the player."""
    exposed_set = set(chain.from_iterable(player.exposed_cards.values())) | set(player.played_cards)
    unguessed_cards = [card for card in DECK if card not in exposed_set]

    # Add the last exposed card from each player
    # North sees no exposed cards when playing - Worst case!
    unguessed_cards.extend(p[-1] for p in player.exposed_cards.values() if p)
    return unguessed_cards


def get_suit_frequencies(hand):
    """Get the count of cards in each suit."""
    freq = defaultdict(int)
    for card in hand:
        freq[card.suit] += 1
    return freq


def update_c_vals_and_guesses(player):
    """Update cvals based on correct and incorrect guesses from exposed cards."""
    cvals = player.cVals.copy()
    guesses = player.guesses.copy()

    for i, guess in enumerate(guesses):
        guessed = [g for g in guess if g in player.exposed_cards[PARTNERS[player.name]]]
        wrongly_guessed = [
            g
            for g in guess
            if g
            in chain.from_iterable(
                player.exposed_cards[op] for op in OPPONENTS[player.name]
            )
        ]

        cvals[i] -= len(guessed)
        guesses[i] = [g for g in guess if g not in guessed and g not in wrongly_guessed]
    return cvals, guesses


def get_remaining_cards(player, all_cards):
    """Returns a list of cards not exposed, played, or in hand."""
    exposed_set = (
        set(chain.from_iterable(player.exposed_cards.values()))
        | set(player.hand)
        | set(player.played_cards)
    )
    remaining_cards = [card for card in all_cards if card not in exposed_set]

    print(f"Remaining cards for player {player.name}: {remaining_cards}")
    return remaining_cards


def group_cards_by_suit(cards):
    """Group cards by suit."""
    suit_groups = defaultdict(list)
    for card in cards:
        suit_groups[card.suit].append(card)
    return suit_groups


def round_1_strategy(player, remaining_cards):
    """Eliminate the cards of min suit and return 4 cards from other suits."""
    suit = player.exposed_cards[PARTNERS[player.name]][-1].suit
    MIN_SUIT[player.name] = suit

    remaining_cards = [card for card in remaining_cards if card.suit != suit]
    suit_groups = group_cards_by_suit(remaining_cards)

    selected_cards = [
        card
        for _, cards in suit_groups.items()
        for card in random.sample(cards, min(4, len(cards)))
    ]
    return selected_cards[:12]


def update_probabilities_from_c_vals(player, probabilities):
    """Update probabilities of remaining cards based on c values and guess history."""
    cvals, guesses = update_c_vals_and_guesses(player)
    prob = probabilities.copy()

    for i, guess in enumerate(guesses):
        c = cvals[i]

        # Remove cards whose c_val was 0
        prob = {
            card: value
            for card, value in prob.items()
            if card not in guess or player.cVals[i] != 0
        }

        for card in prob:
            if card in guess:
                if c == len(guess):  # All cards are right
                    prob[card] *= 10
                elif c > (len(guess) // 2) + 1:  # More than half are right
                    prob[card] *= 5 * (c / len(guess))
                else:  # Boost by c/len(guess)
                    prob[card] *= c / len(guess)
            else:  # Boost unguessed cards
                if len(guess) - c:
                    prob[card] *= (len(guess) - c) / len(guess)
    return prob


def update_probabilities_for_min_max(prob, last_exposed, game_round):
    """Remove cards < min and > max alternating on game rounds."""
    threshold = VAL_TO_NUM[last_exposed.value]
    return {
        card: value
        for card, value in prob.items()
        if not (
            (game_round % 2 != 0 and VAL_TO_NUM[card.value] > threshold)
            or (game_round % 2 == 0 and VAL_TO_NUM[card.value] < threshold)
        )
    }


def playing(player: Player, deck: Deck):
    """If game_round =1: Play min suit
    game_round <=10: Alternate between min and max cards
    game_round >10: Play most similar card from permutaion
    """
    game_round = len(player.played_cards) + 1

    if game_round == 1:
        freq = get_suit_frequencies(player.hand)
        min_suit = min(freq, key=freq.get)
        max_card_in_min_suit = max(
            [card for card in player.hand if card.suit == min_suit],
            key=lambda card: VAL_TO_NUM[card.value],
        )
        return player.hand.index(max_card_in_min_suit)

    if game_round <= 10:
        return (
            player.hand.index(min(player.hand, key=lambda card: VAL_TO_NUM[card.value]))
            if game_round % 2 == 0
            else player.hand.index(
                max(player.hand, key=lambda card: VAL_TO_NUM[card.value])
            )
        )

    unguessed_cards = get_unguessed_cards(player)
    permutations = generate_permutation(13 - game_round, unguessed_cards, 7)
    card_index = 0
    max_sim = 0
    for i, k in enumerate(player.hand):
        perms = permutations[k]
        sim = len((set(player.hand) & set(perms)) - {k})
        if sim > max_sim:
            card_index = i
            max_sim = sim
    return card_index


def guessing(player: Player, cards, game_round):
    """Returns a set of cards guessed at each game round."""
    print(f"\nPlayer: {player.name}")

    unguessed_cards = get_unguessed_cards(player)
    permutations = generate_permutation(13 - game_round, unguessed_cards, 7)

    remaining_cards = get_remaining_cards(player, cards)
    if not remaining_cards:
        print(f"0 cards remaining at game round {game_round}")
        return random.sample(cards, 13 - game_round)

    if game_round == 1:
        return round_1_strategy(player, remaining_cards)

    # Adjust probabilities of min suit
    prob = {
        card: (1 / len(remaining_cards))
        * (0.0013 if card.suit == MIN_SUIT[player.name] else 1)
        for card in remaining_cards
    }
    prob = update_probabilities_from_c_vals(player, prob)

    if game_round <= 10:
        prob = update_probabilities_for_min_max(
            prob, player.exposed_cards[PARTNERS[player.name]][-1], game_round
        )
    else:
        most_sim_p = permutations[player.exposed_cards[PARTNERS[player.name]][-1]]
        print("Most Similar Permutation", most_sim_p)
        for val in most_sim_p:
            if val in prob:
                prob[val] *= 1.1  # Boosting by 1.1

    normalized_weights = np.array(list(prob.values())) / sum(prob.values())
    np.random.seed(7)

    random_indices = np.random.choice(
        len(prob), size=13 - game_round, replace=False, p=normalized_weights
    )
    sampled_cards = [list(prob.keys())[i] for i in random_indices]
    return sampled_cards
