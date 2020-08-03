# Main Monte carlo tree search file
import gym
import numpy as np
import gym_sokoban
import time, os, sys

print(os.getcwd())
sys.path.append('/home/prakyath/gitfolder/sokoban/')
# relative imports
from Agents.cost_functions.cost import MSE
from Agents.trees.MainTree import State, Match_state

class MCTS(object):
    def __init__(self):
        env_name = 'Sokoban-v0'
        self.env = gym.make(env_name)
        self.mse = MSE()
        self.env.render(mode = 'human')
        self.env.OBSERVATION_SPACE = 1
        self.env.ACTION_SPACE = 8
        self.ACTION_LOOKUP = self.env.unwrapped.get_action_lookup()
        self.env.reset()

    def run(self):
        # Main run function to controll all the MCTS
        parent_state = self.env.get_state()
        parent_state = State(parent_state)
        room_state = self.env.room_state
        self._valid_action(parent_state, room_state)

    def _valid_action(self, state, raw_state):
        # simulate throught all the 8 actions and select the best one
        parent_state = state
        save_state = raw_state
        possible_actions = [i for i in range(1,9)]
        for i in range(1,9):
            action = i
            self.env.room_state = save_state
            self.env.step(action, observation_mode = 'raw')
            child_state = self.env.get_state()
            child_state = State(child_state)
            if Match_state(parent_state,child_state):
                possible_actions.pop(i)
                parent_state.add_child(child_state)
            self.env.render()
        return possible_actions





if "__main__" == __name__:
    main_cts = MCTS()
    main_cts.run()
