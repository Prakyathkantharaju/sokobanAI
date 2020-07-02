# General import
import numpy as np

# base class
class cost(object):
    def __init__(self, no_of_goals = 3):
        self.state_number = no_of_goals

    def evaluate(self,goals,target,player):
        raise NotImplemented

# Mean square error
class MSE(cost):
    def __init__(self,no_of_goals = 3, cost_type = 'SUM'):
        super().__init__(no_of_goals)
        self.type = cost_type

    def evaluate(self,goals, target, player):
        weight = 0
        if self.type == 'SUM':
            # remove FOR loops (OMG I am so bad)
            # should get MSE sum of all the weights with respect all the goals
            # n goals x n target
            x = 0
            for i in range(self.no_of_goals):
                x += sum([sum((target[j] - goals[i])(target[j] - goals[i]).T)
                      for j in range(self.no_of_goals)])
            weight = x
        if self.type == 'DIST':
            pass
