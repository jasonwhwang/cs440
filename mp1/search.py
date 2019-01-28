# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018
# Modified by Rahul Kunji (rahulsk2@illinois.edu) on 01/16/2019

"""
This is the main entry point for MP1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""


# Search should return the path and the number of states explored.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# Number of states explored should be a number.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,greedy,astar)

# Node data structure
class Node:
	node_xy = None
	parent_node = None
	children_nodes = None
	depth = None


def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "dfs": dfs,
        "greedy": greedy,
        "astar": astar,
    }.get(searchMethod)(maze)


def dfs(maze):
    stack = []
    explored = []
    path = []
    neighbors = []
    findInProgress = True
    obj = maze.getObjectives()

    curr = Node()
    curr.node_xy = maze.getStart()
    curr.parent_node = None
    curr.children_nodes = []
    curr.depth = 0
    stack.append(curr)

    #find token
    while findInProgress:
        curr = stack.pop()
        explored.append(curr)

        for goal in obj:
            if curr.node_xy == goal:
                findInProgress = False
                break

        neighbors = maze.getNeighbors(curr.node_xy[0], curr.node_xy[1])
        for potential_child_node in neighbors:
            if maze.isValidMove(potential_child_node[0], potential_child_node[1]):
                new_node = Node()
                new_node.node_xy = potential_child_node
                new_node.parent_node = curr
                new_node.children_nodes = []
                new_node.depth = curr.depth + 1
                if new_node in explored:
                    continue
                else:
                    curr.children_nodes.append(new_node)
        for stackNode in curr.children_nodes:
            stack.append(stackNode)

    #set path
    while curr.node_xy != maze.getStart():
        path.append(curr.node_xy)
        curr = curr.parent_node
    #reverse path
    path.reverse()
    return path, len(explored)



def bfs(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    return [], 0


def greedy(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    return [], 0


def astar(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    return [], 0