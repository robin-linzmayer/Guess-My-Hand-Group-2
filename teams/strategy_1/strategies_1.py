import abc
import random
from typing import List

from CardGame import Deck, Player


class PlayingStrategy(abc.ABC):
    @abc.abstractmethod
    def guess(self, player: Player, cards, round) -> List[int]:
        pass
    
    @abc.abstractmethod
    def play(self, player: Player, deck: Deck) -> int:
        pass


class DefaultPlayingStrategy(PlayingStrategy):
    def guess(self, player: Player, cards, round) -> List[int]:
        return random.sample(cards, 13 - round)

    def play(self, player: Player, deck: Deck) -> int:
        if not player.hand:
            return None

        # Find the card with the highest value and suit

        value_order = deck.values
        max_index = 0
        max_value = -1

        for i, card in enumerate(player.hand):
            value = value_order.index(card.value)
            if value > max_value:
                max_value = value
                max_index = i
        return max_index



def playing(player, deck):
    return DefaultPlayingStrategy().play(player, deck)


def guessing(player, cards, round):
    return DefaultPlayingStrategy().guess(player, cards, round)

