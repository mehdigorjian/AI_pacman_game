# myTeam.py
# ---------
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


from captureAgents import CaptureAgent
import random, time, util
from game import Directions
import game

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first = 'DummyAgent', second = 'DummyAgent'):
  """
  This function should return a list of two agents that will form the
  team, initialized using firstIndex and secondIndex as their agent
  index numbers.  isRed is True if the red team is being created, and
  will be False if the blue team is being created.

  As a potentially helpful development aid, this function can take
  additional string-valued keyword arguments ("first" and "second" are
  such arguments in the case of this function), which will come from
  the --redOpts and --blueOpts command-line arguments to capture.py.
  For the nightly contest, however, your team will be created without
  any extra arguments, so you should make sure that the default
  behavior is what you want for the nightly contest.
  """

  # The following line is an example only; feel free to change it.
  return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Agents #
##########

class DummyAgent(CaptureAgent):
  """
  A Dummy agent to serve as an example of the necessary agent structure.
  You should look at baselineTeam.py for more details about how to
  create an agent as this is the bare minimum.
  """

  def registerInitialState(self, gameState):
    """
    This method handles the initial setup of the
    agent to populate useful fields (such as what team
    we're on).

    A distanceCalculator instance caches the maze distances
    between each pair of positions, so your agents can use:
    self.distancer.getDistance(p1, p2)

    IMPORTANT: This method may run for at most 15 seconds.
    """

    '''
    Make sure you do not delete the following line. If you would like to
    use Manhattan distances instead of maze distances in order to save
    on initialization time, please take a look at
    CaptureAgent.registerInitialState in captureAgents.py.
    '''
    CaptureAgent.registerInitialState(self, gameState)

    '''
    Your initialization code goes here, if you need any.
    '''

    self.enemyFood = self.getFood(gameState)
    self.myFood = self.getFoodYouAreDefending(gameState)
    self.myTeam = self.getTeam(gameState)
    self.enemyTeam = self.getOpponents(gameState)
    if gameState.isOnRedTeam(self.index):
      self.enemies = gameState.getBlueTeamIndices()
    else:
      self.enemies = gameState.getRedTeamIndices()


  def chooseAction(self, gameState):
    """
    Picks among actions randomly.
    """
    actions = gameState.getLegalActions(self.index)

    '''
    You should change this in your own agent.
    '''

    # actions = gameState.getLegalActions(self.index)
        actions = [a for a in gameState.getLegalActions(self.index) if a != Directions.STOP]
        
        previousPos = gameState.getAgentState(self.index).getPosition()
        # previousDirection = gameState.getAgentState(self.index).getDirection()
        possibleCells = [self.getActionCoordinates(action, previousPos) for action in actions]

        foodGrid = self.getFood(gameState)
        foodList = foodGrid.asList()
        capsules = self.getCapsules(gameState)
        wallsGrid = gameState.getWalls()
        
        defenseFoodGrid = self.getFoodYouAreDefending(gameState)
        defenseFoodList = defenseFoodGrid.asList()
        defenseCapsules = self.getCapsulesYouAreDefending(gameState)
      
        allies = [gameState.getAgentState(i) for i in self.getTeam(gameState)]
        hunters = [a for a in allies if a.isPacman and a.getPosition() != None]
        defenders = [a for a in allies if not a.isPacman and a.getPosition() != None]
        
        enemies = [gameState.getAgentState(i) for i in self.getOpponents(gameState)]
        invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
        ghosts = [a for a in enemies if not a.isPacman and a.getPosition() != None]
      
        isPacman = gameState.getAgentState(self.index).isPacman
        amScared = gameState.getAgentState(self.index).scaredTimer != 0
        
        defendMode = False
        
        if invaders:
            minDistance = maxint
            closestAllied = None
            for index in self.getTeam(gameState):
                minInvaderDistance = min([self.getMazeDistance(gameState.getAgentState(index).getPosition(), i.getPosition()) for i in invaders])
                if minInvaderDistance < minDistance:
                    minDistance = minInvaderDistance
                    closestAllied = index
            if closestAllied == self.index:
                defendMode = True  
        
        if not defendMode:
            evalFunc = self.generateEvalFunc(self.generateOffensiveGaussians(wallsGrid, foodList, foodGrid, capsules, hunters, ghosts, defenders, possibleCells, previousPos, isPacman))
        else:
            # defensive mode
            # if I was attacking, and I have food nearby, eat the food
            # because I will eventually die and defend OR generate more points than the attacker OR defend because there is no food nearby
            for cell in possibleCells:
                if cell in foodList:
                    return [a for a, c in zip(actions, possibleCells) if c == cell][0]
            
            evalFunc = self.generateEvalFunc(self.generateDefenseGaussians(amScared, defenseFoodList, defenseCapsules, defenders, invaders, ghosts, possibleCells))
            
        
        actionPoints = [evalFunc(cell) for cell in possibleCells]
        
        if not actionPoints:
            return Directions.STOP
        
        maxValue = max(actionPoints)

        bestActions = [a for a, v in zip(actions, actionPoints) if v == maxValue]

        return random.choice(bestActions)

    def generateOffensiveGaussians(self, wallsGrid, foodList, foodGrid, capsules, hunters, ghosts, defenders, possibleCells, previousPos, isPacman):
        gaussians = []
      
        for food in foodList:
            gaussians.append(self.gaussian(self.chromoawesome[0], self.chromoawesome[1], food[0], food[1]))
            
            isLonely = True
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    isCellInGrid = (food[0] + i < foodGrid.width) and (food[0] + i >= 0) and (food[1] + j < foodGrid.height) and (food[1] + j) >= 0
                    if (i != 0 or j != 0) and isCellInGrid and foodGrid[food[0] + i][food[1] + j]:
                        isLonely = False
                        break
            
            if isLonely:
                gaussians.append(self.gaussian(self.chromoawesome[10], self.chromoawesome[11], food[0], food[1]))                            
            
        for capsule in capsules:
            gaussians.append(self.gaussian(self.chromoawesome[8], self.chromoawesome[9], capsule[0], capsule[1]))
      
        for ghost in ghosts:
            if ghost.scaredTimer == 0:  # ghost offers danger
                # If I'm in defense, only worry about if I'm close
                if isPacman or self.getMazeDistance(ghost.getPosition(), previousPos) < 8:
                    ghostGaussian = self.gaussian(self.chromoawesome[2], self.chromoawesome[3], ghost.getPosition()[0], ghost.getPosition()[1])
                    gaussians.append(ghostGaussian)
                    gaussians.append(self.calculateWallPenalty(wallsGrid, ghostGaussian))
            else:
                gaussians.append(self.gaussian(self.chromoawesome[4], self.chromoawesome[5], ghost.getPosition()[0], ghost.getPosition()[1]))
                
        for hunter in hunters:
            # only care about spread if I have more than two choices, not in a corridor
            if len(possibleCells) > 2:
                gaussians.append(self.gaussian(self.chromoawesome[6], self.chromoawesome[7], hunter.getPosition()[0], hunter.getPosition()[1]))
              
        # new, spread ghosts while walking to offense, uses the same chromosome as the defensive spread
        for defender in defenders:
            # only care about spread if I have more than two choices, not in a corridor
            if len(possibleCells) > 2:
                gaussians.append(self.gaussian(self.chromoawesome[18], self.chromoawesome[19], defender.getPosition()[0], defender.getPosition()[1]))
            
        return gaussians
    
    def calculateWallPenalty(self, wallsGrid, ghostGaussian):
        def getWallPenaltyForCell(x, y):
            numberOfWalls = 0
            for i, j in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    isCellInGrid = x + i < wallsGrid.width and x + i >= 0 and y + j < wallsGrid.height and y + j >= 0
                    if isCellInGrid and wallsGrid[int(x + i)][int(y + j)]:
                        numberOfWalls += 1
            
            return numberOfWalls * ghostGaussian(x, y) * self.chromoawesome[22]
            
        return getWallPenaltyForCell
    
    def generateDefenseGaussians(self, amScared, defenseFoodList, defenseCapsules, defenders, invaders, ghosts, possibleCells):
        gaussians = []
      
        for food in defenseFoodList:
            gaussians.append(self.gaussian(self.chromoawesome[12], self.chromoawesome[13], food[0], food[1]))         
            
        for capsule in defenseCapsules:
            gaussians.append(self.gaussian(self.chromoawesome[20], self.chromoawesome[21], capsule[0], capsule[1]))
      
        for invader in invaders:
             if amScared:
                gaussians.append(self.gaussian(self.chromoawesome[14], self.chromoawesome[15], invader.getPosition()[0], invader.getPosition()[1]))
             else:
                gaussians.append(self.gaussian(self.chromoawesome[16], self.chromoawesome[17], invader.getPosition()[0], invader.getPosition()[1]))
                
        for defender in defenders:
            # only care about spread if I have more than two choices, not in a corridor
            if len(possibleCells) > 2:
                gaussians.append(self.gaussian(self.chromoawesome[18], self.chromoawesome[19], defender.getPosition()[0], defender.getPosition()[1]))
              
        return gaussians
    
    def getActionCoordinates(self, action, previousCoordinates):
        dx, dy = Actions.directionToVector(action)
        return (previousCoordinates[0] + dx, previousCoordinates[1] + dy)
    
    def generateEvalFunc(self, gaussians):
        def evalC(coordinate):
            return sumGaussians(coordinate[0], coordinate[1], gaussians)
        return evalC;
      
    def gaussian(self, A, sigma, x0, y0):
        def gaussianFunc(x, y):
            distance = self.getMazeDistance((x, y), (x0, y0))
            return A * exp(-(distance) / (2.0 * sq(sigma)))
        return gaussianFunc
    
    def setChromosome(self, chromosome):
        self.chromoawesome = chromosome

def sq(x):
    return x * x

def gaussianValueAt(x, y, g):
    return g(x, y)

def sumGaussians(x, y, gaussians):
    return sum([gaussianValueAt(x, y, gauss) for gauss in gaussians])    