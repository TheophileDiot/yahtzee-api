# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unrealeased
### Adding
- Ability to specify which Yahtzee rule variant the instantiated Game object should adhere to.

### Changing
- Make Game.players attribute private.
- Check if the top-half 35-point bonus is won after each turn, instead of at the end of the game.
- Shorten some public method names to improve readability and usability. 

## [0.2.0] - 2020-12-11
### Added
- Player.set_dice_to_reroll to the Player class to translate indices on the theoretical scorecard into a list of boolean values of dice to roll.
- This changelog!
- Improved quality of documentation and added example use code.
- Game.print_final() method to print final results of the game. 

### Changed 
- Moved all debug printing to two methods in the Game class and shifted to file printing instead of terminal printing (this is a breaking change, but I'm not doing a major version update because Semantic Versioning specifies that breaking changes during v0.x.x are expected and do not necessitate major updates).
- Game.next_player() no longer returns a list - this has been replaced by a Game object attribute "winner". 

### Removed
- Removed Player.print_player_info(), Player.print_scorecard(), and Player.print_theoretical_scorecard() methods in order to align with moving all debugging to Game class (this is a breaking change, but I'm not doing a major version update because Semantic Versioning specifies that breaking changes during v0.x.x are expected and do not necessitate major updates).

## [0.1.2] - 2020-12-10
First working release - everything is an addition! 0.1.0 and 0.1.1 were mostly broken and thus were erased from existence. This is the first canonical release.