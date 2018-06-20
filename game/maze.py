import numpy as np
import pygame
import random
import time
import sys
from makeMaze import *
from Monster import *

global stepScore, wrongStepScore, monsterScore, exitScore, deathScore, wrongAttack, numOfMonsters, gridSize
gridSize = [10,10]
numOfMonsters = 3

walkScore = 2
monsterScore = 50
exitScore = 1000

wrongStepScore = -1
wrongAttack = -20
deathScore = -100

class maze:
    def __init__(self):
        global numOfMonsters, gridSize
        self.score=0
        grid = initGrid(gridSize[0],gridSize[1])
        mazeWithStart = generateStart(grid)
        path = buildMaze(mazeWithStart[0], [mazeWithStart[1]])
        self.map, y, x, self.monsterCoordinates = drawPath(mazeWithStart[0], path,numOfMonsters)
        self.monsters = self.assignMonsters(self.monsterCoordinates)
        self.exitCoordinates = [y,x]
        self.lastPlayerAction = ""

    #Runs the game: let the player make the first move during a turn, then each monster.
    # End game when player reached exit or is finished.
    def runGame(self, player):
        for _ in range(500):
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
                return

    #Runs the game: let the player make the first move during a turn, then each monster.
    # End game when player reached exit or is finished. Print the maze per turn.
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

            
    #Assumes the player replaces the Exit node, thus leaving an "S" in the place of the "E"
    #If then the player is gone we can assume a monster killed it and the game is finished
    def checkFinished(self):
        global deathScore, exitScore
        y,x = self.getPlayerLocation()
        if x is None or y is None:
            self.score += deathScore
            return True
        elif y == self.exitCoordinates[0] and x == self.exitCoordinates[1]:
            self.score += exitScore
            return True
        else:
            return False

    #Updates the map given the action of monster.
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

    #Assign monster objects to each monster coordinate.
    def assignMonsters(self, monsterCoordinates):
        monsters=[]
        for monster in monsterCoordinates:
            monsters.append(Monster())
        return monsters

    #Gets all possible directions for a monster to move towards to. If there is a wall or a monster or out of bounds,
    # that action is not possible.
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

    #Performs the action that the player indicated he wanted to perform. For attacks,
    #check if a monster got killed and assign score accordingly.
    def performPlayerAction(self,action):
        global monsterScore, walkScore, wrongStepScore, wrongAttack
        y,x = self.getPlayerLocation()
        monsters_killed = 0
        if action=="attack":
            if y > 0:
                if self.map[y-1,x]=="M":
                    self.removeMonster([y-1,x])
                    monsters_killed+=1
            if y < len(self.map)-1:
                if self.map[y+1,x]=="M":
                    self.removeMonster([y+1,x])
                    monsters_killed+=1
            if x > 0:
                if self.map[y,x-1]=="M":
                    self.removeMonster([y,x-1])
                    monsters_killed+=1
            if x < len(self.map)-1:
                if self.map[y,x+1]=="M":
                    self.removeMonster([y,x+1])
                    monsters_killed+=1
                
            if monsters_killed > 0:
                self.score+=monsters_killed*monsterScore
            else:
                self.score+=wrongAttack
        elif action=="moveN":
            self.lastPlayerAction="North"
            if not y-1<0:
                if self.map[y-1,x]=="M":
                    self.map[y,x]="O"
                elif not self.map[y-1,x]=="*":
                    self.score+=walkScore
                    self.map[y-1,x]="S"
                    self.map[y,x]="O"
                else:
                    self.score+=wrongStepScore
            else:
                self.score-=1
        elif action=="moveE":
            self.lastPlayerAction="East"
            if not x+1==self.map.shape[1]:
                if self.map[y,x+1]=="M":
                    self.map[y,x]="O"
                elif not self.map[y,x+1]=="*":
                    self.score+=walkScore
                    self.map[y,x+1]="S"
                    self.map[y,x]="O"  
                else:
                    self.score+=wrongStepScore
            else:
                self.score-=1
        elif action=="moveS":
            self.lastPlayerAction="South"
            if not y+1==self.map.shape[0]:
                if self.map[y+1,x]=="M":
                    self.map[y,x]="O"
                elif not self.map[y+1,x]=="*":  
                    self.score+=walkScore
                    self.map[y+1,x]="S"
                    self.map[y,x]="O"
                else:
                    self.score+=wrongStepScore
            else:
                self.score-=1
        elif action=="moveW":
            self.lastPlayerAction="West"
            if not x-1<0:
                if self.map[y,x-1]=="M":
                    self.map[y,x]="O"
                elif not self.map[y,x-1]=="*":
                    self.score+=walkScore
                    self.map[y,x-1]="S"
                    self.map[y,x]="O"
                else:
                    self.score+=wrongStepScore
            else:
                self.score+=wrongStepScore
        elif action=="stop":
            self.score+=wrongStepScore

    #Remove the monster at a set coordinates from the game.
    def removeMonster(self, coordinates):
        index=self.monsterCoordinates.index(coordinates)
        self.monsterCoordinates.remove(coordinates)
        self.monsters.pop(index)
        self.map[coordinates[0], coordinates[1]] = 'O'

    # Get the coordinates of a given monster.
    def getMonsterLocation(self, monster):
        index = self.monsters.index(monster)
        return self.monsterCoordinates[index]
    
    # Set the coordinates of a monster.
    def setMonsterLocation(self, monster, y, x):
        index = self.monsters.index(monster)
        self.monsterCoordinates[index][0] = y
        self.monsterCoordinates[index][1] = x

    # Get the coordinates of where the player is.
    def getPlayerLocation(self):
        for row in range(len(self.map)):
            for column in range(len(self.map[0])):
                if self.map[row][column] == 'S':
                    return row, column
        return None, None

    # Get the game score.
    def getScore(self):
        return self.score

    #Check if a certain symbol is present in steps in a given direction.
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
            
        x+=modx*steps
        y+=mody*steps
        if x<0 or x>=self.map.shape[1] or y<0 or y>=self.map.shape[0]:
            if symbol=="*":
                return True
            else:
                return False
        if self.map[y][x]==symbol:
            return True
        return False

    #Check if a monster is in a direction in steps.
    def checkMonster(self, direction,steps):
        return self.checkSymbol(direction, steps, "M")

    #Check if an exit is in a direction in steps.
    def checkExit(self, direction,steps):
        return self.checkSymbol(direction, steps, "E")

    #Check if an open space is in a direction in steps.
    def checkSpace(self, direction,steps):
        return self.checkSymbol(direction, steps, "O")

    #Get the last action the player performed.
    def getLastPlayerAction(self):
        return self.lastPlayerAction
