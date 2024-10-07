from CardGame import Card


suit_offset = {"Hearts": 0, "Diamonds": 13, "Clubs": 26, "Spades": 39}
card_val = {
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


def card_to_idx(card: Card) -> int:
    suit_offset = suit_offset[card.suit]
    card_val = card_val[card.value]
    return suit_offset + card_val


