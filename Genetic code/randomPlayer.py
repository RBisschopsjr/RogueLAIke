import random

class randomPlayer:
    def __init__(self):
        self.directions = ["North", "East", "South", "West"]

    #Randomly do an action in a direction. If there is a monster
    # within 1 tile in the direction
    def perform(self,model):
        choice=random.randint(0,len(self.directions))
        if self.directions[choice]=="North":
            if model.checkMonster("North",1):
                return "attackN"
            else:
                return "moveN"
        elif:
            if model.checkMonster("East",1):
                return "attackE"
            else:
                return "moveE"
        elif:
            if model.checkMonster("South",1):
                return "attackS"
            else:
                return "moveS"
        else:
            if model.checkMonster("West",1):
                return "attackW"
            else:
                return "moveW"
