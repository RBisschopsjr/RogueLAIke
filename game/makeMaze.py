import numpy as np
import pygame
import random
import time
import sys

#Creates a numpy array of the specified size
def initGrid(n,m):
    return np.full((n,m), '*')

#Print function for the grid that is redundant
def printGrid(grid):
    print(grid)

#Adds a start token to the given grid argument. 
#Returns a new grid where the start is added and the coordinates of the start.
def generateStart(grid):
    circumference = grid.shape[0] + grid.shape[1] - 2
    #print("Circumference = ", circumference)
    startPoint = random.randint(1, circumference)
    startTuple = 0
    #print("Random generated number = ", startPoint)
    if(startPoint <= grid.shape[0]):
        #print("START on vertical wall")
        #print("StartPoint = ", startPoint)
        if(random.randint(1,2) is 1):
            startTuple = [startPoint - 1,0]
        else:            
            startTuple = [startPoint - 1,grid.shape[1] - 1]
    else:
        #print("START on horizontal wall")
        startPoint = startPoint - grid.shape[0]
        #print("StartPoint = ", startPoint)
        if(random.randint(1,2) is 1):
            startTuple = [0, startPoint]
        else:
            startTuple = [grid.shape[0] - 1, startPoint]
    grid[startTuple[0]][startTuple[1]] = 'S'
    return grid, startTuple

#Initial attempt of building a path in the given grid with a set length.
#This function is not used in the end implementation.
def buildPath(gridWithStart, pathLen):
    path = [gridWithStart[1]]
    #print("Start: ", path)
    maxDims = gridWithStart[0].shape
    #print("Dims: ", maxDims)
    for i in range(0, pathLen):
        path.append(step(maxDims,path))
    return path

#Second attempt for building a path through a given grid.
#Continues until no more steps are possible, this one is used in the eventual implementation.
#Returns a list of tuples where each tuple is a grid point that has to become a path.
def buildPath2(grid, path):
    #print("Start: ", path)
    maxDims = grid.shape
    #print("Dims: ", maxDims)
    stepCheck = True
    while(stepCheck):
        nextStep = step(maxDims, path)
        if(nextStep is None):
            stepCheck = False
        else:
            path.append(nextStep)
    return path

#Check to see if the current point 'el' falls outside the boundaries of a grid, given by 'gridDims'.
#Returns a boolean value.
def outsideGrid(el, gridDims):
    if(el[0] >= gridDims[0] or el[1] >= gridDims[1] or el[0] < 0 or el[1] < 0):
        #print("REMOVAL: ", el, " outside grid!")
        return True
    else:
        return False

#Check to see if th neighbor of the current point 'el' is part of the path.
#Returns a boolean value.
def neighborCheck(el, visited):
    prospectiveNBs = [[el[0]-1,el[1]], [el[0]+1,el[1]], [el[0],el[1]-1], [el[0],el[1]+1]]
    for nb in prospectiveNBs:
        if(nb in visited):
            #print("REMOVAL: ", el, ", ", nb, " found in path!")
            return True
    return False

#Step function that makes the next step in building a path.
#One such step consists of removing neighbors that do not pass the above two checks and then picking a random next point in the grid.
#This point is returned.
def step(gridDims, path):
    last = path[-1]
    visited = path[:-1]
    neighbors = [[last[0]-1,last[1]], [last[0]+1,last[1]], [last[0],last[1]-1], [last[0],last[1]+1]]
    endOptions = []
    #print("Initial candidates: ", neighbors)
    for el in neighbors:
        #print("Checking ", el, "...")
        if(not outsideGrid(el, gridDims) and not el in path and not neighborCheck(el, visited)):
            #print(el, " added to endOptions!")
            endOptions.append(el)
    #print("Candidates after pruning: ", endOptions)
    if(len(endOptions) is not 0):
        toAdd = random.choice(endOptions) 
        #print("Adding ", toAdd)
        return(toAdd)
    else:
        return None

#Draws the path given by buildPath2() in a grid. Also has the add monsters step where int 'nrOfMonsters' monsters are placed on random path points.
#Returns the maze as a matrix, x coordinate for exit, y coordinate for exit and list of monster coordinates in that order.
def drawPath(grid, path, nrOfMonsters):
    for el in path[0][1:]:
        grid[el[0],el[1]] = 'O'
    grid[path[1][0], path[1][1]] = 'E'
    del path[0][0]
    monsters = random.sample(path[0], nrOfMonsters)
    for mon in monsters:
        grid[mon[0], mon[1]] = 'M'
    return grid, path[1][0], path[1][1], monsters

#Function for creating the entire maze in a given grid.
#This function gets the grid and initial path, and then takes 2 steps where it adds noise to the grid in the form of random sidepaths.
#Each path point has a 90% chance to split in a new sidepath, also adds the endpoint of the maze.
#Returns the full list of all coordinate tuples that are path points in the grid, and the coordinates of the end point as a tuple.
def buildMaze(grid, path):
    allPaths = buildPath2(grid, path)
    endPoint = allPaths[-1]
    for i in range (1, len(allPaths)):
        el = allPaths[i]
        allPaths.append(el) 
        allPaths.remove(el)
        if(random.random() > 0.1):
            newPath = buildPath2(grid, allPaths)
            #print('New path added', newPath)
            allPaths = newPath
    for j in range (1, len(allPaths)):
        el = allPaths[j]
        allPaths.append(el) 
        allPaths.remove(el)
        newPath = buildPath2(grid, allPaths)
        #print('New path added', newPath)
        allPaths = newPath       
    return allPaths, endPoint
