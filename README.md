# Project 2: Guess My Hand

## Citation and License
This project belongs to Department of Computer Science, Columbia University. It may be used for educational purposes under Creative Commons **with proper attribution and citation** for the author TAs **Raavi Gupta (First Author), Divyang Mittal and the Instructor, Prof. Kenneth Ross**.

## Summary

Course: COMS 4444 Programming and Problem Solving (Fall 2024)  
Problem Description: https://www.cs.columbia.edu/~kar/4444f24/node19.html  
Course Website: https://www.cs.columbia.edu/~kar/4444f24/  
University: Columbia University  
Instructor: Prof. Kenneth Ross  
Project Language: Python

### TA Designer for this project

Raavi Gupta

### Teaching Assistants for Course
1. Divyang Mittal
2. Raavi Gupta

### All course projects

## Installation

To install tkinter on macOS, run the following command:
```bash
brew install python-tk@3.X
```
For Windows, tkinter can be installed using pip:
```bash
pip install tk
```

## Usage

To view all options use python Guess-my-Hand-GUI.py -h. Apart from seed, the other flags will be used for competition among different teams.
```bash
python Guess-my-Hand-GUI.py  [--seed] 
```

## Testing the code

For testing the code internally in the team, you can use and modify the code present in player_strategies.py and guessing_functions.py.
Please only modify the code present in the following functions:
1. NorthSouthStrategy and EastWestStrategy for the file player_strategies.py
2. NorthSouthGuess and EastWestGuess for the file guessing_functions.py

## Submission

For submitting the code for each deliverable, open a pull request to merge your proposed player strategy and guessing strategy. This should be a single python file named "strategies_{group-number}" present in the teams folder (group number should be the allotted group number for this project). The python file should contain two functions:

1. playing(player, deck): Your strategy for playing a card given the information about your c's and the exposed cards of other players. 
2. guessing(player, cards, round): Your strategy for guessing the cards given the round number. Note: This function should return the guessed cards in the hands of their partner. For example, if the input player is North, the output should be the guess of the cards present in the hand of South.


