from CardGame import Card


def card_to_idx(card: Card) -> int:
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
    suit_offset = suit_offset[card.suit]
    card_val = card_val[card.value]
    return suit_offset + card_val

def idx_to_card(idx: int) -> Card:
    suit = ["Hearts", "Diamonds", "Clubs", "Spades"][idx // 13]
    value = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"][idx % 13]
    return Card(suit, value)


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

def index_in_deck(card: Card, deck: list) -> int:
    for i, c in enumerate(deck):
        if c == card:
            return i
    return -1
