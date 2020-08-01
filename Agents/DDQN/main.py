# general import
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import time, sys
# relative import
sys.path.append('/home/prakyath/gitfolder/sokoban')
from Agents.DDQN.Agent import Agent
import gym
import gym_sokoban

if __name__ == '__main__':
    tf.compat.v1.disable_eager_execution()
    fig, ax = plt.subplots(2,1)
    env_name = 'Sokoban-v0'

    env = gym.make(env_name)
    lr = 0.01
    n_games = 500
    action_space = 9
    observation_space = np.array([10*10])
    agent = Agent(gamma=0.99, epsilon=1.0, lr=lr,
                input_dims=observation_space,
                n_actions= action_space, mem_size=1000000, batch_size= 3000, epsilon_end=0.01, fname = 'models/new_model.h5')
    # agent.load_model()
    score_history = []
    epsilon_history = []
    test_score = [0]
    test_history = []
    main_done = False
    local_done = False
    for n in range(n_games):
        main_counter = 0
        store_local = []
        global_done = False
        env.reset()
        main_counter += 1
        score = 0
        local_done = False
        observation, reward, local_done ,info = env.step(1,observation_mode = 'custom',weight_method = 'custom')
        observation = observation.flatten()
        counter = 0
        while not local_done:
            counter += 1
            action = agent.choose_action(observation)
            observation_, reward, local_done ,info = env.step(action,observation_mode = 'custom', weight_method = 'custom')
            temp = observation_
            observation_ = observation_.flatten()
            score += reward
            agent.store_transition(observation, action, reward, observation_, local_done)
            observation = observation_
            agent.learn()
        print(temp)
        store_local.append(score/counter)
        score_history.append(np.mean(store_local[:-10]))
        print('main counter: {}, part counter: {}, epsilon {}, avg score: {}'.format(n,counter,\
        agent.epsilon,np.mean(store_local)))

    agent.save_model()

