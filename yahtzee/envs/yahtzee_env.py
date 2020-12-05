# Main Yahtzee-V0 Environment class. To make new variations of the environment, start a new file + class in the /envs folder.

import gym
from gym import error, spaces, utils
from gym.utils import seeding

class Yahtzee(gym.Env):
	metadata = {'render.modes': ['human']}
		
