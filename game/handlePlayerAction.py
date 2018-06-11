    def performPlayerAction(self,action):
        x,y = self.getPlayerLocation()
        if action=="attackN":
            if self.map[x,y+1]=="M":
                self.removeMonster(x,y+1)
        elif action=="attackE":
            if self.map[x+1,y]=="M":
                self.removeMonster(x+1,y)
        elif action=="attackS":
            if self.map[x,y-1]=="M":
                self.removeMonster(x,y-1)
        elif action=="attackW":
            if self.map[x-1,y]=="M":
                self.removeMonster(x-1,y)
                
        elif action=="moveN":
            if self.map[x,y+1]=="M":
                self.map[x,y]="0"
            elif not self.map[x,y+1]=="*":
                self.map[x,y+1]="S"
                self.map[x,y]="0"
        elif action=="moveE":
            if self.map[x+1,y]=="M":
                self.map[x,y]="0"
            elif not self.map[x+1,y]=="*":
                self.map[x+1,y]="S"
                self.map[x,y]="0"
        elif action=="moveS":
            if self.map[x,y-1]=="M":
                self.map[x,y]="0"
            elif not self.map[x,y-1]=="*":
                self.map[x,y-1]="S"
                self.map[x,y]="0"
        elif action=="moveS":
            if self.map[x,y-1]=="M":
                self.map[x,y]="0"
            elif not self.map[x,y-1]=="*":
                self.map[x,y+1]="S"
                self.map[x,y]="0"
