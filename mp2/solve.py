# -*- coding: utf-8 -*-

def add_pentomino(board, pent, coord):
    """
    Adds a pentomino pent to the board. The pentomino will be placed such that
    coord[0] is the lowest row index of the pent and coord[1] is the lowest 
    column index. 
    """

    for row in range(pent.shape[0]):
        for col in range(pent.shape[1]):
            if pent[row][col] != 0:
                if board[coord[0]+row][coord[1]+col] != 0: # Overlap
                    return False
                else:
                    board[coord[0]+row][coord[1]+col] = pent[row][col]
    return True
    
def remove_pentomino(board, pent_idx):
    board[board==pent_idx+1] = 0

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
    add_pentomino(board, pents[0], (0,0))
    print(board)
    print(pents[0])
    remove_pentomino(board, 0)
    print(board)
    return []
    # raise NotImplementedError