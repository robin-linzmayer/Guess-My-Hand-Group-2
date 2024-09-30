import random


def NorthSouthGuess(player, cards, round):
    return random.sample(cards, 13 - round)


def EastWestGuess(player, cards, round):
    return random.sample(cards, 13 - round)
