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
    def __init__(self, master, seed=42):
        self.master = master
        self.master.title("Guess My Hand")
        self.master.geometry("1200x800")
        self.seed = seed
        self.round = 1
        self.master.configure(bg='#2ecc71')
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
        self.setup_gui()
        self.deal_initial_cards(self.deck)
        self.update_display()

    def setup_gui(self):
        self.player_frames = []
        for i, player in enumerate(self.players):
            frame = tk.Frame(self.master, borderwidth=2, relief="ridge", bg='#27ae60')
            frame.grid(row=i//2 + 1, column=i%2, padx=10, pady=10, sticky="nsew")
            label = tk.Label(frame, text=player.name, font=("Arial", 14, "bold"), bg='#27ae60', fg='white')
            label.pack(pady=5)
            self.player_frames.append(frame)

        self.reset_button = tk.Button(self.master, text="Reset", command=self.reset_game, font=("Arial", 12), bg='black', fg='white')
        self.reset_button.grid(row=0, column=0, pady=10)

        self.step_button = tk.Button(self.master, text="Step", command=self.step, font=("Arial", 12), bg='black', fg='white')
        self.step_button.grid(row=0, column=0, columnspan=2, pady=10)

        self.play_all_button = tk.Button(self.master, text="Play All", command=self.play_all, font=("Arial", 12), bg='black', fg='white')
        self.play_all_button.grid(row=0, column=1, pady=10)

        self.played_cards_frame = tk.Frame(self.master, borderwidth=2, relief="ridge", bg='#27ae60')
        self.played_cards_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.played_cards_label = tk.Label(self.played_cards_frame, text="Played Cards:", font=("Arial", 14, "bold"), bg='#27ae60', fg='white')
        self.played_cards_label.pack(pady=5)

        self.played_cards_columns = []
        for player in self.players:
            column = tk.Frame(self.played_cards_frame, bg='#27ae60')
            column.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5)
            tk.Label(column, text=player.name, font=("Arial", 12), bg='#27ae60', fg='white').pack()
            self.played_cards_columns.append(column)

        self.score_frame = tk.Frame(self.master, borderwidth=2, relief="ridge", bg='#27ae60')
        self.score_frame.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.individual_score_frame = tk.Frame(self.score_frame, bg='#27ae60')
        self.individual_score_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=10)
        tk.Label(self.individual_score_frame, text="Individual Scores", font=("Arial", 14, "bold"), bg='#27ae60', fg='white').pack(pady=5)

        self.individual_score_labels = {}
        ns_frame = tk.Frame(self.individual_score_frame, bg='#27ae60')
        ns_frame.pack(fill=tk.X)
        ew_frame = tk.Frame(self.individual_score_frame, bg='#27ae60')
        ew_frame.pack(fill=tk.X)

        self.individual_score_labels["North"] = tk.Label(ns_frame, text="North: 0", font=("Arial", 12), bg='#27ae60', fg='white')
        self.individual_score_labels["North"].pack(side=tk.LEFT, expand=True)
        self.individual_score_labels["South"] = tk.Label(ns_frame, text="South: 0", font=("Arial", 12), bg='#27ae60', fg='white')
        self.individual_score_labels["South"].pack(side=tk.LEFT, expand=True)
        self.individual_score_labels["East"] = tk.Label(ew_frame, text="East: 0", font=("Arial", 12), bg='#27ae60', fg='white')
        self.individual_score_labels["East"].pack(side=tk.LEFT, expand=True)
        self.individual_score_labels["West"] = tk.Label(ew_frame, text="West: 0", font=("Arial", 12), bg='#27ae60', fg='white')
        self.individual_score_labels["West"].pack(side=tk.LEFT, expand=True)

        self.partnership_score_frame = tk.Frame(self.score_frame, bg='#27ae60')
        self.partnership_score_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=5)
        tk.Label(self.partnership_score_frame, text="Partnership Scores", font=("Arial", 14, "bold"), bg='#27ae60', fg='white').pack(pady=5)

        self.ns_score_label = tk.Label(self.partnership_score_frame, text="NS: 0", font=("Arial", 12), bg='#27ae60', fg='white')
        self.ns_score_label.pack()
        self.ew_score_label = tk.Label(self.partnership_score_frame, text="EW: 0", font=("Arial", 12), bg='#27ae60', fg='white')
        self.ew_score_label.pack()

        self.guesses_frame = tk.Frame(self.master, borderwidth=2, relief="ridge", bg='#27ae60')
        self.guesses_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        tk.Label(self.guesses_frame, text="Guesses", font=("Arial", 14, "bold"), bg='#27ae60', fg='white').pack(pady=5)
        

        self.status_label = tk.Label(self.master, text="", font=("Arial", 12), bg='#2ecc71', fg='white')
        self.status_label.grid(row=6, column=0, columnspan=2, pady=10)

        for i in range(2):
            self.master.grid_columnconfigure(i, weight=1)
        for i in range(7):
            self.master.grid_rowconfigure(i, weight=1)

    def deal_initial_cards(self, deck):
        for _ in range(13):  # Deal 13 cards to each player
            for player in self.players:
                player.draw(self.deck)
        for player in self.players:
            player.hand = sorted(player.hand, key=lambda element: deck.values.index(element.value))

    def update_display(self):
        for i, player in enumerate(self.players):
            for widget in self.player_frames[i].winfo_children()[1:]:
                widget.destroy()
            card_frame = tk.Frame(self.player_frames[i], bg='#27ae60')
            card_frame.pack(fill=tk.BOTH, expand=True)
            for j, card in enumerate(player.hand):
                color = 'red' if card.suit in ["Hearts", "Diamonds"] else 'black'
                tk.Label(card_frame, text=f"{card.map[card.suit]}{card.value}", font=("Arial", 12), bg='#27ae60', fg=color).pack(side=tk.LEFT, padx=2)

        for i, column in enumerate(self.played_cards_columns):
            for widget in column.winfo_children()[1:]:
                widget.destroy()
            played_cards = self.players[i].played_cards
            for j, card in enumerate(played_cards):
                color = 'red' if card.suit in ["Hearts", "Diamonds"] else 'black'
                tk.Label(column, text=f"{card.map[card.suit]}{card.value}", font=("Arial", 12), bg='#27ae60', fg=color).pack()

        for player_name, score in self.individual_scores.items():
            self.individual_score_labels[player_name].config(text=f"{player_name}: {score}")

        self.ns_score_label.config(text=f"NS: {self.partnership_scores['NS']}")
        self.ew_score_label.config(text=f"EW: {self.partnership_scores['EW']}")

    def reset_game(self):
        self.round = 1
        self.deck = Deck(self.seed)
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
        self.step_button.config(state="normal")
        self.play_all_button.config(state="normal")
        self.update_display()
        self.status_label.config(text="Game reset. Click 'Step' to start a new round.")

        # Reset guesses
        for widget in self.guesses_frame.winfo_children()[1:]:
            widget.destroy()

    def step(self):
        print(f"Round {self.round}")
        for i, player in enumerate(self.players):
            card_index = player.strategy(player, self.deck)
            played_card = player.play_card(card_index)
            print(player.name, played_card.value, played_card.suit)
            # Update exposed cards for other players
            for j, other_player in enumerate(self.players):
                if i != j:
                    other_player.update_exposed_cards(player.name, played_card)

        northGuess = NorthSouthGuess(self.players[0], self.copyCards, self.round)
        eastGuess = EastWestGuess(self.players[1], self.copyCards, self.round)
        southGuess = NorthSouthGuess(self.players[2], self.copyCards, self.round)
        westGuess = EastWestGuess(self.players[3], self.copyCards, self.round)
        for widget in self.guesses_frame.winfo_children()[1:]:
            widget.destroy()

        # Update guess labels with colored cards
        for player_name, guess in zip(["North", "East", "South", "West"], [northGuess, eastGuess, southGuess, westGuess]):
            guess_frame = tk.Frame(self.guesses_frame, bg='#27ae60')
            guess_frame.pack(fill=tk.X)
            guess = sorted(guess, key=lambda element: self.deck.values.index(element.value))
            tk.Label(guess_frame, text=f"{player_name}: ", font=("Arial", 12), bg='#27ae60', fg='white').pack(side=tk.LEFT)
            for card in guess:
                color = 'red' if card.suit in ["Hearts", "Diamonds"] else 'black'
                tk.Label(guess_frame, text=f"{card.map[card.suit]}{card.value}", font=("Arial", 12), bg='#27ae60', fg=color).pack(side=tk.LEFT, padx=2)

        cNorth = len(set(northGuess).intersection(set(self.players[2].hand)))
        self.players[0].cVals.append(cNorth)
        cEast = len(set(eastGuess).intersection(set(self.players[3].hand)))
        self.players[1].cVals.append(cEast)
        cSouth = len(set(southGuess).intersection(set(self.players[0].hand)))
        self.players[2].cVals.append(cSouth)
        cWest = len(set(westGuess).intersection(set(self.players[1].hand)))
        self.players[3].cVals.append(cWest)

        self.individual_scores["North"] = cNorth
        self.individual_scores["East"] = cEast
        self.individual_scores["South"] = cSouth
        self.individual_scores["West"] = cWest
        self.partnership_scores["NS"] += cNorth + cSouth
        self.partnership_scores["EW"] += cEast + cWest

        print("-"*100)
        self.update_display()

        if self.is_game_over():
            self.end_game()
        else:
            self.status_label.config(text=f"Round {self.round} completed. Click 'Step' for the next round.")
            self.round += 1

    def play_all(self):
        while not self.is_game_over():
            self.step()
        self.end_game()

    def is_game_over(self):
        return all(len(player.hand) == 0 for player in self.players)

    def end_game(self):
        self.status_label.config(text=f"Game Over: All cards have been played! Total rounds: {self.round}")
        self.step_button.config(state="disabled")
        self.play_all_button.config(state="disabled")
        self.reset_button.config(state="normal")

def import_class_from_file(folder, file_name, class_name):
    file_path = f"{folder}/{file_name}.py"
    spec = importlib.util.spec_from_file_location(file_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[file_name] = module
    spec.loader.exec_module(module)
    return getattr(module, class_name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Guess My Hand")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for card shuffling")
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
        NorthSouthGuesses = import_class_from_file(folder, file_name, class_name)
    if args.ewGuesses in range(0, 11):
        file_name = f"strategies_{args.ewGuesses}"
        class_name = "guessing"
        EastWestGuesses = import_class_from_file(folder, file_name, class_name)
    else:
        print("Running default code...")

    root = tk.Tk()
    game = Game(root, seed=args.seed)
    root.mainloop()