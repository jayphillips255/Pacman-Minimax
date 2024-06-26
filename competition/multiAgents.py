# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent


class MultiAgentSearchAgent(Agent):
    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        # self.index = 0 # Pacman is always agent index 0
        # self.evaluationFunction = util.lookup(evalFn, globals())
        self.evaluationFunction = better
        self.depth = int(depth)


class ReflexAgent(Agent):
    def getAction(self, gameState):
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions(0) # Passing in '0' as the agent index

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action, 0) # Should be 0 for Jay's agent
        newPos = successorGameState.getPacmanPosition(0)
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        capsules = successorGameState.data.capsules

        x = len(newFood.data)
        y = len(newFood[1])

        # Closer to food increases evaluation
        foodScore = 0
        for i in range(x):
            for j in range(y):
                if (newFood[i][j]):
                    distance = util.manhattanDistance(newPos, (i, j))
                    if (distance == 0):
                        foodScore += 1
                    else:
                        foodScore += 1 / distance
        # Closer to ghosts decreases evaluation
        ghostScore = 0
        for i in range(len(newGhostStates)):
            distance = util.manhattanDistance(newPos, newGhostStates[i].start.pos)
            if (distance == 0):
                ghostScore += -1
            else:
                ghostScore += -1 / distance
        
        # Closer to capsules increases evaluation
        capsuleScore = 0
        for c in capsules:
            distance = util.manhattanDistance(newPos, c)
            if (distance == 0):
                capsuleScore += 1
            else:
                capsuleScore += 1 / distance
        
        # Being closer to food is less important than avoiding ghosts. This is why foodScore has a coefficient
        return successorGameState.getScore0() + ghostScore + foodScore*0.65 + capsuleScore*0.1
    

# Using my Minimax agent with Alpha Beta Pruning
class AlphaBetaAgent(MultiAgentSearchAgent):

    def termState(self, gameState):
        if hasattr(gameState, 'problem'):
            terminalStates = gameState.problem.winStates | gameState.problem.loseStates
            return gameState.state in terminalStates
        else:
            return gameState.data._win or gameState.data._lose

    def minimax(self, gameState, alpha, beta, agentIndex, depth):
        if depth == 0 or self.termState(gameState):
            return self.evaluationFunction(gameState)
        if agentIndex == 0:
            return self.maxValue(gameState, alpha, beta, agentIndex, depth)
        else:
            return self.minValue(gameState, alpha, beta, agentIndex, depth)

    def maxValue(self, gameState, alpha, beta, agentIndex, depth):
        v = float('-inf')
        actions = gameState.getLegalActions(agentIndex)
        for action in actions:
            newState = gameState.generateSuccessor(agentIndex, action)
            v = max(v, self.minimax(newState, alpha, beta, agentIndex + 1, depth))
            if v > beta:
                return v  # Return v if we can't find a better ghost move
            alpha = max(alpha, v)
            self.evals[(gameState, action)] = v  # We need to remember the evaluation of each action
        return v

    def minValue(self, gameState, alpha, beta, agentIndex, depth):
        v = float('inf')
        actions = gameState.getLegalActions(agentIndex)
        # If agent is the last ghost, it's time for Pacman to move (agentIndex will be 0)
        if agentIndex == gameState.getNumAgents() - 1:
            newIndex = 0
            newDepth = depth - 1
        else:
            newIndex = agentIndex + 1
            newDepth = depth
        for action in actions:
            newState = gameState.generateSuccessor(agentIndex, action)
            v = min(v, self.minimax(newState, alpha, beta, newIndex, newDepth))
            if v < alpha:
                return v  # Return v if we can't find a better Pacman move
            beta = min(beta, v)
        return v

    def getAction(self, gameState, agentIndex):
        n = gameState.getNumAgents()
        self.evals = {}  # Dictionary of (state, action), eval pairs 
        actions = gameState.getLegalActions(agentIndex)  # Get a list of possible Pacman actions
        e = self.minimax(gameState, float('-inf'), float('inf'), 0, self.depth)  # Get the evaluation of the best action
        for a in actions:
            if self.evals[(gameState, a)] == e:
                correctAction = a
                break
        return correctAction

        # This has the same format as the Reflex agent's evaluation function
        def evaluationFunction(self, currentGameState, action):
            # Useful information you can extract from a GameState (pacman.py)
            successorGameState = currentGameState.generatePacmanSuccessor(action, 0) # Should be 0 for Jay's agent
            newPos = successorGameState.getPacmanPosition(0)
            newFood = successorGameState.getFood()
            newGhostStates = successorGameState.getGhostStates()
            newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
            capsules = successorGameState.data.capsules

            x = len(newFood.data)
            y = len(newFood[1])

            otherpacman = successorGameState

            # Closer to food increases evaluation
            foodScore = 0
            for i in range(x):
                for j in range(y):
                    if (newFood[i][j]):
                        distance = util.manhattanDistance(newPos, (i, j))
                        if (distance == 0):
                            foodScore += 1
                        else:
                            foodScore += 1 / distance
            # Closer to ghosts decreases evaluation
            ghostScore = 0
            for i in range(len(newGhostStates)):
                distance = util.manhattanDistance(newPos, newGhostStates[i].start.pos)
                if (distance == 0):
                    ghostScore += -1
                else:
                    ghostScore += -1 / distance
            
            # Closer to capsules increases evaluation
            capsuleScore = 0
            for c in capsules:
                distance = util.manhattanDistance(newPos, c)
                if (distance == 0):
                    capsuleScore += 1
                else:
                    capsuleScore += 1 / distance
            
            # Being closer to food is less important than avoiding ghosts. This is why foodScore has a coefficient
            return successorGameState.getScore0() + ghostScore + foodScore*0.65 + capsuleScore*0.1


# The code for this ExpectimaxAgent class came directly from Jay's project2 code.
# This code is here only as a starting point. It will be modified as we progress.
class ExpectimaxAgent(MultiAgentSearchAgent):
    def getAction(self, gameState, agentIndex=0):
        def expectimax(gameState, agentIndex, depth):
            if (depth == 0 or termState(gameState)): 
                return self.evaluationFunction(gameState)
            if (agentIndex == 0):
                return maxValue(gameState, agentIndex, depth)
            else:
                return expValue(gameState, agentIndex, depth)
        def maxValue(gameState, agentIndex, depth):
            v = float('-inf')
            actions = gameState.getLegalActions(agentIndex)
            for action in actions:
                newState = gameState.generateSuccessor(agentIndex, action)
                v = max(v, expectimax(newState, agentIndex + 1, depth))
                evals[(gameState, action)] = v # We need to remember the evaluation of each action
            return v
        def expValue(gameState, agentIndex, depth):
            v = 0
            actions = gameState.getLegalActions(agentIndex)
            # If agent is last ghost, its time for packman to move (AgentIndex will be 0)
            if (agentIndex == n - 1):
                newIndex = 0
                newDepth = depth - 1
            else:
                newIndex = agentIndex + 1
                newDepth = depth
            num = len(actions)
            for i in range(num):
                newState = gameState.generateSuccessor(agentIndex, actions[i])
                v += (1/num)*expectimax(newState, newIndex, newDepth)
            return v
        def termState(gameState):
            if hasattr(gameState, 'problem'):
                terminalStates = gameState.problem.winStates | gameState.problem.loseStates
                return gameState.state in terminalStates
            else:
                return gameState.data._win or gameState.data._lose

        n = gameState.getNumAgents()
        evals = {} # Dictionary of (state, action) eval pairs
        actions = gameState.getLegalActions(0) # Get a list of possible paacman actions
        e = expectimax(gameState, 0, self.depth) # Get the evaluation of the best action

        for a in actions:
            if (evals[(gameState, a)] == e):
                return a


def betterEvaluationFunction(currentGameState):
    newPos = currentGameState.getPacmanPosition(0) # Must be 0 for Jay's Agent
    food = currentGameState.data.food
    newGhostStates = currentGameState.getGhostStates()
    capsules = currentGameState.data.capsules

    x = food.width
    y = food.height

    pacDist = 0
    pacDist = util.manhattanDistance(newPos, currentGameState.data.agentStates[1].configuration.pos) 

    foodScore = 0
    for i in range(x):
        for j in range(y):
            if (food[i][j]):
                distance = util.manhattanDistance(newPos, (i, j))
                if (distance == 0):
                    foodScore += 1
                else:
                    foodScore += 1 / distance

    ghostScore = 0
    for i in range(len(newGhostStates)):
        distance = util.manhattanDistance(newPos, newGhostStates[i].start.pos)
        if (distance == 0):
            ghostScore += -1
        else:
            ghostScore += -1 / distance
    
    capsuleScore = 0
    for c in capsules:
        distance = util.manhattanDistance(newPos, c)
        if (distance == 0):
            capsuleScore += 1
        else:
            capsuleScore += 1 / distance
    
    # Code is the same as q1 with minor changes
    return currentGameState.getScore0() + ghostScore + foodScore*0.65 + capsuleScore + 0.6*pacDist


# Abbreviation
better = betterEvaluationFunction

