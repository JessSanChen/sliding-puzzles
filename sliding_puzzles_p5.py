# Search Algorithms on Sliding Puzzles: Part 1
# 3/15/2020

# Fully successful BFS implementation

from collections import deque
import time

def convert_to_coord(index, size):
    #convert from index to xy coord
    x = index % size
    y = int(index / size)
    return x, y


def convert_to_index(coord, size):
    #convert from xy coord to index
    x = coord[0]
    y = coord[1]
    index = size * y + x
    return index


def print_puzzle(board, size):
    for vertical in range(size):
        for horizontal in range(size):
            print(board[horizontal + (size * vertical)], end=" ")
        print()


def find_goal(board, size):  # confused about array v strings
    temp = []
    for num in range(len(board)):
        if board[num] == '.':
            temp = list(board[:num] + board[num + 1:])
            break
    temp.sort()
    temp.append(".")
    goal = ''.join((map(str, temp)))
    return goal

def global_directions(size):
  return {"up":int(-size),"down":size,"right":1,"left":-1}

def swap(board,start,final,size):
  array = list(board)
  temp = array[final]
  array[final] = array[start]
  array[start] = temp
  return "".join(array)

def read_line(board,size,direction,children):
    dirs = global_directions(size)
    startIndex = board.index(".")
    startCoord = convert_to_coord(startIndex,size) 
    finalIndex = startIndex + dirs.get(direction)
    finalCoord = convert_to_coord(finalIndex,size)
    status = False # checks for feasibility of swap
    if -1<finalIndex<(size*size): 
        if direction == "left" or direction =="right": 
            if finalCoord[1] == startCoord[1]:
                status = True
        elif direction == "down" or direction =="up":
            status = True
    if status == True:
        newBoard = swap(board,startIndex,finalIndex,size)
        result = (newBoard,direction)
        children.add(result)
    """
    if direction == "left":
        origin = size-startCoord[0]
    elif direction == "right":
        origin = startCoord[0]+1
    elif direction == "down":
        origin = startCoord[1]+1
    elif direction == "up":
        origin = size-startCoord[1]
    currentBoard = board
    for step in range(1, origin):
        finalIndex = startIndex + dirs.get(direction)
        newBoard = swap(currentBoard,startIndex,finalIndex,size)
        result = (newBoard,direction+" %s" %(step))
        children.add(result)
        currentBoard = newBoard
        startIndex = finalIndex
    """

def get_children(board, size):
    children = set()
    read_line(board,size,"right",children)
    read_line(board,size,"left",children)
    read_line(board,size,"down",children)
    read_line(board,size,"up",children)
    return children # children is set of tuples (result, direction)

def dfs(board,size):
    # returns all states achievable from goal state
    # each node is a tuple with (node, its parent)
    sourceNode = (find_goal(board,size),None,None)
    visited = set() # what we want
    stack = deque()
    # visit source node and mark visited
    stack.append(sourceNode[0])
    visitedChildOnly = set()
    visitedChildOnly.add(sourceNode[0])
    visited.add(sourceNode)
    while len(stack)>0:
        # take the front state of queue and move off queue
        graph = stack.popleft()
        # visit and mark non-visited children
        children = set(get_children(graph,size))
        for child in children: # a child is (board,direction)
            if child[0] not in visitedChildOnly: 
                stack.append(child[0])
                visitedChildOnly.add(child[0])
                newNode = (child[0],graph,child[1])
                visited.add(newNode) # node is (board,parent,dir)
    return visited

def getPath(board,size):
    # prints path from board to goal state
    path = []
    # first = (board,"Start")
    # path.append(first)
    allNodes = dfs(board,size) # returns all nodes
    allNodesFirstOnly = [x[0] for x in allNodes]
    dictionary = dict(zip(allNodesFirstOnly,allNodes))
    child = dictionary.get(board)
    while child[1] is not None: # stops for-loop at source node
        parent = child[1]
        direction = child[2]
        child = dictionary.get(parent)
        total = (child[0],direction) # tuple of board,dir
        path.append(total)
    return path

with open("slide_puzzle_tests.txt") as f:
    lineNum = 0
    for line in f:
        line = line.strip()
        size = int(line[0])
        board = line[2:len(line)]
        lineNum += 1

        """
        print("line " +str(lineNum))
        print_puzzle(board,size)
        children = get_children(board,size)
        for child in children:
            print(child[1])
            print_puzzle(child[0],size)
        """
        if lineNum < 6:
            start = time.perf_counter()
            print("Line: " +str(lineNum),end=": ")
            print("Board: " + board,end=", ")
            path = getPath(board,size)
            print(str(len(path))+" moves found in",end=" ")

            end = time.perf_counter()
            print("%s seconds" % (end-start))

        """
            print("Path: ")
            for x in path:
                print(x[1])
                print_puzzle(x[0],size)
        """
