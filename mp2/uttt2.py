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
        #self.startBoardIdx=randint(0,8)

        #utility value for reflex offensive and reflex defensive agents
        self.winnerMaxUtility=10000
        self.twoInARowMaxUtility=500
        self.preventThreeInARowMaxUtility=100
        self.cornerMaxUtility=30

        self.winnerMinUtility=-10000
        self.twoInARowMinUtility=-100
        self.preventThreeInARowMinUtility=-500
        self.cornerMinUtility=-30

        self.expandedNodes=0
        self.currPlayer=True


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


    def horizontalCount(self, y, x):
        if self.currPlayer:
            offense = self.maxPlayer
            defense = self.minPlayer
        else:
            offense = self.minPlayer
            defense = self.maxPlayer
        tiar = 0
        prevent = 0
        for row in range(y, y+3):
            oCount = 0
            dCount = 0
            nCount = 0
            for col in range(x, x+3):
                if self.board[row][col] == offense:
                    oCount += 1
                elif self.board[row][col] == defense:
                    dCount += 1
                else:
                    nCount += 1
            
            if oCount == 2 and nCount == 1:
                tiar += 1
            if oCount == 1 and dCount == 2:
                prevent += 1
        return tiar, prevent

    def verticalCount(self, y, x):
        if self.currPlayer:
            offense = self.maxPlayer
            defense = self.minPlayer
        else:
            offense = self.minPlayer
            defense = self.maxPlayer
        tiar = 0
        prevent = 0
        for col in range(x, x+3):
            oCount = 0
            dCount = 0
            nCount = 0
            for row in range(y, y+3):
                if self.board[row][col] == offense:
                    oCount += 1
                elif self.board[row][col] == defense:
                    dCount += 1
                else:
                    nCount += 1
            
            if oCount == 2 and nCount == 1:
                tiar += 1
            if oCount == 1 and dCount == 2:
                prevent += 1
        return tiar, prevent

    def diagonalCount(self, y, x):
        if self.currPlayer:
            offense = self.maxPlayer
            defense = self.minPlayer
        else:
            offense = self.minPlayer
            defense = self.maxPlayer
        tiar = 0
        prevent = 0

        oCount = 0
        dCount = 0
        nCount = 0
        for row in range(0, 3):
            if self.board[y+row][x+row] == offense:
                oCount += 1
            elif self.board[y+row][x+row] == defense:
                dCount += 1
            else:
                nCount += 1
            
        if oCount == 2 and nCount == 1:
            tiar += 1
        if oCount == 1 and dCount == 2:
            prevent += 1
    
        oCount = 0
        dCount = 0
        nCount = 0
        for row in range(0, 3):
            if self.board[y+2-row][x+row] == offense:
                oCount += 1
            elif self.board[y+2-row][x+row] == defense:
                dCount += 1
            else:
                nCount += 1
            
        if oCount == 2 and nCount == 1:
            tiar += 1
        if oCount == 1 and dCount == 2:
            prevent += 1

        return tiar, prevent


    def countLocalTwoInARow(self, currBoardIdx):
        tiar = 0
        prevent = 0
        localIdx = self.globalIdx[currBoardIdx]
        y = localIdx[0]
        x = localIdx[1]
        
        t, p = self.horizontalCount(y,x)
        tiar += t
        prevent += p
        t, p = self.verticalCount(y,x)
        tiar += t
        prevent += p
        t, p = self.diagonalCount(y,x)
        tiar += t
        prevent += p
        return tiar, prevent



    def countCorners(self, currBoardIdx, isMax):
        symbol = self.maxPlayer
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

    # _________________________________________________________________



    def printGameBoard(self):
        """
        This function prints the current game board.
        """
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[:3]])+'\n')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[3:6]])+'\n')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[6:9]])+'\n')


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
        score=0
        
        self.printGameBoard()
        input(str(isMax) + "----->")
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
        movesLeft=True
        return movesLeft

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
        return 0

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
        bestValue=0.0
        values = []
        winner = self.checkLocalWinner(currBoardIdx)

        if winner and isMax:
            self.printGameBoard()
            input(str(winner) + "----->")
            return 10000
        if winner and not isMax:
            self.printGameBoard()
            input(str(winner) + "----->")
            return -10000
        
        if depth >= 3:
            return self.evaluatePredifined(isMax)
        
        currMoves = self.getLocalMoves(currBoardIdx)
        if not currMoves:
            return self.evaluatePredifined(isMax)
        
        for move in currMoves:
            self.drawToBoard(move, not isMax)
            currVal = self.minimax(depth+1,self.getBoardIdx(move), not isMax)
            self.removeFromBoard(move)
            values.append(currVal)

        if isMax:
            bestValue = max(values)
        else:
            bestValue = min(values)

        return bestValue

    def playGamePredifinedAgent(self,maxFirst,isMinimaxOffensive,isMinimaxDefensive):
        """
        This function implements the processes of the game of predifined offensive agent vs defensive agent.
        input args:
        maxFirst(bool): boolean variable indicates whether maxPlayer or minPlayer plays first.
                        True for maxPlayer plays first, and False for minPlayer plays first.
        isMinimaxOffensive(bool):boolean variable indicates whether it's using minimax or alpha-beta pruning algorithm for offensive agent.
                        True is minimax and False is alpha-beta.
        isMinimaxOffensive(bool):boolean variable indicates whether it's using minimax or alpha-beta pruning algorithm for defensive agent.
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
        self.currPlayer = maxFirst
        currBoardIdx = self.startBoardIdx
        currMoves = []
        currBestMove = None
        currBestValue = None
        isOffense = True

        for count in range(0,81):
            currMoves = self.getLocalMoves(currBoardIdx)
            if not currMoves:
                currMoves = self.getAllMoves()
                if not currMoves:
                    break
            
            currBestMove = currMoves[0]
            currBestValue = 0.0
            if isOffense:
                if isMinimaxOffensive:
                    # use minimax
                    for move in currMoves:
                        self.drawToBoard(move, self.currPlayer)
                        tryValue = self.minimax(1, self.getBoardIdx(move), True)
                        self.removeFromBoard(move)

                        if tryValue > currBestValue:
                            currBestMove = move
                            currBestValue = tryValue
                else:
                    # use alphabeta
                    break

            else:
                if isMinimaxDefensive:
                    # use minimax
                    for move in currMoves:
                        self.drawToBoard(move, self.currPlayer)
                        tryValue = self.minimax(1, self.getBoardIdx(move), True)
                        self.removeFromBoard(move)

                        if tryValue > currBestValue:
                            currBestMove = move
                            currBestValue = tryValue
                else:
                    # use alphabeta
                    break


            self.drawToBoard(currBestMove, self.currPlayer)
            bestMove.append(currBestMove)
            bestValue.append(currBestValue)
            gameBoards.append(self.board)
            
            winner = self.checkLocalWinner(currBoardIdx)
            if winner != 0:
                break
            currBoardIdx = self.getBoardIdx(currBestMove)
            isOffense = not isOffense
            self.currPlayer = not self.currPlayer
            self.printGameBoard()
            input(str(count) + "----->")


        self.printGameBoard()
        return gameBoards, bestMove, self.expandedNodes, bestValue, winner

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
    gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playGamePredifinedAgent(True,True,True)
    if winner == 1:
        print("The winner is maxPlayer!!!")
    elif winner == -1:
        print("The winner is minPlayer!!!")
    else:
        print("Tie. No winner:(")
