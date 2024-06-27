# Pacman-Minimax
- A Python-Pacman extravaganza where two pacman compete for the high score
- Each pacman agent has a unique algorithm for selecting a move in a given game state
- This was the final project for Whitworth's Artificial Intelegence class.

## Run this Program
- Make sure you have python 3.7.0 installed on your machine
- Your computer's operating system must be looking inside the /competition directory
- Once you're in, run the terminal command: `py comp.py`

## What I did on this Project
All Agent classes in multiAgents.py, all of comp.py, helperFuncs.py, and small tweaks to nearly every other file in this project.<br>
This project built off existing files from Berkley's introductory AI course. We were given these files by our course instructor, Professor Qian Mao

## Project Goals
At the beginning of this project, we wanted to have our software:
- Run a pacman game with two pacman agents
- Have our agents make informed decisions pertaining to the game state

Did we meet all these goals? Yes, although there are still improvements to be had, more on this later

## This was a Group Project
I was assigned to work on this project with another student. Before we began writing code, we concluded there were three compoents to this project. The first two components were to write 2 pacman agents. We agreed for each of us to write one of them, and we did. The third component was to refactor the pacman game files to accomidate two pacman agents instead of just one, as was initially the case. This was by far the most difficult part of this project. Imagine reading 5 long python files you did not write, and understanding them enough to make our desired refactor. I did nearly all of this, and received virturally no help from the other student. This student was quite busy with other classes at the time, so I was fairly understanding. I acknowledged I was not getting the help needed, but remained respectful knowing their situation with other classes.

## At a Glance
There are two pacman agents. The first one (the one I wrote) is described in multiAgents.py. This agent uses the minimax algorithm with alpha-beta pruning for faster performance. The other pacman agent in multiAgents2.py uses the expectimax algorithm. The game also has two ghosts agents. One ghost chases the nearest pacman and the other ghost is random. We made it random to "seed" each simulation in a sense. If there are no ramdom elements in our game simulation, the same game would play out every time.

The simulation keeps running until a ghost chatches one of the pacman agents. One thing we've noticed is pacman agents tend to stall out and move between the same two positions after some time. We believe this has something to do with our agent's evaluation functions and a small search depth of 2. This needs further investigation.

Agents run calculations on the gamestate data to determine an action for a paticular gamestate. We utilized premade functions to access this data. This includes: coordinate locations of food pellets, capsules, all ghosts and agents, ghost scared timer, and dimensions of the game board.

## Possible Improvements
- Introduce a time limit for agents to produce a move to better compate agent preformance
- Improve the evaluation function to include the scared ghost timer
- Fix trashing, expiriment with larger search depths
- Use threads to speed up our searching algorithms
