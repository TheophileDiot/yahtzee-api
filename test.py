from yahtzee.utils.game import Game
from yahtzee.utils.player import Player

p1 = Player("Tom")
p2 = Player("John")
game = Game()

p1.roll_dice()
print(p1.rolled_dice)
p1.print_theoretical_scorecard()

