# Player class to store information about each player's current status

import random

class Player:
    def __init__(self, player_name):
        self.player_name = player_name
        self.scorecard = {
            "ones": 0,
            "twos": 0,
            "threes": 0,
            "fours": 0,
            "fives": 0,
            "sixes": 0,
            "bonus": 0,
            "three_kind": 0,
            "four_kind": 0,
            "full_house": 0,
            "sm_straight": 0,
            "lg_straight": 0,
            "yahtzee": 0,
            "chance": 0
        }                 
        self.bonus = False                  # Did player get bonus by having >=63 points on top half of scorecard
        self.roll = []                      # Result of the last roll of the dice
        self.frozen_dice = []               # Dice that are not re-rolled
        self.num_dice = 5                   # Dice remaining to re-roll
        self.rolls_left = 3                 # Number of rolls remaining in turn

    def reset(self):
        self.player_name = ""
        self.scorecard = {
            "ones": 0,
            "twos": 0,
            "threes": 0,
            "fours": 0,
            "fives": 0,
            "sixes": 0,
            "bonus": 0,
            "three_kind": 0,
            "four_kind": 0,
            "full_house": 0,
            "sm_straight": 0,
            "lg_straight": 0,
            "yahtzee": 0,
            "chance": 0
        }            
        self.bonus = False
        self.roll = []
        self.frozen_dice = []
        self.num_dice = 5
        self.rolls_left = 3

    # Resets turn-based parameters on player's object
    def end_turn(self):
        self.roll = []
        self.frozen_dice = []
        self.num_dice = 5
        self.rolls_left = 3 

    # Rolls proper number of dice, based on current value of num_dice
    def roll_dice(self):
        if self.rolls_left > 0:
            self.roll = [random.randint(1, 6) for i in range(self.num_dice)]
        else:
            raise Exception("Error in Player.roll(): No rolls remaining.")

    # Puts chosen dice in frozen_dice attribute and subtracts that from total dice remaining for this turn (dice selection happens in algorithm)
    def freeze_dice(self, dice):
        if len(dice) + len(self.frozen_dice) <= 5:
            self.frozen_dice.extend(dice)
            self.num_dice -= len(dice)
        else:
            raise Exception("Error in Player.freeze_dice(): More than 5 dice being stored.")

    # Update player's scorecard at the end of their turn    
    def update_scorecard(self, category, value):
        self.scorecard[category] = value
    
    # Print out the player's scorecard line by line
    def print_scorecard(self):
        for category in self.scorecard:
            print(category, ':', self.scorecard[category])
