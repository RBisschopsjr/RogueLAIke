# -*- coding: utf-8 -*-
"""
Created on Thu May 24 14:28:13 2018

@author: Jake
"""
import numpy as np
import pygame
import random
import time
import sys
from makeMaze import *


def getPlayerLocation(matrix):
    #get begin point
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 'S':
                return i,j
            
def nextMove(matrix, value):
    #go North
    x,y = getPlayerLocation(matrix)
    if value < 0.25:
        return x+1,y
    #go East
    elif value >= 0.25 and value < 0.5:
        return x,y+1
    #go South
    elif value >= 0.5 and value < 0.75:
        return x-1,y
    #go West
    elif value >= 0.75:
        return x,y-1

def showMatrix(matrix):  
    time.sleep(0.5)
    print(matrix, end='\r')
    
    
def movement(matrix):
    done = False
    
    while done == False:
        rand = random.uniform(0,1)
        x,y = getPlayerLocation(matrix)
        x_new, y_new = nextMove(matrix,rand)
        
        try:
            if matrix[x_new][y_new] == 'E':
                print('Done!')
                done = True
            elif matrix[x_new][y_new] == 'O':
                matrix[x][y] = 'O'
                matrix[x_new][y_new] = 'S'
                showMatrix(matrix)
        except:
            showMatrix(matrix)
    
    
if __name__ == "__main__":
    maze = initGrid(10,8)
    print(maze)
    print("==========Initialized Grid==========")
    mazeWithStart = generateStart(maze)
    print(mazeWithStart[0])
    print("==========Added Start==========")
    path = buildMaze(mazeWithStart[0], [mazeWithStart[1]])
    mazeWithPath = drawPath(mazeWithStart[0], path, 3)
    print(mazeWithPath[0])
    print("==========Added Paths, Exit and Monsters==========")