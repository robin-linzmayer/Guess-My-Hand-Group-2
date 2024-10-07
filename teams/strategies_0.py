import random

test_play = {}
test_guess = {}

def playing(player, deck):
    """
    Max First strategy
    """
    if not player.hand:
        return None

    test_play[player.name] = "Playing"
    test_guess[player.name] = "Playing"

    print(test_play)
    print(test_guess)

    value_order = deck.values
    max_index = 0
    max_value = -1
    
    for i, card in enumerate(player.hand):
        value = value_order.index(card.value)
        if value > max_value:
            max_value = value
            max_index = i
    
    return max_index

def guessing(player, cards, round):
    test_play[player.name] = "Guessing"
    test_guess[player.name] = "Guessing"

    print(test_play)
    print(test_guess)

    return random.sample(cards, 13 - round)