import tkinter as tk
import random
import argparse
import importlib.util
import sys
from copy import copy
from CardGame import Card, Deck, Player
from player_strategies import NorthSouthStrategy, EastWestStrategy
from guessing_functions import NorthSouthGuess, EastWestGuess

class Game:
        
    def deal_initial_cards(self, deck):
        for _ in range(13):  # Deal 13 cards to each player
            for player in self.players:
                player.draw(self.deck)
        for player in self.players:
            player.hand = sorted(player.hand, key=lambda element: deck.values.index(element.value))

    def reset_game(self, seed):
        self.round = 1
        self.deck = Deck(seed)
        self.copyCards = copy(self.deck.cards)
        self.players = [
            Player("North", NorthSouthStrategy),
            Player("East", EastWestStrategy),
            Player("South", NorthSouthStrategy),
            Player("West", EastWestStrategy)
        ]
        self.current_player = 0
        self.individual_scores = {"North": 0, "East": 0, "South": 0, "West": 0}
        self.partnership_scores = {"NS": 0, "EW": 0}
        self.deal_initial_cards(self.deck)

    def step(self):
        for i, player in enumerate(self.players):
            card_index = player.strategy(player, self.deck)
            played_card = player.play_card(card_index)
            for j, other_player in enumerate(self.players):
                if i != j:
                    other_player.update_exposed_cards(player.name, played_card)

        northGuess = NorthSouthGuess(self.players[0], self.copyCards, self.round)
        eastGuess = EastWestGuess(self.players[1], self.copyCards, self.round)
        southGuess = NorthSouthGuess(self.players[2], self.copyCards, self.round)
        westGuess = EastWestGuess(self.players[3], self.copyCards, self.round)

        cNorth = len(set(northGuess).intersection(set(self.players[2].hand)))
        cEast = len(set(eastGuess).intersection(set(self.players[3].hand)))
        cSouth = len(set(southGuess).intersection(set(self.players[0].hand)))
        cWest = len(set(westGuess).intersection(set(self.players[1].hand)))

        self.individual_scores["North"] = cNorth
        self.individual_scores["East"] = cEast
        self.individual_scores["South"] = cSouth
        self.individual_scores["West"] = cWest
        self.partnership_scores["NS"] += cNorth + cSouth
        self.partnership_scores["EW"] += cEast + cWest

    def is_game_over(self):
        return all(len(player.hand) == 0 for player in self.players)

    def simulate_game(self):
        while not self.is_game_over():
            self.step()
            self.round += 1

    def simulate_n_games(self, n):
        total_ns_score = 0
        total_ew_score = 0

        for _ in range(n):
            new_seed = random.randint(0, 1000000)  # Generate a new random seed
            self.reset_game(seed=new_seed)
            self.simulate_game()
            total_ns_score += self.partnership_scores['NS']
            total_ew_score += self.partnership_scores['EW']
            print(f"NS Score: {self.partnership_scores['NS']}, EW Score: {self.partnership_scores['EW']}")

        avg_ns_score = total_ns_score / n
        avg_ew_score = total_ew_score / n

        print(f"Average NS Score after {n} games: {avg_ns_score}")
        print(f"Average EW Score after {n} games: {avg_ew_score}")

def import_class_from_file(folder, file_name, class_name):
    file_path = f"{folder}/{file_name}.py"
    spec = importlib.util.spec_from_file_location(file_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[file_name] = module
    spec.loader.exec_module(module)
    return getattr(module, class_name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Guess My Hand")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for card shuffling")
    parser.add_argument('--nsStrategy', type=int, choices=range(0, 11), help='North-South Strategy (1-10)')
    parser.add_argument('--ewStrategy', type=int, choices=range(0, 11), help='East-West Strategy (1-10)')
    parser.add_argument('--nsGuesses', type=int, choices=range(0, 11), help='North-South Guesses (1-10)')
    parser.add_argument('--ewGuesses', type=int, choices=range(0, 11), help='East-West Guesses (1-10)')

    args = parser.parse_args()
    folder = "teams"
    
    # Import strategies based on flag values
    if args.nsStrategy in range(0, 11):
        file_name = f"strategies_{args.nsStrategy}"
        class_name = "playing"
        NorthSouthStrategy = import_class_from_file(folder, file_name, class_name)
    if args.ewStrategy in range(0, 11):
        file_name = f"strategies_{args.ewStrategy}"
        class_name = "playing"
        EastWestStrategy = import_class_from_file(folder, file_name, class_name)
    if args.nsGuesses in range(0, 11):
        file_name = f"strategies_{args.nsGuesses}"
        class_name = "guessing"
        NorthSouthGuess = import_class_from_file(folder, file_name, class_name)
    if args.ewGuesses in range(0, 11):
        file_name = f"strategies_{args.ewGuesses}"
        class_name = "guessing"
        EastWestGuess = import_class_from_file(folder, file_name, class_name)
    else:
        print("Running default code...")

    # Use system time for seeding randomness
    # random.seed()

    game = Game()
    game.simulate_n_games(10000)