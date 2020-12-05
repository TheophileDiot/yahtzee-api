# Init file as specified by documentation found here: https://github.com/openai/gym/blob/master/docs/creating-environments.md
# Additional versions should be added via their own call to the register method as shown in the docs.

from gym.envs.registration import register

register(
    id='yahtzee-v0',
    entry_point='yahtzee.envs:Yahtzee',
)