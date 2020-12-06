# Player class to store information about each player's current status

import random

class Player:
    def __init__(self, player_name):
        self.player_name = player_name
        # Scorecard follows the order of a real yahtzee scorecard, starting with 1's and ending with chance. The bonus is excluded because it is calculated at the end of the game.
        # Each tuple has the following structure: [score, [dice used to get score], number of rolls].
        self.scorecard = [
            [0, [], 0],
            [0, [], 0],
            [0, [], 0],
            [0, [], 0],
            [0, [], 0],
            [0, [], 0],
            [0, [], 0],
            [0, [], 0],
            [0, [], 0],
            [0, [], 0],
            [0, [], 0],
            [0, [], 0],
            [0, [], 0],
        ]
        # This is calculated after every dice roll and shows the possible scores should the algorithm decide to stop rolling and choose one. 
        # Values are only calculated for scores that are empty as of the current turn. This is simply to expose every possible state of the scorecard based on the current roll
        # and status of the game to that point for an algorithm to make decisions.
        self.theoretical_scorecard = [
            [0, [], 0],
            [0, [], 0],
            [0, [], 0],
            [0, [], 0],
            [0, [], 0],
            [0, [], 0],
            [0, [], 0],
            [0, [], 0],
            [0, [], 0],
            [0, [], 0],
            [0, [], 0],
            [0, [], 0],
            [0, [], 0],
        ]
                  
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
            self.reset_theoretical_scorecard()
            self.rolled_dice = [random.randint(1, 6) for i in range(self.num_dice)]
            self.rolls_left -= 1
            self.combine_dice()
            self.calculate_theoretical_scorecard()

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
    def reset_theoretical_scorecard(self):
        self.theoretical_scorecard = [
            [0, [], 0],
            [0, [], 0],
            [0, [], 0],
            [0, [], 0],
            [0, [], 0],
            [0, [], 0],
            [0, [], 0],
            [0, [], 0],
            [0, [], 0],
            [0, [], 0],
            [0, [], 0],
            [0, [], 0],
            [0, [], 0],
        ]

    #-------------------------------------------------------------------------------------------------#
    # The following are computation methods to calculate the potential points for each entry in the scorecard based on the current roll of the dice and the frozen dice. 
    # Each entry in the scorecard has its own method. The computations happen in the Player class because the player would do those computations in a real game.
    # Then, the theoretical scorecard configuration for each entry is presented to whatever algorithm is being simulated. The algorithm makes the choice, and the appropriate dice are frozen. 
    #-------------------------------------------------------------------------------------------------#

    # Calculate top half of scorecard (items above the bonus on a real yahtzee card)
    def calculate_top_half(self):
        # Loop through 1's --> 6's
        for i in range(6):
            # Checks if scorecard entry has not been scored yet. Looks at # of rolls because it is possible to score a 0 on an entry after 3 rolls.
            if self.scorecard[i][2] == 0:
                # Score the relevant dice and store the related data in the corresponding entry in the theoretical scorecard
                current_dice = [x for x in self.combined_dice if x == i + 1]
                self.theoretical_scorecard[i][0] = sum(current_dice)
                self.theoretical_scorecard[i][1] = current_dice
                self.theoretical_scorecard[i][2] = 3 - self.rolls_left                

    # Calculate three of a kind value based on current roll/frozen dice combo
    def calculate_three_kind(self):
        if self.scorecard[6][2] == 0:
            # Check for a three of kind for each possible value of the dice
            for i in range(1, 7):
                current_dice = [x for x in self.combined_dice if x == i]
                if len(current_dice) == 3:
                    self.theoretical_scorecard[6][0] = sum(current_dice)
                    self.theoretical_scorecard[6][1] = current_dice
                    self.theoretical_scorecard[6][2] = 3 - self.rolls_left
                    return
            self.theoretical_scorecard[6][2] = 3 - self.rolls_left

    # Calculate four of a kind value based on current roll/frozen dice combo
    def calculate_four_kind(self):
        if self.scorecard[7][2] == 0:
            # Check for a four of kind for each possible value of the dice
            for i in range(1, 7):
                current_dice = [x for x in self.combined_dice if x == i]
                if len(current_dice) == 4:
                    self.theoretical_scorecard[7][0] = sum(current_dice)
                    self.theoretical_scorecard[7][1] = current_dice
                    self.theoretical_scorecard[7][2] = 3 - self.rolls_left
                    return
            self.theoretical_scorecard[7][2] = 3 - self.rolls_left

    # Calculate full house based on current roll/frozen dice combo
    def calculate_full_house(self):
        if self.scorecard[8][2] == 0:
            # Leveraging the fact that the dice are sorted, just check if first 2 are the same and the last 3 are the same or vice versa and that all 5 are not the same
            if ((self.combined_dice[0] == self.combined_dice[1] and self.combined_dice[2] == self.combined_dice[4]) or \
                (self.combined_dice[0] == self.combined_dice[2] and self.combined_dice[3] == self.combined_dice[4])) and \
                self.combined_dice[0] != self.combined_dice[4]:
                self.theoretical_scorecard[8][0] = 25
                self.theoretical_scorecard[8][1] = self.combined_dice
            self.theoretical_scorecard[8][2] = 3 - self.rolls_left
    # Calculate small straight based on current roll/frozen dice combo
    def calculate_small_straight(self):
        # Remove duplicates from combined dice to remove edge cases from small straight test (i.e., [2, 3, 3, 4, 5]) then check that there are still at least 4 dice
        temp_dice = list(dict.fromkeys(self.combined_dice))
        if len(temp_dice) == 5:
            # Small straight in sorted list of 5 must start at postion 0 or position 1, so do two iterations to check for straight from those positions
            for i in range(2):
                if temp_dice[i + 1] == temp_dice[i] + 1 and temp_dice[i + 2] == temp_dice[i + 1] + 1 and \
                    temp_dice[i + 3] == temp_dice[i + 2] + 1:
                    self.theoretical_scorecard[9][0] = 30
                    self.theoretical_scorecard[9][1] = temp_dice[i:]
            self.theoretical_scorecard[9][2] = 3 - self.rolls_left
        elif len(temp_dice) == 4:
            # Small straight in sorted list of 4 must start at position 0
            if temp_dice[0 + 1] == temp_dice[0] + 1 and temp_dice[2] == temp_dice[1] + 1 and temp_dice[3] == temp_dice[2] + 1:
                self.theoretical_scorecard[9][0] = 30
                self.theoretical_scorecard[9][1] = temp_dice
            self.theoretical_scorecard[9][2] = 3 - self.rolls_left
        else:
            return

    # Calculate large straight based on current roll/frozen dice combo
    def calculate_large_straight(self):
        if self.combined_dice[1] == self.combined_dice[0] + 1 and self.combined_dice[2] == self.combined_dice[1] + 1 and \
            self.combined_dice[3] == self.combined_dice[2] + 1 and self.combined_dice[4] == self.combined_dice[3] + 1:
            self.theoretical_scorecard[10][0] = 40
            self.theoretical_scorecard[10][1] = self.combined_dice
        self.theoretical_scorecard[10][2] = 3 - self.rolls_left
            
    # Calculate Yahtzee based on current roll/frozen dice combo
    def calculate_yahtzee(self):
        if self.combined_dice[0] == self.combined_dice[-1]:
            self.theoretical_scorecard[11][0] = 50
            self.theoretical_scorecard[11][1] = self.combined_dice
        self.theoretical_scorecard[11][2] = 3 - self.rolls_left

    # Calculate Chance value
    def calculate_chance(self):
        self.theoretical_scorecard[12][0] = sum(self.combined_dice)
        self.theoretical_scorecard[12][1] = self.combined_dice
        self.theoretical_scorecard[12][2] = 3 - self.rolls_left

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
        for i in range(13):
            print(self.scorecard[i])

    # Print out the player's theoretical scorecard line by line baesd on their last roll
    def print_theoretical_scorecard(self):
        for i in range(13):
            print(self.theoretical_scorecard[i])
