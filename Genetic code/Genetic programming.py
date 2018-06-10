import random

global actions
global considerations
global mutationRate
actions = ["moveN", "moveE", "moveS", "moveW",
           "attackN", "attackE", "attackS", "attackN",
           "stop"] #All actions possible in the game.
considerations = []
mutationRate=0.05 #Chance that a given branch or leaf mutates.

#Class that considers if there is an monster in n steps. Part of strategy pattern for consideration
class monsterConsideration:
    def __init__(self,direction, steps):
        self.direction=direction
        self.steps=steps

    #Check the game if there is a monster with a certain amount of steps.
    def decide(model):
        model.checkMonster(direction,steps)

    #Print out what the consideration exactly is.
    def printItself():
        print "Monster "
        print self.steps
        print " "
        print self.direction

#Class that considers if there is an wall in n steps. Part of strategy pattern for consideration
class wallConsideration:
    def __init__(self,direction, steps):
        self.direction=direction
        self.steps=steps

    #Check the game if there is a wall with a certain amount of steps.
    def decide(model):
        model.checkWall(direction,steps)

    #Print out what the consideration exactly is.
    def printItself():
        print "wall "
        print self.steps
        print " "
        print self.direction

#Class that considers if there is an exit in n steps. Part of strategy pattern for consideration
class exitConsideration:
    def __init__(self,direction, steps):
        self.direction=direction
        self.steps=steps

    #Check the game if there is an exit with a certain amount of steps.
    def decide(model):
        model.checkExit(direction,steps)

    #Print out what the consideration exactly is.
    def printItself():
        print "exit "
        print self.steps
        print " "
        print self.direction

#The Genetic Program structure. It contains a left branch and right branch, both which can be a branch or a leaf. For the game, the first branch is the player.
class Branch:
    def __init__(self, consider, left, right):
        self.consider=consider
        self.left=left
        self.right=right

    #Return a copy of this tree.
    def clone(self):
        return self.deepcopy()

    #Do an action given the decision of our consideration.
    def perform(self,model):
        if self.consider.decide(model):
            self.left.perform(model)
        else:
            self.right.perform(model)

    #Print the tree: show the actions of left and right, and the consideration in this branch.
    def printTree(self):
        self.left.printTree()
        self.consider.printItself()
        self.right.printTree()

    #Returns the size of the tree: size of left+ size of right+itself.
    def getSizeTree(self):
        return left.getSizeTree()+1+right.getSizeTree()

    # Get a random branch in the tree. This function should only be called from the top: it returns the selected location in the tree as well.
    def getRandomBranch(self):
        size=self.getSizeTree() # Figure out how big the tree is in order to pick a random branch.
        branchSelected=random.randint(2,size) #Select branch.
        result, _ = self.getBranch(branchSelected) #Get branch.
        return result, branchSelected

    # Get a branch on a selected location. Go down the tree. If selected is zero, we need to return this branch.
    def getBranch(self,selected):
        selected-=1
        if selected==0:
            return self.clone(), selected
        else:
            leftResult, selected = self.left.getBranch(selected)
            if selected==0: #The selected branch was in the left branch. Return the branch left told us was the correct one.
                return leftResult, selected
            else:
                rightResult, selected = self.right.getBranch(selected) #The selected branch may or may not be in the right branch. If not, then it will be ignored higher up the recursion.
                return rightResult, selected

    #Replace a branch in the tree with given tree. If index is 1, the branch that has to be replaced is the next branch.
    # We do that here rather than at the branch itself, given that this branch needs to know what its new left and right branch
    # are.
    # If not this branch, return current index for further checks. Also return self in case of trees with a single node (leaf)
    def replaceBranch(self,replacer,index):
        index-=1
        if index==1:
            self.left=replacer
            return self, index-1
        else:
            leftResult,index = self.left.replaceBranch(replacer,index)
            if index==1:
                self.right=replacer
                return self,index
            else:
                return self, index
                    
    # Check to see if we mutate this tree. If so, return the new branch. Else, replace left and right with potential mutations.
    # We will not mutate the branches if this branch is mutated.
    def mutate(self):
        if random.uniform(0,1)<mutationRate:
            return generateRandomBranch()
        else:
            self.left=self.left.mutate()
            self.right=self.right.mutate()
            return self

# Part of the tree: this class has only one action and is the end of the recursive functions.
class Leaf:
    #Leaf is defined with just one action.
    def __init__(self,action):
        self.action=action

    # Return a copy of the leaf.
    def clone(self):
        return self.deepcopy()

    # Perform the action specified in the leaf.
    def perform(self,model):
        return self.action

    #Print the action contained in the leaf.
    def printTree(self):
        print self.action

    #Get the size of the tree. For a leaf, this is one (one node)
    def getSizeTree(self):
        return 1
    
    #get Random Branch is only for the root of the tree
    def getRandomBranch(self):
        return self.clone(), 0

    #Replace a branch in the tree with given tree. If index is zero here, we are the only the branch and thus we need to be replaced.
    def replaceBranch(self,replacer,index):
        index-=index
        if index==0:
            return replacer, index
        else:
            self, index

    #Clone a selected branch. If not this leaf, send to branch above it was not this one.
    def getBranch(self,selected):
        selected -=1
        if selected==0: #If we happen to have a tree of size 1. Otherwise, replacement would have happened at the branch
            return self.clone(), selected
        else:
            return None, selected

    #Mutate the action with mutationRate chance.
    def mutate(self):
        if random.uniform(0,1)<mutationRate:
            return generateRandomBranch()
        return self
        
# Creates a population of numberOf size. Each member is of the form branch(leaf,leaf).
# Consideration and actions is randomly selected.
def createIndividuals(numberOf):
    individuals = []
    for count in range(numberOf):
        ranLeft = random.randint(0,len(actions)-1)
        leftLeaf= Leaf(actions[ranLeft])
        ranRight = random.randint(0,len(actions)-1)
        rightLeaf= Leaf(actions[ranRight])
        ranConsider= random.randint(0,len(considerations)-1)
        newIndividual = Branch(considerations[ranConsider],leftLeaf,rightLeaf)
        individuals.append(newIndividual)
    return individuals

# Get the fitnesses of each individual in the population by playing the game and getting the score.
def getFitnesses(population):
    fitnesses = []
    game = None #TODO: code for randomly generating a game
    for indi in population: # For each individual, keep playing the game until it is finished and returns a score.
        usedGame = game.deepcopy()
        usedGame.play(indi)
        fitnesses.append(usedGame.getScore)
    return fitnesses

# Let the individuals compete with each other and keep the winners for the evolution. Return an empty set population and fitnesess to check if algorithm worked as it should.
#Also return the survivors of the competition. Amount of survivors should 1/2 the population if even population, or 1/2 + 1 the population if uneven.
def getSurvivors(population, fitnesses):
    survivors = []
    while not len(fitnesses)==0:
        if len(fitnesses)==1: # If only one individu left, it wins the competition automatically.
            survivors.append(population.pop(0)) #This should also remove it from population
            fitnesses.pop(0)
        else:
            candidateOne=random.randint(0,len(fitnesses)-1)
            candidateTwo=random.randint(0,len(fitnesses)-1)
            while candidateTwo==candidateOne: # Keep on trying until the two candidates are different.
                candidateTwo=random.randint(0,len(fitnesses)-1)
            if fitnesses[candidateOne]==fitnesses[candidateTwo]: #Both individuals are equal, pick one at random.
                if random.randint(0,1)==0:
                    survivors.append(population[candidateOne])
                else:
                    survivors.append(population[candidateTwo])
            elif fitnesses[candidateOne]>fitnesses[candidateTwo]: #Left is better than right.
                survivors.append(population[candidateOne])
            else: #Right is better than left.
                survivors.append(population[candidateTwo])
            if candidateOne>candidateTwo: #Remove largest index first to prevent shifting values from removing the wrong index.
                fitnesses.pop(candidateOne)
                fitnesses.pop(candidateTwo)
                population.pop(candidateOne)
                population.pop(candidateTwo)
            else:
                fitnesses.pop(candidateTwo)
                fitnesses.pop(candidateOne)
                population.pop(candidateTwo)
                population.pop(candidateOne)
    return survivors, population, fitnesses

# Creating the next generation population. Take the survivors and put them in the new population.
# Further create children from two parents, and mutate them with random chance. Return an empty list of survivors to check
#all survivors were used, and a set of population that is twice the size of survivors.
def getNextGen(survivors, population):
    while not len(survivors)==0:
        if len(survivors)==1: # If uneven amount of survivors, put it in the population and create a child from itself with mutations.
            population.add(survivors[0])
            child = survivors.pop(0).clone()
            child=child.mutate()
            population.add(child)
        else:
            momIndex = random.randint(0,len(survivors)-1)
            dadIndex = random.randint(0,len(survivors)-1)
            while dadIndex==momIndex: # Keep trying until dad individual is someone else than the mother.
                dadIndex=random.randint(0,len(survivors)-1)
            mom=survivors[momIndex]
            dad=survivors[dadIndex]
            population.append(mom)
            population.append(dad)
            #The gens are the branches, the parentSwap is the location where the gen has to go.
            momGen, momSwap=mom.getRandomBranch() 
            dadGen, dadSwap=dad.getRandomBranch()
            daughter=mom.clone() #Daugher is a copy of mom with one branch from the father.
            son=dad.clone() # Son is a copy of the dad with one branch from the mother.
            daughter.replaceBranch(dadGen,momSwap)
            son.replaceBranch(momGen,dadSwap)
            son=son.mutate() #Mutate the two children.
            daughter=daughter.mutate()
            population.append(son)
            population.append(daughter)
    return survivors, population

# Genetic programming algorithm. Take a population of individuals, test their fitness, select survivors and create new population out of survivors.
# Note: if entering population of an uneven individuals, then during the first generation, you will have population+1 individuals. This remains the same for the remainder
# of the code, regardless of the amount of max generations.
def evolve(population, maxGenerations):
    for generation in range(maxGenerations):
        print generation
        fitnesses = getFitnesses(population)

        # Check how good each invididual is in the game.
##        fitnesses = []
##        game = None #TODO: code for randomly generating a game
##        for indi in population: # For each individual, keep playing the game until it is finished and returns a score.
##            usedGame = game.deepcopy()
##            while not usedGame.finished():
##                action=indi.perform(game)
##                usedGame.doAction(action)
##            fitnesses.append(usedGame.getScore)

        # Let the individuals compete with each other and keep the winners for the evolution.
        survivors, population, fitnesses = getSurvivors(population, fitnesses)
##        survivors = []
##        while not len(fitnesses)==0:
##            if len(fitnesses)==1: # If only one individu left, it wins the competition automatically.
##                survivors.append(population.pop(0)) #This should also remove it from population
##                fitnesses.pop(0)
##            else:
##                candidateOne=random.randint(0,len(fitnesses)-1)
##                candidateTwo=random.randint(0,len(fitnesses)-1)
##                while candidateTwo==candidateOne: # Keep on trying until the two candidates are different.
##                    candidateTwo=random.randint(0,len(fitnesses)-1)
##                if fitnesses[candidateOne]==fitnesses[candidateTwo]: #Both individuals are equal, pick one at random.
##                    if random.randint(0,1)==0:
##                        survivors.append(population[candidateOne])
##                    else:
##                        survivors.append(population[candidateTwo])
##                elif fitnesses[candidateOne]>fitnesses[candidateTwo]: #Left is better than right.
##                    survivors.append(population[candidateOne])
##                else: #Right is better than left.
##                    survivors.append(population[candidateTwo])
##                if candidateOne>candidateTwo: #Remove largest index first to prevent shifting values from removing the wrong index.
##                    fitnesses.pop(candidateOne)
##                    fitnesses.pop(candidateTwo)
##                    population.pop(candidateOne)
##                    population.pop(candidateTwo)
##                else:
##                    fitnesses.pop(candidateTwo)
##                    fitnesses.pop(candidateOne)
##                    population.pop(candidateTwo)
##                    population.pop(candidateOne)
        survivors, population = getNextGen(survivors,population)
        # Creating the next generation population. Take the survivors and put them in the new population.
        # Further create children from two parents, and mutate them with random chance.
##        while not len(survivors)==0:
##            if len(survivors)==1: # If uneven amount of survivors, put it in the population and create a child from itself with mutations.
##                population.add(survivors[0])
##                child = survivors.pop(0).clone()
##                child=child.mutate()
##                population.add(child)
##            else:
##                momIndex = random.randint(0,len(survivors)-1)
##                dadIndex = random.randint(0,len(survivors)-1)
##                while dadIndex==momIndex: # Keep trying until dad individual is someone else than the mother.
##                    dadIndex=random.randint(0,len(survivors)-1)
##                mom=survivors[momIndex]
##                dad=survivors[dadIndex]
##                population.append(mom)
##                population.append(dad)
##                momGen, momSwap=mom.getRandomBranch()
##                dadGen, dadSwap=dad.getRandomBranch()
##                daughter=mom.clone()
##                son=dad.clone()
##                daughter.replaceBranch(dadGen,momSwap)
##                son.replaceBranch(momGen,dadSwap)
##                son=son.mutate()
##                daughter=daughter.mutate()
##                population.append(son)
##                population.append(daughter)
                
    #Check which individual performs the best.
    fitnesses = getFitnesses(population)
##    game = None #TODO: code for randomly generating a game
##    for indi in population:
##        usedGame = game.deepcopy()
##        while not usedGame.finished():
##            action=indi.perform(game)
##            usedGame.doAction(action)
##        fitnesses.append(usedGame.getScore)
    bestScore =0
    bestIndividu = None
    for fitnessInd in range(len(fitnesses)-1):
        if fitnesses[fitnessInd]>bestScore:
            bestScore=fitnesses[fitnessInd]
            bestIndividu=population[fitnessInd]
    return bestScore, bestIndividu
    
# Generate a random branch: branch can be a leaf or a branch.
# We pick out a random index from the list [actions,considerations].
# If index is in actions, create leaf.
# Else we create a branch with two random actions.
def generateRandomBranch():
    totalPos=len(actions)+len(considerations)
    chosenIndex=random.randint(0,totalPos-1)
    if chosenIndex<len(actions): # Picked a leaf
        return Leaf(actions[chosenIndex])
    else: #Picked a branch
        chosenCons=considerations[len(actions)-chosenIndex]
        ranLeft = random.randint(0,len(actions)-1)
        leftLeaf= Leaf(actions[ranLeft])
        ranRight = random.randint(0,len(actions)-1)
        rightLeaf= Leaf(actions[ranRight])
        return Branch(chosenCons,leftLeaf,rightLeaf)

#Craft all potential considerations. Any considerations can consider up to allowedMaxStep
def generateConsiderations(allowedMaxStep):
    directions = ["North", "East", "South", "West"]
    for direction in directions:
        for steps in range(1,allowedMaxStep+1):
            considerations.append(monsterConsideration(direction, steps))
            considerations.append(wallConsideration(direction, steps))
            considerations.append(exitConsideration(direction, steps))

if __name__ == "__main__":
    individuals=10;
    generateConsiderations(3)
    print(len(considerations))
##    population=createIndividuals(individuals)
##    score, bestIndividu = evolve(population, 1000)
##    
