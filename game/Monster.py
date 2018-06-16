import random

class Monster:
    
    def __init__(self):
        self.memory=""
        
    # Tell the game what action we take during our turn. Do a random action that
    # does not undo the action we made last turn, unless we can only do that action (deadend)
    def play(self, game):
        directions = game.getDirections(self)
        if len(directions)==1:
            self.memory=directions[0]
            #print(directions[0])
            return directions[0]
        elif len(directions)==0:
            return "stop"
        else:
            bannedAction= self.getReverseAction(self.memory)
            decisionInt = random.randint(0,len(directions)-1)
            action = directions[decisionInt]
            while action==bannedAction:
                decisionInt = random.randint(0,len(directions)-1)
                action = directions[decisionInt]
            self.memory= action
            #print(action)
            return action

    # Get the opposite action from the direction
    def getReverseAction(self,direction):
        if direction == "moveN":
            return "moveS"
        if direction == "moveE":
            return "moveW"
        if direction == "moveS":
            return "moveN"
        if direction == "moveW":
            return "moveE"
