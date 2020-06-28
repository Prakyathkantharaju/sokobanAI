# import general ai
import gym
import numpy as np
# import game
try:
    import sokoban.game as game
except:
    from  env.sokoban_game import game

# this is the gym
class sokoban_env(gym.Env):
    def __init__(self,level):
        self.game = game('env/levels', level)
        self.state = {}
        self.state['worker'] =  0
        self.state['box'] = 0
        self.state['dock'] = 0
    # reset
    def reset(self):
        pass
        #need to reset the game and start again

    # step
    def step(self, action, store = False):
        # action :
        # left = 1
        # right = 2
        # top = 3
        # bottom = 4
        # the True is cause the render will store all the action in the queue
        if action == 1:
            self.game.move(-1,0,store)
        elif action == 2:
            self.game.move(1,0,store)
        elif action == 3:
            self.game.move(0,-1,store)
        elif action == 4:
            self.game.move(0,1,store)
    # render
    def render(self):
        pass
        # render the figure in pygame window

    def close(self):
        # close the data and also the pygame window is open
        pass

    def seed(self):
        # set the random variable of the data
        pass

    def observation(self):
        # get state of the person and the box
        pass

    def get_info(self):
        # set the number of box, number of open space, number of complete goal
        pass

    def reward(self):
        # calculate the euclidian distance from the goal
        pass

    def get_state(self):
        # dock(s) location
        # worker location
        # box location
        WORKER,BOX,DOCK = self.game.get_state()
        WORKER = WORKER[:-1]
        state = {}
        self.state['worker'] = WORKER
        self.state['box'] = BOX
        self.state['dock'] = DOCK
        print(self.get_weight())

    def _state_size(self):
        self.get_state()
        self.len = 1
        self.len += len(self.state['box'])

    def get_weight(self,weight_type = 'euclidian', com_type = 'SUM'):
        # option of getting weight:
        # 'manhattan'
        # 'euclidian'
        # 'diagonal'
        # option to combine weight:
        # 'SUM': add all the weight from each dock to box
        # 'LEAST': add the least distance from the dock for each box
        # 'MEAN': add the weight and divide it by the number of docks
        # TODO: need to add different type of weights
        weight = 0
        if weight_type == 'euclidian':
            for i in self.state['box']:
                for j in self.state['dock']:
                    if com_type == 'SUM':
                        weight += np.sqrt((i[0] - j[0])**2 + (i[1] - j[1])**2)
                    else:
                        weight = 0
        return weight


