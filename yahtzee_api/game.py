"""Module containing the Game class."""

from .player import Player

class Game:
    """Represents the larger game structure for Yahtzee.

    Manages tracking and advancing global turns as well as initiating end-of-game scoring calculations. 
    Creating a game will create a list of instances of the Player object according to the specified number of players passed to the constructor.
    All algorithm development should happen through an instance of this class as it provides a rule-adhering structure and allows access to the Player object and its methods.
    
    Attributes:
        remaining_turns (int): Global turn tracker.
        current_player (Player): The player who is currently rolling dice/scoring.
        num_players (int): Number of players in the game. 
        winner (list): list populated at the end of the game with Player object(s) to store winner(s) (in case of a tie)
    """

    def __init__(self, num_players):
        """Class constructor.
        
        Args:
            num_players (int): Number of players in the game.
        """
        self.__players = [Player("P" + str(i)) for i in range(num_players)]
        self.remaining_turns = 13
        self.current_player = self.__players[0]
        self.num_players = num_players
        self.winner = []

    def next_player(self):
        """Advances to the next player and moves to the next global turn when the last player is detected.
        
        Once the 13th turn is completed, this method will automatically calculate the final scores and
        set the value of self.winner to the winner(s) Player object(s).
        """
        if self.__players.index(self.current_player) == self.num_players - 1:
            self.remaining_turns -= 1
            self.current_player = self.__players[0]
            if self.remaining_turns == 0:
                self.__end_game()
        else:
            self.current_player = self.__players[self.__players.index(self.current_player) + 1]

    def print_status(self, file, overwrite=True):
        """Prints out the current moment-in-time status of the game to a specified file. 
        
        This should be called before a player chooses their score to view maximum detail.
        Args: 
            file (str): Filename to write to.
            overwrite (bool, optional): Whether or not to overwrite existing file data. Defaults to True.
        """
        with open(file, 'w' if overwrite == True else 'a') as f:
            f.write("Current Turn: " + str(13 - self.remaining_turns + 1) + "\n")
            f.write("Turns Remaining: " + str(self.remaining_turns - 1) + "\n")
            f.write("Current Player: " + self.current_player.player_name + "\n")
            f.write("Rolls left this turn: " + str(self.current_player.rolls_left) + "\n")
            f.write("Scorecard:" + "\n")
            for i in range(13):
                f.write(str(self.current_player.scorecard[i]) + "\n")
            f.write("\n")
            f.write("Theoretical Scorecard:" + "\n")
            for i in range(13):
                f.write(str(self.current_player.theoretical_scorecard[i]) + "\n")
            f.write("\n")
            f.write("-----------------------------------------")
            f.write("\n")
        f.close()

    def print_final(self, file, overwrite=True):
        """Prints out the final results of the game to a specified file.
        
        Args: 
            file (str): Filename to write to.
            overwrite (bool, optional): Whether or not to overwrite existing file data. Defaults to True.
        """
        with open(file, 'w' if overwrite == True else 'a') as f:
            f.write("Winner(s): ")
            for player in self.winner:
                f.write(player.player_name + "\n")
                f.write("Scorecard:" + "\n")
                for i in range(13):
                    f.write(str(player.scorecard[i]) + "\n")
                f.write("\n")
            f.write("Score: " + str(self.winner[0].score) + "\n")
            f.write("-----------------------------------------")
            f.write("\n")
        f.close()

    def __end_game(self):
        """Computes final scores for each player and prints the results."""
        final_scores = []
        for player in self.__players:
            for entry in player.scorecard:
                player.score += entry[0]
            final_scores.append(player.score)
        self.winner = [player for player in self.__players if player.score == max(final_scores)]
