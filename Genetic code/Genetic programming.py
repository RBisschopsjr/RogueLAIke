import random

actions = ["moveN", "moveE", "moveS", "moveW",
           "attackN", "attackE", "attackS", "attackN",
           "stop"]
considerations = ["no","yes"]

class branch:
    def __init__(self, consider, left, right):
        self.consider=consider
        self.left=left
        self.right=right

    def clone():
        return self.deepcopy()

    def perform(model):
        if self.consider=considerations[0]:
            if model:
                self.left.perform(model)
            else:
                self.right.perform(model)
        elif self.consider=considerations[0]:
            if model:
                self.right.perform(model)
            else:
                self.left.perform(model)

class leaf:
    def __init__(self,action):
        self.action=action

    def clone():
        return self.deepcopy()

    def perform(model):
        return self.action
