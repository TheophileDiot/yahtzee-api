"""Module containing the Player class.

Author: Tom Arbeiter
"""

import random
import copy

class Player:
    """Stores information about each player's current status including score, theoretical score, rolls remaining in their turn, and the status of their last roll.
    
    This class tracks the data associated with each player, and additionally performs all scoring calculations including all possible scores based on the current 
    configuration of the dice and their scorecard. 
    
    Attributes:
        player_name (str): A string containing the name of the player.
        score (int): An integer value indicating the point total for the player (calculated at the end of the game).
        scorecard (list): A list tracking each row of a Yahtzee scorecard according to the following structure: [score, [dice used to get score], number of rolls].
        theoretical_scorecard (list): A list tracking each row of a Yahtzee scorecard, calculated after each roll, according to the following structure: [score, [indices in self.dice of dice used to get score], number of rolls].
        dice (list): A list of the 5 dice in play - index is preserved throughout calculations.
    """
    def __init__(self, player_name):
        """Constructor method for Player class.
        
        Args:
            player_name: A string specifying the name for the instance of the Player class.
        """
        self.player_name = player_name
        self.score = 0          
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
        self.theoretical_scorecard = [   
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
        self.dice = [0, 0, 0, 0, 0]         # Master list of dice - index matters, and these dice are preserved positionally in all scoring and rolling calculations
        self._sorted_dice = []               # Sorted version of master dice list to make some scoring calculations easier. Index does not matter in this list - calculations are performed with sorted list then mapped back to the indices of master list
        self.rolls_left = 3                
         
    def roll_dice(self, dice_to_roll):
        """Rolls dice specified by the dice_to_roll list, updates related class attributes, and calculates the theoretical scorecard values.

        Args:
            dice_to_roll (list): A list of length 5 containing boolean values where "True" indicates the die in that position should be rolled.
        
        Raises:
            ValueError: If the number of rolls remaining less than or equal to 0.
            ValueError: If the length of dice_to_roll is not 5.
            TypeError: If dice_to_roll is not a list.
        """
        if self.rolls_left <= 0:
            raise ValueError("ValueError in Player.roll_dice(): No rolls remaining.")
        if len(dice_to_roll) != 5:
            raise ValueError("ValueError in Player.roll_dice(): dice_to_roll argument must be a list of length 5.")
        if not isinstance(dice_to_roll, list):
            raise TypeError("TypeError in Player.roll_dice(): dice_to_roll must be of type list.")
        for i in range(5):
            if dice_to_roll[i] == True:
                self.dice[i] = random.randint(1, 6)
        self.rolls_left -= 1
        self._sorted_dice = copy.deepcopy(self.dice)     
        self._sorted_dice.sort()                           
        self._calculate_yahtzee_bonus()                    
        self._reset_theoretical_scorecard()                  
        self._calculate_theoretical_scorecard()

    def end_turn(self, score_type):
        """Resets turn-based parameters and fills in scorecard based on player choice.
        
        Args:
            score_type (int): Index of the scorecard entry that the player has chosen to score for this round. 
        """
        self.scorecard[score_type][0] = self._theoretical_scorecard[score_type][0]
        self.scorecard[score_type][1] = self.dice
        self.scorecard[score_type][2] = 3 - self.rolls_left
        self.rolls_left = 3 
        self._reset_theoretical_scorecard()
    
    def calculate_final_score(self):
        """Sums the total points a player has scored and stores it in the Player.score attribute.
        
        This function can only be called at the end of the game when all 13 scorecard values have been scored. 
        
        Raises:
            ValueError: If scorecard is not complete (implying the game is not over).
        """
        for entry in self.scorecard:
            if entry[2] == 0:
                raise ValueError("Error in Player.calculate_final_score(): Player has unscored entries on scorecard.")
            self.score += entry[0]
        self._calculate_bonus()

    def print_scorecard(self):
        """Prints out the player's scorecard line by line.
        
        Scorecard indices are as follows:
           [0]: 1's
           [1]: 2's
           [2]: 3's
           [3]: 4's
           [4]: 5's
           [5]: 6's
           [6]: Three of a Kind
           [7]: Four of a Kind
           [8]: Full House
           [9]: Small Straight
           [10]: Large Straight
           [11]: Yahtzee
           [12]: Chance

        The list in position [1] of each sublist contains the values of the 5 dice rolled to achieve the associated score.

        The integer in position [2] of each sublist represents the number of rolls used to obtain that score.
         """
        print("Scorecard:")
        for i in range(13):
            print(self.scorecard[i])
        print("\n")

    def print_theoretical_scorecard(self):
        """Prints out the player's theoretical scorecard line by line baesd on their last roll.
        
        Theoretical Scorecard indices are as follows:
           [0]: 1's
           [1]: 2's
           [2]: 3's
           [3]: 4's
           [4]: 5's
           [5]: 6's
           [6]: Three of a Kind
           [7]: Four of a Kind
           [8]: Full House
           [9]: Small Straight
           [10]: Large Straight
           [11]: Yahtzee
           [12]: Chance

        The list in position [1] of each sublist contains the values of the indices of the dice used to calculate the associated score.

        The integer in position [2] of each sublist represents the number of rolls used to obtain that score.
        """
        print("Theoretical Scorecard:")
        for i in range(13):
            print(self._theoretical_scorecard[i])
        print("\n")

    def print_player_info(self):
        """Prints out player's entire information"""
        print(self.player_name)
        print(self.dice)
        print(self.rolls_left)
        self.print_scorecard()
        self.print_theoretical_scorecard()

    def _reset_theoretical_scorecard(self):
        """Resets the theoretical scorecard. Called after each roll of the dice."""
        self._theoretical_scorecard = [
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

    def _calculate_top_half(self):
        """Calculate values for 1's --> 6's based on the current roll and store result in the theoretical scorecard."""
        for i in range(6):                                                          
            if self.scorecard[i][2] == 0:                                           # Checks if scorecard entry has not been scored yet. Looks at # of rolls because it is possible to score a 0 on an entry after 3 rolls.
                dice_indices = [j for j in range(5) if self.dice[j] == i + 1]     # Store the index of the dice used to score the given value.
                self._theoretical_scorecard[i][0] = len(dice_indices) * (i + 1)    
                self._theoretical_scorecard[i][1] = dice_indices                   
                self._theoretical_scorecard[i][2] = 3 - self.rolls_left                

    def _calculate_three_kind(self):
        """Calculate three of a kind value based on the current roll and store result in the theoretical scorecard."""
        if self.scorecard[6][2] == 0:                                               # Checks if scorecard entry has not been scored yet. Looks at # of rolls because it is possible to score a 0 on an entry after 3 rolls.
            for i in range(6):                                                      # For each die value, look for three of a kind, store the indices of the dice in the dice_indices array, and update theoretical scorecard.
                dice_indices = [j for j in range(5) if self.dice[j] == i + 1]     # Store the index of the dice used to score the given value.
                if len(dice_indices) == 3:                                          # Only one three of a kind can exist, so once it is found update the theoretical scorecard and return from the function.
                    self._theoretical_scorecard[6][0] = 3 * (i + 1)
                    self._theoretical_scorecard[6][1] = dice_indices
                    self._theoretical_scorecard[6][2] = 3 - self.rolls_left
                    return
            self._theoretical_scorecard[6][2] = 3 - self.rolls_left              # Set the rolls used even if we don't have a three of a kind to keep track of how many it actually takes.

    def _calculate_four_kind(self):
        """Calculate four of a kind value based on the current roll and store result in the theoretical scorecard."""
        if self.scorecard[7][2] == 0:                                               # Checks if scorecard entry has not been scored yet. Looks at # of rolls because it is possible to score a 0 on an entry after 3 rolls.
            for i in range(6):                                                      # For each die value, look for four of a kind, store the indices of the dice in the dice_indices array, and update theoretical scorecard.
                dice_indices = [j for j in range(5) if self.dice[j] == i + 1]     # Store the index of the dice used to score the given value.
                if len(dice_indices) == 4:                                          # Only one four of a kind can exist, so once it is found update the theoretical scorecard and return from the function.
                    self._theoretical_scorecard[7][0] = 4 * (i + 1)
                    self._theoretical_scorecard[7][1] = dice_indices
                    self._theoretical_scorecard[7][2] = 3 - self.rolls_left
                    return
            self._theoretical_scorecard[7][2] = 3 - self.rolls_left              # Set the rolls used even if we don't have a four of a kind to keep track of how many it actually takes.

    def _calculate_full_house(self):
        """Calculate full house based on current roll (uses sorted dice) and store result in the theoretical scorecard.
        
        Leverages the fact that the dice are sorted, so just check if first 2 are the same and the last 3 are the same or vice versa, and that all 5 are not the same.
        """
        if self.scorecard[8][2] == 0:                                                                                    # Checks if scorecard entry has not been scored yet. Looks at # of rolls because it is possible to score a 0 on an entry after 3 rolls.
            if ((self._sorted_dice[0] == self._sorted_dice[1] and self._sorted_dice[2] == self._sorted_dice[4]) or \
                (self._sorted_dice[0] == self._sorted_dice[2] and self._sorted_dice[3] == self._sorted_dice[4])) and \
                self._sorted_dice[0] != self._sorted_dice[4]:
                self._theoretical_scorecard[8][0] = 25
                self._theoretical_scorecard[8][1] = [j for i in range(6) for j in range(5) if self.dice[j] == i + 1]     # Maps sorted dice back on to master dice lise in increasing value of dice, so if the full house is 2's and 3's, it will give indices of all 2's, then all 3's regardless of which one occurs 2 times or 3 times. 
            self._theoretical_scorecard[8][2] = 3 - self.rolls_left                                                      # Set the rolls used even if we don't have a full house to keep track of how many it actually takes.

    def _calculate_small_straight(self):
        """Calculate small straight based on current roll (uses sorted dice and additionally removes duplicates) and store result in the theoretical scorecard."""
        if self.scorecard[9][2] == 0:
            temp_dice = copy.deepcopy(list(dict.fromkeys(self._sorted_dice)))                                            # Remove duplicates from combined dice to remove edge cases from small straight test (i.e., [2, 3, 3, 4, 5]) then check that there are still at least 4 dice.
            if len(temp_dice) == 5:                                                                                         
                for i in range(2):                                                                                       # Small straight in sorted list of 5 must start at postion 0 or position 1, so do two iterations to check for straight from those positions.             
                    if temp_dice[i + 1] == temp_dice[i] + 1 and temp_dice[i + 2] == temp_dice[i + 1] + 1 and \
                    temp_dice[i + 3] == temp_dice[i + 2] + 1:
                        self._theoretical_scorecard[9][0] = 30
                        self._theoretical_scorecard[9][1] = [self.dice.index(temp_dice[j]) for j in range(i, i + 4)]     # Map sorted dice back on to master dice list.
                self._theoretical_scorecard[9][2] = 3 - self.rolls_left                                                  # Set the rolls used even if we don't have a small straight to keep track of how many it actually takes.
            elif len(temp_dice) == 4:                                                                                       
                if temp_dice[1] == temp_dice[0] + 1 and temp_dice[2] == temp_dice[1] + 1 and \
                temp_dice[3] == temp_dice[2] + 1:                                                                        # Small straight in sorted list of 4 must start at position 0.
                    self._theoretical_scorecard[9][0] = 30
                    self._theoretical_scorecard[9][1] = [self.dice.index(temp_dice[j]) for j in range(4)]
                self._theoretical_scorecard[9][2] = 3 - self.rolls_left                                                  # Set the rolls used even if we don't have a small straight to keep track of how many it actually takes.
            else:                                                                                                        # Case with >1 duplicate found, small straight is impossible.
                self._theoretical_scorecard[9][2] = 3 - self.rolls_left

    def _calculate_large_straight(self):
        """Calculate large straight based on current roll (uses sorted dice) and store result in theoretical scorecard."""
        if self.scorecard[10][2] == 0:
            if self._sorted_dice[1] == self._sorted_dice[0] + 1 and self._sorted_dice[2] == self._sorted_dice[1] + 1 and \
                self._sorted_dice[3] == self._sorted_dice[2] + 1 and self._sorted_dice[4] == self._sorted_dice[3] + 1:
                self._theoretical_scorecard[10][0] = 40
                self._theoretical_scorecard[10][1] = [self.dice.index(self._sorted_dice[j]) for j in range(5)]          # Map sorted dice back on to master dice list.
            self._theoretical_scorecard[10][2] = 3 - self.rolls_left                                                    # Set the rolls used even if we don't have a large straight to keep track of how many it actually takes.

    def _calculate_yahtzee(self):
        """Calculate Yahtzee based on current roll/frozen dice combo (uses sorted dice) and store result in theoretical scorecard."""
        if self.scorecard[11][2] == 0:
            if self._sorted_dice[0] == self._sorted_dice[-1]:
                self._theoretical_scorecard[11][0] = 50
                self._theoretical_scorecard[11][1] = [0, 1, 2, 3, 4]              
            self._theoretical_scorecard[11][2] = 3 - self.rolls_left             # Set the rolls used even if we don't have a yahtzee to keep track of how many it actually takes.

    def _calculate_chance(self):
        """Calculate chance value and store result in theoretical scorecard."""
        if self.scorecard[12][2] == 0:
            self._theoretical_scorecard[12][0] = sum(self.dice)
            self._theoretical_scorecard[12][1] = [0, 1, 2, 3, 4]
            self._theoretical_scorecard[12][2] = 3 - self.rolls_left

    def _calculate_bonus(self):
        """Determine if Player has earned the top-half bonus by scoring at least 63 points on the first 6 scorecard entries.
        
        Function is called at the end of the game when the final score is being tallied.
        """
        total = 0
        for i in range(6):
            total += self.scorecard[i][0]
        if total >= 63:
            self.score += 35

    def _calculate_yahtzee_bonus(self):
        """Add Yahtzee bonus to Player's total score.
        
        Yahtzee bonus is earned by rolling more than one Yahtzee in a single game and is worth 100 points.
        """
        if self.scorecard[11][0] == 50 and self._sorted_dice[0] == self._sorted_dice[4]:
            self.score += 100
            print("Yahtzee bonus added")

    def _calculate_theoretical_scorecard(self):
        """Wrapper function to fill in the entire theoretical scorecard after each roll."""
        self._calculate_top_half()
        self._calculate_three_kind()
        self._calculate_four_kind()
        self._calculate_full_house()
        self._calculate_small_straight()
        self._calculate_large_straight()
        self._calculate_yahtzee()
        self._calculate_chance()
