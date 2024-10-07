import random
from CardGame import Deck

shuffled_card_dict = {}
PARTNERS = {
    'North': 'South',
    'East': 'West',
    'South': 'North',
    'West': 'East',
}

previous_guesses = []  # Global variable to keep track of previous guesses

def playing(player, deck):
    """
    Playing strategy goes here (what card will the player expose to their partner)
    """
    if not player.hand:
        return None
    print(" ")
    print(f"-------------- Playing: {player.name} -----------------")
    # First round of the game the cards in the player's hand need to be added to our shuffled dictionary so the mapped
    # index can be used by our strategy.
    if len(player.hand) == 13:
        create_shuffled_card_dict(player.hand, True)

    in_hand_dict = {key: value for key, value in shuffled_card_dict.items() if value['is_in_hand']}
    # Strategy
    print("XXX", len(in_hand_dict))
    card_to_play = get_max_card(in_hand_dict)
    # Need to return the index of the card to play from the player's hand
    return player.hand.index(card_to_play)

def create_shuffled_card_dict(cards, is_in_hand):
    """
    This function takes in a deck of cards and fills in a dictionary where:
    - Key: The scrambled index from hash_card_index
    - Value: dict
    """
    for card in cards:
        index = shuffle_card_index(card)
        # Check to only initialize a card once
        if index not in shuffled_card_dict.keys():
            if is_in_hand:
                shuffled_card_dict[index] = {
                    'card': card,
                    'is_in_hand': is_in_hand,
                    'is_certain': True,
                    'is_in_partner_hand': False,
                    'has_been_exposed': False,
                }
            else:
                shuffled_card_dict[index] = {
                    'card': card,
                    'numer': int(1),
                    'denom': int(39),
                    'is_in_hand': is_in_hand,
                    'is_certain': False,
                    'is_in_partner_hand': False,
                    'has_been_exposed': False,
                }
    return

def shuffle_card_index(card):
    """
    This function maps cards to an index and scrambles the index.
    """
    suit_order = {"Hearts": 0, "Diamonds": 2, "Clubs": 1, "Spades": 3}
    value_order = {"2": 7, "3": 10, "4": 4, "5": 5, "6": 11, "7": 3, "8": 2, "9": 13, "10": 6, "J": 1, "Q": 9, "K": 12,
                   "A": 8}

    # Hash formula that combines suit and value in a less predictable way
    suit = suit_order[card.suit]
    value = value_order[card.value]

    index = suit * 13 + value
    return index

def get_max_card(in_hand_dict):
    """
    Play card with the highest index to create upper bound value.
    """
    max_index = max(in_hand_dict.keys())
    in_hand_dict[max_index]['has_been_exposed'] = True
    max_card = in_hand_dict[max_index]['card']
    return max_card


############################
def get_partner_exposed_card(player):
    return player.exposed_cards[PARTNERS[player.name]][-1]

def update_exposed_cards(exposed_cards):
    # exposed_cards = {"North": [], "East": [], "South": [], "West": []}
    # Update every has_been_exposed value in shuffled_card_dict
    for player, cards in exposed_cards.items():
        for card in cards:
            shuffled_card_dict = {k: {**v, 'is_in_hand': True} if v['card'] == card else v for k, v in shuffled_card_dict.items()}

def remove_impossible_guesses():
    guess_dict = {key: value for key, value in shuffled_card_dict.items() if not value['is_in_hand']}
    guess_dict = {key: value for key, value in guess_dict.items() if not value['has_been_exposed']}
    return guess_dict

def guessing(player, cards, round):
    """
    Guessing strategy goes here (number of guesses of your partner's cards)
    """
    print(" ")
    print(f"-------------- Guessing: {player.name} -----------------")

    # Initialize cards into the shuffled_card_dict
    if round == 1:  # The initial round
        create_shuffled_card_dict(cards)  # Initialize the dictionary
    # Update probability of existing cards
    else:
        # After receiving the c_value from the previous round
        if player.cVals:
            c_value = player.cVals[-1]  # Get the last c_value
            # Update the list of total possible cards (K)
            total_possible_cards = len(shuffled_card_dict)
            # Calculate the partner's current unexposed hand size (M)
            partner_hand_size = 13 - (round - 1)  # Since partner exposes one card each round
            # UNDO comment below
            # update_probabilities(previous_guesses, c_value, total_possible_cards, partner_hand_size)
            # Print updated probabilities
            print("Updated Probabilities:")
            # Sort probabilities in descending order
            sorted_probs = sorted(
                ((value[0], value[1] / value[2]) for value in shuffled_card_dict.values()),
                key=lambda x: -x[1]
            )
            for card, prob in sorted_probs:
                print(f"{card}: {prob:.4f}")


    update_exposed_cards(player.exposed_cards)
    print("Number of cards to guess from: ", len(shuffled_card_dict))
    guess_dict = remove_impossible_guesses()
    print("Number of cards to guess from: ", len(guess_dict))

    exposed_card = get_partner_exposed_card(player)

    # Partner player's exposed card is used as an upper bound for values to guess from.
    guesses = use_max_value_index(exposed_card, guess_dict, round)

    print(player.cVals, sum(player.cVals))
    return guesses


def use_max_value_index(exposed_card, not_in_hand_dict, round):
    """
    Use the upper bound value strategy to inform guess
    """
    # Get ranked value index of the card your partner exposed
    for index, value in enumerate(RANKED_CARD_VALUES):
        if value == exposed_card.value:
            print(f"Value exposed as upper bound: {value} with the index of {index}")
            max_value_index = index
            break

    possible_values = RANKED_CARD_VALUES[:max_value_index + 1]
    print(f"Remaining possible values: {possible_values}")
    for card in guess_deck:
        if card.value not in possible_values:
            guess_deck.remove(card)
            print(f"Removed {card}")

    return random.sample(guess_deck, 13 - round)

def get_guess_deck(player, cards):
    """
    This function takes in the list of all cards in the game and removes cards that would be illogical guesses.
    Illogical guesses include:
        - Cards in the players own hand
        - Cards that have been exposed by other players in the game

    :param player:
    :param cards: list[Card]
    :return: list[Card]
    """
    # Remove cards in player's hand
    guess_deck = set(cards) - set(player.hand)
    # Remove cards that have been exposed
    for _, exposed_cards in player.exposed_cards.items():
        if len(exposed_cards) > 0:
            guess_deck = guess_deck - set(exposed_cards)
    return list(guess_deck)






def update_probabilities(guesses, c_value, total_possible_cards, partner_hand_size):
    N = len(guesses)  # Number of guesses made in the previous round
    K = total_possible_cards  # Total possible cards that could be in partner's hand
    M = partner_hand_size  # Partner's current unexposed hand size after exposing a card
    C = c_value  # Number of correct guesses

    if N == 0 or K - N == 0:
        print("Division by zero encountered in update_probabilities.")
        return

    guessed_card_factor = C / N
    unguessed_card_factor = (M - C) / (K - N)

    total_probability = 0  # To accumulate total probability for normalization

    for index, value in shuffled_card_dict.items():
        card = value[0]
        old_prob = value[1] / value[2] if value[2] != 0 else 0

        if card in guesses:
            new_prob = old_prob * guessed_card_factor
        else:
            new_prob = old_prob * unguessed_card_factor

        value[1] = new_prob
        value[2] = 1

        total_probability += new_prob

    # Normalize probabilities so that they sum to M (current partner hand size)
    if total_probability == 0:
        print("Total probability is zero after updates. Cannot normalize probabilities.")
        return

    normalization_factor = M / total_probability

    for index, value in shuffled_card_dict.items():
        prob = value[1] / value[2]
        normalized_prob = prob * normalization_factor
        value[1] = normalized_prob  # Update numerator with normalized probability
        value[2] = 1  # Denominator remains 1