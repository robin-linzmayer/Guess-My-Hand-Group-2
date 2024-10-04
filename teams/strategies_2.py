import random
from CardGame import Deck

PARTNERS = {
    'North': 'South',
    'East': 'West',
    'South': 'North',
    'West': 'East',
}

deck = Deck()
RANKED_CARD_VALUES = deck.values

def playing(player, deck):
    """
    Playing strategy goes here (what card will the player expose to their partner)
    """
    if not player.hand:
        return None

    # Todo set lower bound (maybe on suit?) to get a smaller range for guessing.
    card_to_play = get_max_value_index(player)
    print("Play: ", card_to_play)
    return card_to_play

def get_max_value_index(player):
    """
    Play card to create upper bound value.
    """
    max_index = 0
    max_value = -1

    for i, card in enumerate(player.hand):
        value = RANKED_CARD_VALUES.index(card.value)
        if value > max_value:
            max_value = value
            max_index = i
    return max_index

def use_max_value_index(exposed_card, guess_deck, round):
    """
    Use the upper bound value strategy to inform guess
    """
    print(f"Exposed Card: {exposed_card}")
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

    # Todo this would be improved by guessing all suits of that max value of the card that our partner exposed (since it is asserting that they have at least one card to set that max).

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

def get_partner_exposed_card(player):
    return player.exposed_cards[PARTNERS[player.name]][-1]

def guessing(player, cards, round):
    """
    Guessing strategy goes here (number of guesses of your partner's cards)
    """
    print(" ")
    print(f"Player: {player.name}")
    
    ############### Tom (10/3):
    if round == 1: # The initial round
        create_card_dictionary(cards) # Initialize the dictionary
        for idx, value in guesser_card_dict.items():
            print(f"Index {idx}: {value[0]}, numerator={value[1]}, denominator={value[2]}, is_certain={value[3]}, is_in_partner_hand={value[4]}")
    ###########################
    
    guess_deck = get_guess_deck(player, cards)
    exposed_card = get_partner_exposed_card(player)

    # Partner player's exposed card is used as an upper bound for values to guess from.
    guesses = use_max_value_index(exposed_card, guess_deck, round)

    print(player.cVals, sum(player.cVals))
    return guesses


################################################################################################################### Tom (10/3):
guesser_card_dict = {}

def hash_card_index(card):
    """
    This function maps cards to an index and scrambles the index.
    """
    suit_order = {"Hearts": 0, "Diamonds": 2, "Clubs": 1, "Spades": 3}
    value_order = {"2": 7, "3": 10, "4": 4, "5": 5, "6": 11, "7": 3, "8": 2, "9": 13, "10": 6, "J": 1, "Q": 9, "K": 12, "A": 8}
    
    # Hash formula that combines suit and value in a less predictable way
    suit = suit_order[card.suit]
    value = value_order[card.value]
    
    index = suit * 13 + value
    
    return index

def create_card_dictionary(deck):
    """
    This function takes in a deck of cards and fills in a dictionary where:
    - Key: The scrambled index from hash_card_index
    - Value: A list:
    [card in Card, numerator in int, denominator in int, is_certain in boolean, is_in_partner_hand in bool2]    
    """
    counter=0
    for card in deck:
        index = hash_card_index(card)
        guesser_card_dict[index] = [card, 1, 52, False, False]  # Initializing with 2 integers and 2 booleans
        counter += 1
    return 1
##############################################################################################################

