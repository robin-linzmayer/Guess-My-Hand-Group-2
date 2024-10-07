import random
import time
from CardGame import Card

random_seed = 11024891

def playing(player, deck):
    """
    Playing min/max boundaries strategy.
    
    Returns an integer representing the index of the card in the player's hand to play.
    """
    if not player.hand:
        return None

    deck = get_deck_of_cards()
    cards_to_indices = create_card_to_index_mapping(random_seed, deck)
    turn = 14 - len(player.hand)

    if turn % 2 == 1:
        # on odd turns, expose the card with the highest index value
        bound_card = max(player.hand, key=lambda card: cards_to_indices[card])
    else:
        # on even turns, expose the card with the lowest index value
        bound_card = min(player.hand, key=lambda card: cards_to_indices[card])

    return player.hand.index(bound_card)

def guessing(player, cards, round):
    """
    Returns a list of n Card objects to guess partner's hand, incorporating feedback from previous guesses.
    """
    card_probs_by_index = {index: 1/52 for index in range(1, 53)}
    partner = get_partner(player.name)

    deck = get_deck_of_cards()
    cards_to_indices, indices_to_cards = create_card_to_index_mapping(random_seed, deck, True)

    all_cards_exposed = []
    partner_cards_exposed = []
    for player_name, cards in player.exposed_cards.items():
        if player_name == partner:
            partner_cards_exposed += cards
       
        all_cards_exposed += cards
    
    # Delete cards of your own
    for own_card in list(set(player.hand)):
        del card_probs_by_index[cards_to_indices[own_card]]
    
    # Delete cards which have been previously exposed
    for exposed_card in all_cards_exposed:
        del card_probs_by_index[cards_to_indices[exposed_card]]

    # Delete cards based on partner's min/max boundary information
    for i in range(len(partner_cards_exposed)):
        bound = cards_to_indices[partner_cards_exposed[i]]
        if (i + 1) % 2 == 1:
            indices_to_delete = [index for index in card_probs_by_index if index > bound]
        else:
            indices_to_delete = [index for index in card_probs_by_index if index < bound]
        
        for index in indices_to_delete:
            del card_probs_by_index[index]

    # Update card probabilities based on previous guesses
    card_probs_by_index = update_probs_from_guesses(card_probs_by_index, player, all_cards_exposed, cards_to_indices)

    # Determine your guesses by finding n cards with highest probabilities
    n = 13 - round
    sorted_card_probs_by_index = sorted(card_probs_by_index, key=card_probs_by_index.get, reverse=True)
    top_n_card_prob_indices = sorted_card_probs_by_index[:n]
    random.shuffle(top_n_card_prob_indices)

    card_guesses = []
    for index in top_n_card_prob_indices:
        card_guesses.append(indices_to_cards[index])

    return card_guesses

def update_probs_from_guesses(card_probs_by_index, player, all_cards_exposed, cards_to_indices):
    """
    Adjusts the probabilities of remaining cards based on feedback from previous guesses.
    """
    
    for guesses, c_value in zip(player.guesses, player.cVals):
        continue

        # exposed_in_guess = [ctuple for ctuple in ctuple_guess if ctuple in partner_ctuples_exposed]
        # remaining_in_guess = [ctuple for ctuple in ctuple_guess if ctuple not in partner_ctuples_exposed]
        
        # # If cards from the guess have been exposed, update the probabilities of the remaining ones
        # if len(exposed_in_guess) < c_value:
        #     for ctuple in remaining_in_guess:
        #         index = ctuples_to_indices[ctuple]
        #         if index in card_probs_by_index:
        #             card_probs_by_index[index] *= 1.5  # Increase probability if it's still valid
        
        # # If too many cards have been exposed, reduce the probabilities of remaining ones
        # elif len(exposed_in_guess) > c_value:
        #     for ctuple in remaining_in_guess:
        #         index = ctuples_to_indices[ctuple]
        #         if index in card_probs_by_index:
        #             card_probs_by_index[index] *= 0.5  # Decrease probability
        
    return card_probs_by_index

def create_card_to_index_mapping(seed, cards, createReverseMap=False):
    """
    Method which maps a card to a random index between 1-52.
    """
    random.seed(seed)
    indices = random.sample(range(1, 53), 52)

    cards_to_indices = {card: index for card, index in zip(cards, indices)}
    
    if createReverseMap:
        indices_to_cards = {index: card for card, index in cards_to_indices.items()}
        return cards_to_indices, indices_to_cards
    
    return cards_to_indices

def get_deck_of_cards():
    suits = ["Hearts", "Diamonds", "Clubs", "Spades"] 
    values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    
    return [Card(suit, value) for value in values for suit in suits]

def get_partner(my_name):
    if my_name == "North":
        return "South"
    elif my_name == "East":
        return "West"
    elif my_name == "South":
        return "North"
    elif my_name == "West":
        return "East"
