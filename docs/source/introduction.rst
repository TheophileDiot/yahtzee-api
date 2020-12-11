Introduction
============
Welcome to the Yahtzee API! This package provides the core functionalities to programmatically play a game of Yahtzee. The purpose of this package is for use with custom OpenAI Gym reinforcement learning environments (in development), however it is generalized for many different use cases including simple algorithm development. Currently the API is still pre version 1.0.0 and is being iterated rapidly so stability should not be taken for granted until 1.0.0 is released. See below for a further note on versioning.
This package is composed of two class: the Game class and the Player class. The Game class provides the general structure and manages advancing turns and determining the winner. 
Instantiating a Game object will create a list of Player objects that can be interacted with using the methods outlined in these docs. Click into the links on the left panel for a detailed description of the public methods and attributes for each class.

GitHub Repo
***********
To view the source code and examples for the Yahtzee API, visit the GitHub repo here `here <https://github.com/tomarbeiter/yahtzee_api>`__.

Installation
************
To install this package, run: ``pip install yahtzee-api``

A Note on Versioning
********************
This project is my first headfirst dive into the world of publishing Python packages, using Sphinx for documentation, GitHub Actions, etc. As such, there are plenty of junk commits and mistakes in the repo. I've done my best to clean it up and make sure that what is presented is accurate, up-to-date, and at least somewhat helpful. 
Canonically, v0.1.2 is the first release of this package. Yes, v0.1.0 and v0.1.1 existed, but both fell victim to my inexperience with Python publishing (amongst other things). From v0.1.2 on, all changes and versioning will following semantic versioning guidelines specified by `semver <https://semver.org/>`__.

Contact
*******
Questions? Comments? Want to contribute? Reach out to me via `email <arbeitertom@gmail.com>`__!