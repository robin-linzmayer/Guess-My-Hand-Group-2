import numpy as np
import heapq

# Shared global variables
PARTNERS = {
    "North": "South",
    "East": "West",
    "South": "North",
    "West": "East",
}
SUIT_ORDER = {"Hearts": 0, "Diamonds": 2, "Clubs": 1, "Spades": 3}
VALUE_ORDER = {
    "2": 7,
    "3": 10,
    "4": 4,
    "5": 5,
    "6": 11,
    "7": 3,
    "8": 2,
    "9": 13,
    "10": 6,
    "J": 1,
    "Q": 9,
    "K": 12,
    "A": 8,
}
NUM_GAP_ROUNDS = 6 # Number of rounds that we cluster before max/min
GAPS_NE = None
GAPS_SW = None

def playing(player, deck):
    """
    Playing strategy goes here (what card will the player expose to their partner)
    """
    if not player.hand:
        return None

    print(" ")
    print(f"-------------- Playing: {player.name} -----------------")

    hand_indices = [get_card_index(card) for card in player.hand]
    round = len(player.guesses) + 1

    # Get Gaps
    # Note that we only calculate them once because otherwise they will be unstable between rounds as cards are exposed.
    if round <= NUM_GAP_ROUNDS:
        if round == 1:
            gaps = get_gaps(hand_indices)
            gaps_flat = [item for gap_range in gaps for item in gap_range]
            print(f"Gaps: {gaps_flat}")
            if player.name in ['North', 'East']:
                GAPS_NE = gaps_flat
            else:
                GAPS_SW = gaps_flat

        if player.name in ['North', 'East']:
            card_to_play_index = GAPS_NE[round-1]
        else:
            card_to_play_index = GAPS_SW[round-1]

    # Fall back to Max index strategy
    else:
        card_to_play_index = get_max_card(hand_indices)

    print(f"Card index to play: {card_to_play_index}")
    return card_to_play_index

def use_gap_index(player, g_cards, round):

    guess_indices = [get_card_index(card) for card in g_cards]
    exposed_card_indices = [get_card_index(card) for card in player.exposed_cards[PARTNERS[player.name]]]

    # First round we only have the MAX of a gap. Consequently return only the 12 cards ABOVE that max
    # Reminder that BELOW the MAX is the gap.
    # For example --> the gap (10,1) means that [9,8,...2] are NOT present in our partner's hand. We don't yet know that 2 is the lower bound but directionally guessing 10-22 is better and we have equal information there.
    # Take card exposed by partner and use it to inform the rest of our guesses
    if round == 1:
        max_index = exposed_card_indices[0]
        guess_indices.sort(reverse=True) # Descending
        sample = 13 - round
        values_above_max = [x for x in guess_indices if x > max_index]

        # For example if the max in the range is 18 and only 19, 22 are above, then sample from the lowest numbers.
        if len(values_above_max) < sample:
            looped_values = guess_indices[-(sample - len(values_above_max)):]
            values_below_max = looped_values + values_above_max
        else:
            values_below_max = values_above_max[-sample:]

        return values_below_max

    else:
        if round % 2 == 0:
            guess_indices_minus_gap = remove_multiple_gaps(guess_indices, exposed_card_indices, round)
            return guess_indices_minus_gap

        else:
            guess_indices_minus_gap = remove_multiple_gaps(guess_indices, exposed_card_indices, round-1)
            gap_partial_max = exposed_card_indices[round-1]
            guess_indices_minus_gap = remove_next_largest(guess_indices_minus_gap, gap_partial_max)
            return guess_indices_minus_gap

def remove_multiple_gaps(guess_indices, exposed_card_indices, round):
    guess_indices_minus_gap = guess_indices
    # Iterate over all even numbers and get the pairs of gap bounds from previously exposed cards.
    for e in range(0, round, 2):
        gap_max = exposed_card_indices[e]
        gap_min = exposed_card_indices[e + 1]
        guess_indices_minus_gap = remove_gap(guess_indices_minus_gap, gap_max, gap_min)
    return guess_indices_minus_gap

def remove_gap(list_of_indices, gap_max, gap_min):
    if max > min:
        indices_minus_gap = [x for x in list_of_indices if not gap_min <= x <= gap_max]
    else:
        indices_minus_gap = [x for x in list_of_indices if not (x <= gap_max or x > gap_min)]
    return indices_minus_gap

def remove_next_largest(guess_indices, gap_partial_max):
    # Get the minimum index that is larger than the partial max bound
    larger_than_partial_max = [num for num in guess_indices if num > gap_partial_max]
    if len(larger_than_partial_max) > 0:
        next_largest = min(larger_than_partial_max)
    else:
        next_largest = min(guess_indices)
    return guess_indices.remove(next_largest)

def get_card_index(card):
    """
    This function maps cards to an index and scrambles the index.
    """
    # Hash formula that combines suit and value in a less predictable way
    suit = SUIT_ORDER[card.suit]
    value = VALUE_ORDER[card.value]

    index = suit * 13 + value
    return index

def get_max_card(hand_indices):
    """
    Play card with the highest index to create upper bound value.
    """
    max_index = hand_indices.index(max(hand_indices))
    return max_index

def use_max_value_index(player, g_cards):
    """
    Use the upper bound value strategy to inform guess
    """
    # Take card exposed by partner and use it to inform the rest of our guesses
    partner_exposed_card = player.exposed_cards[PARTNERS[player.name]][-1]
    max_index = get_card_index(partner_exposed_card)

    guess_indices = [get_card_index(card) for card in g_cards]

    index_filter = []
    for i, guess_index in enumerate(guess_indices):
        if guess_index<max_index:
            index_filter.append(i)

    below_max_cards = [g_cards[i] for i in index_filter]
    return below_max_cards

def get_guessable_cards(player, cards):
    # Remove cards that in the player's hand
    g_cards = list(set(cards) - set(player.hand))
    # Remove cards that have been exposed in gameplay
    for _, exposed in player.exposed_cards.items():
        g_cards = list(set(g_cards) - set(exposed))
    return g_cards

def get_card_prob(player, s_cards, round):

    P = 13 - round    # Number of cards in your Partner's hand
    T = len(s_cards)  # Number of cards that could be in partner's hand based on Strategy (all possible cards to build our guess from)
    probs = [1 / T] * T
    print(f"P: {P}, T: {T}")

    if P == T or round == 1:
        return probs

    if player.guesses:
        # Get cValue from previous round
        C = player.cVals[round - 2]  # Minus 2 because first round is skipped so index at Round 2 starts at 0.
        # Remove historical guesses that are no longer valid before calculating probabilities
        guess = player.guesses[round - 2]
        adj_guess = [card for card in guess if card in s_cards]
        G = len(adj_guess) # Number of guesses made that can be used with the cvalue.

        if G == 0:
            return probs

        print(f"Possible cards: {len(s_cards)}, {s_cards}")
        print(f"Guesses: {G}, {adj_guess}")
        print(f"cval: {C}")

        # There are cases where the previous guesses have had cards eliminated to the cvalue given is higher than the number of cards that are possible to include in our guess.
        if C >= G or T <= P:
            prob_guessed_card = 1
            prob_not_guessed_card = 0.001
            total_prob = prob_guessed_card * P
        else:
            prob_guessed_card = C / G  # Probability for each guessed card
            prob_not_guessed_card = (G - C) / (T - P)  # Probability for each unguessed card
            total_prob = prob_guessed_card * P + prob_not_guessed_card * (T - P)

        # Normalize probabilities to ensure they sum to 1
        prob_guessed_card /= total_prob
        prob_not_guessed_card /= total_prob

        # Add these probabilities to a list
        probs = []
        for card in s_cards:
            if card in adj_guess:
                probs.append(prob_guessed_card)
            else:
                probs.append(prob_not_guessed_card)

        # Add a check to ensure the probabilities sum to 1
        total_sum = sum(probs)
        print("total_sum is: " + str(total_sum))
        if total_sum != 1:
            # force to renomrmalize
            probs = [p / total_sum for p in probs]

    return probs

def get_gaps(cards: list[int]) -> list[(int,int)]:
    """
    :param cards: list of integers representing the player's hand

    return an array of length NUM_GAP_ROUNDS / 2 conveying the largest gaps in our hand
    Each value in the array is a tuple (x,y) where x is the value larger than the values in the gap, 
    and y is the value smaller than the values in the gap.
    Note that this is cyclic, so if x < y, then we know that there are no values less than x and 
    no values greater than y.
    """
    num_gaps = int(NUM_GAP_ROUNDS / 2)
    if num_gaps < 1: return []

    gap_dict = {}
    cards.sort()

    for i in range(len(cards)-1):
        card = cards[i]
        next_card = cards[(i+1)%len(cards)]
        gap = (next_card-card)%51
        if i < len(cards)-1:
            # special considerations for "cycle" piece
            gap -= 1

        if gap > 0:
            # if these are not in a row, then there is a gap
            gap_dict[(next_card,card)] = gap
            
    return heapq.nlargest(num_gaps, gap_dict, key=gap_dict.get)

"""
NOTE
  - on first turn we don't have knowledge of a full gap, so we should only guess cards that are less than and close to
    the card that our partner played. To make it more convenient, we can just guess the 12 cards immediately below our partner's
    first played card.

  - after NUM_GAP_ROUNDS number of rounds, we switch back to a min/max playing strategy.

  - at ODD TURNS we have info about full gaps and info about the top bound of a new gap. We can safely eliminate the card
    immediately below that top bound. Is it useful to eliminate more than 1? Can make that a parameter.

TODO [HANITA]:
  - get_gaps takes in player.hand and returns the NUM_GAP_ROUNDS / 2 gaps in descending length order

TODO [ROBIN]:
  - Implement the elimination of those cards by the guesser
"""

def guessing(player, cards, round):
    """
    Guessing strategy based on ranking guessable cards from highest to lowest probability 
    and selecting top N guesses.

    :param player: The Player object.
    :param cards: List of all Card objects in the game.
    :param round: Integer representing the current round number.
    :return: List of guessed Card objects.
    """
    print(" ")
    print(f"-------------- Guessing: {player.name}, Round: {round} -----------------")

    # Determine the number of guesses needed
    num_guesses = 13 - round
    print(f"Round {round}: Number of guesses needed: {num_guesses}")

    if num_guesses <= 0:
        print(f"Round {round}: No guesses needed.")
        return []

    # Remove cards from list that are not valid guesses for this round.
    g_cards = get_guessable_cards(player, cards)
    print(f"Round {round}: Guessable cards after filtering: {g_cards}")

    # Apply strategy to narrow possible cards
    if round <= NUM_GAP_ROUNDS:
        s_cards = use_gap_index(player, g_cards, round)
    else:
        s_cards = use_max_value_index(player, g_cards)
    print(f"Round {round}: Cards after applying max value index strategy: {s_cards}")

    if not s_cards:
        print(f"Round {round}: No guessable cards available after applying strategy.")
        return []

    # Update probability of possible cards
    p_cards = get_card_prob(player, s_cards, round)
    print(f"Round {round}: Probabilities of guessable cards: {p_cards}")

    if not p_cards or len(p_cards) != len(s_cards):
        print(f"Round {round}: Invalid probability distribution. Assigning uniform probabilities.")
        p_cards = [1 / len(s_cards)] * len(s_cards)

    # Pair each card with its probability
    card_prob_pairs = list(zip(s_cards, p_cards))

    # Sort the pairs based on probability in descending order
    sorted_pairs = sorted(card_prob_pairs, key=lambda pair: pair[1], reverse=True)
    print(f"Round {round}: Sorted guessable cards by probability: {sorted_pairs}")

    # Select the top N cards based on the current round
    selected_guesses = [card for card, prob in sorted_pairs[:num_guesses]]
    print(f"Round {round}: Selected guesses: {selected_guesses}")

    return selected_guesses

