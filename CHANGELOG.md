# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.2] - 2021-2-11
### Changed
- Player scorecard and theoretical scorecard dice index lists for each score are now initialized to [0, 0, 0, 0, 0] instead of [].

## [1.0.1] - 2021-1-31
### Fixed
- 3 and 4 of a Kind scoring functions now properly score all 5 dice, not just the 3/4 of a kind.

## [1.0.0] - 2021-1-23
### Changed
- Make Game.players attribute private.
- Check if the top-half 35-point bonus is won after each turn, instead of at the end of the game.
- Adheres to 1961 Joker rules for extra Yahtzee's.
- Rework Theoretical scorecard so dice used in calculation are marked with a 1 instead of storing the actual indices.
- Rolling is now based on 0 (roll) and 1 (don't roll) instead of True/False.
- Cleaned code for PEP 8 conformity.
- Renamed Player.roll_dice() to Player.roll()
- Renamed Player.theoretical_scorecard to t_scorecard
- Renamed Game.current_player() to Game.c_player()

### Removed
- Player.calulcate_final_score() method (unnecessary).
- Player.set_dice_to_reroll() method.

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