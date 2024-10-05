import random
from CardGame import Player, Deck
from CardGame import Deck
from tqdm import tqdm
import math
import zlib
from itertools import combinations


def get_card_value(card):
    f"{card.value}{card.suit[0]}"
    rank_map = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 
        'J': 11, 'Q': 12, 'K': 13, 'A': 14
    }
    suit_map = {'Hearts': 0.1, 'Diamonds': 0.2, 'Clubs': 0.3, 'Spades': 0.4}
    
    rank = rank_map[card.value]
    suit = suit_map[card.suit]
    
    return rank + suit

def get_card_order(cards, rank):
    """
    Given a list of 7 cards and a number (rank), return the order in which they should be played.
    :param cards: A list of 7 cards in any order.
    :param rank: The rank number (1 to 7!) that represents the specific permutation.
    :return: A list representing the order in which the cards should be played. (0th index is the first card to play)
    """
    cards = sorted(cards, key=get_card_value)
    order = []
    rank -= 1  
    n = len(cards)

    for i in range(n, 0, -1):
        factorial = math.factorial(i - 1)
        index = rank // factorial
        order.append(cards.pop(index))
        rank %= factorial

    return order # NEED TO CHANGE THIS TO be 0 - 5040!!!!!!

def get_rank_from_order(played_order):
    """
    Given the order of 7 played cards, return the rank number (1 to 7!) that corresponds to this order.
    :param played_order: The specific order of the 7 played cards.
    :return: The rank number (1 to 7!) corresponding to the played order. # NEED TO CHANGE THIS TO be 0 - 5040!!!!!!
    """
    available_cards = sorted(played_order, key=get_card_value)
    rank = 0
    n = len(played_order)

    for i in range(n):
        index = available_cards.index(played_order[i])
        rank += index * math.factorial(n - 1 - i)
        available_cards.pop(index)

    return rank + 1  # Weird hack Need to look at the ranks of the encoding and decoding. I think we might be off by 1

def hash_combination(cards):
    simpleHand = [f"{card.value}{card.suit[0]}" for card in cards] 
    # return card_hashing.hash_combination_cpp(simpleHand)
    combo_str = ''.join(simpleHand)  
    return zlib.crc32(combo_str.encode()) % (5040)

def create_hash_map(cards):
    sorted_cards = sorted(cards, key=get_card_value)
    
    combos = combinations(sorted_cards, 13)
    # combos = combinations(cards, 13)
    totalCombos = math.comb(len(cards), 13)
    hash_map = {i: [] for i in range(5040)} 
    
    for combo in tqdm(combos, desc="Hashing combinations", unit="combo", total=totalCombos):
        # sorted_combo = sorted(combo, key=get_card_value)
        hash_value = hash_combination(combo)
        hash_map[hash_value].append(combo)
    
    return hash_map


ourHandHash = {}
first_7_cards_to_play = {}

def playing(player: Player, deck: Deck):
    global ourHandHash
    global first_7_cards_to_play
    turn = len(player.played_cards) + 1

    if turn == 1:
        # Hash our cards and figure out what we are going to play
        # simpleHand = [f"{card.value}{card.suit[0]}" for card in player.hand]
        ourHandSorted = sorted(player.hand, key=get_card_value)
        ourHandHash[player.name] = hash_combination(ourHandSorted)
        print(f"Player: {player.name} Sending: {ourHandHash[player.name]}")

        first_7_cards_to_play[player.name] = get_card_order(ourHandSorted[0:7], ourHandHash[player.name]) # Should prob use sorted hand here
    if turn <= 7:
        if first_7_cards_to_play[player.name]:
            card_to_play = first_7_cards_to_play[player.name].pop(0) # get first element in list
            return player.hand.index(card_to_play)
        else:
            raise ValueError("first_7_cards_to_play was not initialized properly.")
        # card_to_play = first_7_cards_to_play.pop(0)
        # return player.hand.index(card_to_play)
    else: 
        return random.randint(0, len(player.hand) - 1)

hash_index_to_search = {}
hash_map = {}
sorted_first_7_cards_of_team_mate = {}
def guessing(player, cards, round):
    global hash_map
    global hash_index_to_search
    global ourHandHash
    global sorted_first_7_cards_of_team_mate
    
    teamMatesPlayedCards = get_team_mates_exposed_cards(player)
    
    if round == 7: # only create map on round 7
        cards_copy = cards.copy()
        viableCards = get_viable_cards(cards_copy, player)
        hash_map[player.name] = create_hash_map(viableCards)
        sorted_first_7_cards_of_team_mate[player.name] = get_tuple_representation_of_cards(sorted(teamMatesPlayedCards, key=get_card_value))
        hash_index_to_search[player.name] = get_rank_from_order(teamMatesPlayedCards)
        print(f"Player: {player.name} Received: {hash_index_to_search[player.name]}")

    if player.name in hash_index_to_search:
        personal_hash_map = hash_map[player.name]
        personal_hash_index = hash_index_to_search[player.name]

        # Can do better here by also making sure the cards played by the other team are not in any of the options
        print(sorted_first_7_cards_of_team_mate[player.name])
        options = [combo for combo in personal_hash_map[personal_hash_index] 
                   if set(teamMatesPlayedCards).issubset(combo) 
                   and set(combo).issubset(cards) 
                   and not set(get_other_teams_exposed_cards(player)).intersection(set(combo)) # Make sure the other team has not played any of these cards
                   and get_tuple_representation_of_cards(combo[0:7]) == sorted_first_7_cards_of_team_mate[player.name] # Check if first 7 cards are the same
                   ]
        
        print(f"Number of Options: {len(options)}")
        chosen = random.choice(options)
        return list(set(chosen) - set(teamMatesPlayedCards))
    else:
        viableCardsMinusTeamMatePlayed = list(set(get_viable_cards(cards, player)) - set(teamMatesPlayedCards))
        return random.sample(viableCardsMinusTeamMatePlayed, 13 - round)

def get_tuple_representation_of_cards(cards):
    return [(card.value, card.suit) for card in cards]
def get_team_mates_exposed_cards(player) -> list:
    if player.name == "East":
        return player.exposed_cards["West"]
    elif player.name == "West":
        return player.exposed_cards["East"]
    elif player.name == "North":
        return player.exposed_cards["South"]
    elif player.name == "South":
        return player.exposed_cards["North"]

def get_viable_cards(cards, player):
    card_set = set(cards)
    player_hand_set = set(player.hand).union(set(player.played_cards))
    other_teams_exposed_cards = set(get_other_teams_exposed_cards(player))
    viable_cards = card_set - player_hand_set - other_teams_exposed_cards
    return list(viable_cards)


def get_other_teams_exposed_cards(player) -> list:
    if player.name == "East" or player.name == "West":
        return player.exposed_cards["North"] + player.exposed_cards["South"]
    elif player.name == "North" or player.name == "South":
        return player.exposed_cards["East"] + player.exposed_cards["West"]
