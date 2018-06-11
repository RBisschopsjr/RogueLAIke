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
        emptyMap, x, y = drawPath(mazeWithStart[0], path)
        self.map = generateMonsters(emptyMap, 3)
        self.monsters, self.monsterCoordinates = self.assignMonsters(self.map)
        self.exitCoordinates = [x,y]

    def runGame(self, player):
        for iteration in range(500):
            action = player.perform(self)
            #Use action to perform movement/attack
            if self.checkFinished():
                self.score+=100
                return
            for monster in self.monsters:
                action = monster.play(self)
                #update map given action
                self.updateMap(monster, action)
                
            if self.checkFinished:
                return
            
    #Assumes the player replaces the Exit node, thus leaving an "S" in the place of the "E"
    #If then the player is gone we can assume a monster killed it and the game is finished
    def checkFinished(self):
        x,y = self.getPlayerLocation()
        if x == self.exitCoordinates[0] and y == self.exitCoordinates[1]:
            return True, "Won"
        elif x is None or y is None:
            return True, "Loss"
        else:
            return False

    def updateMap(self, monster, action):
        x,y = self.getMonsterLocation(monster)[0], self.getMonsterLocation(monster)[1]
        if action == "moveN":
            self.setMonsterLocation(monster, x+1,y)
            self.map[x][y] = 'O'
            self.map[x+1][y] = 'M'
        elif action == "moveE":
            self.setMonsterLocation(monster, x,y+1)
            self.map[x][y] = 'O'
            self.map[x][y+1] = 'M'
        elif action == "moveS":
            self.setMonsterLocation(monster, x-1,y)
            self.map[x][y] = 'O'
            self.map[x-1][y] = 'M'
        elif action == "moveW":
            self.setMonsterLocation(monster, x,y-1)
            self.map[x][y] = 'O'
            self.map[x][y-1] = 'M'
        
    def assignMonsters(self):
        monsters=[]
        monsterCoordinates=[]
        for row in range(len(self.map)):
            for column in range(len(self.map[0])):
                if self.map[row][column] == 'M':
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

    def removeMonster(self, monster, coordinates):
        self.monsters.remove(monster)
        self.monsterCoordinates.remove(coordinates)
        self.map[coordinates[0], coordinates[1]] = 'O'

    def getMonsterLocation(self, monster):
        index = self.monsters.index(monster)
        return self.monsterCoordinates[index]
    
    def setMonsterLocation(self, monster, x, y):
        index = self.monsters.index(monster)
        self.monsterCoordinates[index][0] = x
        self.monsterCoordinates[index][0] = y

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
