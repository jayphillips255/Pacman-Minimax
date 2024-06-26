# helperFuncs.py
# This file contains helper functions that are used in comp.py, our main file

import math

def getLayoutString(path):
    with open(path, 'r') as file:
        lines = [line.rstrip('\n') for line in file.readlines()]
    return lines

def getNesrestPacmanDist(ghostPos, pacman1Pos, pacman2Pos):
    distance1 = abs(ghostPos[0] - pacman1Pos[0]) + abs(ghostPos[1] - pacman1Pos[1])
    distance2 = abs(ghostPos[0] - pacman2Pos[0]) + abs(ghostPos[1] - pacman2Pos[1])
    if distance1 < distance2:
        return pacman1Pos
    else:
        return pacman2Pos