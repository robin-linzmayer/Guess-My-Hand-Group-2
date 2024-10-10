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

    if turn % 2 == 0:
        # on even turns, expose the card with the highest index value
        bound_card = max(player.hand, key=lambda card: cards_to_indices[card])
    else:
        # on odd turns, expose the card with the lowest index value
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

    all_other_cards_exposed = []
    partner_cards_exposed = []
    for player_name, cards in player.exposed_cards.items():
        if player_name == partner:
            partner_cards_exposed += cards
        else:
            all_other_cards_exposed += cards
    
    # Delete cards of your own
    for own_card in list(set(player.hand)):
        del card_probs_by_index[cards_to_indices[own_card]]
    
    # Delete cards which have been previously exposed
    for exposed_card in (set(partner_cards_exposed) | set(all_other_cards_exposed)):
        del card_probs_by_index[cards_to_indices[exposed_card]]

    # Delete cards based on partner's min/max boundary information
    for i in range(len(partner_cards_exposed)):
        bound = cards_to_indices[partner_cards_exposed[i]]
        if (i + 1) % 2 == 0:
            indices_to_delete = [index for index in card_probs_by_index if index > bound]
        else:
            indices_to_delete = [index for index in card_probs_by_index if index < bound]
        
        for index in indices_to_delete:
            del card_probs_by_index[index]

    # Update card probabilities based on previous guesses
    card_probs_by_index = update_probs_from_guesses(card_probs_by_index, player, partner_cards_exposed, all_other_cards_exposed, cards_to_indices, indices_to_cards)

    # Determine your guesses by finding n cards with highest probabilities
    n = 13 - round
    sorted_card_probs_by_index = sorted(card_probs_by_index, key=card_probs_by_index.get, reverse=True)
    top_n_card_prob_indices = sorted_card_probs_by_index[:n]

    card_guesses = []
    for index in top_n_card_prob_indices:
        card_guesses.append(indices_to_cards[index])

    # if player.name == "North":
    #     print(f"Guess Set: {card_guesses}")
    return card_guesses

def update_probs_from_guesses(card_probs_by_index, player, partner_cards_exposed, all_other_cards_exposed, cards_to_indices, indices_to_cards):
    """
    Adjusts the probabilities of remaining cards based on feedback from previous guesses.
    """
    for turn, (guess, c_val) in enumerate(zip(player.guesses, player.cVals)):
        guess = set(guess)
        # if player.name == "North":
        #     print(f"Guess cVal: {c_val}")
        all_other_cards_exposed = set(all_other_cards_exposed)
        correct_guess_count = c_val
        valid_guess_count = len(guess)

        exposed_card_count = 4
        for card in guess:
            if card in partner_cards_exposed:
                correct_guess_count -= 1
                valid_guess_count -= 1
                exposed_card_count -= 1
            if card in all_other_cards_exposed:
                valid_guess_count -= 1
                exposed_card_count -= 1
        
        valid_unguessed_count = 39 - 4*(turn+1) - len(guess) - exposed_card_count + 1

        # if player.name == "North":
        #     print(f"Numerator: {correct_guess_count}")
        #     print(f"Denominator: {valid_guess_count}")
        #     print(f"Guess probability = {correct_guess_count} / {valid_guess_count}")
        #     print(f"NonGuess probability = {12 - turn - c_val} / {valid_unguessed_count}")
        
        indices_to_delete = []
        for card in guess:
            card_idx = cards_to_indices[card]
            if card_idx in card_probs_by_index:
                if valid_guess_count > 0:
                    prob = correct_guess_count / valid_guess_count
                    if prob >= 0:
                        card_probs_by_index[card_idx] *= prob
                    else:
                        indices_to_delete.append(card_idx)

        for card_idx in card_probs_by_index:
            card = indices_to_cards[card_idx]
            if card not in guess:
                if valid_unguessed_count > 0:
                    prob = (len(guess) - c_val + 1) / valid_unguessed_count
                    if prob >= 0:
                        card_probs_by_index[card_idx] *= prob
                    else:
                        indices_to_delete.append(card_idx)
        
        for idx in indices_to_delete:
            del card_probs_by_index[idx]

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
