from collections import defaultdict, deque
from CardGame import Card, Deck, Player
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
    '2' : 0,
    '3' : 1,
    '4' : 2,
    '5' : 3,
    '6' : 4,
    '7' : 5,
    '8' : 6,
    '9' : 7,
    '10' : 8,
    'J' : 9,
    'Q' : 10,
    'K' : 11,
    'A' : 12,
}
# Use to shift card value
card_shift = {
    '2' : '3',
    '3' : '4',
    '4' : '5',
    '5' : '6',
    '6' : '7',
    '7' : '8',
    '8' : '9',
    '9' : '10',
    '10' : 'J',
    'J' : 'Q',
    'Q' : 'K',
    'K' : 'A',
    'A' : 'A',
}
# Use to get suit value
suit_val = {
    'Spades' : 0,
    'Clubs' : 1,
    'Hearts' : 2,
    'Diamonds' : 3,
}

# Use to get teammate of current player
teammate = {
    "North" : "South",
    "South" : "North",
    "East" : "West",
    "West" : "East",
}

teammate_max = ''
player_guesses = {
    'North' : [],
    'East' : [],
    'South' : [],
    'West' : []
}

# Use to get anti-suit
# anti_suits  = {
#     "Spades" : "Diamonds",
#     "Clubs" : "Spades",
#     "Hearts" : "Clubs",
#     "Diamonds" : "Hearts",
# }

# anti_suit_guess = deque(['Diamonds', 'Hearts,', 'Clubs', 'Spades'])

def check_possible(card, player):
    return (card not in player.hand) and (card not in [card for cards in player.exposed_cards.values() for card in cards])

def shuffle(player, deck, seed):
    exposed_cards = [card for cards in player.exposed_cards.values() for card in cards]
    left_cards = list(set(deck.cards) - set(exposed_cards))
    original_cards = left_cards.copy()
    
    # Shuffle left_cards using the provided seed for consistency
    random.seed(seed)
    random.shuffle(left_cards)
    
    # TODO
    mapping = 0
    
    return mapping

# Converts a card to the index in card_probability
# def card_to_index (suit, val):
#     return (13 * suit_val[suit]) + card_val[val]
# Use to get the current probability of guessing a card
# Keys: Card Object, Val : 1/52

# Remove cards from player.hand in card_probability 
def remove_cards_from_hand(player, card_probability):
    for card in player.hand:
        if card in card_probability:
            del card_probability[card]

# Remove cards from exposed cards in card_probability 
def remove_cards_from_exposed_cards(player, card_probability):
    for cards in player.exposed_cards.values():
        for exposed_card in cards:
            for card in card_probability:
                if card in card_probability and card.suit == exposed_card and card_val[card.value] <= card_val[exposed_card]:
                    del card_probability[card]


# Updates card_probability based on previous guesses
def update_card_probability(player, card_probability):
    total_viable_cards = len(card_probability)
    teammate_played_cards = player.exposed_cards[teammate[player.name]]

    for ind, guesses in enumerate(player_guesses[player.name]):
        correct_guesses = player.cVals[ind]
        total_guesses = len(guesses)

        num = correct_guesses
        den = total_guesses

        for card in guesses:
            if card not in card_probability:
                den -= 1
            elif card in teammate_played_cards:
                num -= 1
        
        if den > 0:
            guess_prob = num / den

            for card in guesses:
                if card in card_probability:
                    card_probability[card] = max(guess_prob, card_probability[card])
        
        unguessed_cards = set()

        for card in card_probability:
            if card not in guesses:
                unguessed_cards.add(card)
        
        num_of_unguessed_cards = len(unguessed_cards)

        if num_of_unguessed_cards > 0:
            missed_guesses = total_guesses - correct_guesses
            unGuess_prob = missed_guesses / num_of_unguessed_cards

            for card in unguessed_cards:
                card_probability[card] = max(unGuess_prob, card_probability[card])


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

# def guessing(player, cards, round):
#     """
#     Guesses the Anti-Suit based on teammate's exposed card
#     """

#     card_probability = {card : 1/52 for card in cards}
#     remove_cards_from_hand(player, card_probability)
#     remove_cards_from_exposed_cards(player, card_probability)
#     # print("Guesses: ", player_guesses)
#     print("Player cVals: ", player.cVals)
#     if round > 1:
#         update_card_probability(player, card_probability)

#     num_of_guesses = 13 - round
#     teammate_suit = player.exposed_cards[teammate[player.name]][0].suit
#     anti_suits = deque(['Diamonds', 'Hearts', 'Clubs', 'Spades'])
#     anti_suits.rotate(abs(anti_suits.index(teammate_suit) - (len(anti_suits) - 1)))
#     # if not player.cVals:
#     #     anti_suit = anti_suits[0]
#     #     teammate_max = anti_suit
#     # elif player.cVals[-1] == 0:
#     #     anti_suits.rotate(round - 1)
#     #     anti_suit = anti_suits[0]
#     #     teammate_max = anti_suit
#     # else:
#     #     anti_suit = anti_suits[0]
#     #     teammate_max = anti_suit
#     if player.cVals and player.cVals[-1] == 0:
#         anti_suits.rotate(round - 1)
#         anti_suit = anti_suits[0]
#         teammate_max = anti_suit
#     else:
#         anti_suit = anti_suits[0]
#         teammate_max = anti_suit

#     # print(teammate_suit, anti_suit)
    

#     # # This is a testing print
#     # val_check_arr = []
#     # for card in potential_guesses:
#     #     val_check_arr.append((card.value, card.suit))
#     # print("Potential Guesses:", val_check_arr)
    
#     potential_guesses = [card for card in card_probability if card.suit == teammate_max] # All 13 cards of the teammate_suit
#     potential_guesses.sort(key=lambda x:card_val[x.value])
#     # This is a testing print
#     val_check_arr = []
#     for card in potential_guesses:
#         val_check_arr.append((card.value, card.suit))
#     print("Potential Guesses:", val_check_arr)
    
#     if len(potential_guesses) < num_of_guesses:
#         num_of_missing_cards = num_of_guesses - len(potential_guesses)
#         extra_guesses = []
#         for card in card_probability.keys():
#             if card not in potential_guesses:
#                 extra_guesses.append(card)
#         potential_guesses.extend(sorted(extra_guesses, key=lambda x : card_probability[x], reverse=True)[:num_of_missing_cards])

#     if len(potential_guesses) > num_of_guesses:
#         potential_guesses = potential_guesses[:13-round]

#     player_guesses[player.name].append(potential_guesses)

#     return potential_guesses

def guessing(player, cards, round):
    """
    Guesses the Anti-Suit based on teammate's exposed card
    """
    num_of_guesses = 14 - round
    teammate_value = player.exposed_cards[teammate[player.name]][0].value
    teammate_suit = player.exposed_cards[teammate[player.name]][0].suit
    anti_suits = deque(['Diamonds', 'Hearts', 'Clubs', 'Spades'])
    anti_suits.rotate(abs(anti_suits.index(teammate_suit) - (len(anti_suits) - 1)))

    if player.cVals and player.cVals[-1] == 0:
        anti_suits.rotate(round - 1)
        anti_suit = anti_suits[0]
        teammate_max = anti_suit
    else:
        anti_suit = anti_suits[0]
        teammate_max = anti_suit

    potential_guesses = [card for card in cards if (card.suit == teammate_max and check_possible(card, player))] # All 13 cards of the teammate_suit
    potential_guesses.sort(key=lambda x:card_val[x.value])

    while len(potential_guesses) < num_of_guesses:
        teammate_value = card_shift[teammate_value]
        if check_possible(Card(teammate_suit, teammate_value), player):
            potential_guesses.append(Card(teammate_suit, str(teammate_value)))

    return potential_guesses[:num_of_guesses]