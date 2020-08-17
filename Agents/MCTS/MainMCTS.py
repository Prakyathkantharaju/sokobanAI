# Main Monte carlo tree search file
import collections
import gym
import numpy as np
import gym_sokoban, copy
import time, os, sys
from Agents.utils import MinMaxStats

print(os.getcwd())
sys.path.append('/home/prakyath/gitfolder/sokoban/')
# relative imports
from Agents.cost_functions.cost import MSE
from Agents.trees.MainTree import State, Match_state
KnownBounds = collections.namedtuple('KnownBounds', ['min', 'max'])
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
        parent_state = self.expand(parent_state, room_state)

    def main_mcts(self, root):
        for i in range(10):
            node = root
            search_path = [node]

            min_max_bounds = MinMaxStats(KnownBounds)
            while not(node.expanded()):
                action, node = self.select_child(node, min_max_stats)
        # first I need to expand
         # till you reach the terminal state or no childen
        pass


    def select_child(self, node, min_max_stats):
        if node.visit == 0:
            return random.sample(node.child.items(), 1][0]


        _, action, child = max(

    def expand_old(self,list_of_actions, state):
        self.expantion += 1
        # do till the there are no possible action or ten children
        while len(list_of_actions) != 0 or self.expantion < 10:
            self.env.room_state = state.room_state
            new_state = State(self.env.get_state())
            new_state.room_state = self.env.room_state
            state.add_child(State(self.env.get_state()))
            list_of_actions.pop(0)
        return state


    def expand(self, state, raw_state):
        # simulate throught all the 8 actions and select the best one
        parent_state = state
        player_position = np.copy(self.env.player_position)
        save_state = np.copy(raw_state)
        test_ =np.copy( save_state)
        print(np.where(test_ == 5))
        possible_actions = [i for i in range(1,9)]
        for i in range(1,9):
            action = i
            print('*'*25)
            print('action:',i)
            self.env.update_room_state(test_, player_position)
            observation, reward, done, info = self.env.step(action, weight_method = 'custom')
            child_state = self.env.get_state()
            child_state = State(child_state)
            parent_state.add_child(child_state, i)
            time.sleep(2)
            self.env.render()
        return state

    def _calculate_cost(self, state):
        state = state.room_state.flatten





if "__main__" == __name__:
    main_cts = MCTS()
    main_cts.run()
