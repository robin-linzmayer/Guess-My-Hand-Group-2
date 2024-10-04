import random
import numpy as np
from CardGame import Card, Deck, Player

# G7 is the best

<<<<<<< HEAD
<<<<<<< HEAD
flag = 0
card_probability = {}   # dictionary to store the probability of each card in the deck
for i in range(2, 15):
    card_probability[i] = 1 / 13  # Initialize each card's probability
=======
=======
>>>>>>> 66d82f1 (Added c based updates)

SUITS = ["Clubs", "Diamonds", "Hearts", "Spades"]
VALUES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
NUM_CARDS = len(SUITS) * len(VALUES)
CARD_PROBABILITIES = {num:1/39 for num in range(NUM_CARDS)}

# Create a dictionary that maps 0-51 to (value, suit)
NUM_TO_CARD = {
    i: (SUITS[i // 13], VALUES[i % 13])  # i % 13 gives the card value, i // 13 gives the suit
    for i in range(NUM_CARDS)
}

REV_CARD_TO_NUM = {value:key for key, value in NUM_TO_CARD.items()}
<<<<<<< HEAD
>>>>>>> 2b381cd (Probability logic complete, seems to not work because of bad object implementation in the game)
=======
=======
# Aaaumptions:

# guessed_cards is a dict mapping turn number/round number -> player -> list of guessed cards that turn
# probability dict map indexed based on certain ordering -> probability of it being in your partners hand. 

def update_prob_based_on_correct_answers(probability_dict, guessed_cards, correct_answers):
    """
    Updates the probabilities for the cards in the guessed_cards list.

    Args:
        probability_dict (dict): A dictionary where keys are integers (0-51) representing cards
                                and probabilities.
        guessed_cards (list): A list of card indices representing the guessed cards.
        
    Returns:
        None: The probability_dict is updated in-place.
    """

    perc_correct = correct_answers / len(guessed_cards)  # Factor to boost guessed cards
    perc_wrong =  1 - perc_correct

    for card in guessed_cards:
            probability_dict[card] *= perc_correct

    non_guessed_cards = [card for card in probability_dict if card not in guessed_cards]

    for card in non_guessed_cards:
        probability_dict[card] *= perc_wrong

    normalize(probability_dict)

def normalize(probability_dict):
    total_prob = sum(probability_dict.values())
    if total_prob > 0:
        for card in probability_dict:
            probability_dict[card] /= total_prob
>>>>>>> 3ae8532 (Added c based updates)
>>>>>>> 66d82f1 (Added c based updates)

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

<<<<<<< HEAD

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
=======
def normalize_probabilities():
    total = sum(CARD_PROBABILITIES.values())
    if total > 0:
        for card in CARD_PROBABILITIES:
            CARD_PROBABILITIES[card] /= total
    else:
        # This is after all the cards have been played - so no exception
        CARD_PROBABILITIES[0] = 1

def zero_probabilities(cards):
    for card in cards:
        suit = card.suit
        val = card.value
        num = REV_CARD_TO_NUM[(suit, val)]
        CARD_PROBABILITIES[num] = 0.0
    normalize_probabilities()


def guessing(player, cards, round):
    if round == 1:
        global CARD_PROBABILITIES
        CARD_PROBABILITIES = {num:1/39 for num in range(NUM_CARDS)}
        zero_probabilities(player.hand)
        
    normalize_probabilities()
    
    exposed_cards = [i for j in list(player.exposed_cards.values()) for i in j]
    zero_probabilities(exposed_cards)
    zero_probabilities(player.played_cards)

    choice = np.random.choice(
        list(CARD_PROBABILITIES.keys()),
        13 - round,
        p=list(CARD_PROBABILITIES.values()),
        replace=False)
    card_choices = [NUM_TO_CARD[card] for card in choice]
    card_choices_obj = [Card(card[0], card[1]) for card in card_choices]
    return card_choices_obj
    return random.sample(cards, 13 - round)
>>>>>>> 2b381cd (Probability logic complete, seems to not work because of bad object implementation in the game)
