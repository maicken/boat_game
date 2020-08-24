# Boat Game

First attempt to use Reinforcement Learning in order to train a simple boat to cross a river.

Boat has two paddles which the AI can use, for each paddle the AI should provide a force, direction and if the paddle is under the water or above. Those values will make the boat move according to real world physics. Reward function tries to value speed and the distance that the boat has travelled, it also punishes beats.

The game interface was developped using Pygame, it can save and load different DL models. I tried to use Genetic alrogithms in order to train the AI, but without success. This project will be resumed as soon as I get more knowledge on the subject. 
