"""Module containing the Player class."""

import random
import copy

class Player:
    """Stores information about each player's current status including score, theoretical score, rolls remaining in their turn, and the status of their last roll.
    
    This class tracks the data associated with each player, and additionally performs all scoring calculations including all possible scores based on the current 
    configuration of the dice and their scorecard. The Player object will expose all of the relevant information needed for algorithmic decision making,
    including a theoretical scorecard that gives all the possible scores based on what the player has already scored and the current configuration of the dice. 
    
    Attributes:
        player_name (str): A string containing the name of the player.
        score (int): An integer value indicating the point total for the player (calculated at the end of the game).
        scorecard (list): A list of lists tracking each row of a Yahtzee scorecard, with each row (inner list) of the card following this structure: [score, [dice used to get score], number of rolls]. This is updated when a player ends their turn with the end_turn() method.
            
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

        theoretical_scorecard (list): A list of lists tracking each row of a Yahtzee scorecard, calculated after each roll, with each row of the card following this structure:
        [score, [0 if index is unused, 1 if index is used (for calculating this score)], number of rolls]. 
        This is calculated after every roll and can be used to make decisions about which dice to roll again, which score to take, and more. 
        This scorecard stores the indices of the dice, rather than the dice values themselves, 
        to make it more useful for choosing which dice to reroll based on what score entry the player wants to pursue.
            
            Theoretical Scorecard indices are as follows:
            
            [0]: 1's

            [1]: 2's

            [2]: 3's

            [3]: 4's

            [4]: 5's

            [5]: 6's

            [6]: Three of a Kind

            [7]: Four of a Kind

            [8]: Full House     (will always be the indices of the pair followed by the triple)

            [9]: Small Straight

            [10]: Large Straight

            [11]: Yahtzee

            [12]: Chance

        dice (list): A list of the 5 dice in play - index is preserved throughout calculations.
        rolls_left (int): Integer tracking how many rolls the player has left on the current turn (there are 3 rolls per turn).
        jokers (int): Tracks how many times a Yahtzee was used as a Joker score.
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
        self.dice = [0, 0, 0, 0, 0]     # Master list of dice - index matters, and these dice are preserved positionally in all scoring and rolling calculations
        self.rolls_left = 3  
        self.jokers = 0                 # Tracks how many times a Yahtzee has been used to score a full house or straight as a Joker (sanity check)
        self.__sorted_dice = []         # Sorted version of master dice list to make some scoring calculations easier. Index does not matter in this list - calculations are performed with sorted list then mapped back to the indices of master list
        self.__bonus = False
              
    def roll_dice(self, dice_to_roll):
        """Rolls dice specified by the dice_to_roll list, updates related class attributes, and calculates the theoretical scorecard values.

        Args:
            dice_to_roll (list): A list of length 5 containing binary values where 0 indicates the die in that position should be rolled.
        
        Raises:
            ValueError: If the number of rolls remaining is less than or equal to 0.
            TypeError: If dice_to_roll is not a list.
            ValueError: If the length of dice_to_roll is not 5.
            TypeError: If the dice_to_roll list does not contain only binary values.
            ValueError: If the player attempts to roll fewer than 5 dice on the first roll of their turn.
        """
        if self.rolls_left <= 0:
            raise ValueError("ValueError in Player.roll_dice(): No rolls remaining.")
        if not isinstance(dice_to_roll, list):
            raise TypeError("TypeError in Player.roll_dice(): dice_to_roll must be of type list.")
        if len(dice_to_roll) != 5:
            raise ValueError("ValueError in Player.roll_dice(): dice_to_roll argument must be a list of length 5.")
        if len([x for x in dice_to_roll if x not in [0, 1]]) != 0:
            raise TypeError("TypeError in Player.roll_dice(): dice_to_roll argument must contain only binary values.")
        if self.rolls_left == 3 and len([x for x in dice_to_roll if x != 0]) > 0:
            raise ValueError("ValueError in Player.roll_dice(): All 5 dice must be rolled on the first roll of the turn.")
        for i in range(5):
            if dice_to_roll[i] == 0:
                self.dice[i] = random.randint(1, 6)
        self.rolls_left -= 1
        self.__sorted_dice = copy.deepcopy(self.dice)     
        self.__sorted_dice.sort()                           
        self.__calculate_yahtzee_bonus()                    
        self.__reset_theoretical_scorecard()                  
        self.__calculate_theoretical_scorecard()

    def end_turn(self, score_type):
        """Resets turn-based parameters and fills in scorecard based on player choice.
        
        Args:
            score_type (int): Index of the scorecard entry that the player has chosen to score for this round. 
        Raises:
            ValueError: If score_type is not between 0 and 12.
        """
        if score_type < 0 or score_type > 12:
            raise ValueError("ValueError in Player.end_turn(): score_type must be between 0 and 12, inclusive.")

        # Check if Joker rules apply to this score
        if score_type == 8 or score_type == 9 or score_type == 10 and self.__sorted_dice[0] == self.__sorted_dice[-1]:
            self.jokers += 1    
        self.scorecard[score_type][0] = self.theoretical_scorecard[score_type][0]
        self.scorecard[score_type][1] = copy.deepcopy(self.dice)
        self.scorecard[score_type][2] = 3 - self.rolls_left
        self.__calculate_bonus()
        self.rolls_left = 3 
        self.dice = copy.deepcopy([0, 0, 0, 0, 0])
        self.__reset_theoretical_scorecard()

    def __reset_theoretical_scorecard(self):
        """Resets the theoretical scorecard. Called after each roll of the dice."""
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

    def __calculate_top_half(self):
        """Calculates values for 1's --> 6's based on the current roll and store result in the theoretical scorecard."""
        for i in range(6):                                                          
            if self.scorecard[i][2] == 0:                                               # Checks if scorecard entry has not been scored yet. Looks at # of rolls because it is possible to score a 0 on an entry after 3 rolls.
                dice_indices = [1 if self.dice[j] == i + 1 else 0 for j in range(5)]    # Builds list tracking which indices are used in calculation
                self.theoretical_scorecard[i][0] = dice_indices.count(1) * (i + 1)    
                self.theoretical_scorecard[i][1] = dice_indices                   
                self.theoretical_scorecard[i][2] = 3 - self.rolls_left                

    def __calculate_three_kind(self):
        """Calculates three of a kind value based on the current roll and store result in the theoretical scorecard."""
        if self.scorecard[6][2] == 0:                                                   # Checks if scorecard entry has not been scored yet. Looks at # of rolls because it is possible to score a 0 on an entry after 3 rolls.
            for i in range(6):                                                          # For each die value, look for three of a kind, store the indices of the dice in the dice_indices array, and update theoretical scorecard.
                dice_indices = [1 if self.dice[j] == i + 1 else 0 for j in range(5)]    # Builds list tracking which indices are used in calculation
                if dice_indices.count(1) == 3:                                          # Only one three of a kind can exist, so once it is found update the theoretical scorecard and return from the function.
                    self.theoretical_scorecard[6][0] = 3 * (i + 1)
                    self.theoretical_scorecard[6][1] = dice_indices
                    self.theoretical_scorecard[6][2] = 3 - self.rolls_left
                    return
            self.theoretical_scorecard[6][2] = 3 - self.rolls_left                      # Set the rolls used even if we don't have a three of a kind to keep track of how many it actually takes.

    def __calculate_four_kind(self):
        """Calculates four of a kind value based on the current roll and store result in the theoretical scorecard."""
        if self.scorecard[7][2] == 0:                                                   # Checks if scorecard entry has not been scored yet. Looks at # of rolls because it is possible to score a 0 on an entry after 3 rolls.
            for i in range(6):                                                          # For each die value, look for four of a kind, store the indices of the dice in the dice_indices array, and update theoretical scorecard.
                dice_indices = [1 if self.dice[j] == i + 1 else 0 for j in range(5)]    # Builds list tracking which indices are used in calculation
                if dice_indices.count(1) == 4:                                          # Only one four of a kind can exist, so once it is found update the theoretical scorecard and return from the function.
                    self.theoretical_scorecard[7][0] = 4 * (i + 1)
                    self.theoretical_scorecard[7][1] = dice_indices
                    self.theoretical_scorecard[7][2] = 3 - self.rolls_left
                    return
            self.theoretical_scorecard[7][2] = 3 - self.rolls_left                 # Set the rolls used even if we don't have a four of a kind to keep track of how many it actually takes.

    def __calculate_full_house(self):
        """Calculates full house based on current roll (uses sorted dice) and store result in the theoretical scorecard.
        
        Leverages the fact that the dice are sorted, so just check if first 2 are the same and the last 3 are the same or vice versa, and that all 5 are not the same.
        """
        if self.scorecard[8][2] == 0:                                        # Checks if scorecard entry has not been scored yet. Looks at # of rolls because it is possible to score a 0 on an entry after 3 rolls.
            if self.__sorted_dice[0] == self.__sorted_dice[1] and self.__sorted_dice[2] == self.__sorted_dice[4]  and \
               self.__sorted_dice[0] != self.__sorted_dice[4]:
                self.theoretical_scorecard[8][0] = 25 
                self.theoretical_scorecard[8][1] = [1, 1, 1, 1, 1] 
            if self.__sorted_dice[0] == self.__sorted_dice[2] and self.__sorted_dice[3] == self.__sorted_dice[4]  and \
               self.__sorted_dice[0] != self.__sorted_dice[4]:
                self.theoretical_scorecard[8][0] = 25 
                self.theoretical_scorecard[8][1] = [1, 1, 1, 1, 1]
            self.theoretical_scorecard[8][2] = 3 - self.rolls_left           # Set the rolls used even if we don't have a full house to keep track of how many it actually takes.

    def __calculate_small_straight(self):
        """Calculates small straight based on current roll (uses sorted dice and additionally removes duplicates) and store result in the theoretical scorecard."""
        if self.scorecard[9][2] == 0:
            found = False
            temp_dice = copy.deepcopy(list(dict.fromkeys(self.__sorted_dice)))          # Remove duplicates from combined dice to remove edge cases from small straight test (i.e., [2, 3, 3, 4, 5]) then check that there are still at least 4 dice.
            dice_indices = [0, 0, 0, 0, 0]                                                                                      
            if len(temp_dice) == 5:                                                                                         
                for i in range(2):                                                      # Small straight in sorted list of 5 must start at postion 0 or position 1, so do two iterations to check for straight from those positions.             
                    if temp_dice[i + 1] == temp_dice[i] + 1 and temp_dice[i + 2] == temp_dice[i + 1] + 1 and \
                    temp_dice[i + 3] == temp_dice[i + 2] + 1:
                        found = True                         
                        temp_dice = temp_dice[1:5] if i == 1 else temp_dice[0:4]  
                        break
            elif len(temp_dice) == 4:                                                                                       
                if temp_dice[1] == temp_dice[0] + 1 and temp_dice[2] == temp_dice[1] + 1 and \
                temp_dice[3] == temp_dice[2] + 1:                                       # Small straight in sorted list of 4 must start at position 0.
                    found = True  
            if found:
                for elt in temp_dice:
                    if elt in self.dice:
                        dice_indices[self.dice.index(elt)] = 1
                self.theoretical_scorecard[9][0] = 30
                self.theoretical_scorecard[9][1] = dice_indices                                                                                                                                                    
            self.theoretical_scorecard[9][2] = 3 - self.rolls_left

    def __calculate_large_straight(self):
        """Calculates large straight based on current roll (uses sorted dice) and store result in theoretical scorecard."""
        if self.scorecard[10][2] == 0:
            if self.__sorted_dice[1] == self.__sorted_dice[0] + 1 and self.__sorted_dice[2] == self.__sorted_dice[1] + 1 and \
                self.__sorted_dice[3] == self.__sorted_dice[2] + 1 and self.__sorted_dice[4] == self.__sorted_dice[3] + 1:
                self.theoretical_scorecard[10][0] = 40
                self.theoretical_scorecard[10][1] = [1, 1, 1, 1, 1]
            self.theoretical_scorecard[10][2] = 3 - self.rolls_left                                                    # Set the rolls used even if we don't have a large straight to keep track of how many it actually takes.

    def __calculate_yahtzee(self):
        """Calculates Yahtzee based on current roll/frozen dice combo (uses sorted dice) and store result in theoretical scorecard."""
        if self.scorecard[11][2] == 0:
            if self.__sorted_dice[0] == self.__sorted_dice[-1]:
                self.theoretical_scorecard[11][0] = 50
                self.theoretical_scorecard[11][1] = [1, 1, 1, 1, 1]              
            self.theoretical_scorecard[11][2] = 3 - self.rolls_left        # Set the rolls used even if we don't have a yahtzee to keep track of how many it actually takes.
        elif self.scorecard[self.dice[0] - 1][2] != 0:                     # If the number making the Yahtzee has been scored in the upper half, Joker rules apply
            if self.scorecard[6][2] == 0:
                self.theoretical_scorecard[6][0] = sum(self.dice)
                self.theoretical_scorecard[6][1] = [1, 1, 1, 1, 1]
                self.theoretical_scorecard[6][2] = 3 -self.rolls_left
            if self.scorecard[7][2] == 0:
                self.theoretical_scorecard[7][0] = sum(self.dice)
                self.theoretical_scorecard[7][1] = [1, 1, 1, 1, 1]
                self.theoretical_scorecard[7][2] = 3 -self.rolls_left
            if self.scorecard[8][2] == 0:
                self.theoretical_scorecard[8][0] = 25
                self.theoretical_scorecard[8][1] = [1, 1, 1, 1, 1]
                self.theoretical_scorecard[8][2] = 3 -self.rolls_left
            if self.scorecard[9][2] == 0:
                self.theoretical_scorecard[9][0] = 30
                self.theoretical_scorecard[9][1] = [1, 1, 1, 1, 1]
                self.theoretical_scorecard[9][2] = 3 -self.rolls_left
            if self.scorecard[10][2] == 0:
                self.theoretical_scorecard[10][0] = 40
                self.theoretical_scorecard[10][1] = [1, 1, 1, 1, 1]
                self.theoretical_scorecard[10][2] = 3 -self.rolls_left

    def __calculate_chance(self):
        """Calculates chance value and store result in theoretical scorecard."""
        if self.scorecard[12][2] == 0:
            self.theoretical_scorecard[12][0] = sum(self.dice)
            self.theoretical_scorecard[12][1] = [1, 1, 1, 1, 1]
            self.theoretical_scorecard[12][2] = 3 - self.rolls_left

    def __calculate_bonus(self):
        """Determines if Player has earned the top-half bonus by scoring at least 63 points on the first 6 scorecard entries."""
        total = 0
        for i in range(6):
            total += self.scorecard[i][0]
        if total >= 63 and not self.__bonus:
            self.score += 35
            self.bonus = True

    def __calculate_yahtzee_bonus(self):
        """Adds Yahtzee bonus to Player's total score when earned.
        
        Yahtzee bonus is earned by rolling more than one Yahtzee in a single game and is worth 100 points.
        """
        if self.scorecard[11][0] == 50 and self.__sorted_dice[0] == self.__sorted_dice[4]:
            self.score += 100

    def __calculate_theoretical_scorecard(self):
        """Wrapper function to fill in the entire theoretical scorecard after each roll."""
        self.__calculate_top_half()
        self.__calculate_three_kind()
        self.__calculate_four_kind()
        self.__calculate_full_house()
        self.__calculate_small_straight()
        self.__calculate_large_straight()
        self.__calculate_yahtzee()
        self.__calculate_chance()
