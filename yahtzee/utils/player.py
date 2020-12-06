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
        self.theoretical_scorecard = {      # Scorecard that is calculated after each dice roll to see what scores are possible given that roll
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
        self.rolled_dice = []               # Result of the last roll of the dice
        self.frozen_dice = []               # Dice that are not re-rolled
        self.combined_dice = []             # Combination of dice that were just rolled and existing frozen dice
        self.num_dice = 5                   # Dice remaining to re-roll
        self.rolls_left = 3                 # Number of rolls remaining in turn



    #-------------------------------------------------------------------------------------------------#
    # Basic functionality methods
    #-------------------------------------------------------------------------------------------------#           

    # Utility method to combine rolled dice with frozen dice into one list, sort it, and validate its length 
    def combine_dice(self):
        self.combined_dice = self.rolled_dice + self.frozen_dice
        self.combined_dice.sort()
        if len(self.combined_dice) != 5:
            raise Exception("Error in Player.combine_dice: list of dice is not of length 5.")
        else:
            return True

    # Rolls proper number of dice, based on current value of num_dice
    def roll_dice(self):
        if self.rolls_left > 0:
            self.rest_theoretical_scorecard()
            self.rolled_dice = [random.randint(1, 6) for i in range(self.num_dice)]
            self.combine_dice()
            self.calculate_theoretical_scorecard()
            self.rolls_left -= 1
        else:
            raise Exception("Error in Player.roll(): No rolls remaining.")

    # Puts chosen dice in frozen_dice attribute and subtracts that from total dice remaining for this turn (dice selection happens in algorithm)
    def freeze_dice(self, dice):
        if len(dice) + len(self.frozen_dice) <= 5:
            self.frozen_dice.extend(dice)
            self.num_dice -= len(dice)
        else:
            raise Exception("Error in Player.freeze_dice(): More than 5 dice being stored.")
    
    # Resets turn-based parameters on player's object
    def end_turn(self):
        self.rolled_dice = []
        self.frozen_dice = []
        self.num_dice = 5
        self.rolls_left = 3 
    
    # Reset theoretical scorecard
    def rest_theoretical_scorecard(self):
        self.theoretical_scorecard = { 
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

    #-------------------------------------------------------------------------------------------------#
    # The following are computation methods to calculate the potential points for each entry in the scorecard based on the current roll of the dice and the frozen dice. 
    # Each entry in the scorecard has its own method. The computations happen in the Player class because the player would do those computations in a real game.
    # Then, the theoretical scorecard configuration for each entry is presented to whatever algorithm is being simulated. The algorithm makes the choice, and the appropriate dice are frozen. 
    #-------------------------------------------------------------------------------------------------#

    # Calculate top half of scorecard (items above the bonus)
    def calculate_top_half(self):
        # A very ugly way to iterate over the first 6 entries in the dictionary and make the relevant score calculations
        i = 1
        for key in self.theoretical_scorecard:
            total_score = 0
            for die in self.combined_dice:
                if die == i:
                    total_score += die
            self.theoretical_scorecard[key] = total_score
            i += 1
            if i > 6: 
                return 

    # Calculate three of a kind value based on current roll/frozen dice combo
    def calculate_three_kind(self):
        for i in range(1, 7):
            count = 0
            for die in self.combined_dice:
                if die == i:
                    count += 1
                # In a set of 5 dice, there can only be 1 three of a kind, so as soon as one is found set the score and return from this function
                if count == 3:
                    self.theoretical_scorecard["three_kind"] = 3 * i
                    return

    # Calculate four of a kind value based on current roll/frozen dice combo
    def calculate_four_kind(self):
        for i in range(1, 7):
            count = 0
            for die in self.combined_dice:
                if die == i:
                    count += 1
                # In a set of 5 dice, there can only be 1 four of a kind, so as soon as one is found set the score and return from this function
                if count == 4:
                    self.theoretical_scorecard["four_kind"] = 4 * i
                    return

    # Calculate full house based on current roll/frozen dice combo
    def calculate_full_house(self):
        # Leveraging the fact that the dice are sorted, just check if first 2 are the same and the last 3 are the same or vice versa and that all 5 are not the same
        if ((self.combined_dice[0] == self.combined_dice[1] and self.combined_dice[2] == self.combined_dice[4]) or \
            (self.combined_dice[0] == self.combined_dice[2] and self.combined_dice[3] == self.combined_dice[4])) and \
            self.combined_dice[0] != self.combined_dice[4]:
            self.theoretical_scorecard["full_house"] = 25

    # Calculate small straight based on current roll/frozen dice combo
    # There is definitely a cleaner way to do this, will revisit in the future
    def calculate_small_straight(self):
        # Remove duplicates from combined dice to remove edge cases from small straight test (i.e., [2, 3, 3, 4, 5]) then check that there are still at least 4 dice
        temp_dice = list(dict.fromkeys(self.combined_dice))
        if len(temp_dice) == 5:
            # Small straight in sorted list of 5 must start at postion 0 or position 1, so do two iterations to check for straight from those positions
            for i in range(2):
                if temp_dice[i + 1] == temp_dice[i] + 1 and temp_dice[i + 2] == temp_dice[i + 1] + 1 and \
                    temp_dice[i + 3] == temp_dice[i + 2] + 1:
                    self.theoretical_scorecard["sm_straight"] = 30
        elif len(temp_dice) == 4:
            # Small straight in sorted list of 4 must start at position 0
            if temp_dice[0 + 1] == temp_dice[0] + 1 and temp_dice[2] == temp_dice[1] + 1 and temp_dice[3] == temp_dice[2] + 1:
                self.theoretical_scorecard["sm_straight"] = 30
        else:
            return

    # Calculate large straight based on current roll/frozen dice combo
    def calculate_large_straight(self):
        if self.combined_dice[1] == self.combined_dice[0] + 1 and self.combined_dice[2] == self.combined_dice[1] + 1 and \
            self.combined_dice[3] == self.combined_dice[2] + 1 and self.combined_dice[4] == self.combined_dice[3] + 1:
            self.theoretical_scorecard["lg_straight"] = 40
            
    # Calculate Yahtzee based on current roll/frozen dice combo
    def calculate_yahtzee(self):
        if self.combined_dice[0] == self.combined_dice[-1]:
            self.theoretical_scorecard["yahtzee"] = 50

    # Calculate Chance value
    def calculate_chance(self):
        self.theoretical_scorecard["chance"] = sum(self.combined_dice)

    # Use all calculation methods to produce the theoretical scorecard for a given roll
    def calculate_theoretical_scorecard(self):
        self.calculate_top_half()
        self.calculate_three_kind()
        self.calculate_four_kind()
        self.calculate_full_house()
        self.calculate_small_straight()
        self.calculate_large_straight()
        self.calculate_yahtzee()
        self.calculate_chance()

    #-------------------------------------------------------------------------------------------------#
    # Debugging methods
    #-------------------------------------------------------------------------------------------------#

    # Print out the player's scorecard line by line
    def print_scorecard(self):
        for category in self.scorecard:
            print(category, ':', self.scorecard[category])

    # Print out the player's theoretical scorecard line by line baesd on their last roll
    def print_theoretical_scorecard(self):
        for category in self.theoretical_scorecard:
            print(category, ':', self.theoretical_scorecard[category])
