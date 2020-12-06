# Main Yahtzee-V0 Environment class. To make new variations of the environment, start a new file + class in the /envs folder.

import gym
from gym import error, spaces, utils
from gym.utils import seeding
from yahtzee.utils.game import Game


class Yahtzee(gym.Env):
	metadata = {'render.modes': ['human']}
	
	# Initialize environment by creating a new game
	def __init__(self):
		self.game = Game()

	# Reset environment after iteration is complete
	def reset(self):
		self.game.reset_game()

