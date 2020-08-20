# general imports
import numpy as np

# This file  is for state tree construction
# This will have following class/function
# - State: each state class
# - Match_state: function to return true is states are matched

class State(object):
    """State."""

    '''
    state class
    to have child, parent and occurance information
    also can add weight
    '''
    def __init__(self, state):
        """__init__.

        :param state:
        """
        self.parent = []
        self.child = {}
        self.state = state
        self.visit = 0
        self.reward = [0]
        self.sum_reward = 0
        self.prior = 0

    def add_child(self, child, action):
        self.child[action] = child

    def add_parent(self, parent):
        self.parent.append(parent)

    def add_visit(self):
        self.visit += 1

    def add_reward(self, reward):
        self.reward.append(reward)

    def add_roomstate(self, room_state):
        self.room_state = room_state

    def get_roomstate(self):
        return np.copy(self.room_state)

    def value(self):
        return self.reward[-1]

    def expanded(self):
        if len(self.child.values()) == 0:
            return True
        else:
            return False

def Match_state(state1,state2):
    '''
    function to check if the state1 and state2 match
    return
    True if they match
    False if they do not match
    '''

    if type(state1) == type(None) or type(state2) == type(None):
        return False
    comparision = state1.state == state2.state
    return comparision.all()

def Search_tree(old_state,new_state):
    '''
        Search tree function is for searching if the there is a same state before
        return (True/False,state) True/False if there exists with state
    '''
    queue = []
    match = None
    queue = old_state.child
    while len(queue) != 0:
        # picking at no particular order
        curr_child = queue[0]
        queue = queue + curr_child.child
        if Match_state(new_state,curr_child):
            return True, curr_child
        queue.pop(0)
    return False, match
