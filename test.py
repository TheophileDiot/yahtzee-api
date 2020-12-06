from yahtzee.api.game import Game
from yahtzee.api.player import Player

p1 = Player("Tom")
p2 = Player("John")
game = Game()

p1.combined_dice = [2,2,2,2,2]
print(p1.combined_dice)
p1.rolls_left -= 1
p1.calculate_theoretical_scorecard()
p1.print_theoretical_scorecard()

