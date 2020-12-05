from player import Player
from game import Game

p1 = Player("Tom")
p2 = Player("John")
game = Game([p1, p2])

game.print_status()