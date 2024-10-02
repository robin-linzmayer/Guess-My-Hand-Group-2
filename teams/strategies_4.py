import random
from collections import defaultdict

Pairs ={"Hearts": "Spades", "Spades": "Hearts", "Clubs": "Diamonds", "Diamonds": "Clubs"}
PlayerPairs = {"North": "South", "South": "North", "East": "West", "West": "East"}
max_suit_of_partner = None
min_suit_of_partner = None
max_suit_cards = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
max_suit_of_partner1 = None
min_suit_of_partner1 = None
max_suit_cards1 = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]


def playing(player, deck):
    """
    Just return the opposite of maximum frequency suit. If opposite is not there, return min suit
    """
    if not player.hand:
        return None
    
    freq = defaultdict(lambda:0)
    
    for card in player.hand:
        freq[card.suit]+=1
    
    maxSuit =  max(freq, key=freq.get)
    oppSuit = Pairs[maxSuit]
    for i,card in enumerate(player.hand):
        if card.suit == oppSuit:
            return i

    # What if no opposite suit? Rn return min suit
    minSuit = min(freq, key=freq.get)
    for i,card in enumerate(player.hand):
        if card.suit == minSuit:
            return i


def guessing(player, cards, round):
    global max_suit_of_partner1
    global min_suit_of_partner1
    global max_suit_cards1
    global max_suit_of_partner
    global min_suit_of_partner
    global max_suit_cards

    exposedCards = player.exposed_cards[PlayerPairs[player.name]]
    if player.name == "North" or player.name == "East":
        max_suit_of_partner_local = max_suit_of_partner1
        min_suit_of_partner_local = min_suit_of_partner1
        max_suit_cards_local = max_suit_cards1
    else:
        max_suit_of_partner_local = max_suit_of_partner
        min_suit_of_partner_local = min_suit_of_partner
        max_suit_cards_local = max_suit_cards

    if round == 1:
        max_suit_of_partner_local = Pairs[exposedCards[0].suit]     
    elif round == 2:
        if player.cVals[-1] < 5: #Worst case 0H 5S 3C 4D 
            # Suit guess was wrong. Why? Maybe opposite did not exist [No H]
            min_suit_of_partner_local = max_suit_of_partner_local
            all_suits = set(["Hearts", "Clubs", "Spades", "Diamonds"])
            remove_suit = set([min_suit_of_partner_local, Pairs[min_suit_of_partner_local]])
            max_suit_of_partner_local = random.choice(list(all_suits - remove_suit)) #Either H or S
    elif round == 3:
        if player.cVals[-2] < 5 and player.cVals[-1] < 5:  #0 5 2 4 
            max_suit_of_partner_local = Pairs[max_suit_of_partner_local]

    for p in player.exposed_cards:
        for card in player.exposed_cards[p]:
            if card.suit == max_suit_of_partner_local and card.value in max_suit_cards_local:
                max_suit_cards_local.remove(card.value)

    # What if we have only 5 choices in max suit cards but we need to guess 6 cards?
    if len(max_suit_cards_local) >= 13-round:
        guesses = random.sample(max_suit_cards_local, 13-round) 
    else:
        guesses =  max_suit_cards_local 
        guesses+= random.choices(max_suit_cards_local, k=13-round-len(max_suit_cards_local)) #Duplicates but we don't care
    
    # Right now set intersection in game gui does it with object ref not value so had to use cards passed - ineffecient 
    returncards=[]
    for guess in guesses:
        for card in cards:
            if card.suit == max_suit_of_partner_local and card.value == guess:
                returncards.append(card)
                break

    if player.name == "North" or player.name == "East":
        max_suit_of_partner1 = max_suit_of_partner_local
        min_suit_of_partner1 = min_suit_of_partner_local
        max_suit_cards1 = max_suit_cards_local
    else:
        max_suit_of_partner = max_suit_of_partner_local
        min_suit_of_partner = min_suit_of_partner_local
        max_suit_cards = max_suit_cards_local

    return returncards
