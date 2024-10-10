import random
from itertools import chain
from collections import defaultdict
from CardGame import Player, Deck, Card
import numpy as np

PARTNERS = {
    "North": "South",
    "East": "West",
    "South": "North",
    "West": "East",
}

OPPONENTS = {
    "North": ["East", "West"],
    "South": ["East", "West"],
    "East": ["North", "South"],
    "West": ["North", "South"]
}

SUIT_TO_NUM = {"Hearts": 0, "Spades": 13, "Diamonds": 26, "Clubs": 39}

VAL_TO_NUM = {
    "A": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
}

NUM_TO_SUIT = {v: k for k, v in SUIT_TO_NUM.items()}
NUM_TO_VAL = {v: k for k, v in VAL_TO_NUM.items()}
MIN_SUIT = {"North": -1, "South": -1, "East": -1, "West": -1}

# SHORTEST_SUIT_DISTR = {
#     3: "4-3-3-3",5-5-3-0, 6-4-3-0, 7-3-3-0,10-3-0-0,
#     2: ["4-4-3-2", "5-3-3-2", "5-4-2-2", "6-3-2-2", "7-2-2-2",6-5-2-0, 7-4-2-0, 8-3-2-0,9-2-2-0,11-2-0-0, 
#     1: [4-4-4-1, 5-4-3-1, 5-5-2-1, 6-3-3-1, 6-4-2-1, 6-5-1-1, 7-3-2-1, 7-4-1-1, 8-2-2-1, 8-3-1-1, 9-2-1-1, 10-1-1-1,6-6-1-0,7-5-1-0,8-4-1-0,9-3-1-0, 10-2-1-0,11-1-1-0,  12-1-0-0,
#     4: [5-4-4-0, 9-4-0-0,
#     6: 7-6-0-0,
#     5:  8-5-0-0, 
#     13:   13-0-0-0
# }

# round =1: eliminate 13 cards of min SUIT
# 2: if min suit is the same -> find how many cards remain in each suit use it for probability


def generate_permutation(perm_size, cards, seed):
    """Generates a permutation dictionary, each card points to one permutation"""
    perms = {}
    for i in cards:
        random.seed(seed)
        perms[i] = random.sample(cards, perm_size)
    return perms


def get_unguessed_cards(player):
    """Get all cards that have not been guessed by player"""
    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
    values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    allcards = [Card(suit, value) for suit in suits for value in values]

    # All possible cards except exposed cards
    unguessed_cards = []
    for card in allcards:
        if card not in set(
            chain.from_iterable(player.exposed_cards.values())
        ) and card not in set(player.played_cards):
            unguessed_cards.append(card)

    # Add cards exposed in this round as partner might not have had that information during exposing
    for p in player.exposed_cards:
        if player.exposed_cards[p]:
            unguessed_cards.append(player.exposed_cards[p][-1])
    return unguessed_cards


def playing(player: Player, deck: Deck):
    game_round = len(player.played_cards) + 1
    # Play min suit
    freq = defaultdict(int)
    for card in player.hand:
        freq[card.suit] += 1

    min_suit = min(freq, key=freq.get)
    # The only cases where this will throw us off 13-0-0-0 [Veryyy unlikely]
    # Other cases where player will lose points > 3 [5-4-4-0, 9-4-0-0, 8-5-0-0, 7-6-0-0]
    # Or always we just sacrifice 1,2 or 3 max points but we get to eliminate 13 cards entirely

    #1,2,3,4,5,6,7,8,9,10,11,12

    # Max min suit cards == 3 most likely, extreme cases 4,5,6,13
    
    if game_round == 13:
        min_suit_cards = [card for card in player.hand if card.suit == min_suit]
        max_card = max(min_suit_cards, key=lambda card: VAL_TO_NUM[card.value])
        return player.hand.index(max_card)
    #return random.randint(0, len(player.hand)-1)

    if game_round <=10:
        min_card = min(player.hand, key=lambda card: VAL_TO_NUM[card.value])
        max_card = max(player.hand, key=lambda card: VAL_TO_NUM[card.value])
        if game_round %2 ==0:
            return player.hand.index(min_card)
        else:
            return player.hand.index(max_card)
    else:
                # Find most similar permutations to players cards
            unguessed_cards = get_unguessed_cards(player)
            permutations = generate_permutation(13 - game_round, unguessed_cards, 7)
            card_index = 0
            max_sim = 0
            for i, k in enumerate(player.hand):
                perms = permutations[k]
                sim = len((set(player.hand) & set(perms)) - {k})
                if sim > max_sim:
                    card_index = i
                    max_sim = sim
            return card_index

def guessing(player: Player, cards, round):
    print("\n Player: ", player.name)
    unguessed_cards = get_unguessed_cards(player)
    permutations = generate_permutation(13 - round, unguessed_cards, 7)
    remaining_cards = []
    for card in cards:
        if (
            card not in set(chain.from_iterable(player.exposed_cards.values()))
            and card not in set(player.hand)
            and card not in set(player.played_cards)
        ):
            remaining_cards.append(card)
    print("Remaining cards for player ", player.name, " : ", remaining_cards)

    if not remaining_cards:
        print("0 remaining at round", round)
        return random.sample(cards, 13 - round)

    if round == 1:
        suit = player.exposed_cards[PARTNERS[player.name]][-1].suit
        MIN_SUIT[player.name] = suit
        # Eliminate suit of card played
        remaining_cards = [card for card in remaining_cards if card.suit != suit]

        # Now we have total max of 26 cards, the most likely suit distribution is 4432
        # Guess 4,4,4 from remaining cards - [TODO: Can I improve using my suit distribution?]
        suit_groups = defaultdict(list)
        for card in remaining_cards:
            suit_groups[card.suit].append(card)

        # Select up to 4 cards. I think there will always be atleast 4 left
        selected_cards = [
            card
            for _, cards in suit_groups.items()
            for card in random.sample(cards, min(4, len(cards)))
        ]
        selected_cards = selected_cards[:12]
        return selected_cards

    #remaining_cards = [card for card in remaining_cards if card.suit != MIN_SUIT[player.name]]
    prob = {card: (1 / len(remaining_cards)) for card in remaining_cards}
    
    for card in prob:
        if card.suit == MIN_SUIT[player.name]:
            prob[card]*=0.0013

    cvals = player.cVals.copy()
    guesses = player.guesses.copy()

    for i in range(round-1):
        guessed = []
        wronglyGuessed = []
        #print(f"Round {i} Guess {player.guesses[i]} c {player.cVals[i]}")
        for g in player.guesses[i]:
            if g in player.exposed_cards[PARTNERS[player.name]]:
                guessed.append(g)
            elif g in player.exposed_cards[OPPONENTS[player.name][0]] or g in player.exposed_cards[OPPONENTS[player.name][1]]:
                wronglyGuessed.append(g)
            
        cvals[i] -= len(guessed)
        guesses[i] = [guess for guess in player.guesses[i] if (guess not in guessed) and (guess not in wronglyGuessed)]


    #print("Newer c vals")
    for i in range(round - 1):
        guess = guesses[i]
        c = cvals[i]
        #print(f"Round {i} Guess {guess} c {c}")
        remove_prob = []
        for card in prob:
            if card in guess:
                if player.cVals[i] == 0: #What if our new c is 0?
                    #print("Deleting card", card)
                    remove_prob.append(card)
                elif c== len(guess): #All cards are right!
                    prob[card] *=10
                elif c > (len(guess)//2)+1: # More than half right
                    prob[card] *= 5*(c/len(guess))                        
                else:
                    prob[card] *= c / len(guess)
            else:
                if len(guess) - c != 0:
                    prob[card] *= (len(guess) - c) / len(guess)

        for card in remove_prob:
            del prob[card]
    
    #Intersection:
    # most recent guess with all previous guesses
    #guess[-1]&guess[0] , guess[-1]&guess[1] ... guess[-1]&guess[-2]

    #guess[-1] and guess[-2]
    # for i in range(len(guesses)-1,max(len(guessed)-2,0),-1):
    #     intersection =[]
    #     for j in guesses[i]:
    #         if j in guesses[i-1]:
    #             intersection.append(j)
    #     cdiff = (cvals[i] - cvals[i-1])
    #     if cdiff == 0:
    #         for card in intersection:
    #             prob[card]*=5
    # if cdiff < 0:
    #     #cvals[-2] was bigger than cvals[-1] 3,4,5,9
    #     1,2,3,4,6,8 + 3,5,6,7,9
    #     int - 3,6
    #     c1 = 2
    #     c2 = 3
    #     cdiff = -1

    #     s2-s1 = 5,7,9 #Increase -> guessing wrong once snowballs into guessing wrong all the time! 
    #     s1-s2 = 1,2,8,4 #Decrease all these probabilities nooo because 4 is in set!!

    #     actual ans = 3,4,5


        

    last_exposed = player.exposed_cards[PARTNERS[player.name]][-1]

    if round <= 10:
        if round %2 !=0:
            maxcard = last_exposed
            remove_cards =[]
            for card in prob:
                if VAL_TO_NUM[card.value] > VAL_TO_NUM[maxcard.value]:
                    remove_cards.append(card)
            
            for card in remove_cards:
                del prob[card]

        else:
            mincard = last_exposed
            remove_cards =[]
            for card in prob:
                if VAL_TO_NUM[card.value] < VAL_TO_NUM[mincard.value]:
                    remove_cards.append(card)
            
            for card in remove_cards:
                del prob[card]
    else:
        mostSimP = permutations[last_exposed]
        print("Most Similar Permutation", mostSimP)
        boost_factor = 1.1
        for val in mostSimP:
            if val in prob:
                prob[val] *= boost_factor
        #mostSim

    # most_sim_p = 
    # print("Most Similar Permutation", most_sim_p)

    total_weight = sum(prob.values())
    #print(prob.keys(), prob.values())
    normalized_weights = [val / total_weight for val in prob.values()]
    np.random.seed(7)
    print(prob.keys())
    random_indices = np.random.choice(
        np.arange(len(prob.keys())),
        size=13 - round,
        replace=False,
        p=normalized_weights,
    )
    sampled_cards = [list(prob.keys())[i] for i in random_indices]
    return sampled_cards
