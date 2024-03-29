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
import pdb

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below giis provided as a guide.  You are welcome to change
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
        "*** YOUR CODE HERE ***"
        if (newPos in successorGameState.getCapsules()):
            return 10000
        pts = 0
        oldPos = currentGameState.getPacmanPosition()
        g = 0
        for ghost in newGhostStates:
            gPos = ghost.getPosition()
            oldDist = abs(oldPos[0] - gPos[0]) + abs(oldPos[1] - gPos[1])
            newDist = abs(newPos[0] - gPos[0]) + abs(newPos[1] - gPos[1])
            flag = 1
            if (newScaredTimes[g] > 0):
                flag = -1
            pts += (oldDist - newDist)
            g += 1
            if (newDist <= 1):
                return -5000 * flag
        return successorGameState.getScore() + pts

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
        def maxPac(state,numGhosts,depth):
            if state.isWin() or state.isLose() or depth == 0:
                return self.evaluationFunction(state)
            score = -float('inf')
            temp = score
            pMoves = state.getLegalActions(0)
            for move in pMoves:
                score = max(score,minGhost(state.generateSuccessor(0,move),1,numGhosts,depth))
            return score

        
        def minGhost(state,ghost,numGhosts,depth):
            if state.isWin() or state.isLose() or depth == 0:
                return self.evaluationFunction(state)
            score = float('inf')
            gMoves = state.getLegalActions(ghost)
            for move in gMoves:
                if ghost < numGhosts:
                    score = min(score,minGhost(state.generateSuccessor(ghost,move),ghost+1,numGhosts,depth))
                else:
                    score = min(score, maxPac(state.generateSuccessor(ghost,move),numGhosts,depth-1))
            return score

        score = -float('inf')
        temp = score
        pMoves = gameState.getLegalActions(0)
        numGhosts = gameState.getNumAgents()-1
        action = None
        for move in pMoves:
            score = max(score,minGhost(gameState.generateSuccessor(0,move),1,numGhosts,self.depth))
            if score > temp:
                temp = score
                action = move
        return action

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def maxPac(state,numGhosts,depth,alpha,beta):
            if state.isWin() or state.isLose() or depth == 0:
                return self.evaluationFunction(state)
            score = -float('inf')
            temp = score
            pMoves = state.getLegalActions(0)
            for move in pMoves:
                score = max(score,minGhost(state.generateSuccessor(0,move),1,numGhosts,depth,alpha,beta))
                if score > beta:
                    return score
                alpha = max(alpha,score)
            return score

        
        def minGhost(state,ghost,numGhosts,depth,alpha,beta):
            if state.isWin() or state.isLose() or depth == 0:
                return self.evaluationFunction(state)
            score = float('inf')
            gMoves = state.getLegalActions(ghost)
            for move in gMoves:
                if ghost < numGhosts:
                    score = min(score,minGhost(state.generateSuccessor(ghost,move),ghost+1,numGhosts,depth,alpha,beta))
                    if score < alpha:
                        return score
                    beta = min(beta,score)
                else:
                    score = min(score, maxPac(state.generateSuccessor(ghost,move),numGhosts,depth-1,alpha,beta))
                    if score < alpha:
                        return score
                    beta = min(beta,score)
            return score

        score = -float('inf')
        temp = score
        alpha = temp
        beta = float('inf')
        pMoves = gameState.getLegalActions(0)
        numGhosts = gameState.getNumAgents()-1
        action = None
        for move in pMoves:
            score = max(score,minGhost(gameState.generateSuccessor(0,move),1,numGhosts,self.depth,alpha,beta))
            if score > temp:
                temp = score
                action = move
            if score >= beta:
                action = move
                return action
            alpha = max(alpha,score)
        return action
        util.raiseNotDefined()

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
        def maxPac(state,numGhosts,depth):
            if state.isWin() or state.isLose() or depth == 0:
                return self.evaluationFunction(state)
            score = -float('inf')
            temp = score
            pMoves = state.getLegalActions(0)
            for move in pMoves:
                score = max(score,expGhost(state.generateSuccessor(0,move),1,numGhosts,depth))
            return score

        
        def expGhost(state,ghost,numGhosts,depth):
            if state.isWin() or state.isLose() or depth == 0:
                return self.evaluationFunction(state)
            score = 0
            gMoves = state.getLegalActions(ghost)
            p = 1/len(gMoves)
            for move in gMoves:
                if ghost < numGhosts:
                    score += p*expGhost(state.generateSuccessor(ghost,move),ghost+1,numGhosts,depth)
                else:
                    score += p*maxPac(state.generateSuccessor(ghost,move),numGhosts,depth-1)
            return score

        score = -float('inf')
        temp = score
        pMoves = gameState.getLegalActions(0)
        numGhosts = gameState.getNumAgents()-1
        action = None
        for move in pMoves:
            score = max(score,expGhost(gameState.generateSuccessor(0,move),1,numGhosts,self.depth))
            if score > temp:
                temp = score
                action = move

        return action

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: 

    Reading the official description of the ai projects at http://ai.berkeley.edu/multiagent.html
    gave the hint to return a linear combination of features that we consider important to the game.
    Additionally, the hint to use reciprocal values was also given there.
    Therefore, we used the reciprocal values to return higher numbers based on all food, capsules, 
    and ghosts in the game. As these are really the only three things needed to complete the game
    no other information was considered.

    For the linear combination we weighted food the highest, at 2 times value, capsules second highest,
    at 1.5 times value, and ghosts the lowest (as all we need to do is avoid them), at .35

    I wish I could say I have a mathematical reasoning for using these values, but I dont. In reality 
    these were the best values that I could come up with when altering them to see their effects.
    """
    "*** YOUR CODE HERE ***"

    score = currentGameState.getScore()
    pac = currentGameState.getPacmanPosition()
    
    # distance to foods
    food = 0
    foodList = currentGameState.getFood().asList()
    for foods in foodList:
        food += 1/manhattanDistance(pac,foods)

    # distance to capsules
    capsule = 0
    for blob in currentGameState.getCapsules():
        capsule += 1/manhattanDistance(pac,blob)

    #distance to ghosts
    adv,g = 0,0
    newScaredTimes = [ghostState.scaredTimer for ghostState in currentGameState.getGhostStates()]
    for ghost in currentGameState.getGhostStates():
        gPos = ghost.getPosition()
        flag = 1
        if (newScaredTimes[g] > 0):
            flag = -1
        demon = manhattanDistance(pac,gPos)
        if (demon == 0):
            demon = float('inf')
        adv += flag*(1/demon)
        g += 1
    
    return score + 2*food + 1.5*capsule + .35*adv

# Abbreviation
better = betterEvaluationFunction