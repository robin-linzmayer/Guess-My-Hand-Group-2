import random

def playing(player, deck):
    """
    This strategy discards cards from the suit the player has the fewest cards in.
    
    Parameters:
    player (Player): The current player object.
    deck (Deck): The current deck object.

    Returns:
    int: The index of the card to be played.
    """
    if not player.hand:
        return None
    
    # Create a count of cards per suit in the player's hand
    suit_count = {suit: 0 for suit in deck.suits}
    for card in player.hand:
        suit_count[card.suit] += 1

    # Find the suit with the fewest cards
    weakest_suit = min(suit_count, key=suit_count.get)

    # Select a card from the weakest suit to discard
    weakest_suit_cards = [card for card in player.hand if card.suit == weakest_suit]

    if weakest_suit_cards:
        # Play the first card of the weakest suit
        card_to_play = weakest_suit_cards[0]
        return player.hand.index(card_to_play)

    # Fallback: If no card from the weakest suit (shouldn't happen normally)
    return random.randint(0, len(player.hand) - 1)

def guessing(player, cards, round):
    """
    This guessing strategy guesses unexposed cards from suits the player's partner has not discarded,
    with a reduced probability of choosing cards from suits that have been discarded more often.

    Parameters:
    player (Player): The current player object.
    cards (list): A list of all possible cards (usually the full deck or a subset).
    round (int): The current round of the game (used to calculate how many cards to guess).

    Returns:
    list: A list of cards that are guessed to be in the partner's hand.
    """
    # Get the number of cards to guess
    num_cards_to_guess = 13 - round

    # Identify the player's partner based on seating
    if player.name == "North":
        partner_discarded = player.exposed_cards["South"]
    elif player.name == "South":
        partner_discarded = player.exposed_cards["North"]
    elif player.name == "East":
        partner_discarded = player.exposed_cards["West"]
    else:  # player.name == "West"
        partner_discarded = player.exposed_cards["East"]

    # Count how many times the partner has discarded cards from each suit
    discard_count = {suit: 0 for suit in ["Hearts", "Diamonds", "Clubs", "Spades"]}
    for card in partner_discarded:
        discard_count[card.suit] += 1

    # Find the unexposed cards in the full list (cards that are not in any player's exposed cards)
    all_exposed_cards = set(player.exposed_cards["North"] + 
                            player.exposed_cards["East"] + 
                            player.exposed_cards["South"] + 
                            player.exposed_cards["West"])

    remaining_cards = [card for card in cards if card not in all_exposed_cards]

    # Assign weights inversely proportional to the number of discards in each suit
    max_discard_count = max(discard_count.values()) + 1  # Adding 1 to avoid division by zero
    card_weights = [max_discard_count - discard_count[card.suit] for card in remaining_cards]

    # Use weighted sampling without repetition
    guessed_cards = random.choices(remaining_cards, weights=card_weights, k=num_cards_to_guess)

    # Ensure guessed_cards has unique entries (since random.choices could allow duplicates)
    return list(set(guessed_cards))