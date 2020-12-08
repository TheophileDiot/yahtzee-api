"""Module containing the Game class.

Author: Tom Arbeiter
"""

from .player import Player

class Game:
    """Represents the larger game structure for Yahtzee.

    Manages tracking and advancing global turns as well as initiating end-of-game scoring calculations.
    
    Attributes:
        players (list): A list of Player object instances, one for each participant.
        remaining_turns (int): Global turn tracker.
        current_player (Player): The player who is currently rolling dice/scoring.
        num_players (int): Number of players in the game. 
    """

    def __init__(self, num_players):
        """Class constructor.
        
        Args:
            num_players (int): Number of palyers in the game.
        """
        self.players = [Player("P" + str(i + 1)) for i in range(num_players)]
        self.remaining_turns = 13
        self.current_player = self.players[0]
        self.num_players = num_players

    def next_turn(self):
        """Advances global turn by one and designates the first player as the current player."""
        self.remaining_turns -= 1
        self.current_player = self.players[0]

    def end_game(self):
        """Computes final scores for each player and prints the results."""
        for player in self.players:
            player.calculate_final_score()
            player.print_scorecard()
            player.print_final_score()
            print("----- End of Game -----")

    def print_status(self):
        """Prints out the current moment-in-time status of the game."""
        print("Turns Remaining: ", self.remaining_turns)
        print("Current player:", self.current_player.player_name)
        print("\n")
        for player in self.players:
            print(player.player_name + "'s scorecard:")
            player.print_scorecard()
