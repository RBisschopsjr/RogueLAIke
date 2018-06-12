import numpy as np
import pygame
import random
import time
import sys
from makeMaze import *
from Monster import *

class maze:
    def __init__(self):
        self.score=0
        grid = initGrid(10,10)
        mazeWithStart = generateStart(grid)
        path = buildMaze(mazeWithStart[0], [mazeWithStart[1]])
        self.map, y, x, self.monsterCoordinates = drawPath(mazeWithStart[0], path,3)
        self.monsters = self.assignMonsters(self.monsterCoordinates)
        print(self.map[0][1])
        self.exitCoordinates = [y,x]

    def runGame(self, player):
        for iteration in range(500):
            print(self.map)
            action = player.perform(self)
            #Use action to perform movement/attack
            self.performPlayerAction(action)
            
            if self.checkFinished():
                return
            for monster in self.monsters:
                action = monster.play(self)
                #update map given action
                self.updateMap(monster, action)
                
            if self.checkFinished():
                print(self.map)
                return
            self.score-=1
            print("hi")
        print("500 rounds")
            
    #Assumes the player replaces the Exit node, thus leaving an "S" in the place of the "E"
    #If then the player is gone we can assume a monster killed it and the game is finished
    def checkFinished(self):
        y,x = self.getPlayerLocation()
        if y == self.exitCoordinates[0] and x == self.exitCoordinates[1]:
            print("Hello")
            self.score+=100
            return True
        elif x is None or y is None:
            self.score-=50
            return True
        else:
            return False

    def updateMap(self, monster, action):
        y,x = self.getMonsterLocation(monster)[0], self.getMonsterLocation(monster)[1]
        if action == "moveN":
            self.setMonsterLocation(monster, y+1,x)
            self.map[y][x] = 'O'
            self.map[y][x+1] = 'M'
        elif action == "moveE":
            self.setMonsterLocation(monster, y,x+1)
            self.map[y][x] = 'O'
            self.map[y][x+1] = 'M'
        elif action == "moveS":
            self.setMonsterLocation(monster, y-1,x)
            self.map[y][x] = 'O'
            self.map[y-1][x] = 'M'
        elif action == "moveW":
            self.setMonsterLocation(monster, y,x-1)
            self.map[y][x] = 'O'
            self.map[y][x-1] = 'M'
        
    def assignMonsters(self, monsterCoordinates):
        monsters=[]
        for monster in monsterCoordinates:
            monsters.append(Monster())
        return monsters

    def getDirections(self, monster):
        #directions = []
        coordinates = self.getMonsterLocation(monster)
        y = coordinates[0]
        x = coordinates[1]
        try:
            if not self.map[y+1,x]=="*" or self.map[y+1,x]=="E":
                coordinates.append("moveN")
        except:
            pass
        try:
            if not self.map[y,x+1]=="*" or self.map[y,x+1]=="E":
                coordinates.append("moveE")
        except:
            pass
        try:
            if not self.map[y-1,x]=="*" or self.map[y-1,x]=="E":
                coordinates.append("moveS")
        except:
            pass
        try:
            if not self.map[y,x-1]=="*" or self.map[y,x-1]=="E":
                coordinates.append("moveW")
        except:
            pass
        return coordinates
    
    def performPlayerAction(self,action):
        y,x = self.getPlayerLocation()
        if action=="attackN":
            if self.map[y,x+1]=="M":
                self.removeMonster(y+1,x)
        elif action=="attackE":
            if self.map[y+1,x]=="M":
                self.removeMonster(y,x+1)
        elif action=="attackS":
            if self.map[y,x-1]=="M":
                self.removeMonster(y-1,x)
        elif action=="attackW":
            if self.map[y-1,x]=="M":
                self.removeMonster(y,x-1)
                
        elif action=="moveN":
            if self.map[y+1,x]=="M":
                self.map[y,x]="0"
            elif not self.map[y+1,x]=="*":
                self.map[y+1,x]="S"
                self.map[y,x]="0"
        elif action=="moveE":
            if self.map[y,x+1]=="M":
                self.map[y,x]="0"
            elif not self.map[y,x+1]=="*":
                self.map[y+1,x]="S"
                self.map[y,x]="0"
        elif action=="moveS":
            if self.map[y-1,x]=="M":
                self.map[y,x]="0"
            elif not self.map[y-1,x]=="*":
                self.map[y-1,x]="S"
                self.map[y,x]="0"
        elif action=="moveW":
            if self.map[y,x-1]=="M":
                self.map[y,x]="0"
            elif not self.map[y,x-1]=="*":
                self.map[y,x-1]="S"
                self.map[y,x]="0"


    def removeMonster(self, monster, coordinates):
        self.monsters.remove(monster)
        self.monsterCoordinates.remove(coordinates)
        self.map[coordinates[0], coordinates[1]] = 'O'
        self.score+=10

    def getMonsterLocation(self, monster):
        index = self.monsters.index(monster)
        return self.monsterCoordinates[index]
    
    def setMonsterLocation(self, monster, y, x):
        index = self.monsters.index(monster)
        self.monsterCoordinates[index][0] = y
        self.monsterCoordinates[index][1] = x

    def getPlayerLocation(self):
        for row in range(len(self.map)):
            for column in range(len(self.map[0])):
                if self.map[row][column] == 'S':
                    return row, column

    def getScore(self):
        return self.score

    def checkSymbol(self, direction, steps, symbol):
        y,x = self.getPlayerLocation()
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
            try:
                if self.map[y][x]==symbol:
                    return True
            except:
                if symbol=="*":
                    return True
        return False

    def checkMonster(self, direction,steps):
        return self.checkSymbol(direction, steps, "M")

    def checkExit(self, direction,steps):
        return self.checkSymbol(direction, steps, "E")

    def checkWall(self, direction,steps):
        return self.checkSymbol(direction, steps, "*")
