# Main Monte carlo tree search file
import collections, math
import gym, time
import numpy as np
import gym_sokoban, copy, random
import time, os, sys
print(os.getcwd())
sys.path.append('/home/prakyath/gitfolder/sokoban/')
from Agents.utils import MinMaxStats

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

        # term to penalize the if the same state is achieved again and again.
        self.cost_append = 0

    def run(self):
        # Main run function to controll all the MCTS
        # TODO: move left is not working
        parent_state = self.env.get_state()
        parent_state = State(parent_state)
        room_state = self.env.room_state
        parent_state.add_roomstate(room_state)
        print(room_state)
        parent_state = self.expand(parent_state, room_state)
        state_list = [parent_state]
        for i in range(100):
            current_state = state_list[-1]
            self.main_mcts(current_state)
            action, child_ = max(current_state.child.items(), key = lambda item: item[1].visit)
            for action_list,child in current_state.child.items():
                print(action_list,child.visit, 'action and child count')
            print(action)
            player_position = np.copy(self.env.player_position)
            self.env.update_room_state(np.copy(room_state))
            print('before')
            print(self.env.room_state)
            observation, reward, done, info = self.env.step(action,player_position,weight_method = 'custom')
            print('after state')
            print(self.env.room_state)
            child_state = self.env.get_state()
            child_state = State(child_state)
            child_state.add_roomstate(np.copy(self.env.room_state))
            room_state = np.copy(self.env.room_state)
            child_state = self.expand(child_state,room_state)
            state_list.append(child_state)
            time.sleep(3)
            print(self.env.get_action_lookup())
            if Match_state(state_list[-1],state_list[-2]) :
                self.cost_append += 1
            else:
                self.cost_append = 0
        # input('test')

    def main_mcts(self, root):
        min_max_bounds = MinMaxStats(None)
        # eenforced exploration
        epsilon = np.random.randint(20, size = 20)
        print(epsilon)
        for i in range(100):
            node = root
            search_path = [node]
            action_history = []
            counter = 0
            while not(node.expanded()):
                if i in epsilon:
                    action,node = self.select_child(node, min_max_bounds, explore = True)
                else:
                    action, node = self.select_child(node, min_max_bounds)
                search_path.append(node)
                action_history.append(action)
                # if node.expanded() == True:
                    # print(node.get_roomstate())
                    # print(len(node.child.values()))
            parent = search_path[-2]
            room_state = node.get_roomstate()
            node = self.expand(node, room_state)
            self.backprop(search_path, min_max_bounds)



    def select_child(self, node, min_max_stats, explore = False):
        if node.visit == 0 or random == True:
            return random.sample(node.child.items(), 1)[0]
        else:
            t, action, child = \
            max((self.ucb_score(node, child, min_max_stats), action, child) \
                for action , child in node.child.items())
            return action , child

    def backprop(self, search_path, min_max_stats):
        value = 0
        for node in search_path[::-1]:
            node.sum_reward += value
            min_max_stats.update(node.value())
            value = node.value() + 0.99 * value
            node.add_visit()



    def ucb_score(self, parent, child, min_max_stats):
        pb_c = math.log((parent.visit + 19652 + 1) / 19652) + 1.25
        pb_c *= math.sqrt(parent.visit) / (child.visit + 1)

        prior_score = pb_c * child.prior
        value_score = min_max_stats.normalize(child.value())
        return prior_score + value_score

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
        player_position = self.env.get_player()
        # print('player',player_position.shape)
        save_state = copy.deepcopy(raw_state)
        test_ = copy.deepcopy(save_state)
        list_state = save_state.tolist()
        # print(np.where(test_ == 5))
        possible_actions = [i for i in range(1,9)]
        for i in range(1,9):
            action = i
            # print('action:',i)
            # print('actual player position', np.where(test_ == 5), np.where(save_state == 5),np.where(np.array(list_state) == 5))
            self.env.update_room_state(test_)
            observation, reward, done, info = self.env.step(action,player_position,weight_method = 'custom')
            child_state = self.env.get_state()
            child_state = State(child_state)
            child_state.add_reward(reward)
            child_state.add_roomstate(np.copy(self.env.room_state))
            # print(player_position)
            parent_state.add_child(child_state, i)
            self.env.render()
        return state

    def _calculate_cost(self, state):
        state = state.room_state.flatten





if "__main__" == __name__:
    main_cts = MCTS()
    main_cts.run()
