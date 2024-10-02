import random

"""
Card Representation:

In this game, cards are represented by the Card class with two attributes:
- suit: A string representing the suit of the card ("♥", "♦", "♣", "♠")
- value: A string representing the value of the card ("2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A")

To output a specific card in a player's strategy:
1. Find the index of the desired card in the player's hand.
2. Return that index.

Example:
To output the 2 of clubs, a player's strategy should:
1. Search their hand for a Card object with suit "♣" and value "2".
2. Return the index of that card in their hand.

If the 2 of clubs is the first card in the player's hand:
    return 0
If it's the second card:
    return 1
And so on.

If the card is not in the player's hand, the strategy should handle this case appropriately by choosing a different card.
"""


def NorthSouthStrategy(player, deck):
    """
    North-South player strategy.

    This function should implement the strategy for North and South players.
    It should return the index of the card to be played from the player's hand.

    Parameters:
    player (Player): The current player object.
    deck (Deck): The current deck object.

    Returns:
    int or None: The index of the card to be played, or None if no card can be played.

    Example implementation (Random strategy):

    """
    return BoundariesStrategy(player, deck)


def EastWestStrategy(player, deck):
    """
    East-West player strategy.

    This function should implement the strategy for East and West players.
    It should return the index of the card to be played from the player's hand.

    Parameters:
    player (Player): The current player object.
    deck (Deck): The current deck object.

    Returns:
    int or None: The index of the card to be played, or None if no card can be played.

    Example implementation (Max first strategy):
    """
    return BoundariesStrategy(player, deck)


# Additional example strategies


def RandomStrategy(player, deck):
    """
    Random strategy.

    This strategy randomly selects a card from the player's hand.

    Parameters:
    player (Player): The current player object.
    deck (Deck): The current deck object.

    Returns:
    int or None: The index of the card to be played, or None if no card can be played.
    """
    if player.hand:
        return random.randint(0, len(player.hand) - 1)
    return None


def MaxFirstStrategy(player, deck):
    """
    Max First strategy.

    This strategy always plays the highest-value card in the player's hand.

    Parameters:
    player (Player): The current player object.
    deck (Deck): The current deck object.

    Returns:
    int or None: The index of the card to be played, or None if no card can be played.
    """
    if not player.hand:
        return None

    value_order = deck.values
    max_index = 0
    max_value = -1

    for i, card in enumerate(player.hand):
        value = value_order.index(card.value)
        if value > max_value:
            max_value = value
            max_index = i

    return max_index


def BoundariesStrategy(player, deck):
    """
    Playing boundaries strategy
    """
    if not player.hand:
        return None

    turn_number = len(player.cVals) + 1
    card_vals = [card_to_val(card) for card in player.hand]

    extrema = max(card_vals) if turn_number % 2 else min(card_vals)

    return card_vals.index(extrema)


def card_to_val(card):
    return (rank_to_val[card.value] * 4) + suit_to_val[card.suit]


rank_to_val = {
    "2": 0,
    "3": 1,
    "4": 2,
    "5": 3,
    "6": 4,
    "7": 5,
    "8": 6,
    "9": 7,
    "10": 8,
    "J": 9,
    "Q": 10,
    "K": 11,
    "A": 12,
}

suit_to_val = {"Hearts": 0, "Diamonds": 1, "Clubs": 2, "Spades": 3}
