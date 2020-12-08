# Player class to store information about each player's current status

import random
import copy

class Player:
    def __init__(self, player_name):
        self.player_name = player_name
        self.score = 0          # Total score, calculated at the end of the game

        # Scorecard follows the order of a real yahtzee scorecard, starting with 1's and ending with chance. The bonus is excluded because it is calculated at the end of the game
        # Each tuple has the following structure: [score, [dice used to get score], number of rolls]
        self.scorecard = [
            [0, [], 0],         # 1's (value of dice)
            [0, [], 0],         # 2's (value of dice)
            [0, [], 0],         # 3's (value of dice)
            [0, [], 0],         # 4's (value of dice)
            [0, [], 0],         # 5's (value of dice)
            [0, [], 0],         # 6's (value of dice)
            [0, [], 0],         # Three of a Kind (value of dice)
            [0, [], 0],         # Four of a Kind (value of dice)
            [0, [], 0],         # Full House (25)
            [0, [], 0],         # Small Straight (30)
            [0, [], 0],         # Large Straight (40)
            [0, [], 0],         # Yahtzee (50)
            [0, [], 0],         # Chance (value of dice)
        ]

        # This is calculated after every dice roll and shows the possible scores for the given set of dice
        # Values are only calculated for scores that are empty as of the current turn. This is simply to only show feasible outcomes based on the roll and state of the game
        # Each tuple has the following structure: [score, [indices in self.__dice of dice used to get score], number of rolls]
        self.__theoretical_scorecard = [
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
        self.__dice = [0, 0, 0, 0, 0]         # Master list of dice - index matters, and these dice are preserved positionally in all scoring and rolling calculations
        self.__sorted_dice = []               # Sorted version of master dice list to make some scoring calculations easier. Index does not matter in this list - calculations are performed with sorted list then mapped back to the indices of master list
        self.__rolls_left = 3                 # Number of rolls remaining in turn


    #-------------------------------------------------------------------------------------------------#
    # Basic functionality methods
    #-------------------------------------------------------------------------------------------------#           

    # Rolls dice according to the dice_to_roll boolean list and calculates the theoretical scorecard which results (Positions with "True" are rolled).
    # For example, if self.__dice = [2, 3, 4, 4, 3] and dice_to_roll = [True, False, False, True, True], after this method self.__dice = [?, 3, 4, ?, ?] where '?' means the die was rolled.
    def roll_dice(self, dice_to_roll):
        if self.__rolls_left > 0:
            for i in range(5):
                if dice_to_roll[i] == True:
                    self.__dice[i] = random.randint(1, 6)
            self.__rolls_left -= 1
            self.__sorted_dice = copy.deepcopy(self.__dice)     # Deepcopy to avoid any issues when perfomring calculations and moving things around
            self.__sorted_dice.sort()                           # Sort the rolled dice for some scoring calculations
            self.__calculate_yahtzee_bonus()                    # Check to see if this is the palyer's second (or more) yahtzee to assign +100 point bonus
            self.__reset_theoretical_scorecard()                # Clear theoretical scorecard from last roll   
            self.__calculate_theoretical_scorecard()
        else:
            raise Exception("Error in Player.roll_dice(): No rolls remaining.")


    # Resets turn-based parameters on player's object and fills in whatever scoring option is chosen for that round
    # Inputs are the index of the score type on the score card (i.e., if scoring 1's, enter 0.) and dice_indices stored in the theoretical scorecard
    # We store the indices on the theoretical scorecard but the actual dice on the real scorecard because the indices are meaningless after the turn is over
    def end_turn(self, score_type):
        self.scorecard[score_type][0] = self.__theoretical_scorecard[score_type][0]
        self.scorecard[score_type][1] = self.__dice
        self.scorecard[score_type][2] = 3 - self.__rolls_left
        self.__rolls_left = 3 
        self.__reset_theoretical_scorecard()
    

    # Reset theoretical scorecard
    def __reset_theoretical_scorecard(self):
        self.__theoretical_scorecard = [
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
    # Computation methods to calculate the potential points for each entry in the scorecard based on the current roll of the dice
    #-------------------------------------------------------------------------------------------------#

    # Calculate top half of scorecard (items above the bonus on a real yahtzee card)
    def __calculate_top_half(self):
        
        for i in range(6):                                                          # Loop through 1's --> 6's
            if self.scorecard[i][2] == 0:                                           # Checks if scorecard entry has not been scored yet. Looks at # of rolls because it is possible to score a 0 on an entry after 3 rolls
                dice_indices = [j for j in range(5) if self.__dice[j] == i + 1]     # Store the index of the dice used to score the given value
                self.__theoretical_scorecard[i][0] = len(dice_indices) * (i + 1)    
                self.__theoretical_scorecard[i][1] = dice_indices                   
                self.__theoretical_scorecard[i][2] = 3 - self.__rolls_left                


    # Calculate three of a kind value based on current roll
    def __calculate_three_kind(self):
        if self.scorecard[6][2] == 0:                                               # Checks if scorecard entry has not been scored yet. Looks at # of rolls because it is possible to score a 0 on an entry after 3 rolls
            for i in range(6):                                                      # For each die value, look for three of a kind, store the indices of the dice in the dice_indices array, and update theoretical scorecard
                dice_indices = [j for j in range(5) if self.__dice[j] == i + 1]     # Store the index of the dice used to score the given value
                if len(dice_indices) == 3:                                          # Only one three of a kind can exist, so once it is found update the theoretical scorecard and return from the function
                    self.__theoretical_scorecard[6][0] = 3 * (i + 1)
                    self.__theoretical_scorecard[6][1] = dice_indices
                    self.__theoretical_scorecard[6][2] = 3 - self.__rolls_left
                    return
            self.__theoretical_scorecard[6][2] = 3 - self.__rolls_left              # Set the rolls used even if we don't have a three of a kind to keep track of how many it actually takes


    # Calculate four of a kind value based on current roll
    def __calculate_four_kind(self):
        if self.scorecard[7][2] == 0:                                               # Checks if scorecard entry has not been scored yet. Looks at # of rolls because it is possible to score a 0 on an entry after 3 rolls
            for i in range(6):                                                      # For each die value, look for four of a kind, store the indices of the dice in the dice_indices array, and update theoretical scorecard
                dice_indices = [j for j in range(5) if self.__dice[j] == i + 1]     # Store the index of the dice used to score the given value
                if len(dice_indices) == 4:                                          # Only one four of a kind can exist, so once it is found update the theoretical scorecard and return from the function
                    self.__theoretical_scorecard[7][0] = 4 * (i + 1)
                    self.__theoretical_scorecard[7][1] = dice_indices
                    self.__theoretical_scorecard[7][2] = 3 - self.__rolls_left
                    return
            self.__theoretical_scorecard[7][2] = 3 - self.__rolls_left              # Set the rolls used even if we don't have a four of a kind to keep track of how many it actually takes


    # Calculate full house based on current roll (uses sorted dice)
    # Leveraging the fact that the dice are sorted, so we just check if first 2 are the same and the last 3 are the same or vice versa and that all 5 are not the same
    def __calculate_full_house(self):
        if self.scorecard[8][2] == 0:                                                                                       # Checks if scorecard entry has not been scored yet. Looks at # of rolls because it is possible to score a 0 on an entry after 3 rolls
            if ((self.__sorted_dice[0] == self.__sorted_dice[1] and self.__sorted_dice[2] == self.__sorted_dice[4]) or \
                (self.__sorted_dice[0] == self.__sorted_dice[2] and self.__sorted_dice[3] == self.__sorted_dice[4])) and \
                self.__sorted_dice[0] != self.__sorted_dice[4]:
                self.__theoretical_scorecard[8][0] = 25
                self.__theoretical_scorecard[8][1] = [j for i in range(6) for j in range(5) if self.__dice[j] == i + 1]     # Maps sorted dice back on to master dice lise in increasing value of dice, so if the full house is 2's and 3's, it will give indices of all 2's, then all 3's regardless of which one occurs 2 times or 3 times   
            self.__theoretical_scorecard[8][2] = 3 - self.__rolls_left                                                      # Set the rolls used even if we don't have a full house to keep track of how many it actually takes


    # Calculate small straight based on current roll (uses sorted dice and additionally removes duplicates)
    def __calculate_small_straight(self):
        if self.scorecard[9][2] == 0:
            temp_dice = copy.deepcopy(list(dict.fromkeys(self.__sorted_dice)))                                              # Remove duplicates from combined dice to remove edge cases from small straight test (i.e., [2, 3, 3, 4, 5]) then check that there are still at least 4 dice
            if len(temp_dice) == 5:                                                                                         # Case with no duplicates found
                for i in range(2):                                                                                          # Small straight in sorted list of 5 must start at postion 0 or position 1, so do two iterations to check for straight from those positions              
                    if temp_dice[i + 1] == temp_dice[i] + 1 and temp_dice[i + 2] == temp_dice[i + 1] + 1 and \
                    temp_dice[i + 3] == temp_dice[i + 2] + 1:
                        self.__theoretical_scorecard[9][0] = 30
                        self.__theoretical_scorecard[9][1] = [self.__dice.index(temp_dice[j]) for j in range(i, i + 4)]     # Map sorted dice back on to master dice list
                self.__theoretical_scorecard[9][2] = 3 - self.__rolls_left                                                  # Set the rolls used even if we don't have a small straight to keep track of how many it actually takes
            elif len(temp_dice) == 4:                                                                                       # Case with 1 duplicate found
                if temp_dice[1] == temp_dice[0] + 1 and temp_dice[2] == temp_dice[1] + 1 and \
                temp_dice[3] == temp_dice[2] + 1:                                                                           # Small straight in sorted list of 4 must start at position 0
                    self.__theoretical_scorecard[9][0] = 30
                    self.__theoretical_scorecard[9][1] = [self.__dice.index(temp_dice[j]) for j in range(4)]
                self.__theoretical_scorecard[9][2] = 3 - self.__rolls_left                                                  # Set the rolls used even if we don't have a small straight to keep track of how many it actually takes
            else:                                                                                                           # Case with >1 duplicate found, small straight is impossible
                self.__theoretical_scorecard[9][2] = 3 - self.__rolls_left


    # Calculate large straight based on current roll (uses sorted dice)
    def __calculate_large_straight(self):
        if self.scorecard[10][2] == 0:
            if self.__sorted_dice[1] == self.__sorted_dice[0] + 1 and self.__sorted_dice[2] == self.__sorted_dice[1] + 1 and \
                self.__sorted_dice[3] == self.__sorted_dice[2] + 1 and self.__sorted_dice[4] == self.__sorted_dice[3] + 1:
                self.__theoretical_scorecard[10][0] = 40
                self.__theoretical_scorecard[10][1] = [self.__dice.index(self.__sorted_dice[j]) for j in range(5)]          # Map sorted dice back on to master dice list
            self.__theoretical_scorecard[10][2] = 3 - self.__rolls_left                                                     # Set the rolls used even if we don't have a large straight to keep track of how many it actually takes


    # Calculate Yahtzee based on current roll/frozen dice combo (uses sorted dice)
    def __calculate_yahtzee(self):
        if self.scorecard[11][2] == 0:
            if self.__sorted_dice[0] == self.__sorted_dice[-1]:
                self.__theoretical_scorecard[11][0] = 50
                self.__theoretical_scorecard[11][1] = [0, 1, 2, 3, 4]               # All dice are the same so index doesn't particularly matter
            self.__theoretical_scorecard[11][2] = 3 - self.__rolls_left             # Set the rolls used even if we don't have a yahtzee to keep track of how many it actually takes


    # Calculate Chance value
    def __calculate_chance(self):
        if self.scorecard[12][2] == 0:
            self.__theoretical_scorecard[12][0] = sum(self.__dice)
            self.__theoretical_scorecard[12][1] = [0, 1, 2, 3, 4]
            self.__theoretical_scorecard[12][2] = 3 - self.__rolls_left


    # Calculate bonus 
    def __calculate_bonus(self):
        total = 0
        for i in range(6):
            total += self.scorecard[i][0]
        if total >= 63:
            self.score += 35

    # Calculates the Yahtzee bonus - if player has already scored a yahtzee and thrrows another, they get 100 points and can score that yahtzee in the upper half of the scorecard
    def __calculate_yahtzee_bonus(self):
        if self.scorecard[11][0] == 50 and self.__sorted_dice[0] == self.__sorted_dice[4]:
            self.score += 100
            print("Yahtzee bonus added")

    # Use all calculation methods to produce the theoretical scorecard for a given roll
    def __calculate_theoretical_scorecard(self):
        self.__calculate_top_half()
        self.__calculate_three_kind()
        self.__calculate_four_kind()
        self.__calculate_full_house()
        self.__calculate_small_straight()
        self.__calculate_large_straight()
        self.__calculate_yahtzee()
        self.__calculate_chance()

    # Calculates the final score when the game ends. If a player has received a yahtzee bonus of 100 points, this is already factored into the score at the time the second yahtzee was rolled
    def calculate_final_score(self):
        for entry in self.scorecard:
            self.score += entry[0]
        self.__calculate_bonus()

    #-------------------------------------------------------------------------------------------------#
    # Debugging methods
    #-------------------------------------------------------------------------------------------------#

    # Print out the player's scorecard line by line
    def print_scorecard(self):
        print("Scorecard:")
        for i in range(13):
            print(self.scorecard[i])
        print("\n")

    # Print out the player's theoretical scorecard line by line baesd on their last roll
    def print_theoretical_scorecard(self):
        print("Theoretical Scorecard:")
        for i in range(13):
            print(self.__theoretical_scorecard[i])
        print("\n")

    # Print current dice after last roll
    def print_dice(self):
        print("Current dice:", self.__dice)

    # Print current sorted dice after last roll
    def print_sorted_dice(self):
        print("Current sorted dice:", self.__sorted_dice)
    
    # Print number of rolls remaining
    def print_rolls_left(self):
        print("Rolls remaining in turn:", self.__rolls_left)

    # Print out final score
    def print_final_score(self):
        print("Final score:", self.score)

    # Print out player's entire information
    def print_player_info(self):
        print(self.player_name)
        self.print_rolls_left()
        self.print_dice()
        self.print_sorted_dice()
        self.print_scorecard()
        self.print_theoretical_scorecard()

