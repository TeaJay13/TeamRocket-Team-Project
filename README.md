## Table of Contents

1. [Overview](#overview)
2. [How to Play](#how-to-play)
3. [Controls](#controls)
4. [Development Environment](#development-environment)
5. [Collaborators](#collaborators)
6. [Useful Websites](#useful-websites)
7. [Future Work](#future-work)

# Overview

The goal of this project is to create a game using the pygame module in python. The program uses several classes that integrate with the main game.py file to run the different parts of the game. The game stores user and game data to a database. The game uses inputs from the player to move around a 2d environment with dynamic enemies and obstacles. The player is able to move, jump, and use a weapon. The game contains a start and end screen to indicate what the player needs to do to start the game or end the game, and when they lose they are shown the top 5 scores and then the player can quit.

## How to Play

When the game is launched the player is given the options between 2 maps, and a quit button if they choose to do so. Upon picking a map there player character will be spawned in the 2d arena environment. This is where the game loop starts. The player must move around and fire their weapon to defeat enemies with ranging health, the enemies are always following the player. The game ends when an enemy reaches the player. Upon death the player's score is saved to a database, and the top 5 scores are shown. After a minute of playtime the bullet firing cooldown is reduced to 0 allowing the player to fire at will at the endless onslaught of bugs.

### Controls:

* `SPACE` - Jump
* `A` - Move Left
* `D` - Move Right
* `MOUSE_LEFT_CLICK` - Fire Bullet

<!-- [Software Demo Video](???LINK???) -->

# Development Environment

In creation of this project we used the Python3 programming language and used the community-made pygame module for game creation. We used several online tutorials and the assistance of AI. We also used a SQLite datatbase to store scores for the users.

Here is a list of the libraries used in python:
* pygame
* sys
* math
* random
* sqlite3

# Collaborators

* David Larsen - Team Leader, Project Manager
* Connor Babb - Documentation Manager
* Andrew Olson - Quality Assurance
* Egor Smirnov - Graphic Designer
* TJ Strickland - Configuration Manager

# Useful Websites

* [YouTube.com - Pygame Tutorial](https://www.youtube.com/watch?v=2gABYM5M0ww)
* [pygame.org](https://www.pygame.org/wiki/tutorials)

# Future Work

* Add more enemies/powerups/weapons
* Create more maps/randomize obstacles
* Add music/sounds. Add more graphics