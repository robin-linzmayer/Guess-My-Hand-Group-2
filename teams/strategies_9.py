import random
from collections import defaultdict, deque

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

teammate_max = ''

# Use to get anti-suit
# anti_suits  = {
#     "Spades" : "Diamonds",
#     "Clubs" : "Spades",
#     "Hearts" : "Clubs",
#     "Diamonds" : "Hearts",
# }

# anti_suit_guess = deque(['Diamonds', 'Hearts,', 'Clubs', 'Spades'])

def playing(player, deck):
    """
    Greedy Suit Strategy
    """
    if not player.hand:
        return None
    
    hand = defaultdict(list)
    for card in player.hand:
        hand[card.suit].append(card.value)

    max_suit = max(hand, key=lambda key : len(hand[key]))
    # print(max_suit, hand[max_suit])

    # improve to min-max
    if len(hand[max_suit]) == len(player.hand):
        play_value = min(hand[max_suit])
        play_card = [idx for idx in range(len(player.hand)) if player.hand[idx].value == play_value and player.hand[idx].suit == max_suit][0]
        return play_card

    anti_suits = deque(['Spades', 'Clubs', 'Hearts', 'Diamonds'])
    # print(abs(anti_suits.index(max_suit) - len(anti_suits)))
    # print(anti_suits)
    anti_suits.rotate(abs(anti_suits.index(max_suit) - (len(anti_suits) - 1)))
    # print(anti_suits)
    anti_suit = anti_suits[0]
    # print(max_suit, anti_suit)

    play_card = -1
    while play_card < 0:
        if hand[anti_suit]:
            play_value = min(hand[anti_suit])
            play_card = [idx for idx in range(len(player.hand)) if player.hand[idx].value == play_value and player.hand[idx].suit == anti_suit][0]
            # print(play_card)
        else:
            anti_suits.rotate(-1)
            anti_suit = anti_suits[0]

    return play_card

def guessing(player, cards, round):
    """
    Guesses the Anti-Suit based on teammate's exposed card
    """
    num_of_guesses = 13 - round
    teammate_suit = player.exposed_cards[teammate[player.name]][0].suit
    anti_suits = deque(['Diamonds', 'Hearts', 'Clubs', 'Spades'])
    anti_suits.rotate(abs(anti_suits.index(teammate_suit) - (len(anti_suits) - 1)))
    # if not player.cVals:
    #     anti_suit = anti_suits[0]
    #     teammate_max = anti_suit
    # elif player.cVals[-1] == 0:
    #     anti_suits.rotate(round - 1)
    #     anti_suit = anti_suits[0]
    #     teammate_max = anti_suit
    # else:
    #     anti_suit = anti_suits[0]
    #     teammate_max = anti_suit
    if player.cVals and player.cVals[-1] == 0:
        anti_suits.rotate(round - 1)
        anti_suit = anti_suits[0]
        teammate_max = anti_suit
    else:
        anti_suit = anti_suits[0]
        teammate_max = anti_suit



        
    # print(teammate_suit, anti_suit)
    potential_guesses = [card for card in cards if card.suit == teammate_max] # All 13 cards of the teammate_suit
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

    return potential_guesses[:-round]
