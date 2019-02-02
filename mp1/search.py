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

from queue import Queue
from collections import deque
from dataclasses import dataclass, field
from typing import Any
from math import sqrt

@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any=field(compare=False)

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
    #data structures
    stack = []
    explored = dict()
    path = []
    neighbors = []
    findInProgress = True
    maxCounter = 0
    obj = maze.getObjectives()

    #initialize start/root node
    curr = Node()
    curr.node_xy = maze.getStart()
    curr.parent_node = None
    curr.children_nodes = []
    curr.depth = 0
    stack.append(curr)

    #traverse maze and find token
    while findInProgress and maxCounter < 100000:
        #pop stack and add current node to explored
        curr = stack.pop()
        explored[curr.node_xy] = curr

        #if node is goal, token found, exit loop
        for goal in obj:
            if curr.node_xy == goal:
                findInProgress = False
                break

        #else get the neighbors for the current node
        #if the neighbor is a valid move and has not been explored, add to stack
        neighbors = maze.getNeighbors(curr.node_xy[0], curr.node_xy[1])
        for potential_child_node in neighbors:
            if maze.isValidMove(potential_child_node[0], potential_child_node[1]):
                if potential_child_node in explored:
                    continue
                else:
                    new_node = Node()
                    new_node.node_xy = potential_child_node
                    new_node.parent_node = curr
                    new_node.children_nodes = []
                    new_node.depth = curr.depth + 1
                    curr.children_nodes.append(new_node)
        
        #add all children nodes to the stack
        for stackNode in curr.children_nodes:
            stack.append(stackNode)
        #increment counter to prevent infinite looping
        maxCounter += 1

    #path has been found, so chart path starting from goal
    while curr.node_xy != maze.getStart():
        path.append(curr.node_xy)
        curr = curr.parent_node
    #reverse path to start from root node
    path.reverse()
    return path, len(explored)


def bfs(maze):
    #data structures
    queue = Queue(maxsize=0)
    explored = dict()
    path = []
    neighbors = []
    findInProgress = True
    maxCounter = 0
    obj = maze.getObjectives()

    #initialize start/root node
    curr = Node()
    curr.node_xy = maze.getStart()
    curr.parent_node = None
    curr.children_nodes = []
    curr.depth = 0
    queue.put(curr)

    #traverse maze and find token, maxCounter number of loops to prevent infinite search
    while findInProgress and maxCounter < 1000000:
        #pop queue and add current node to explored
        curr = queue.get()
        explored[curr.node_xy] = curr

        #if node is goal, token found, exit loop
        for goal in obj:
            if curr.node_xy == goal:
                findInProgress = False
                break

        #else get the neighbors for the current node
        #if the neighbor is a valid move and has not been explored, add to queue
        neighbors = maze.getNeighbors(curr.node_xy[0], curr.node_xy[1])
        for potential_child_node in neighbors:
            if maze.isValidMove(potential_child_node[0], potential_child_node[1]):
                if potential_child_node in explored:
                    continue
                else:
                    new_node = Node()
                    new_node.node_xy = potential_child_node
                    new_node.parent_node = curr
                    new_node.children_nodes = []
                    new_node.depth = curr.depth + 1
                    curr.children_nodes.append(new_node)
        
        #add all children nodes to the queue
        for queueNode in curr.children_nodes:
            queue.put(queueNode)
        #increment counter to prevent infinite looping
        maxCounter += 1

    #path has been found, so chart path starting from goal
    while curr.node_xy != maze.getStart():
        path.append(curr.node_xy)
        curr = curr.parent_node
    #reverse path to start from root node
    path.reverse()
    return path, len(explored)


def greedy(maze):
    #data structures
    queue = deque([])
    explored = dict()
    path = []
    neighbors = []
    findInProgress = True
    maxCounter = 0
    obj = maze.getObjectives()
    goalList = []
    currGoal = None
    distance = 0
    nodeTuple = None

    #initialize start/root node
    curr = Node()
    curr.node_xy = maze.getStart()
    curr.parent_node = None
    curr.children_nodes = []
    curr.depth = 0
    queue.append(PrioritizedItem(0,curr))

    #traverse maze and find token, maxCounter number of loops to prevent infinite search
    while findInProgress and maxCounter < 10000:
        #pop queue and add current node to explored
        curr = queue.popleft().item
        explored[curr.node_xy] = curr

        #Sort Goals by their distance to the current location
        #if node is goal, token found, exit loop
        for goal in obj:
            distance = abs(curr.node_xy[0]-goal[0]) + abs(curr.node_xy[1]-goal[1])
            goalList.append( PrioritizedItem(distance, goal) )
            if curr.node_xy == goal:
                findInProgress = False
                break
        goalList = sorted(goalList)
        currGoal = goalList[0].item
        goalList = []

        #else get the neighbors for the current node
        #if the neighbor is a valid move and has not been explored, add to queue
        neighbors = maze.getNeighbors(curr.node_xy[0], curr.node_xy[1])
        for potential_child_node in neighbors:
            if maze.isValidMove(potential_child_node[0], potential_child_node[1]):
                if potential_child_node in explored:
                    continue
                else:
                    new_node = Node()
                    new_node.node_xy = potential_child_node
                    new_node.parent_node = curr
                    new_node.children_nodes = []
                    new_node.depth = curr.depth + 1

                    distance = abs(potential_child_node[0]-currGoal[0]) + abs(potential_child_node[1]-currGoal[1])
                    nodeTuple = PrioritizedItem(distance, new_node)
                    curr.children_nodes.append( nodeTuple )
        
        #add all children nodes to the queue
        curr.children_nodes = sorted(curr.children_nodes)
        for queueNode in curr.children_nodes:
            queue.append(queueNode)
        temp = list(queue)
        temp = sorted(temp)
        queue = deque(temp)

        #increment counter to prevent infinite looping
        maxCounter += 1

    #path has been found, so chart path starting from goal
    while curr.node_xy != maze.getStart():
        path.append(curr.node_xy)
        curr = curr.parent_node
    #reverse path to start from root node
    path.reverse()
    return path, len(explored)

def astarS(maze):
    #**********SINGLE TOKEN ASTAR**********#

    #data structures
    queue = deque([])
    explored = dict()
    path = []
    neighbors = []
    findInProgress = True
    maxCounter = 0
    obj = maze.getObjectives()
    start = maze.getStart()
    goalList = []
    currGoal = None
    distance = 0
    nodeTuple = None

    #initialize start/root node
    curr = Node()
    curr.node_xy = maze.getStart()
    curr.parent_node = None
    curr.children_nodes = []
    curr.depth = 0
    queue.append(PrioritizedItem(0,curr))

    #traverse maze and find token, maxCounter number of loops to prevent infinite search
    while findInProgress and maxCounter < 10000:
        #pop queue and add current node to explored
        curr = queue.popleft().item
        explored[curr.node_xy] = curr

        #Sort Goals by their distance to the current location
        #if node is goal, token found, exit loop
        for goal in obj:
            distance = abs(curr.node_xy[0]-goal[0]) + abs(curr.node_xy[1]-goal[1])
            goalList.append( PrioritizedItem(distance, goal) )
            if curr.node_xy == goal:
                findInProgress = False
                break
        goalList = sorted(goalList)
        currGoal = goalList[0].item
        goalList = []

        #else get the neighbors for the current node
        #if the neighbor is a valid move and has not been explored, add to queue
        neighbors = maze.getNeighbors(curr.node_xy[0], curr.node_xy[1])
        for potential_child_node in neighbors:
            if maze.isValidMove(potential_child_node[0], potential_child_node[1]):
                if potential_child_node in explored:
                    continue
                else:
                    new_node = Node()
                    new_node.node_xy = potential_child_node
                    new_node.parent_node = curr
                    new_node.children_nodes = []
                    new_node.depth = curr.depth + 1
                    distance = sqrt(abs(potential_child_node[0]-currGoal[0])**2 + abs(potential_child_node[1]-currGoal[1])**2)
                    distance += sqrt(abs(start[0]-potential_child_node[0])**2 + abs(start[1]-potential_child_node[1])**2)
                    nodeTuple = PrioritizedItem(distance, new_node)
                    curr.children_nodes.append( nodeTuple )
        
        #add all children nodes to the queue
        for queueNode in curr.children_nodes:
            queue.append(queueNode)
        temp = list(queue)
        temp = sorted(temp)
        queue = deque(temp)

        #increment counter to prevent infinite looping
        maxCounter += 1

    #path has been found, so chart path starting from goal
    while curr.node_xy != maze.getStart():
        path.append(curr.node_xy)
        curr = curr.parent_node
    #reverse path to start from root node
    path.reverse()
    return path, len(explored)

# AStarNode data structure
class AStarNode:
	node_xy = None
	parent_node = None
	children_nodes = None
	distance = None

#*** Change function name to "astar" to test***#
def astar(maze):
    # *** MULTIPLE TOKENS *** #

    # get start and objectives
    curr = maze.getStart()
    objectives = maze.getObjectives()
    objectivesCount = len(objectives)
    objectivesOrder = []
    points = []
    explored = []
    smallestNode = None
    smallestDistance = None
    path = []
    newPath = []
    exploredSum = 0

    points.append(curr)
    for obj in objectives:
        points.append(obj)

    # find distance between start and all objectives in the maze
    edges = dict()
    pointsLength = len(points)
    for i in range(0, pointsLength-1, 1):
        for j in range(i+1, pointsLength, 1):
            distance = astarDistance(maze, points[i], points[j])
            edges[(points[i], points[j])] = distance
            edges[(points[j], points[i])] = distance
    
    # use astar to find the shortest path between all tokens in the maze
    # Nearest Neighbor Algorithm: https://en.wikipedia.org/wiki/Nearest_neighbour_algorithm
    # Used to solve traveling salesman problems, in our case collecting all tokens problem
    while len(objectivesOrder) < objectivesCount:
        explored.append(curr)
        # starting from "Start", find the objective not in the explored list with the smallest distance
        # once found, add that objective to explored and to objectivesOrder
        for obj in objectives:
            if curr == obj:
                continue
            elif obj in explored:
                continue
            elif smallestNode == None:
                smallestNode = obj
                smallestDistance = edges[curr, obj]
            elif edges[curr, obj] < smallestDistance:
                smallestNode = obj
                smallestDistance = edges[curr, obj]
        
        objectivesOrder.append((curr, smallestNode))
        curr = smallestNode
        smallestNode = None
        smallestDistance = 0
    
    # print(objectivesOrder)
    for nodePath in objectivesOrder:
        newPath = astarPath(maze, nodePath[0], nodePath[1])
        # print(newPath)
        for everyPath in newPath[0]:
            path.append(everyPath)
        exploredSum += exploredSum + newPath[1]
    print(path)
    return path, exploredSum

# Distance between points in maze
def astarDistance(maze, start, end):
    #data structures
    queue = deque([])
    explored = dict()
    neighbors = []
    findInProgress = True
    nodeTuple = None

    #initialize start/root node
    curr = Node()
    curr.node_xy = start
    curr.parent_node = None
    curr.children_nodes = []
    curr.depth = 0
    queue.append(PrioritizedItem(0,curr))

    #traverse maze and find token, maxCounter number of loops to prevent infinite search
    while findInProgress:
        #pop queue and add current node to explored
        curr = queue.popleft().item
        explored[curr.node_xy] = curr

        if curr.node_xy == end:
            findInProgress = False
            break

        #else get the neighbors for the current node
        #if the neighbor is a valid move and has not been explored, add to queue
        neighbors = maze.getNeighbors(curr.node_xy[0], curr.node_xy[1])
        for potential_child_node in neighbors:
            if maze.isValidMove(potential_child_node[0], potential_child_node[1]):
                if potential_child_node in explored:
                    continue
                else:
                    new_node = Node()
                    new_node.node_xy = potential_child_node
                    new_node.parent_node = curr
                    new_node.children_nodes = []
                    new_node.depth = curr.depth + 1
                    distance = sqrt(abs(potential_child_node[0]-end[0])**2 + abs(potential_child_node[1]-end[1])**2)
                    distance += sqrt(abs(start[0]-potential_child_node[0])**2 + abs(start[1]-potential_child_node[1])**2)
                    nodeTuple = PrioritizedItem(distance, new_node)
                    curr.children_nodes.append( nodeTuple )
        
        #add all children nodes to the queue
        for queueNode in curr.children_nodes:
            queue.append(queueNode)
        temp = list(queue)
        temp = sorted(temp)
        queue = deque(temp)

    return curr.depth


    # Path between points in maze
def astarPath(maze, start, end):
    #data structures
    queue = deque([])
    explored = dict()
    neighbors = []
    path = []
    findInProgress = True
    nodeTuple = None

    #initialize start/root node
    curr = Node()
    curr.node_xy = start
    curr.parent_node = None
    curr.children_nodes = []
    curr.depth = 0
    queue.append(PrioritizedItem(0,curr))

    #traverse maze and find token, maxCounter number of loops to prevent infinite search
    while findInProgress:
        #pop queue and add current node to explored
        curr = queue.popleft().item
        explored[curr.node_xy] = curr

        if curr.node_xy == end:
            findInProgress = False
            break

        #else get the neighbors for the current node
        #if the neighbor is a valid move and has not been explored, add to queue
        neighbors = maze.getNeighbors(curr.node_xy[0], curr.node_xy[1])
        for potential_child_node in neighbors:
            if maze.isValidMove(potential_child_node[0], potential_child_node[1]):
                if potential_child_node in explored:
                    continue
                else:
                    new_node = Node()
                    new_node.node_xy = potential_child_node
                    new_node.parent_node = curr
                    new_node.children_nodes = []
                    new_node.depth = curr.depth + 1
                    distance = sqrt(abs(potential_child_node[0]-end[0])**2 + abs(potential_child_node[1]-end[1])**2)
                    distance += sqrt(abs(start[0]-potential_child_node[0])**2 + abs(start[1]-potential_child_node[1])**2)
                    nodeTuple = PrioritizedItem(distance, new_node)
                    curr.children_nodes.append( nodeTuple )
        
        #add all children nodes to the queue
        for queueNode in curr.children_nodes:
            queue.append(queueNode)
        temp = list(queue)
        temp = sorted(temp)
        queue = deque(temp)

    #path has been found, so chart path starting from goal
    while curr.node_xy != start:
        path.append(curr.node_xy)
        curr = curr.parent_node
    #reverse path to start from root node
    path.reverse()
    return path, len(explored)

# return path, num_states_explored