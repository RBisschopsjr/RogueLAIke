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
        self.map, y, x, self.monsterCoordinates = drawPath(mazeWithStart[0], path,0)
        self.monsters = self.assignMonsters(self.monsterCoordinates)
        self.exitCoordinates = [y,x]
        self.lastPlayerAction = ""

    def runGame(self, player):
        visitedCoordinates=[]
        for _ in range(500):
            y,x = self.getPlayerLocation()
            if not [y,x] in visitedCoordinates:
                visitedCoordinates.append([y,x])
            action = player.perform(self)
            #Use action to perform movement/attack
            self.performPlayerAction(action)
            if(self.score<-500):
                print(action)
            if self.checkFinished():
                return
            for monster in self.monsters:
                action = monster.play(self)
                #update map given action
                self.updateMap(monster, action)
                
            if self.checkFinished():
                return
        self.score+=10*len(visitedCoordinates)

    def runAndPrintGame(self, player):
        for _ in range(500):
            action = player.perform(self)
            #Use action to perform movement/attack
            self.performPlayerAction(action)
            if(self.score<-500):
                print(action)
            if self.checkFinished():
                return
            for monster in self.monsters:
                action = monster.play(self)
                #update map given action
                self.updateMap(monster, action)
                
            if self.checkFinished():
                return
            print(self.map)
        y,x = self.getPlayerLocation()
        self.score=float(self.score)-abs(y-self.exitCoordinates[0])*10-abs(x-self.exitCoordinates[1])*10
            
    #Assumes the player replaces the Exit node, thus leaving an "S" in the place of the "E"
    #If then the player is gone we can assume a monster killed it and the game is finished
    def checkFinished(self):
        y,x = self.getPlayerLocation()
        if x is None or y is None:
            self.score-=500
            return True
        elif y == self.exitCoordinates[0] and x == self.exitCoordinates[1]:
            self.score+=1000
            return True
        else:
            return False

    def updateMap(self, monster, action):
        y,x = self.getMonsterLocation(monster)[0], self.getMonsterLocation(monster)[1]
        if action == "moveN":
            self.setMonsterLocation(monster, y-1,x)
            self.map[y][x] = 'O'
            self.map[y-1][x] = 'M'
        elif action == "moveE":
            self.setMonsterLocation(monster, y,x+1)
            self.map[y][x] = 'O'
            self.map[y][x+1] = 'M'
        elif action == "moveS":
            self.setMonsterLocation(monster, y+1,x)
            self.map[y][x] = 'O'
            self.map[y+1][x] = 'M'
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
        directions = []
        coordinates = self.getMonsterLocation(monster)
        y = coordinates[0]
        x = coordinates[1]
        if not y-1<0:
            if not (self.map[y-1,x]=="*" or self.map[y-1,x]=="E" or self.map[y-1,x]=="M"):
                directions.append("moveN")

        if not x+1==self.map.shape[1]:
            if not (self.map[y,x+1]=="*" or self.map[y,x+1]=="E" or self.map[y,x+1]=="M"):
                directions.append("moveE")

        if not y+1==self.map.shape[0]:
            if not (self.map[y+1,x]=="*" or self.map[y+1,x]=="E" or self.map[y+1,x]=="M"):
                directions.append("moveS")

        if not x-1<0:
            if not (self.map[y,x-1]=="*" or self.map[y,x-1]=="E" or self.map[y,x-1]=="M"):
                directions.append("moveW")

        return directions
    
    def performPlayerAction(self,action):
        y,x = self.getPlayerLocation()
        if action=="attackN":
            if not y-1<0:
                if self.map[y-1,x]=="M":
                    self.removeMonster([y-1,x])
                else:
                    self.score-=1
            else:
                self.score-=1
        elif action=="attackE":
            if not x+1==self.map.shape[1]:
                if self.map[y,x+1]=="M":
                    self.removeMonster([y,x+1])
                else:
                    self.score-=1
            else:
                self.score-=1
        elif action=="attackS":
            if not y+1==self.map.shape[0]:
                if self.map[y+1,x]=="M":
                    self.removeMonster([y+1,x])
                else:
                    self.score-=1
            else:
                self.score-=1
        elif action=="attackW":
            if not x-1<0:
                if self.map[y,x-1]=="M":
                    self.removeMonster([y,x-1])
                else:
                    self.score-=1
            else:
                self.score-=1
                    
        elif action=="moveN":
            self.lastPlayerAction="North"
            if not y-1<0:
                if self.map[y-1,x]=="M":
                    self.map[y,x]="O"
                elif not self.map[y-1,x]=="*":
                    self.map[y-1,x]="S"
                    self.map[y,x]="O"
                    #self.score+=2
                else:
                    self.score-=1
            else:
                self.score-=1
        elif action=="moveE":
            self.lastPlayerAction="East"
            if not x+1==self.map.shape[1]:
                if self.map[y,x+1]=="M":
                    self.map[y,x]="O"
                elif not self.map[y,x+1]=="*":
                    self.map[y,x+1]="S"
                    self.map[y,x]="O"
                    #self.score+=2
                else:
                    self.score-=1
            else:
                self.score-=1
        elif action=="moveS":
            self.lastPlayerAction="South"
            if not y+1==self.map.shape[0]:
                if self.map[y+1,x]=="M":
                    self.map[y,x]="O"
                elif not self.map[y+1,x]=="*":
                    self.map[y+1,x]="S"
                    self.map[y,x]="O"
                    #self.score+=2
                else:
                    self.score-=1
            else:
                self.score-=1
        elif action=="moveW":
            self.lastPlayerAction="West"
            if not x-1<0:
                if self.map[y,x-1]=="M":
                    self.map[y,x]="O"
                elif not self.map[y,x-1]=="*":
                    self.map[y,x-1]="S"
                    self.map[y,x]="O"
                    #self.score+=2
                else:
                    self.score-=1
            else:
                self.score-=1
        elif action=="stop":
            self.score-=1

    def removeMonster(self, coordinates):
        index=self.monsterCoordinates.index(coordinates)
        self.monsterCoordinates.remove(coordinates)
        self.monsters.pop(index)
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
        return None, None

    def getScore(self):
        return self.score

    def checkSymbol(self, direction, steps, symbol):
        y,x = self.getPlayerLocation()
        if direction=="North":
            modx=0
            mody=-1
        elif direction=="East":
            modx=1
            mody=0
        elif direction=="South":
            modx=0
            mody=1
        else: #or direction is East
            modx=-1
            mody=0
        for step in range(steps):
            x+=modx
            y+=mody
            if x<0 or x==self.map.shape[1] or y<0 or y==self.map.shape[0]:
                if symbol=="*":
                    return True
                else:
                    return False
            if self.map[y][x]==symbol:
                return True
            if self.map[y][x]=="*": #We are looking at a wall, and the wall
                #is not our target. Thus it is false.
                return False
        return False

    def checkMonster(self, direction,steps):
        return self.checkSymbol(direction, steps, "M")

    def checkExit(self, direction,steps):
        return self.checkSymbol(direction, steps, "E")

    def checkWall(self, direction,steps):
        return self.checkSymbol(direction, steps, "*")

    def getLastPlayerAction(self):
        return self.lastPlayerAction
