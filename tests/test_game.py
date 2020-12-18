"""Unit tests for each public method of the Game class."""

import pytest
from yahtzee_api.game import Game

class TestGame:
    """Class containing all unit tests for the Game class."""

    def test_next_player_normal(self):
        """Tests functionality for switching when player is not the last player on the list."""
        g = Game(3)
        g.next_player()
        assert g.remaining_turns == 13
        assert g.current_player.player_name == "P1"

    def test_next_player_last_player(self):
        """Tests functionality for switching from last player back to first player."""
        g = Game(2)
        g.next_player()
        g.next_player()
        assert g.remaining_turns == 12
        assert g.current_player.player_name == "P0"

    def test_next_player_end_game(self):
        """Tests that next_player() function triggers end of game flow when the number of remaining turns hits 0."""
        g = Game(1)
        g.remaining_turns = 1
        g.current_player.scorecard = [      
            [0, [], 1],
            [0, [], 1],
            [0, [], 1],
            [0, [], 1],
            [0, [], 1],
            [0, [], 1],
            [0, [], 1],
            [0, [], 1],
            [0, [], 1],
            [0, [], 1],
            [0, [], 1],
            [0, [], 1],
            [0, [], 1],
        ]
        g.next_player()
        assert len(g.winner) > 0
        