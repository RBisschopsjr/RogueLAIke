# -*- coding: utf-8 -*-
"""
Created on Thu May 24 14:28:13 2018

@author: Jake
"""
import numpy as np
import pygame
import random


def ascii_2_matrix(file):
    fp = open(file)
    lines = fp.readlines()
    matrix = []
    for i in range(0,len(lines)):
        chars = [word.strip() for word in lines[i].split(',') if word.strip()]
        matrix.append(chars)
    return matrix

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
    print(matrix)
    
    
def movement(matrix):
    done = False
    
    while done == False:
        rand = random.uniform(0,1)
        x,y = getPlayerLocation(matrix)
        x_new, y_new = nextMove(matrix,rand)
        
        if matrix[x_new][y_new] == 'E':
            print('Done!')
            done = True
        elif matrix[x_new][y_new] == 'O':
            matrix[x][y] = 'O'
            matrix[x_new][y_new] = 'S'
            showMatrix(matrix)
        else:
            showMatrix(matrix)
            break
    
    
if __name__ == "__main__":
    matrix = ascii_2_matrix('testMaze01.txt')
    movement(matrix)