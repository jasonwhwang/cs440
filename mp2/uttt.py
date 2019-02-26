from time import sleep
from math import inf
from random import randint

class ultimateTicTacToe:
    def __init__(self):
        """
        Initialization of the game.
        """
        self.board=[['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_']]
        self.maxPlayer='X'
        self.minPlayer='O'
        self.maxDepth=3
        #The start indexes of each local board
        self.globalIdx=[(0,0),(0,3),(0,6),(3,0),(3,3),(3,6),(6,0),(6,3),(6,6)]

        #Start local board index for reflex agent playing
        self.startBoardIdx=4
        # self.startBoardIdx=randint(0,8)

        #utility value for reflex offensive and reflex defensive agents
        self.winnerMaxUtility=10000
        self.twoInARowMaxUtility=500
        self.preventThreeInARowMaxUtility=100
        self.cornerMaxUtility=30

        self.winnerMinUtility=-10000
        self.twoInARowMinUtility=-100
        self.preventThreeInARowMinUtility=-500
        self.cornerMinUtility=-30

    def printGameBoard(self):
        """
        This function prints the current game board.
        """
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[:3]])+'\n')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[3:6]])+'\n')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[6:9]])+'\n')


    # ----------------------------------------------------------------
    # Helper Functions
    # ----------------------------------------------------------------
    def drawToBoard(self, coor, isMax):
        if isMax:
            self.board[coor[0]][coor[1]] = self.maxPlayer
        else:
            self.board[coor[0]][coor[1]] = self.minPlayer

    def removeFromBoard(self, coor):
        self.board[coor[0]][coor[1]] = '_'
    
    def getBoardIdx(self, coor):
        modY = coor[0] % 3
        modX = coor[1] % 3
        if modY == 0 and modX == 0:
            return 0
        if modY == 0 and modX == 1:
            return 1
        if modY == 0 and modX == 2:
            return 2
        if modY == 1 and modX == 0:
            return 3
        if modY == 1 and modX == 1:
            return 4
        if modY == 1 and modX == 2:
            return 5
        if modY == 2 and modX == 0:
            return 6
        if modY == 2 and modX == 1:
            return 7
        if modY == 2 and modX == 2:
            return 8

    def getLocalMoves(self, currBoardIdx):
        localMovesList = []
        localIdx = self.globalIdx[currBoardIdx]
        for row in range(localIdx[0], localIdx[0]+3):
            for col in range(localIdx[1], localIdx[1]+3):
                if self.board[row][col] == '_':
                    localMovesList.append((row,col))
        return localMovesList

    def getAllMoves(self):
        localMovesList = []
        for row in range(0, 9):
            for col in range(0, 9):
                if self.board[row][col] == '_':
                    localMovesList.append((row,col))
        return localMovesList

    def checkLocalWinner(self, currBoardIdx):
        localIdx = self.globalIdx[currBoardIdx]
        y = localIdx[0]
        x = localIdx[1]
        # Check Horizontals
        for row in range(y, y+3):
            if self.board[row][x] == self.maxPlayer and self.board[row][x+1] == self.maxPlayer and self.board[row][x+2] == self.maxPlayer:
                return 1
            if self.board[row][x] == self.minPlayer and self.board[row][x+1] == self.minPlayer and self.board[row][x+2] == self.minPlayer:
                return -1
        # Check Verticals
        for col in range(x, x+3):
            if self.board[y][col] == self.maxPlayer and self.board[y+1][col] == self.maxPlayer and self.board[y+2][col] == self.maxPlayer:
                return 1
            if self.board[y][col] == self.minPlayer and self.board[y+1][col] == self.minPlayer and self.board[y+2][col] == self.minPlayer:
                return -1
        # Check Diagonals
        if self.board[y][x] == self.maxPlayer and self.board[y+1][x+1] == self.maxPlayer and self.board[y+2][x+2] == self.maxPlayer:
            return 1
        if self.board[y][x] == self.minPlayer and self.board[y+1][x+1] == self.minPlayer and self.board[y+2][x+2] == self.minPlayer:
            return -1
        if self.board[y+2][x] == self.maxPlayer and self.board[y+1][x+1] == self.maxPlayer and self.board[y][x+2] == self.maxPlayer:
            return 1
        if self.board[y+2][x] == self.minPlayer and self.board[y+1][x+1] == self.minPlayer and self.board[y][x+2] == self.minPlayer:
            return -1
        
        return 0


    def countLocalTwoInARow(self, currBoardIdx, isMax):
        offense = 'X' if isMax else 'O'
        defense = 'O' if isMax else 'X'
        tiar = 0
        prevent = 0
        startCoor = self.globalIdx[currBoardIdx]
        cCoor = (startCoor[0]+1, startCoor[1]+1)
        tCoor = (startCoor[0], startCoor[1]+1)
        lCoor = (startCoor[0]+1, startCoor[1])
        bCoor = (startCoor[0]+2, startCoor[1]+1)
        rCoor = (startCoor[0]+1, startCoor[1]+2)


        # Check middle squares of top, bottom, left, and right 
        # top
        if self.board[tCoor[0]][tCoor[1]] == offense:
            if self.board[tCoor[0]][tCoor[1]-1] == offense and self.board[tCoor[0]][tCoor[1]+1] == '_':
                tiar += 1
            if self.board[tCoor[0]][tCoor[1]-1] == '_' and self.board[tCoor[0]][tCoor[1]+1] == offense:
                tiar += 1
            if self.board[tCoor[0]+1][tCoor[1]] == offense and self.board[tCoor[0]+2][tCoor[1]] == '_':
                tiar += 1
        if self.board[tCoor[0]][tCoor[1]] == defense:
            if self.board[tCoor[0]][tCoor[1]-1] == defense and self.board[tCoor[0]][tCoor[1]+1] == offense:
                prevent += 1
            if self.board[tCoor[0]][tCoor[1]-1] == offense and self.board[tCoor[0]][tCoor[1]+1] == defense:
                prevent += 1
            if self.board[tCoor[0]+1][tCoor[1]] == defense and self.board[tCoor[0]+2][tCoor[1]] == offense:
                prevent += 1
        # bottom
        if self.board[bCoor[0]][bCoor[1]] == offense:
            if self.board[bCoor[0]][bCoor[1]-1] == offense and self.board[bCoor[0]][bCoor[1]+1] == '_':
                tiar += 1
            if self.board[bCoor[0]][bCoor[1]-1] == '_' and self.board[bCoor[0]][bCoor[1]+1] == offense:
                tiar += 1
            if self.board[bCoor[0]-1][bCoor[1]] == offense and self.board[bCoor[0]-2][bCoor[1]] == '_':
                tiar += 1
        if self.board[bCoor[0]][bCoor[1]] == defense:
            if self.board[bCoor[0]][bCoor[1]-1] == defense and self.board[bCoor[0]][bCoor[1]+1] == offense:
                prevent += 1
            if self.board[bCoor[0]][bCoor[1]-1] == offense and self.board[bCoor[0]][bCoor[1]+1] == defense:
                prevent += 1
            if self.board[bCoor[0]-1][bCoor[1]] == defense and self.board[bCoor[0]-2][bCoor[1]] == offense:
                prevent += 1
        # left
        if self.board[lCoor[0]][lCoor[1]] == offense:
            if self.board[lCoor[0]-1][lCoor[1]] == offense and self.board[lCoor[0]+1][lCoor[1]] == '_':
                tiar += 1
            if self.board[lCoor[0]-1][lCoor[1]] == '_' and self.board[lCoor[0]+1][lCoor[1]] == offense:
                tiar += 1
            if self.board[lCoor[0]][lCoor[1]+1] == offense and self.board[lCoor[0]][lCoor[1]+2] == '_':
                tiar += 1
        if self.board[lCoor[0]][lCoor[1]] == defense:
            if self.board[lCoor[0]-1][lCoor[1]] == defense and self.board[lCoor[0]+1][lCoor[1]] == offense:
                prevent += 1
            if self.board[lCoor[0]-1][lCoor[1]] == offense and self.board[lCoor[0]+1][lCoor[1]] == defense:
                prevent += 1
            if self.board[lCoor[0]][lCoor[1]+1] == defense and self.board[lCoor[0]][lCoor[1]+2] == offense:
                prevent += 1
        # right
        if self.board[rCoor[0]][rCoor[1]] == offense:
            if self.board[rCoor[0]-1][rCoor[1]] == offense and self.board[rCoor[0]+1][rCoor[1]] == '_':
                tiar += 1
            if self.board[rCoor[0]-1][rCoor[1]] == '_' and self.board[rCoor[0]+1][rCoor[1]] == offense:
                tiar += 1
            if self.board[rCoor[0]][rCoor[1]-1] == offense and self.board[rCoor[0]][rCoor[1]-2] == '_':
                tiar += 1
        if self.board[rCoor[0]][rCoor[1]] == defense:
            if self.board[rCoor[0]-1][rCoor[1]] == defense and self.board[rCoor[0]+1][rCoor[1]] == offense:
                prevent += 1
            if self.board[rCoor[0]-1][rCoor[1]] == offense and self.board[rCoor[0]+1][rCoor[1]] == defense:
                prevent += 1
            if self.board[rCoor[0]][rCoor[1]-1] == defense and self.board[rCoor[0]][rCoor[1]-2] == offense:
                prevent += 1


        # diagonal
        if self.board[cCoor[0]][cCoor[1]] == offense:
            if self.board[cCoor[0]-1][cCoor[1]-1] == offense and self.board[cCoor[0]+1][cCoor[1]+1] == '_':
                tiar += 1
            if self.board[cCoor[0]-1][cCoor[1]-1] == '_' and self.board[cCoor[0]+1][cCoor[1]+1] == offense:
                tiar += 1
            if self.board[cCoor[0]+1][cCoor[1]-1] == offense and self.board[cCoor[0]-1][cCoor[1]+1] == '_':
                tiar += 1
            if self.board[cCoor[0]+1][cCoor[1]-1] == '_' and self.board[cCoor[0]-1][cCoor[1]+1] == offense:
                tiar += 1
        if self.board[cCoor[0]][cCoor[1]] == defense:
            if self.board[cCoor[0]-1][cCoor[1]-1] == defense and self.board[cCoor[0]+1][cCoor[1]+1] == offense:
                prevent += 1
            if self.board[cCoor[0]-1][cCoor[1]-1] == offense and self.board[cCoor[0]+1][cCoor[1]+1] == defense:
                prevent += 1
            if self.board[cCoor[0]+1][cCoor[1]-1] == defense and self.board[cCoor[0]-1][cCoor[1]+1] == offense:
                prevent += 1
            if self.board[cCoor[0]+1][cCoor[1]-1] == offense and self.board[cCoor[0]-1][cCoor[1]+1] == defense:
                prevent += 1
        
        return tiar, prevent

    def countCorners(self, currBoardIdx, isMax):
        symbol = 'X' if isMax else 'O'
        coor = self.globalIdx[currBoardIdx]
        count = 0
        if self.board[coor[0]][coor[1]] == symbol:
            count += 1
        if self.board[coor[0]][coor[1]+2] == symbol:
            count += 1
        if self.board[coor[0]+2][coor[1]] == symbol:
            count += 1
        if self.board[coor[0]+2][coor[1]+2] == symbol:
            count += 1
        return count


    # _________________________________________________________________

    def evaluatePredifined(self, isMax):
        """
        This function implements the evaluation function for ultimate tic tac toe for predifined agent.
        input args:
        isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        score(float): estimated utility score for maxPlayer or minPlayer
        """
        #YOUR CODE HERE
        score = 0
        tiar = 0
        prevent = 0
        corners = 0

        for count in range(0,9):
            tiar, prevent = self.countLocalTwoInARow(count, isMax)
            if isMax:    
                score += tiar*500
                score += prevent*100
            else:    
                score -= tiar*100
                score -= prevent*500
        if score != 0:
            return score

        for count in range(0,9):
            corners = self.countCorners(count, isMax)
            if isMax:
                score += corners*30
            else:
                score -= corners*30
        return score



    def evaluateDesigned(self, isMax):
        """
        This function implements the evaluation function for ultimate tic tac toe for your own agent.
        input args:
        isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        score(float): estimated utility score for maxPlayer or minPlayer
        """
        #YOUR CODE HERE
        score=0
        return score


    def checkMovesLeft(self):
        """
        This function checks whether any legal move remains on the board.
        output:
        movesLeft(bool): boolean variable indicates whether any legal move remains
                        on the board.
        """
        #YOUR CODE HERE
        # movesLeft=True
        for row in range(0, 9):
            for col in range(0, 9):
                if self.board[row][col] == '_':
                    return True
        return False

    def checkWinner(self):
        #Return termimnal node status for maximizer player 1-win,0-tie,-1-lose
        """
        This function checks whether there is a winner on the board.
        output:
        winner(int): Return 0 if there is no winner.
                     Return 1 if maxPlayer is the winner.
                     Return -1 if miniPlayer is the winner.
        """
        #YOUR CODE HERE
        winner=0
        for count in range(0,9):
            winner = self.checkLocalWinner(count)
            if winner != 0:
                return winner
        return winner

    def alphabeta(self,depth,currBoardIdx,alpha,beta,isMax):
        """
        This function implements alpha-beta algorithm for ultimate tic-tac-toe game.
        input args:
        depth(int): current depth level
        currBoardIdx(int): current local board index
        alpha(float): alpha value
        beta(float): beta value
        isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        bestValue(float):the bestValue that current player may have
        """
        #YOUR CODE HERE
        bestValue=0.0
        return bestValue

    def minimax(self, depth, currBoardIdx, isMax):
        """
        This function implements minimax algorithm for ultimate tic-tac-toe game.
        input args:
        depth(int): current depth level
        currBoardIdx(int): current local board index
        alpha(float): alpha value
        beta(float): beta value
        isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        bestValue(float):the bestValue that current player may have
        """
        #YOUR CODE HERE
        allValues = []

        if depth >= self.maxDepth:
            if self.checkLocalWinner(currBoardIdx) != 0:
                return 10000 if self.checkLocalWinner(currBoardIdx) == 1 else -10000
            return self.evaluatePredifined(isMax)

        currValidMoves = self.getLocalMoves(currBoardIdx)
        if not currValidMoves:
            if self.checkLocalWinner(currBoardIdx) != 0:
                return 10000 if self.checkLocalWinner(currBoardIdx) == 1 else -10000
            return self.evaluatePredifined(isMax)

        for validMove in currValidMoves:
            self.drawToBoard(validMove, isMax)
            currValue = self.minimax(depth+1, self.getBoardIdx(validMove), not isMax)
            self.removeFromBoard(validMove)
            allValues.append(currValue)

        return min(allValues)

    def playGamePredifinedAgent(self,maxFirst,isMinimax):
        bestMove=[]
        bestValue=[]
        gameBoards=[]
        winner=0
        expandedNodes = []
        currBoardIdx = self.startBoardIdx
        isMax = isMinimax
        currBestMove = None


        for count in range(0,81):

            currValidMoves = self.getLocalMoves(currBoardIdx)
            if not currValidMoves:
                currValidMoves = self.getAllMoves()
                if not currValidMoves:
                    break

            currBestMove = currValidMoves[0]
            currBestValue = 0.0
            if isMinimax:
                for validMove in currValidMoves:
                    self.drawToBoard(validMove,isMax)
                    tryValue = self.minimax(1, self.getBoardIdx(validMove), not isMax)
                    self.removeFromBoard(validMove)
                    if tryValue >= currBestValue:
                        currBestMove = validMove
                        currBestValue = tryValue
            
            self.drawToBoard(currBestMove, isMax)
            bestMove.append(currBestMove)
            bestValue.append(currBestValue)
            gameBoards.append(self.board)

            if self.checkLocalWinner(currBoardIdx) != 0:
                winner = self.checkLocalWinner(currBoardIdx)
                break

            currBoardIdx = self.getBoardIdx(currBestMove)
            isMax = not isMax

            self.printGameBoard()
            input(str(count) + "-->")
        
        self.printGameBoard()
        return gameBoards, bestMove, expandedNodes, bestValue, winner






    def playGamePredifinedAgentOG(self,maxFirst,isMinimax):
        """
        This function implements the processes of the game of predifined offensive agent vs defensive agent.
        input args:
        maxFirst(bool): boolean variable indicates whether maxPlayer or minPlayer plays first.
                        True for maxPlayer plays first, and False for minPlayer plays first.
        isMinimax(bool):boolean variable indicates whether it's using minimax or alpha-beta pruning algorithm.
                        True is minimax and False is alpha-beta.
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        bestValue(list of float): list of bestValue at each move
        expandedNodes(list of int): list of expanded nodes at each move
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE
        bestMove=[]
        bestValue=[]
        gameBoards=[]
        winner=0

        global expandedNodes

        # Algorithm
        # - Check if winner
        #   - If true, set winner end game
        #   - Else, continue
        # - Check if local board has valid move 
        #   - If so, get all possible moves for local board
        #   - Else, all possible moves include all non-empty positions
        #   - Else, if no non-empty positions, result is tie, break.
        #       - DFS on all moves
        #           - Check if offensive(max)/defensive(min), minimax or alphabeta
        #           - While depth is less than 3, continue search
        #           - For each expanded node, increment counter
        #           - when reach max depth, evaluate move
        # - Choose best move, push to list bestMove
        # - Push best value to bestValue
        # - Add move to board, push board to gameBoards
        # - Push number of expanded nodes to expandedNodes, reset to 0
        # - Change currBoardIdx to next board idx
        # - Change player
        #   - Print board
        #   - use input to pause game

        currBoardIdx = self.startBoardIdx
        currValidMoves = []
        currBestMove = None
        currBestValue = None
       
        isMax = maxFirst

        for count in range(0,81):
            # 1. Check Winner
            # if self.checkWinner() != 0:
            #     break

            # 2. Get Valid Moves
            currValidMoves = self.getLocalMoves(currBoardIdx)
            if not currValidMoves:
                currValidMoves = self.getAllMoves()
                if not currValidMoves:
                    break

            # 3. MiniMax/AlphaBeta
            currBestMove = currValidMoves[0]
            currBestValue = 0.0


            if isMinimax:
                for validMove in currValidMoves:
                    
                    tryValue = self.minimax(0, currBoardIdx, not isMax)
                    if tryValue > currBestValue:
                        currBestMove = validMove
                        currBestValue = tryValue

            # else:
            #     for validMove in currValidMoves:
            #         tryValue = self.alphabeta(0, currBoardIdx, 0, 0, isMax)
            #         if tryValue > currBestValue:
            #             currBestMove = validMove
            #             currBestValue = tryValue
            
            bestMove.append(currBestMove)
            bestValue.append(currBestValue)

            # - Add move to board, push board to gameBoards
            # - Push number of expanded nodes to expandedNodes, reset to 0
            # - Change currBoardIdx to next board idx
            
            isMax = not isMax
            self.printGameBoard()
            input(str(count) + "-->")

        self.printGameBoard()
        return gameBoards, bestMove, expandedNodes, bestValue, winner

    def playGameYourAgent(self):
        """
        This function implements the processes of the game of your own agent vs predifined offensive agent.
        input args:
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE
        bestMove=[]
        gameBoards=[]
        winner=0
        return gameBoards, bestMove, winner


    def playGameHuman(self):
        """
        This function implements the processes of the game of your own agent vs a human.
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE
        bestMove=[]
        gameBoards=[]
        winner=0
        return gameBoards, bestMove, winner

if __name__=="__main__":
    uttt=ultimateTicTacToe()
    gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playGamePredifinedAgent(True, True)
    if winner == 1:
        print("The winner is maxPlayer!!!")
    elif winner == -1:
        print("The winner is minPlayer!!!")
    else:
        print("Tie. No winner:(")
