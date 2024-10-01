import random

def playing(player, deck):
    """
    Playing strategy goes here (what card will the player expose to their partner)
    """
    # Todo some basic way of conveying information to be used in guessing
    return 0

def get_guess_deck(player, cards):
    """
    This function takes in the list of all cards in the game and removes cards that would be illogical guesses.
    Illogical guesses include:
        - Cards in the players own hand
        - Cards that have been exposed by other players in the game

    :param player:
    :param cards: list[Card]
    :return: list[Card]
    """
    # Remove cards in player's hand
    guess_deck = set(cards) - set(player.hand)
    # Remove cards that have been exposed
    for _, exposed_cards in player.exposed_cards.items():
        if len(exposed_cards) > 0:
            guess_deck = guess_deck - set(exposed_cards)
    return list(guess_deck)

def guessing(player, cards, round):
    """
    Guessing strategy goes here (number of guesses of your partner's cards)
    """
    guess_deck = get_guess_deck(player, cards)
    # Todo use exposed hand from partner on turn to reweight guesses
    # Todo in guess_deck there could be a distribution of probablities (currently uniform) to weight guessing.
    return random.sample(guess_deck, 13 - round)
