import random

# Shared global variables
PARTNERS = {
    'North': 'South',
    'East': 'West',
    'South': 'North',
    'West': 'East',
}
SUIT_ORDER = {"Hearts": 0, "Diamonds": 2, "Clubs": 1, "Spades": 3}
VALUE_ORDER = {"2": 7, "3": 10, "4": 4, "5": 5, "6": 11, "7": 3, "8": 2, "9": 13, "10": 6, "J": 1, "Q": 9, "K": 12,
               "A": 8}

# Global variables that will be split on player.name
deck_state_dict = {}
guess_history_dict = {}

def playing(player, deck):
    """
    Playing strategy goes here (what card will the player expose to their partner)
    """
    if not player.hand:
        return None

    print(" ")
    print(f"-------------- Playing: {player.name} -----------------")

    hand_indices = [get_card_index(card) for card in player.hand]
    card_to_play_index = get_max_card(hand_indices)
    return card_to_play_index

def create_deck_state_dict(player, cards):
    """
    This function takes in a deck of cards and fills in a dictionary where:
    - Key: The scrambled index from hash_card_index
    - Value: dict
    """
    if player.name not in deck_state_dict.keys():
        deck_state_dict[player.name] = {}

    for card in cards:
        if card in player.hand:
            is_in_hand = True
        else:
            is_in_hand = False

        index = get_card_index(card)
        if is_in_hand:
            deck_state_dict[player.name][index] = {
                'card': card,
                'is_certain': True,
                'is_possible_guess': False,
                'is_in_hand': is_in_hand,
                'is_in_partner_hand': False,
            }
        else:
            deck_state_dict[player.name][index] = {
                'card': card,
                'numer': int(1),
                'denom': int(39),
                'prob': 0.025641,
                'is_certain': False,
                'is_possible_guess': True,
                'is_in_hand': is_in_hand,
                'is_in_partner_hand': False,
            }
    return

def get_card_index(card):
    """
    This function maps cards to an index and scrambles the index.
    """
    # Hash formula that combines suit and value in a less predictable way
    suit = SUIT_ORDER[card.suit]
    value = VALUE_ORDER[card.value]

    index = suit * 13 + value
    return index

def get_max_card(hand_indices):
    """
    Play card with the highest index to create upper bound value.
    """
    max_index = hand_indices.index(max(hand_indices))
    return max_index

def use_max_value_index(player, round):
    """
    Use the upper bound value strategy to inform guess
    """
    # Select cards that we are certain are in our partner's hand
    certain_dict = get_certain_guesses(player)
    num_certain_guesses = len(certain_dict)
    certain_guesses = [certain_dict[key]['card'] for key in certain_dict.keys()]

    # Select other cards that are possible logical guesses
    guess_dict = get_possible_guesses(player)

    # Take card exposed by partner and use it to inform the rest of our guesses
    partner_exposed_card = get_partner_exposed_card(player)
    exposed_index = get_card_index(partner_exposed_card)

    # Apply max value strategy and filter to cards with rank < exposed_index
    below_max_dict = {key: value for key, value in guess_dict.items() if key < exposed_index}

    indices = list(below_max_dict.keys())
    probs = [below_max_dict[idx]['prob'] for idx in indices]

    #todo this was a band-aid fix
    if round == 13:
        combined_guesses = certain_guesses
    elif 13-round > len(indices):
        # Combined strategic and certain guesses
        combined_guesses = random.sample(certain_guesses, 13-round)
    else:
        index_guesses = random.choices(indices, weights=probs, k=13-round-num_certain_guesses)
        max_card_guesses = [below_max_dict[key]['card'] for key in index_guesses]

        # Combined strategic and certain guesses
        combined_guesses = max_card_guesses + certain_guesses
    return combined_guesses

def update_guess_history_dict(player, guesses, round):
    if player.name not in guess_history_dict.keys():
        guess_history_dict[player.name] = {}
    guess_history_dict[player.name][round] = {'card_guesses': guesses,
                                              'index_guesses': [get_card_index(card) for card in guesses],
                                              'c_value': None,
                                              }

def get_partner_exposed_card(player):
    return player.exposed_cards[PARTNERS[player.name]][-1]

def get_possible_guesses(player):
    possible_guesses = {key: value for key, value in deck_state_dict[player.name].items() if value['is_possible_guess'] and not value['is_in_partner_hand']}
    print("POSSIBLE GUESSES", len(possible_guesses))
    return possible_guesses

def get_certain_guesses(player):
    certain_guesses = {key: value for key, value in deck_state_dict[player.name].items() if value['is_in_partner_hand'] and value['is_possible_guess']}
    print("CERTAIN GUESSES", len(certain_guesses))
    return certain_guesses

def update_exposed_cards(player):
    # exposed_cards = {"North": [], "East": [], "South": [], "West": []}
    # Update all exposed cards to impossible guesses
    for _, cards in player.exposed_cards.items():
        for card in cards:
            deck_state_dict[player.name] = {k: {**v, 'is_possible_guess': False} if v['card'] == card else v for k, v in deck_state_dict[player.name].items()}

def guessing(player, cards, round):
    """
    Guessing strategy goes here (number of guesses of your partner's cards)
    """
    print(" ")
    print(f"-------------- Guessing: {player.name} -----------------")

    # Initialize cards into the deck_state_dict
    if round == 1:
        create_deck_state_dict(player, cards)

    # Update cards that were exposed this round in deck state as is_possible_guess: False
    update_exposed_cards(player)

    # Update probability of existing cards
    if player.cVals:
        c_value = player.cVals[-1]
        guess_history_dict[player.name][round-1]['c_value'] = c_value

        # Update probabilities of cards in the deck_state_dict
        # Todo - change this so that we are updating more dynamically across rounds of the game as we learn more info
        prev_round = round-1
        update_probabilities(player, guess_history_dict[player.name], prev_round)


    # Partner player's exposed card is used as an upper bound for values to guess from.
    guesses = use_max_value_index(player, round)
    update_guess_history_dict(player, guesses, round)

    return guesses

def update_probabilities(player, guess_history_dict, prev_round):

    # This means all guessed cards from the previous turn are NOT in your partner's hand.
    if guess_history_dict[prev_round]['c_value'] == 0:
        for index in guess_history_dict[prev_round]['index_guesses']:
            deck_state_dict[player.name][index]['is_possible_guess'] = False
            deck_state_dict[player.name][index]['is_certain'] = True
            deck_state_dict[player.name][index]['numer'] = None
            deck_state_dict[player.name][index]['denom'] = None
    # This means all guessed cards from the previous turn are IN your partner's hand.
    elif guess_history_dict[prev_round]['c_value'] == len(guess_history_dict[prev_round]['index_guesses']):
        for index in guess_history_dict[prev_round]['index_guesses']:
            deck_state_dict[player.name][index]['is_possible_guess'] = True
            deck_state_dict[player.name][index]['is_certain'] = True
            deck_state_dict[player.name][index]['is_in_partner_hand'] = True
            deck_state_dict[player.name][index]['numer'] = None
            deck_state_dict[player.name][index]['denom'] = None
    else:
        possible_guesses_dict = get_possible_guesses(player)
        num_possible_cards = len(get_possible_guesses(player))
        num_guesses = len(guess_history_dict[prev_round]['index_guesses'])
        num_correct = guess_history_dict[prev_round]['c_value']
        partner_hand_size = 13 - (prev_round - 1)  # Since partner exposes one card each round

        guessed_card_factor = num_correct / num_guesses
        # todo - sometimes this throws errors bc denom is 0
        unguessed_card_factor = (partner_hand_size - num_correct) / (num_possible_cards - num_guesses)

        total_probability = 0  # To accumulate total probability for normalization
        for index, value in possible_guesses_dict.items():
            card = possible_guesses_dict[index]['card']
            numer = possible_guesses_dict[index]['numer']
            denom = possible_guesses_dict[index]['denom']
            old_prob = numer/denom if denom != 0 else 0

            if card in guess_history_dict[prev_round]['card_guesses']:
                new_prob = old_prob * guessed_card_factor
            else:
                new_prob = old_prob * unguessed_card_factor

            deck_state_dict[player.name][index]['prob'] = new_prob
            total_probability += new_prob