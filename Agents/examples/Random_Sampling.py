import gym
import numpy as np
import gym_sokoban
import time
import os,sys
# realtive import
print(os.getcwd())
sys.path.append('/home/prakyath/gitfolder/sokoban')
from Agents.cost_functions.cost import MSE

# Before you can make a Sokoban Environment you need to call:
# import gym_sokoban
# This import statement registers all Sokoban environments
# provided by this package
env_name = 'Sokoban-v0'
env = gym.make(env_name)

ACTION_LOOKUP = env.unwrapped.get_action_lookup()
print("Created environment: {}".format(env_name))

for i_episode in range(1):#20
    observation = env.reset()

    for t in range(100):#100
        env.render(mode='human')
        action = env.action_space.sample()

        # Sleep makes the actions visible for users
        time.sleep(1)
        observation, reward, done, info = env.step(action, observation_mode = 'raw')

        print(ACTION_LOOKUP[action], reward, done, info)
        wall,goals,boxes,player = observation[0],observation[1],observation[2],observation[3]
        print(np.argwhere(player == 1))
        print(np.argwhere(goals == 1))
        print(np.argwhere(boxes == 1))
        if done:
            print("Episode finished after {} timesteps".format(t+1))
            env.render()
            break

    env.close()

time.sleep(10)
