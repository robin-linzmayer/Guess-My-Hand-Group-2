import random
import time
from CardGame import Card, Deck, Player

random_seed = 11024891

def playing(player, deck):
    """
    Playing min/max boundaries strategy.
    
    Returns an integer representing the index of the card in the player's hand to play.
    """
    if not player.hand:
        return None

    ctuples = get_ctuple_deck_of_cards()
    ctuples_to_indices = create_ctuple_to_index_mapping(random_seed, ctuples)
    turn = 14 - len(player.hand)
    ctuples_in_hand = get_card_tuples(player.hand)

    if turn % 2 == 1:
        # on odd turns, expose the card with the highest index value
        bound_card = max(ctuples_in_hand, key=lambda card: ctuples_to_indices[card])
    else:
        # on even turns, expose the card with the lowest index value
        bound_card = min(ctuples_in_hand, key=lambda card: ctuples_to_indices[card])

    return ctuples_in_hand.index(bound_card)

def guessing(player, cards, round):
    """
    Returns a list of n Card objects to guess partner's hand.
    """
    card_probs_by_index = {index: 1/52 for index in range(1, 53)}
    partner = get_partner(player.name)

    ctuples = get_ctuple_deck_of_cards()
    ctuples_to_indices, indices_to_ctuples = create_ctuple_to_index_mapping(random_seed, ctuples, True)
    ctuples_to_cards = map_ctuples_to_cards(cards)

    ctuples_in_hand = get_card_tuples(player.hand)
    ctuples_played = get_card_tuples(player.played_cards)
    all_ctuples_exposed = []
    partner_ctuples_exposed = []
    for player_name, cards in player.exposed_cards.items():
        if player_name == partner:
            partner_ctuples_exposed += get_card_tuples(cards)
       
        all_ctuples_exposed += get_card_tuples(cards)
    
    # Delete cards of your own
    for own_card in list(set(ctuples_in_hand) | set(ctuples_played)):
        del card_probs_by_index[ctuples_to_indices[own_card]]
    
    # Delete cards which have been previously exposed
    for exposed_card in all_ctuples_exposed:
        del card_probs_by_index[ctuples_to_indices[exposed_card]]

    # Delete cards based on partner's min/max boundary information
    for i in range(len(partner_ctuples_exposed)):
        bound = ctuples_to_indices[partner_ctuples_exposed[i]]
        if (i + 1) % 2 == 1:
            indices_to_delete = [index for index in card_probs_by_index if index > bound]
        else:
            indices_to_delete = [index for index in card_probs_by_index if index < bound]
        
        for index in indices_to_delete:
            del card_probs_by_index[index]

    # Update card probabilities based on previous guesses
    # COMPLETE THIS

    # Determine your guesses by finding n cards with highest probabilities
    n = 13 - round
    sorted_card_probs_by_index = sorted(card_probs_by_index, key=card_probs_by_index.get, reverse=True)
    top_n_card_prob_indices = sorted_card_probs_by_index[:n]
    random.shuffle(top_n_card_prob_indices)

    card_guesses = []
    for index in top_n_card_prob_indices:
        card_guesses.append(ctuples_to_cards[indices_to_ctuples[index]])

    return card_guesses

def create_ctuple_to_index_mapping(seed, ctuples, createReverseMap=False):
    """
    Method which maps a card tuple (value, suit) to a random index between 1-52.
    """
    random.seed(seed)
    indices = random.sample(range(1, 53), 52)

    ctuples_to_indices = {ctuple: index for ctuple, index in zip(ctuples, indices)}
    
    if createReverseMap:
        indices_to_ctuples = {index: card for card, index in ctuples_to_indices.items()}
        return ctuples_to_indices, indices_to_ctuples
    
    return ctuples_to_indices

def get_ctuple_deck_of_cards():
    suits = ["Hearts", "Diamonds", "Clubs", "Spades"] 
    values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    
    return [(value, suit) for value in values for suit in suits]

def map_ctuples_to_cards(cards):
    """
    Method which maps a card tuple (value, suit) to its corresponding Card object.
    """
    ctuples_to_cards = {}
    for card in cards:
            ctuples_to_cards[(card.value, card.suit)] = card
    
    return ctuples_to_cards

def get_card_tuples(cards):
    """
    Method which returns a list of card tuple (value, suit) from a list of Card objects.
    """
    card_tuple_list = []
    for card in cards:
        card_tuple_list.append((card.value, card.suit))
    
    return card_tuple_list

def get_partner(my_name):
    if my_name == "North":
        return "South"
    elif my_name == "East":
        return "West"
    elif my_name == "South":
        return "North"
    elif my_name == "West":
        return "East"