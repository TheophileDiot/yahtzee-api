# Game object class to manage the larger game structure (advancing turns, etc.). Currently supports 2 player games, may be generalized in the future.

from player import Player

class Game:
    def __init__(self, players):
        self.players = players
        self.remaining_turns = 13
        self.current_player = self.players[0].player_name
    
    # Global turns, so once all players have completed the current turn, move to the next
    def next_turn(self):
        self.remaining_turns -= 1
        self.current_player = self.players[0]

    # Print out current status of the game
    def print_status(self):
        print("Turns Remaining: ", self.remaining_turns)
        print("Current player:", self.current_player)
        print("\n")
        for player in self.players:
            print(player.player_name + "'s scorecard:")
            player.print_scorecard()
            print("\n")