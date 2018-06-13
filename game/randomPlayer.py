import random
import sys
import maze
import copy

class randomPlayer:
    #Type of player that performs an action to a random direction. If a monster
    #is in the direction, attack it. Else the player tries to move towards it.
    def __init__(self):
        self.directions = ["North", "East", "South", "West"]

    #Randomly do an action in a direction. If there is a monster
    # within 1 tile in the direction
    def perform(self,model):
        choice=random.randint(0,len(self.directions)-1)
        if self.directions[choice]=="North":
            if model.checkMonster("North",1):
                return "attackN"
            else:
                return "moveN"
        elif self.directions[choice]=="East":
            if model.checkMonster("East",1):
                return "attackE"
            else:
                return "moveE"
        elif self.directions[choice]=="South":
            if model.checkMonster("South",1):
                return "attackS"
            else:
                return "moveS"
        else:
            if model.checkMonster("West",1):
                return "attackW"
            else:
                return "moveW"

if __name__ == "__main__":
    randomPlayer = randomPlayer()
    maze = maze.maze()
    maze.runGame(randomPlayer)
