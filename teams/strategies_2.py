import numpy as np

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

def playing(player, deck):
    """
    Playing strategy goes here (what card will the player expose to their partner)
    """
    if not player.hand:
        return None

    print(" ")
    print(f"-------------- Playing: {player.name} -----------------")

    hand_indices = [get_card_index(card) for card in player.hand]
    card_to_play_index = get_max_card(hand_indices)
    return card_to_play_index

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

def get_card_prob(player, g_cards, round):

    # Get constants
    G = 13 - round  # Number of guesses / cards in your partner's hand
    T = len(g_cards)  # Number of cards that are possible guesses

    # Calculate probabilities for different rounds
    if round == 1:
        # First round we won't have any information about previous guesses

        ########### Tom (10/8):
        #even_prob = (G / T) / T
        #probs = [even_prob] * T
        probs = [1 / T] * T
        #### Tom last line ###

    elif round == 12:
        print(f"guesses: {player.guesses[round-2]}")
        print(f"cval: {player.cVals[round-2]}")
    else:
        #todo - Make this work for more than just the previous round of guesses
        probs = []
        C = player.cVals[round-2] # Minus 2 because first round is skipped so index at Round 2 starts at 0.
        guesses = player.guesses[round-2]

        ######### Tom (10/8):
        # prob_guessed_card = (C / G) / G
        # prob_not_guessed_card = ((G - C) / (T - G)) / (T - G)
        prob_guessed_card = C / (G + 1)  # Probability for each guessed card
        prob_not_guessed_card = (G + 1 - C) / (T - G)  # Probability for each unguessed card

        # Normalize probabilities to ensure they sum to 1
        total_prob = prob_guessed_card * G + prob_not_guessed_card * (T - G)
        prob_guessed_card /= total_prob
        prob_not_guessed_card /= total_prob
        ### Tom last line ###


        for card in g_cards:
            if card in guesses:
                probs.append(prob_guessed_card)
            else:
                probs.append(prob_not_guessed_card)

        ######### Tom (10/8):
        # Add a check to ensure the probabilities sum to 1
        total_sum = sum(probs)
        print("total_sum is: " + str(total_sum))
        if total_sum != 1:
            # force to renomrmalize
            probs = [p / total_sum for p in probs]
        ### Tom last line ###

    return probs

def guessing(player, cards, round):
    """
    Guessing strategy goes here (number of guesses of your partner's cards)
    """
    print(" ")
    print(f"-------------- Guessing: {player.name}, Round: {round} -----------------")

    # Remove cards from list that are not valid guesses for this round.
    g_cards = get_guessable_cards(player, cards)

    # Apply strategy to narrow possible cards
    s_cards = use_max_value_index(player, g_cards)

    # Update probability of possible cards
    p_cards = get_card_prob(player, s_cards, round)

    # Sample cards based on their computed probabilities
    return np.random.choice(s_cards, p=p_cards, size=13 - round, replace=False)



