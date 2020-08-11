# Main Monte carlo tree search file
import gym
import numpy as np
import gym_sokoban, copy
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
        # expansion counter
        self.expantion = 0

    def run(self):
        # Main run function to controll all the MCTS
        parent_state = self.env.get_state()
        parent_state = State(parent_state)
        room_state = self.env.room_state
        parent_state.add_roomstate(room_state)
        print(room_state)
        list_of_actions = self._valid_action(parent_state, room_state)
        self.expand(list_of_actions, parent_state)

    def expand(self,list_of_actions, state):
        self.expantion += 1
        # do till the there are no possible action or ten children
        while len(list_of_actions) != 0 or self.expantion < 10:
            self.env.room_state = state.room_state
            new_state = State(self.env.get_state())
            new_state.room_state = self.env.room_state
            state.add_child(State(self.env.get_state()))
            list_of_actions.pop(0)


    def _valid_action(self, state, raw_state):
        # simulate throught all the 8 actions and select the best one
        parent_state = state
        save_state = copy.deepcopy(raw_state)
        possible_actions = [i for i in range(1,9)]
        for i in range(1,9):
            action = i
            self.env.room_state = save_state
            print('\n')
            print(self.env.room_state,'\n', save_state)
            print('\n')
            observation, reward, done, info = self.env.step(action, weight_method = 'custom')
            child_state = self.env.get_state()
            child_state = State(child_state)
            if Match_state(parent_state,child_state):
                possible_actions.pop(i)
                print(i)
                parent_state.add_child(child_state)
            time.sleep(2)
            self.env.render()
        print(possible_actions)
        return possible_actions

    def _calculate_cost(self, state):
        state = state.room_state.flatten





if "__main__" == __name__:
    main_cts = MCTS()
    main_cts.run()
