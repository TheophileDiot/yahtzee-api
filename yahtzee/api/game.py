# Game object class to manage the larger game structure (advancing turns, etc.).

from .player import Player

class Game:
    def __init__(self, num_players):
        self.players = [Player("P" + str(i + 1)) for i in range(num_players)]
        self.remaining_turns = 13
        self.current_player = self.players[0].player_name
        self.num_players = num_players


    #-------------------------------------------------------------------------------------#
    # Basic functionality methods
    #-------------------------------------------------------------------------------------#

    # Reset game to start state
    def reset_game(self):
        self.players = [Player("P" + str(i + 1)) for i in range(self.num_players)]
        self.remaining_turns = 13
        self.current_player = self.players[0].player_name

    # Advance global turn
    def next_turn(self):
        self.remaining_turns -= 1
        self.current_player = self.players[0]


    #-------------------------------------------------------------------------------------#
    # Debugging methods
    #-------------------------------------------------------------------------------------#

    # Print out current status of the game
    def print_status(self):
        print("Turns Remaining: ", self.remaining_turns)
        print("Current player:", self.current_player)
        print("\n")
        for player in self.players:
            print(player.player_name + "'s scorecard:")
            player.print_scorecard()
            print("\n")
