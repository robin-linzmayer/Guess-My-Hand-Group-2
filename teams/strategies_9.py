import random

"""
PLAYER CLASS VARIABLES

self.name = name
self.hand = []
self.played_cards = []
self.strategy = strategy
self.exposed_cards = {"North": [], "East": [], "South": [], "West": []}
self.cVals = []
"""

"""
CARDS CLASS VARIABLES

self.suit = suit
self.value = value
self.map = {"Hearts": "♥", "Diamonds": "♦", "Clubs": "♣", "Spades": "♠"}
self.rmap = {"♥": "Hearts", "♦": "Diamonds", "♣": "Clubs", "♠": "Spades"}
"""

"""
DECK CLASS VARIABLES

self.suits = ["Hearts", "Diamonds", "Clubs", "Spades"] 
self.values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
self.cards = [Card(suit, value) for suit in self.suits for value in self.values]
"""

# Use to get card value with order 2 to A
card_val = {
    '2' : 1,
    '3' : 2,
    '4' : 3,
    '5' : 4,
    '6' : 5,
    '7' : 6,
    '8' : 7,
    '9' : 8,
    '10' : 9,
    'J' : 10,
    'Q' : 11,
    'K' : 12,
    'A' : 13,
}
# Use to get teammate of current player
teammate = {
    "North" : "South",
    "South" : "North",
    "East" : "West",
    "West" : "East",
}

# Use to get anti-suit
anti_suit = {
    "Hearts" : "Diamonds",
    "Diamonds" : "Hearts",
    "Spades" : "Clubs",
    "Clubs" : "Spades",
}

def playing(player, deck):
    """
    Greedy Suit Strategy
    """
    if not player.hand:
        return None
    
    return 0

def guessing(player, cards, round):
    """
    Guesses the Anti-Suit based on teammate's exposed card
    """
    num_of_guesses = 13 - round
    teammate_suit = player.exposed_cards[teammate[player.name]][-1].suit
    potential_guesses = [card for card in cards if card.suit == anti_suit[teammate_suit]] # All 13 cards of the teammate_suit
    potential_guesses.sort(key=lambda x:card_val[x.value])

    # val_check_arr = []
    # for card in potential_guesses:
    #     val_check_arr.append(card.value)
    # print(val_check_arr)
    
    # # Remove from potential_guesses if in our own hand 
    # for card in player.hands:
    #     if card in potential_guesses:
    #         potential_guesses.remove(card)

    # # Remove from potential_guesses if it has been played
    # for card in player.exposed_cards.values():
    #     if card in potential_guesses:
    #         potential_guesses.remove(card)

    return potential_guesses[:-1]
