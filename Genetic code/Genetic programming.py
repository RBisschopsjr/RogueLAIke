import random

global actions
global considerations
global mutationRate
actions = ["moveN", "moveE", "moveS", "moveW",
           "attackN", "attackE", "attackS", "attackN",
           "stop"]
considerations = ["no","yes"]
mutationRate=0.05

class Branch:
    def __init__(self, consider, left, right):
        self.consider=consider
        self.left=left
        self.right=right

    def clone(self):
        return self.deepcopy()

    def perform(self,model):
        if self.consider==considerations[0]:
            if model:
                return self.left.perform(model)
            else:
                return self.right.perform(model)
        elif self.consider==considerations[0]:
            if model:
                return self.right.perform(model)
            else:
                return self.left.perform(model)

    def printTree(self):
        self.left.printTree()
        print self.consider
        self.right.printTree()

    def getSizeTree(self):
        return left.getSizeTree()+1+right.getSizeTree()

    def getRandomBranch(self):
        size=self.getSizeTree()
        branchSelected=random.randint(2,size)
        result, _ = self.getBranch(branchSelected)
        return result, branchSelected

    def getBranch(self,selected):
        selected-=1
        if selected==0:
            return self.clone(), selected
        else:
            leftResult, selected = self.left.getBranch(selected)
            if selected==0:
                return leftResult, selected
            else:
                rightResult, selected = self.right.getBranch(selected)
                return rightResult, selected

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
                    

    def mutate(self):
        if random.uniform(0,1)<mutationRate:
            return generateRandomBranch()
        else:
            self.left=self.left.mutate()
            self.right=self.right.mutate()
            return self


class Leaf:
    def __init__(self,action):
        self.action=action

    def clone(self):
        return self.deepcopy()

    def perform(self,model):
        return self.action

    def printTree(self):
        print self.action

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

# Genetic programming algorithm. Take a population of individuals, test their fitness, select survivors and create new population out of survivors.
# Note: if entering population of an uneven individuals, then during the first generation, you will have population+1 individuals. This remains the same for the remainder
# of the code, regardless of the amount of max generations.
def evolve(population, maxGenerations):
    for generation in range(maxGenerations):
        print generation

        # Check how good each invididual is in the game.
        fitnesses = []
        game = None #TODO: code for randomly generating a game
        for indi in population:
            usedGame = game.deepcopy()
            while not usedGame.finished():
                action=indi.perform(game)
                usedGame.doAction(action)
            fitnesses.append(usedGame.getScore)

        # Let the individuals compete with each other and keep the winners for the evolution.
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
        
        # Creating the next generation population. Take the survivors and put them in the new population.
        # Further create children from two parents, and mutate them with random chance.
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
                momGen, momSwap=mom.getRandomBranch()
                dadGen, dadSwap=dad.getRandomBranch()
                daughter=mom.clone()
                son=dad.clone()
                daughter.replaceBranch(dadGen,momSwap)
                son.replaceBranch(momGen,dadSwap)
                son=son.mutate()
                daughter=daughter.mutate()
                population.append(son)
                population.append(daughter)
    #Check which individual performs the best.
    fitnesses = []
    game = None #TODO: code for randomly generating a game
    for indi in population:
        usedGame = game.deepcopy()
        while not usedGame.finished():
            action=indi.perform(game)
            usedGame.doAction(action)
        fitnesses.append(usedGame.getScore)
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
        

if __name__ == "__main__":
    individuals=10;   
    population=createIndividuals(individuals)
    score, bestIndividu = evolve(population, 1000)
    
