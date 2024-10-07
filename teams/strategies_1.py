import abc
import random
from typing import List

from CardGame import Deck, Player
from teams.strategies_5 import partner
from teams.strategy_1.turn_suits import get_fake_suits
from teams.strategy_1.util import card_to_idx

remaining_cards_1 = {}
remaining_cards_2 = {}


def initialize_totals(deck, remaining_cards):
    for card in deck.copyCards:
        remaining_cards[card] = 1

def initialize_totals_guessing(deck, remaining_cards):
    for card in deck:
        remaining_cards[card_to_idx(card)] = 1

def remove_seen_till_last_round(exposed_cards, remaining_cards):
    for player in exposed_cards:
        remove_card(exposed_cards[player], remaining_cards)

def remove_card(hand, remaining_cards):
    for card in hand:
        remaining_cards[card] = -1

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
    if player.name == "North" or player.name == "East":
        remaining_cards_local = remaining_cards_1
    else:
        remaining_cards_local = remaining_cards_2
    if remaining_cards_local == {}:
        initialize_totals(deck, remaining_cards_local)

    # remove_card(player.hand, remaining_cards_local)
    remove_seen_till_last_round(player.exposed_cards, remaining_cards_local)
    rem = []
    for card in remaining_cards_local.keys():
        if remaining_cards_local[card] != -1:
            rem.append(card)
    turn_number = len(player.cVals) + 1
    fake_suits = get_fake_suits(turn_number, rem, 4)

    # Check which suit has the most cards in it matching with the player's hand
    max_suit = -1
    max_suit_count = -1
    for suit in fake_suits:
        # Find number of cards matching with the player's hand
        count = 0
        for card in player.hand:
            if card.suit in suit:
                count += 1
        if count > max_suit_count:
            max_suit = suit
            max_suit_count = count

    # Find the card with the highest value and present in fake_suits[max_suit]
    max_index = 0
    max_value = -1
    for i, card in enumerate(player.hand):
        value = deck.values.index(card.value)
        if value > max_value and card.suit in max_suit:
            max_value = value
            max_index = i
    return max_index

def guessing(player, cards, round):
    if player.name == "North" or player.name == "East":
        remaining_cards_local = remaining_cards_1
    else:
        remaining_cards_local = remaining_cards_2

    if remaining_cards_local == {}:
        initialize_totals_guessing(cards, remaining_cards_local)
    remove_seen_till_last_round(player.exposed_cards, remaining_cards_local)
    rem = []
    for card in remaining_cards_local.keys():
        if remaining_cards_local[card] != -1:
            rem.append(card)
    turn_number = len(player.cVals) + 1
    fake_suits = get_fake_suits(turn_number, rem, 4)

    partner_card = player.exposed_cards[partner(player.name)][0]
    partner_card_idx = card_to_idx(partner_card)
    # Find the suit of the card exposed by the partner
    partner_suit = None

    # Get the suit containing partner card
    for suit in fake_suits:
        if partner_card_idx in suit:
            partner_suit = suit
            break

    # Return the cards in the fake_suits[partner_suit]
    returned_cards = []
    for i, card in enumerate(partner_suit):
        if i > 12 - round:
            break
        returned_cards.append(cards[card])
    return returned_cards

