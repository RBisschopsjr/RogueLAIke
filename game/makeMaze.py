import numpy as np
import pygame
import random
import time
import sys

def initGrid(n,m):
    return np.full((n,m), '*')

def printGrid(grid):
    print(grid)

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

def buildPath(gridWithStart, pathLen):
    path = [gridWithStart[1]]
    #print("Start: ", path)
    maxDims = gridWithStart[0].shape
    #print("Dims: ", maxDims)
    for i in range(0, pathLen):
        path.append(step(maxDims,path))
    return path

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

def outsideGrid(el, gridDims):
    if(el[0] >= gridDims[0] or el[1] >= gridDims[1] or el[0] < 0 or el[1] < 0):
        #print("REMOVAL: ", el, " outside grid!")
        return True
    else:
        return False

def neighborCheck(el, visited):
    prospectiveNBs = [[el[0]-1,el[1]], [el[0]+1,el[1]], [el[0],el[1]-1], [el[0],el[1]+1]]
    for nb in prospectiveNBs:
        if(nb in visited):
            #print("REMOVAL: ", el, ", ", nb, " found in path!")
            return True
    return False

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

def drawPath(grid, path):
    for el in path[0][1:]:
        grid[el[0],el[1]] = 'O'
    grid[path[1][0], path[1][1]] = 'E'
    return grid, path[1][0], path[1][1]

def generateMonsters(grid, amount):
    x,y = len(grid),len(grid[0])
    while amount is not 0:
        rx = random.randint(0,x)
        ry = random.randint(0,y)
        if grid[rx][ry] == 'O':
            grid[rx][ry] = 'M'
            amount-=1
    return grid

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