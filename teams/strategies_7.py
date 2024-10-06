import random

# G7 is the best

flag = 0
card_probability = {}   # dictionary to store the probability of each card in the deck
for i in range(2, 15):
    card_probability[i] = 1 / 13  # Initialize each card's probability

def playing(player, deck):

    global flag
    if flag == 0:
        flag = 1
        return max_first(player, deck)
    else:
        flag = 0
        return min_first(player, deck)
    

def guessing(player, cards, round):
    return random.sample(cards, 13 - round)




def max_first(player, deck):
    """
    Max First strategy.
    
    This strategy always plays the highest-value card in the player's hand.
    
    Parameters:
    player (Player): The current player object.
    deck (Deck): The current deck object.
    
    Returns:
    int or None: The index of the card to be played, or None if no card can be played.
    """
    if not player.hand:
        return None
    
    value_order = deck.values
    max_index = 0
    max_value = -1
    
    for i, card in enumerate(player.hand):
        value = value_order.index(card.value)
        if value > max_value:
            max_value = value
            max_index = i
    
    return max_index


def min_first(player, deck):
    """
    Min First strategy.
    
    This strategy always plays the lowest-value card in the player's hand.
    
    Parameters:
    player (Player): The current player object.
    deck (Deck): The current deck object.
    
    Returns:
    int or None: The index of the card to be played, or None if no card can be played.
    """
    if not player.hand:
        return None
    
    value_order = deck.values
    min_index = 0
    min_value = len(value_order)
    
    for i, card in enumerate(player.hand):
        value = value_order.index(card.value)
        if value < min_value:
            min_value = value
            min_index = i
    
    return min_index


def update_card_probablities(player, cards, round):
    """
    Update the probability of each card in the deck.
    """

    full_deck_size = 52
    
    global card_probability

    remaining_cards = full_deck_size - len(player.played_cards) - len(player.hand)

    for card in player.played_cards:
        card_probability[card] = 0

    for card in player.hand:
        card_probability[card] = 0

    # else, set its probability to 1 / # of cards remaining in the deck
    for key in card_probability:
        if key not in player.played_cards:
            card_probability[key] = 1 / remaining_cards


    for key in card_probability:
        card_probability[key] = 1 / 13