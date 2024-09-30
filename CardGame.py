import random

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        self.map = {"Hearts": "♥", "Diamonds": "♦", "Clubs": "♣", "Spades": "♠"}
        self.rmap = {"♥": "Hearts", "♦": "Diamonds", "♣": "Clubs", "♠": "Spades"}

    def __str__(self):
        return f"{self.value} of {self.suit}"

class Deck:
    def __init__(self, seed=42):
        self.suits = ["Hearts", "Diamonds", "Clubs", "Spades"] 
        self.values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        self.cards = [Card(suit, value) for suit in self.suits for value in self.values]
        random.seed(seed)
        random.shuffle(self.cards)

    def draw(self):
        if len(self.cards) > 0:
            return self.cards.pop()
        return None

class Player:
    def __init__(self, name, strategy):
        self.name = name
        self.hand = []
        self.played_cards = []
        self.strategy = strategy
        self.exposed_cards = {"North": [], "East": [], "South": [], "West": []}
        self.cVals = []


    def draw(self, deck):
        card = deck.draw()
        if card:
            self.hand.append(card)

    def play_card(self, index):
        if 0 <= index < len(self.hand):
            card = self.hand.pop(index)
            self.played_cards.append(card)
            return card
        return None

    def update_exposed_cards(self, player_name, card):
        self.exposed_cards[player_name].append(card)
