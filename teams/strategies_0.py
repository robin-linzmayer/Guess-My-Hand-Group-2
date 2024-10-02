import random

def playing(player, deck):
    """
    Max First strategy
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

def guessing(player, cards, round):
    return random.sample(cards, 13 - round)