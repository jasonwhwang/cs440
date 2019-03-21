# -*- coding: utf-8 -*-
import numpy as np


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

def get_pent_idx(pent):
    """
    Returns the index of a pentomino.
    """
    pidx = 0
    for i in range(pent.shape[0]):
        for j in range(pent.shape[1]):
            if pent[i][j] != 0:
                pidx = pent[i][j]
                break
        if pidx != 0:
            break
    if pidx == 0:
        return -1
    return pidx - 1

def sol_list(board,pents):
    list = []
    for p in pents:
        idx = get_pent_idx(p)+1
        board_copy = np.copy(board)
        board_copy[board_copy ==idx] = 0
        wow,loc = place(board_copy,p)
        list.append((wow,loc))
    return list

def place(board,pent):
    orient = allOrients(pent)
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            for z in orient:
                if(can_add_pentomino(board,z,(i,j))):
                    add_pentomino(board,z,(i,j))
                    return (z,(i,j))

def add_pentomino(board, pent, coord):
    """
    Adds a pentomino pent to the board. The pentomino will be placed such that
    coord[0] is the lowest row index of the pent and coord[1] is the lowest
    column index.
    """
    for row in range(len(pent)):
        for col in range(len(pent[0])):
            if pent[row][col] != 0:
                board[coord[0]+row][coord[1]+col] = pent[row][col]
    return True


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

def allPositions(board,pent):
    positions = []
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            orient = allOrients(pent)
            for z in orient:
                if(can_add_pentomino(board,z,(i,j))):
                    board_copy = np.copy(board)
                    add_pentomino(board_copy,z,(i,j))
                    board_copy[board_copy>0] =1
                    positions.append(np.reshape(board_copy,board.shape[0]*board.shape[1]))
    return positions


def exact_cover(A,depth):
    # If matrix has no columns, terminate successfully.
    depth+=1
    if A.shape[1] == 1:
        print("*****")
        sol = []
        sol.append("*")
        return sol
    else:
        # Choose a column c with the fewest 1s.
        #c = A.sum(axis=0)
        vals = np.count_nonzero(A,axis=0)
        c = vals.argmin()
        if(np.sum(A[:,c], axis=0)==0):
            return [":("]

        # For each row r such that A[r,c] = 1,
        r = []
        for L in range(A.shape[0]):
            if(A[L][c]>0):
                r.append(A[L])
        for r in r:
            # For each column j such that A[r,j] = 1,
            B = A
            cols = []
            rows = []
            for i in range(len(r)):
                if(i==len(r)-1):
                    continue
                if r[i]> 0:
                    cols.append(i)
            if(cols):
                for j in cols:
                    # Delete each row i such that A[i,j] = 1
                    for x in range(A[:,j].shape[0]):
                        if(A[x][j]>0):
                            rows.append(x)
                    #B = np.delete(B, list, 0)
                    # then delete column j.
                    #if(B.shape[0]>0):
                        #B = np.delete(B, B[j],1)
            B = np.delete(B,rows,0)
            B = np.delete(B,cols,1)
            sol = exact_cover(B,depth)
            if(sol[0]=="*"):
                sol.append(r)
                return sol
    return [":("]


def solve(board, pents):
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
    board = board-1
    flat_board = np.reshape(board,board.shape[0]*board.shape[1])
    rows = []
    size = board.shape[0]*board.shape[1]
    count =0
    for i, P in enumerate(pents):
        for A in allPositions(board,P):
            A = np.append(A, np.zeros(len(pents)+1, dtype='int'))
            A[size + i] = i+2
            A[size+len(pents)] = count
            count+=1
            rows.append(list(A))
    mat = np.array(rows, dtype="int")
    answer = exact_cover(mat,0)
    del answer[0]
    for i in range(len(answer)):
        pent=0
        for j in range(len(answer[i])):
            if(j==len(answer[i])-1):
                num = answer[i][j]
                gg = rows[num]
                for wow in range(size):
                    if(gg[wow]==1):
                        flat_board[wow] = pent
            else:
                if(answer[i][j]>1):
                    pent = answer[i][j]-1
    sol = np.reshape(flat_board,(board.shape[0],board.shape[1]))
    sol = np.array(sol,dtype=int)
    print(sol)
    listy = sol_list(sol,pents)
    print(listy)
    new_board = np.zeros(board.shape)
    return listy
    #covers = np.array(list(exact_cover(A,sol)), dtype='int')
    #np.savetxt('exact-covers.csv', covers, delimiter=',', fmt='%d')