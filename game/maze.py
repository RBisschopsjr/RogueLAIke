import numpy as np
import pygame
import random
import time
import sys
from makeMaze import *

class maze:
    def __init__(self):
        self.score=0
        mazeWithStart = generateStart(maze)
        path = buildMaze(mazeWithStart[0], [mazeWithStart[1]])
        self.map = drawPath(mazeWithStart[0], path)
        self.monsters = generateMonsters(self.map, 3)
        self.monsterCoordinates = [] #TODO: map monsters to their location. Best done at same time, so that monster at index 1 has the coordinates at index 1

    def play(self, player):
        print("TODO")
    

    def getDirections(self, monster):
        directions = []
        coordinates = getMonsterLocation(monster)
        x = coordinates[0]
        y = coordinates[1]
        if not self.map[x,y+1]=="*":
            coordinates.append("moveN")
        if not self.map[x+1,y]=="*":
            coordinates.append("moveE")
        if not self.map[x,y-1]=="*":
            coordinates.append("moveS")
        if not self.map[x-1,y+1]=="*":
            coordinates.append("moveW")
        return coordinates

    def removeMonster(self, coordinates): #TODO: when monster is defeated, remove it and its index.
        print('hoi')

    def getMonsterLocation(monster):
        index = self.monsters.index(monster)
        return self.monsterCoordinates[index]

    def getPlayerLocation(self):
        for row in range(len(self.map)):
            for column in range(len(self.map[0])):
                if matrix[row][column] == 'S':
                    return row, column

    def getScore(self):
        return self.score

    def checkSymbol(self, direction, steps, symbol):
        x,y = getPlayerLocation()
        if direction=="North":
            modx=0
            mody=1
        elif direction=="East":
            modx=1
            mody=0
        elif direction=="South":
            modx=0
            mody=-1
        else: #or direction is East
            modx=-1
            mody=0
        for step in range(steps):
            x+=modx
            y+=mody
            if self.map[x][y]==symbol:
                return True
        return False

    def checkMonster(self, direction,steps):
        return checkSymbol(direction, steps, "M")

    def checkExit(self, direction,steps):
        return checkSymbol(direction, steps, "E")

    def checkWall(self, direction,steps):
        return checkSymbol(direction, steps, "*")
