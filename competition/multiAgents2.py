# multiAgents2.py
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

# Jesse's agent

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


# This is Jay's reflex agent from P2. This is just a starting point
class ReflexAgent(Agent):
    def getAction(self, gameState, agentIndex=1):
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions(1) # Passing in '1' as the agent index

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action, 1) # Should be 1 for Jesse's agent
        newPos = successorGameState.getPacmanPosition(1)
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
        return successorGameState.getScore1() + ghostScore + foodScore*0.65 + capsuleScore*0.1


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Jesse's expectimax agent (question 4)
    """
    def getAction(self, gameState, agentIndex=1):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        def value(state, searchingAtDepth, agentIndex): 
            if searchingAtDepth == self.depth or state.isWin() or state.isLose(): 
                # print('D'+ str(searchingAtDepth), state.isWin(), state.isLose())
                    return self.evaluationFunction(state), None
            else:
                if agentIndex + 1 == gameState.getNumAgents(): # if all the agents have been processed through,
                    return max_value(state, searchingAtDepth) # restart the search at the next level of depth with Pacman
                else:
                    return chanceNode(state, searchingAtDepth, agentIndex + 1)

        # Max function - maximizing positive utility values for Pacman
        def max_value(state, searchingAtDepth, agentIndex=1):
            v, move = -float('inf'), None
            for action in state.getLegalActions(1): # for all Pacman's legal actions...
                v2, a = value(state.generateSuccessor(1, action), searchingAtDepth, 1) # the (low) value of the ghosts' best/chosen action (their action doesn't matter to Pacman in the end, only the best value possible)
                # print('D:', searchingAtDepth,'(PACMAN) Act:', action, 'Val:', v2)
                if v2 > v: # this is Pacman CHECKING THE MAX VALUE from all generated nodes
                    # print(v2,action, 'D'+ str(searchingAtDepth), end=';')
                    v, move = v2, action # this is Pacman TAKING THE MAX VALUE and recording the associated action into move
            # print('PACMTaking:', move, 'D:', searchingAtDepth, 'V:', v)
            return v, move # best value and action for Pacman

        # Min function - minimizing negative utility values for ghosts
        def chanceNode(state, searchingAtDepth, agentIndex):
            v, move = 0, None
            actions = state.getLegalActions(agentIndex)
            if agentIndex + 1 == gameState.getNumAgents(): searchingAtDepth += 1 # if we're at the last ghost, advance depth and check for end of search in value()
            for action in state.getLegalActions(agentIndex): 
                v2, a = value(state.generateSuccessor(agentIndex, action), searchingAtDepth, agentIndex) # the (high) value of the next agent's best/chosen action
                v += v2 / len(actions) # average the values of all the ghost's actions
            # print('GHOSTaking:', move, 'D:', searchingAtDepth, 'V:', v)
            return v, move

        irrelevantValue, action = max_value(gameState, 0)
        return action # Pacman's best, highest value action



def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    # print('betterEvaluationFunction!!!')
    # Food state points
    foodList = currentGameState.getFood().asList()
    numFood = len(foodList)
    if numFood > 0:
        closestFood = min(foodList, key=lambda tupl: manhattanDistance(currentGameState.getPacmanPosition(1), tupl) ) # Must be 1 for Jesse's Agent
        distToClosestFood = manhattanDistance(currentGameState.getPacmanPosition(1), closestFood)
    else:
        return currentGameState.getScore1() # return without food points
    return 1./numFood + 1./distToClosestFood + currentGameState.getScore1()


# Abbreviation
better = betterEvaluationFunction
