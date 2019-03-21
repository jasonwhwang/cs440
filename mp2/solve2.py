# -*- coding: utf-8 -*-
import numpy as np
import math
def get_pent_idx(pent):
    """
    Returns the index of a pentomino.
    """
    pidx = 0
    for i in range(len(pent)):
        for j in range(len(pent[0])):
            if pent[i][j] != 0:
                pidx = pent[i][j]
                break
        if pidx != 0:
            break
    if pidx == 0:
        return -1
    return pidx - 1


def can_add_pentomino(board, pent, coord):
    """
    Adds a pentomino pent to the board. The pentomino will be placed such that
    coord[0] is the lowest row index of the pent and coord[1] is the lowest 
    column index. 
    """
    for row in range(len(pent)):
        for col in range(len(pent[0])):
            if pent[row][col] != 0:
                if coord[0]+row >= board.shape[0] or coord[1]+col >= board.shape[1]:
                    return False
                if board[coord[0]+row][coord[1]+col] != 0:  # Overlap
                    return False
    return True


def add_pentomino(board, pent, coord):
    """
    Adds a pentomino pent to the board. The pentomino will be placed such that
    coord[0] is the lowest row index of the pent and coord[1] is the lowest 
    column index. 
    """
    for row in range(len(pent)):
        for col in range(len(pent[0])):
            if pent[row][col] != 0:
                if coord[0]+row >= board.shape[0] or coord[1]+col >= board.shape[1]:
                    remove_pentomino(board, get_pent_idx(pent))
                    return False
                if board[coord[0]+row][coord[1]+col] != 0:  # Overlap
                    remove_pentomino(board, get_pent_idx(pent))
                    return False
                else:
                    board[coord[0]+row][coord[1]+col] = pent[row][col]
    return True

def remove_pentomino(board, pent_idx):
    board[board == pent_idx+1] = 0


def LRV_update(board,pents,LRV):
    for y in range(board.shape[0]):
        for x in range(board.shape[1]):
            for p in pents:
                orient = allOrients(p)
                for z in orient:
                    if(can_add_pentomino(board,z,(y,x))):    #and check_if_filled(board,z,(y,x))):
                        idx = getNum(z) -1
                        LRV[idx] +=1
    return LRV

def find_next(board,pents):
    for y in range(board.shape[0]):
        for x in range(board.shape[1]):
            if(board[y][x]==0):
                return (y,x)
    return False

def getNum(pent):
    for i in range(pent.shape[0]):
        for j in range(pent.shape[1]):
            if(pent[i][j]>0):
                return pent[i][j]

def check_if_filled(board, pent, coor):
    add_pentomino(board, pent, coor)
    if board[coor[0]][coor[1]] != 0:
        remove_pentomino(board, get_pent_idx(pent))
        return True
    else:
        remove_pentomino(board, get_pent_idx(pent))
        return False


def removePent(pents, pent):
    p = []
    for pt in pents:
        if get_pent_idx(pt) != get_pent_idx(pent):
            p.append(pt)
    return p

def numVals(board,pents,coor):
    num = 0
    i,j = coor
    for p in pents:
        orient = allOrients(p)
        for z in orient:
            if(can_add_pentomino(board,z,coor)): #and check_if_filled(board,z,coor)):
                num+=1
    return (num,i,j)

def allPositions(board,pent):
    positions = []
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            orient = allOrients(pent)
            bool = False
            for x in orient:
                if(can_add_pentomino(board,x,(i,j))):
                    bool = True
            if(bool):
                positions.append((i,j))
    return positions    

def allOrients(pent):
    seen = []
    ret = []
    for flip in range(2):
        for rotate in range(4):
            if pent.tolist() not in seen:
                seen.append(pent.tolist())
                ret.append(pent)
            pent = np.rot90(pent)
        pent = np.flip(pent,1)
    return ret

import time
solution = []

def removePentFromSolution(pent):
    global solution
    p = []
    for pt in solution:
        if get_pent_idx(pt[0]) != get_pent_idx(pent):
            p.append(pt)
    solution = p
    return
count = 0
def checkHoles(board,pents):
    visited = np.zeros(board.shape)
    for i in range(visited.shape[0]):
        for j in range(visited.shape[1]):
            if(board[i][j]==0 and not visited[i][j]):
                global count
                count = 0
                DFS(board,(i,j),visited)
                if(count <5):
                    return True
    return False
def DFS(board,coor,visited):
    global count
    count+=1
    rowNbr = [-1,0,0,1]
    colNbr = [0,-1,1,0]
    i,j = coor
    visited[i][j] = 1
    for k in range(4):
        if(isSafe((i + rowNbr[k],j+colNbr[k]),visited,board)):
            DFS(board,(i + rowNbr[k],j+colNbr[k]),visited)


def isSafe(coor,visited,board):
    return(coor[0]>=0 and coor[1]>=0
     and coor[0]<board.shape[0] and coor[1]<board.shape[1]
     and board[coor[0]][coor[1]]==0 and not visited[coor[0]][coor[1]])

def boardSolve(board, pents,tried,size):
    if(len(pents)==0):
        return True
    if(checkHoles(board,pents)):
        return False        
    global solution
    # print(board)
    #pents_copy = pents.copy()
    LRV = np.zeros(size)
    LRV = LRV_update(board,pents,LRV)
    for i in range(tried.size):
        if(tried[i] ==1):
            LRV[i] = 999
        if(LRV[i] ==0):
            return False
    # print(LRV)
    idx = np.argmin(LRV)
    for p in pents:
        if(getNum(p)-1 == idx ):
            positions = allPositions(board,p)
            ordered = np.zeros((len(positions),3),dtype = int)
            for i in range(len(positions)):
                ordered[i]= numVals(board,pents,positions[i])
            from operator import itemgetter
            ordered = sorted(ordered,key = itemgetter(0))
            for z in range(len(ordered)):
                i = ordered[z][1]
                j = ordered[z][2]
                amt = ordered[z][0]
                orients = allOrients(p)
                for x in orients:
                    if(can_add_pentomino(board,x,(i,j))):
                        add_pentomino(board,x,(i,j))
                        pents = removePent(pents,x)
                        solution.append((x,(i,j)))
                        tried[idx] = 1
                        if(boardSolve(board,pents,tried,size)):
                            return True
                        else:
                            tried[idx] = 0
                            remove_pentomino(board,get_pent_idx(x))
                            pents.append(x)
                            removePentFromSolution(x)

    
    return False

def solve(board, pents):
    board = board - 1
    size = len(pents)
    tried = np.zeros(len(pents))
    boardSolve(board, pents,tried,size)
    global solution
    print(board)
    return solution






def solveOG(board, pents):
    count = 0           # Used to prevent infinte looping
    board = board-1     # flip board to 0s and -1s
    usedPents = []      # keep track of all pents used, if all used board is solved
    currStack = []      # stack of pent being tested
    stack = []          # stack of the entire board
    sol = []            # keeps track of the current nodes
    coor = (0, 0)       # keeps track of (y,x) location on board
    inProgress = True   # break loop when done

    # 1. INITIALIZE STACK
    # - Initialize stack, starting at coord (y=0, x=0)
    # - Go through all coordinates on the board
    # - Try all possible pents that can fill the coordinate
    # - Combinations include roations and reflections
    for pent in pents:
        p = pent
        for rotate in range(0, 4):
            if can_add_pentomino(board, p, coor) and check_if_filled(board, p, coor) and (p.tolist(), coor) not in stack:
                stack.append((p.tolist(), coor))
            p = np.rot90(p)
        p = np.flip(p, 1)
        for rotate in range(0, 4):
            if can_add_pentomino(board, p, coor) and check_if_filled(board, p, coor) and (p.tolist(), coor) not in stack:
                stack.append((p.tolist(), coor))
            p = np.rot90(p)

    # 2. Start Loop
    # - Pop off block off stack and add to Current Solution (sol)
    # - Add current solution to the board and used pents
    # - Find next empty coordinate and find pents
    while count < 10  and inProgress:
        curr = stack.pop()

        if get_pent_idx(curr[0]) in usedPents:
            continue

        sol.append(curr)
        add_pentomino(board, curr[0], curr[1])
        usedPents.append(get_pent_idx(curr[0]))
        coor = find_next(board, pents)

        if len(sol) == len(pents):
            print("HIT CHECK")
            break
        #     if check_correctness(sol, board, pents):
        #         inProgress = False
        #         break

        # if count == 29:
        #     print(board)
        #     print(usedPents)
        #     print(curr[1])
            # for block in stack:
            #     print(block[1])
            #     print(np.array(block[0]))

        # 3. Find Pents
        # - Repeat steps as in the initialize stack step
        for pent in pents:
            if get_pent_idx(pent) not in usedPents:
                p = pent
                for rotate in range(0, 4):
                    if can_add_pentomino(board, p, coor) and check_if_filled(board, p, coor) and (p.tolist(), coor) not in currStack:
                        currStack.append((p.tolist(), coor))
                    p = np.rot90(p)
                p = np.flip(p, 1)
                for rotate in range(0, 4):
                    if can_add_pentomino(board, p, coor) and check_if_filled(board, p, coor) and (p.tolist(), coor) not in currStack:
                        currStack.append((p.tolist(), coor))
                    p = np.rot90(p)
        # 4. Add to Stack/Backtrack
        # - Append additional pent options to stack
        # - If no options, backtrack
        if currStack:
            stack += currStack
            currStack = []
        else:
            remove_pentomino(board, get_pent_idx(curr[0]))
            usedPents.remove(get_pent_idx(curr[0]))

            # 5. Remove Solution
            # - Remove curr pent from solution
            # - If removed solution's coordinate is different from the coordinate of the next solution
            #   then all possible pents for that solution stack have been tried, so remove pent
            #   and try the next pent on the stack
            popSol = sol.pop()
            
            if len(stack)-1 >= 0 and popSol[1] != stack[len(stack)-1][1]:
                removeSol = sol.pop()
                # print(np.array(removeSol[0]))
                remove_pentomino(board, get_pent_idx(removeSol[0]))
                usedPents.remove(get_pent_idx(removeSol[0]))

        count += 1

    print(board)
    # print(usedPents)
    new_list = [x+1 for x in usedPents]
    print(new_list)
    print(curr[1])
    # for block in stack:
    #     print(block[1])
    #     print(np.array(block[0]))

    retSol = []
    for block in sol:
        retSol.append((np.array(block[0]), block[1]))

    return retSol
    # raise NotImplementedError

def check_correctness(sol_list, board, pents):
    """
    Sol is a list of pentominos (possibly rotated) and their upper left coordinate
    """
    # All tiles used
    if len(sol_list) != len(pents):
        return False
    # Construct board
    sol_board = np.zeros(board.shape)
    seen_pents = [0]*len(pents)
    for pent, coord in sol_list:
        pidx = get_pent_idx(pent)
        if seen_pents[pidx] != 0:
            return False
        else:
            seen_pents[pidx] = 1
        if not add_pentomino(sol_board, pent, coord):
            return False

    # Check same number of squares occupied
    if np.count_nonzero(board) != np.count_nonzero(sol_board):
        return False
    # Check overlap
    if np.count_nonzero(board) != np.count_nonzero(np.multiply(board, sol_board)):
        return False

    return True

    """
    This is the function you will implement. It will take in a numpy array of the board
    as well as a list of n tiles in the form of numpy arrays. The solution returned
    is of the form [(p1, (row1, col1))...(pn,  (rown, coln))]
    where pi is a tile (may be rotated or flipped), and (rowi, coli) is 
    the coordinate of the upper left corner of pi in the board (lowest row and column index 
    that the tile covers).
    
    -Use np.flip and np.rot90 to manipulate pentominos.
    
    -You can assume there will always be a solution.
    """