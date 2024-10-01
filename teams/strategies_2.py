import random


def playing(player, deck):
    """
    Playing strategy goes here
    """
    print("Playing strategy")
    if not player.hand:
        return None

    return 0


def guessing(player, cards, round):
    """
        Guessing strategy goes here
    """
    print("Guessing strategy")
    return random.sample(cards, 13 - round)
