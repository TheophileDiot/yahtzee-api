"""Module containing the Game class."""

from .player import Player

class Game:
    """Represents the larger game structure for Yahtzee.

    Manages tracking and advancing global turns as well as initiating end-of-game scoring calculations. 
    Creating a game will create instances of the Player object according to the specified number of players passed to the constructor.
    
    Attributes:
        players (list): A list of Player object instances, one for each participant. The player_name attribute is set to "P{index_in_players_list}" which can be used to distinguish players.
        remaining_turns (int): Global turn tracker.
        current_player (Player): The player who is currently rolling dice/scoring.
        num_players (int): Number of players in the game. 
        winner (Player): Player who wins the game.
        tie (boolean): True if game ends in a tie - in this case, winner attribute will remain none.
    """

    def __init__(self, num_players):
        """Class constructor.
        
        Args:
            num_players (int): Number of palyers in the game.
        """
        self.players = [Player("P" + str(i)) for i in range(num_players)]
        self.remaining_turns = 13
        self.current_player = self.players[0]
        self.num_players = num_players
        self.winner = None
        self.tie = False

    def next_player(self):
        """Advances to the next player and moves to the next global turn when the last player is detected.
        
        Once the 13th turn is completed, this method will automatically calculate the final scores and set the value of the winner attribute.
        """
        if self.players.index(self.current_player) == self.num_players - 1:
            self.remaining_turns -= 1
            self.current_player = self.players[0]
            if self.remaining_turns == 0:
                self._end_game()
        else:
            self.current_player = self.players[self.players.index(self.current_player) + 1]

    def print_status(self):
        """Prints out the current moment-in-time status of the game."""
        print("Turns Remaining: ", self.remaining_turns)
        print("Current player:", self.current_player.player_name)
        print("\n")
        for player in self.players:
            print(player.player_name + "'s scorecard:")
            player.print_scorecard()

    def _end_game(self):
        """Computes final scores for each player and prints the results."""
        final_scores = []
        for player in self.players:
            player.calculate_final_score()
            player.print_scorecard()
            player.print_final_score()
            final_scores.append(player.score)

        winner = [player for player in self.players if player.score == max(final_scores)]
        if len(winner) == 1: 
            self.winner = winner[0]
            print("Winner:", self.winner.player_name)
        elif len(winner) > 1:
            self.winner = None
            self.tie = True
            print("The game ended in a tie.")
        else:
            raise ValueError("Error in Game._end_game(): No winner determined.")

        print("----- End of Game -----")