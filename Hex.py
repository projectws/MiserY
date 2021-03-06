__author__ = 'Arnaud'
import numpy as np
import random
class Hex:
    def __init__(self,index,level):
        self.index=index
        self.neighbors=[]
        self.color="EMPTY"
        self.side=[]
        self.sideconnected=[]
        self.level=level
    def getColor(self):
        return self.color
    def changeColor(self,newcolor):
        self.color=newcolor
    def getNeighbors(self):
        return self.neighbors
    def addNeighbors(self,newneigh):
        self.neighbors.append(newneigh)
    def getSide(self):
        return self.side
    def addSide(self,side):
        self.side.append(side)
        self.sideconnected.append(side)
    def getSideConnected(self):
	return self.sideconnected
    def isSide(self,side):
        if side in self.side:
            return True
        else:
            return False
    def getLevel(self):
        return self.level

def minindexlevel(level):
    return 1+level*(level-1)/2

def maxindexlevel(level):
    return level+(level*(level-1)/2)

def findneighbors(hex,N):
    level=hex.getLevel()
    index=hex.index
    neighindex=[]

    if minindexlevel(level)<=index-1<=maxindexlevel(level):
        neighindex.append(index-1)
    if minindexlevel(level)<=index+1<=maxindexlevel(level):
        neighindex.append(index+1)

    if level-1>0:
        if minindexlevel(level-1)<=index-(level)<=maxindexlevel(level-1):
            neighindex.append(index-(level))
        if minindexlevel(level-1)<=index-(level)+1<=maxindexlevel(level-1):
            neighindex.append(index-(level)+1)
    if level+1<N+1:
        if minindexlevel(level+1)<=index+(level)<=maxindexlevel(level+1):
            neighindex.append(index+(level))
        if minindexlevel(level+1)<=index+(level)+1<=maxindexlevel(level+1):
            neighindex.append(index+(level)+1)
    return neighindex

def findpath(hex,board):
        for neigh in hex.getNeighbors():
            if neigh.getColor()==hex.getColor(): 
                for side in neigh.sideconnected:
                    hex.sideconnected.append(side)
        shrink=[]
        if 1 in hex.sideconnected:
            shrink.append(1)
        if 2 in hex.sideconnected:
            shrink.append(2)
        if 3 in hex.sideconnected:
            shrink.append(3)
        hex.sideconnected=shrink

def update_board(board,N):
    for i in range(N):
        for hex in board.values():
            if hex.getColor()!="EMPTY":
                findpath(hex,board)
                if 1 in hex.sideconnected and 2 in hex.sideconnected and 3 in hex.sideconnected:
                    return True,hex.getColor()
    return False,"EMPTY"

def willLose(board, computerColor, index, N):
	update_board(board,N)
	hex = board[index]
	sides = []
	for neigh in hex.getNeighbors():
		if neigh.getColor() == computerColor:
			sides.extend(neigh.getSideConnected())
	sides.extend(hex.getSide())
	sides = set(sides)
	return (1 in sides) and (2 in sides) and (3 in sides)

def createBoard(N):
    board={}
    index=1

    for i in range(1,N+1):
        for j in range(1,i+1):

            newhex=Hex(index,i)
            if j==1:
                side=1
                newhex.addSide(side)
            if j==i:
                side=2
                newhex.addSide(side)
            if i==N:
                side=3
                newhex.addSide(side)
            board[newhex.index]=newhex
            index=index+1

    for hex in board.values():
        neighborsindex=findneighbors(hex,N)
        for index in neighborsindex:
            hex.addNeighbors(board[index])

    return board

def createCornerStack(corner,N):
        #create the list of indexes from a corner, along parallel lines from this corner
	tiles = []
	if corner == 1:
		#corresponds to index 1
		tiles = range(1,N*(N+1)/2 + 1)
	elif corner == 2:
		#corresponds to index N(N+1)/2 - N+1
		for l in range(0,N):
			s = len(tiles)
			for i in range(0,l):
				tiles.append(tiles[s-i-1]+1)
			tiles.append((N-l)*(N-l+1)/2 - (N-l)+ 1) #we are at level N-l
	elif corner == 3:
		#corresponds to index N(N+1)/2
		for l in range(0,N):
			s = len(tiles)
			for i in range(0,l):
				tiles.append(tiles[s-i-1]-1)
			tiles.append((N-l)*(N-l+1)/2) #we are at level N-l
	print tiles
	return tiles

def chooseCorner(board, computerColor, N):
	#we check if there is already a corner played by the computer
	corner = 1
	cornerStack = createCornerStack(corner,N)
	while board[cornerStack[0]].getColor() != computerColor and corner < 3:
		corner = corner + 1
		cornerStack = createCornerStack(corner,N)
	#if not: choose an empty corner
	if board[cornerStack[0]].getColor() != computerColor:
		corner = 1
		cornerStack = createCornerStack(corner,N)
		while board[cornerStack[0]].getColor() != "EMPTY" and corner < 3:
			corner = corner + 1
			cornerStack = createCornerStack(corner,N)
	print 'Chosen corner: ', corner
	return cornerStack

def findNextEmpty(board, cornerStack, N):
        #it finds the indext of the next empty tile
	index = 0
	hex = board[cornerStack[index]]
	while hex.getColor() != "EMPTY" and index < N*(N+1)/2 - 1:
		index = index + 1
		hex = board[cornerStack[index]]	
	return cornerStack[index]

def findEmptyNonLosing(board, cornerStack, N, computerColor):
        #constructs the list of non-losing possible moves
	possibleMoves = []
	for i in cornerStack:
		hex = board[i]
		if hex.getColor()=="EMPTY" and not willLose(board, computerColor, i, N):
			possibleMoves.append(i)
	return possibleMoves

def findFirstOnSide(board, positions):
        #returns the first index in list positions whose tile is on a side of the board
	for i in positions:
		if len(board[i].getSide())>0:
			return i
	return 0

def nextmove(board,computercolor,N):
	cornerStack = chooseCorner(board, computercolor, N)
	#compute the possible non-losing moves
	possibleMoves = findEmptyNonLosing(board, cornerStack, N, computercolor)
	if len(possibleMoves)==0:
                #if we lose, we chose the first non-empty tile
		index = findNextEmpty(board, cornerStack, N)
	else:
                #we try to find a non-losing move on a side
		moveOnSide = findFirstOnSide(board,possibleMoves)
		if moveOnSide == 0:
                        #if there is no non-losing move on a side, we take the first non-losing move
			index = possibleMoves[0]
		else:
			index = moveOnSide

	hex = board[index]
	losing = willLose(board, computercolor, index, N)	
	print 'Index ', index, ' will lose: ', losing		     
	hex.changeColor(computercolor)
	return hex
