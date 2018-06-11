import numpy as np
import pygame
import random
import time
import sys
from makeMaze import *
import Monster

class maze:
    def __init__(self):
        self.score=0
        mazeWithStart = generateStart(maze)
        path = buildMaze(mazeWithStart[0], [mazeWithStart[1]])
        emptyMap = drawPath(mazeWithStart[0], path)
        self.map = generateMonsters(emptyMap, 3)
        self.monsters, self.monsterCoordinates = assignMonsters(self.map)

    def runGame(self, player):
        for iteration in range(500):
            action = player.perform(self)
            #Use action to perform movement/attack
            if checkFinished():
                self.score+=100
                return
            for monster in self.monsters:
                action = monster.play(self)
                #update map given action
            if checkFinished:
                return

    def assignMonsters(self, map):
        monsters=[]
        monsterCoordinates=[]
        for row in range(len(self.map)):
            for column in range(len(self.map[0])):
                if matrix[row][column] == 'M':
                    monsterCoordinates.append([row,column])
                    monsters.append(Monster)
        return monsters, monsterCoordinates

    def getDirections(self, monster):
        #directions = []
        coordinates = self.getMonsterLocation(monster)
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

    def getPlayerLocation(self, matrix):
        for row in range(len(self.map)):
            for column in range(len(self.map[0])):
                if matrix[row][column] == 'S':
                    return row, column

    def getScore(self):
        return self.score

    def checkSymbol(self, direction, steps, symbol):
        x,y = self.getPlayerLocation()
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
        return self.checkSymbol(direction, steps, "M")

    def checkExit(self, direction,steps):
        return self.checkSymbol(direction, steps, "E")

    def checkWall(self, direction,steps):
        return self.checkSymbol(direction, steps, "*")
