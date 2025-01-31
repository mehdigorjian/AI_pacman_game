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

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        print('successorGameState: ',successorGameState)
        print('newPos: ', newPos)
        print('newFood: ', newFood)
        print('newGhostStates: ', newGhostStates)
        print('newScaredTimes', newScaredTimes)

        "*** YOUR CODE HERE ***"

        #Food dist
        newFoodList = newFood.asList()
        min_food_dist = -1
        for food in newFoodList:
            dist = util.manhattanDistance(newPos, food)
            if min_food_dist >= dist or min_food_dist == -1:
                min_food_dist = dist

        #Ghost dist
        dist_to_ghosts = 1
        approx_to_ghosts = 0
        for ghost_state in successorGameState.getGhostPositions():
            dist = util.manhattanDistance(newPos, ghost_state)
            dist_to_ghosts += dist
            if dist <= 1:
                approx_to_ghosts += 1



        return successorGameState.getScore() + (1 / float(min_food_dist)) - (
                1 / float(dist_to_ghosts)) - approx_to_ghosts

        #return successorGameState.getScore()


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        #player = gameState.getNumAgents()

        def minMaxHelper(gameState, deepness, agent):
            if agent >= gameState.getNumAgents():
                agent = 0
                deepness += 1
            if (deepness == self.depth or gameState.isWin() or gameState.isLose()):
                return self.evaluationFunction(gameState)
            elif (agent == 0):
                return maxFinder(gameState, deepness, agent)
            else:
                return minFinder(gameState, deepness, agent)

        def maxFinder(gameState, deepness, agent):
            output = ["meow", -float("inf")]
            pacActions = gameState.getLegalActions(agent)

            if not pacActions:
                return self.evaluationFunction(gameState)

            for action in pacActions:
                currState = gameState.generateSuccessor(agent, action)
                currValue = minMaxHelper(currState, deepness, agent + 1)
                if type(currValue) is list:
                    testVal = currValue[1]
                else:
                    testVal = currValue
                if testVal > output[1]:
                    output = [action, testVal]
            return output

        def minFinder(gameState, deepness, agent):
            output = ["meow", float("inf")]
            ghostActions = gameState.getLegalActions(agent)

            if not ghostActions:
                return self.evaluationFunction(gameState)

            for action in ghostActions:
                currState = gameState.generateSuccessor(agent, action)
                currValue = minMaxHelper(currState, deepness, agent + 1)
                if type(currValue) is list:
                    testVal = currValue[1]
                else:
                    testVal = currValue
                if testVal < output[1]:
                    output = [action, testVal]
            return output

        outputList = minMaxHelper(gameState, 0, 0)
        return outputList[0]

        #util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def minMaxHelper(gameState, deepness, agent, alpha, beta):
            if agent >= gameState.getNumAgents():
                agent = 0
                deepness += 1
            if (deepness == self.depth or gameState.isWin() or gameState.isLose()):
                return self.evaluationFunction(gameState)
            elif (agent == 0):
                return maxFinder(gameState, deepness, agent, alpha, beta)
            else:
                return minFinder(gameState, deepness, agent, alpha, beta)

        def maxFinder(gameState, deepness, agent, alpha, beta):
            output = ["meow", -float("inf")]
            pacActions = gameState.getLegalActions(agent)

            if not pacActions:
                return self.evaluationFunction(gameState)

            for action in pacActions:
                currState = gameState.generateSuccessor(agent, action)
                currValue = minMaxHelper(currState, deepness, agent + 1, alpha, beta)

                if type(currValue) is list:
                    testVal = currValue[1]
                else:
                    testVal = currValue

                # real logic
                if testVal > output[1]:
                    output = [action, testVal]
                if testVal > beta:
                    return [action, testVal]
                alpha = max(alpha, testVal)
            return output

        def minFinder(gameState, deepness, agent, alpha, beta):
            output = ["meow", float("inf")]
            ghostActions = gameState.getLegalActions(agent)

            if not ghostActions:
                return self.evaluationFunction(gameState)

            for action in ghostActions:
                currState = gameState.generateSuccessor(agent, action)
                currValue = minMaxHelper(currState, deepness, agent + 1, alpha, beta)

                if type(currValue) is list:
                    testVal = currValue[1]
                else:
                    testVal = currValue

                if testVal < output[1]:
                    output = [action, testVal]
                if testVal < alpha:
                    return [action, testVal]
                beta = min(beta, testVal)
            return output

        outputList = minMaxHelper(gameState, 0, 0, -float("inf"), float("inf"))
        return outputList[0]

        #util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"

        def expHelper(gameState, deepness, agent):
            if agent >= gameState.getNumAgents():
                agent = 0
                deepness += 1
            if (deepness == self.depth or gameState.isWin() or gameState.isLose()):
                return self.evaluationFunction(gameState)
            elif (agent == 0):
                return maxFinder(gameState, deepness, agent)
            else:
                return expFinder(gameState, deepness, agent)

        def maxFinder(gameState, deepness, agent):
            output = ["meow", -float("inf")]
            pacActions = gameState.getLegalActions(agent)

            if not pacActions:
                return self.evaluationFunction(gameState)

            for action in pacActions:
                currState = gameState.generateSuccessor(agent, action)
                currValue = expHelper(currState, deepness, agent + 1)
                if type(currValue) is list:
                    testVal = currValue[1]
                else:
                    testVal = currValue
                if testVal > output[1]:
                    output = [action, testVal]
            return output

        def expFinder(gameState, deepness, agent):
            output = ["meow", 0]
            ghostActions = gameState.getLegalActions(agent)

            if not ghostActions:
                return self.evaluationFunction(gameState)

            probability = 1.0 / len(ghostActions)

            for action in ghostActions:
                currState = gameState.generateSuccessor(agent, action)
                currValue = expHelper(currState, deepness, agent + 1)
                if type(currValue) is list:
                    val = currValue[1]
                else:
                    val = currValue
                output[0] = action
                output[1] += val * probability
            return output

        outputList = expHelper(gameState, 0, 0)
        return outputList[0]

        #util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    foodPos = currentGameState.getFood().asList()
    foodDist = []
    ghostStates = currentGameState.getGhostStates()
    capPos = currentGameState.getCapsules()
    currentPos = list(currentGameState.getPacmanPosition())

    for food in foodPos:
        food2pacmanDist = manhattanDistance(food, currentPos)
        foodDist.append(-1 * food2pacmanDist)

    if not foodDist:
        foodDist.append(0)

    return max(foodDist) + currentGameState.getScore()

    #util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
