from collections import defaultdict
import random


def playing(player, deck):
    """
    Playing boundaries strategy
    """
    if not player.hand:
        return None

    turn_number = len(player.cVals) + 1
    card_vals = [card_to_val(card) for card in player.hand]

    extrema = max(card_vals) if turn_number % 2 == 0 else min(card_vals)

    return card_vals.index(extrema)


avg = [0] * 12
count = 0


def guessing(player, cards, round):
    # if round == 13:
    #     global count
    #     count += 1
    #     for i in range(len(player.cVals)):
    #         avg[i] = (avg[i] * (count - 1) + player.cVals[i]) / count

    #     print(player.name, avg)
    cp = {val: 1 / 52 for val in range(52)}

    for held_card in player.hand:
        del cp[card_to_val(held_card)]

    for exposed_cards_li in player.exposed_cards.values():
        for exposed_card in exposed_cards_li:
            del cp[card_to_val(exposed_card)]

    for played_card in player.played_cards:
        if card_to_val(played_card) in cp:
            del cp[card_to_val(played_card)]

    partner_name = partner(player.name)
    for i, card in enumerate(player.exposed_cards[partner_name]):
        val = card_to_val(card)
        if i % 2 == 0:
            for key in list(cp.keys()):
                if key <= val:
                    del cp[key]
        else:
            for key in list(cp.keys()):
                if key >= val:
                    del cp[key]

    for val in cp.keys():
        cp[val] = (13 - round) / len(cp)

    update_probabilities_with_guesses(player, cp, round)

    selected_vals = sorted(cp.keys(), key=lambda val: cp[val], reverse=True)[
        : 13 - round
    ]

    selected = []
    for card in cards:
        if card_to_val(card) in selected_vals:
            selected.append(card)
    # print(selected_vals, len(cp))
    # for k in cp:
    #     print(k, ":", cp[k])
    # print("\n\n")
    return selected


def update_probabilities_with_guesses(player, cp, round):
    """
    Update probabilities using previous guesses and correct guesses count (player.cVals).
    """
    partner_cards = {
        card_to_val(card) for card in player.exposed_cards[partner(player.name)]
    }
    for past_round, guess_set in enumerate(player.guesses):
        guess_set = [card_to_val(card) for card in guess_set]
        numerator = player.cVals[past_round]
        denominator = len(guess_set)

        for card_val in guess_set:
            if card_val in partner_cards:
                numerator -= 1

            elif card_val not in cp:
                denominator -= 1

        if denominator > 0:
            remaining_prob = numerator / denominator
            # print("Guessed", guess_set, remaining_prob, numerator)
            for card_val in guess_set:
                if card_val in cp:
                    if numerator <= 0:
                        del cp[card_val]
                    else:
                        cp[card_val] *= remaining_prob

        unguessed_cards = set()
        for card_val in cp:
            if card_val not in guess_set:
                unguessed_cards.add(card_val)

        # print(len(unguessed_cards), len(guess_set), len(cp))

        if len(unguessed_cards) > 0:
            missed_guesses = len(guess_set) - player.cVals[past_round]
            remaining_prob = min(missed_guesses / len(unguessed_cards), 1)
            # print("Unguessed", unguessed_cards, remaining_prob, missed_guesses)
            # print(missed_guesses, len(unguessed_cards))
            for card_val in unguessed_cards:
                if missed_guesses <= 0:
                    del cp[card_val]
                else:
                    cp[card_val] *= remaining_prob


def partner(name):
    if name == "North":
        return "South"
    if name == "South":
        return "North"
    if name == "East":
        return "West"
    if name == "West":
        return "East"
    raise Exception("Invalid name")


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
ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
