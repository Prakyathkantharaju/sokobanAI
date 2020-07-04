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
    env.OBSERVATION_SPACE = np.array([1])
    env.ACTION_SPACE = 8
    lr = 0.01
    n_games = 200
    agent = Agent(gamma=0.99, epsilon=1.0, lr=lr,
                input_dims=env.OBSERVATION_SPACE,
                n_actions=env.ACTION_SPACE, mem_size=100000, batch_size= 300, epsilon_end=0.001, fname = 'models/new_model.h5')
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
        while not global_done:
            main_counter += 1
            score = 0
            local_done = False
            observation = env.state
            counter = 0
            while not local_done:
                counter += 1
                action = agent.choose_action(observation)
                observation_, reward, local_done, global_done ,info = env.step(action)
                score += reward
                agent.store_transition(observation, action, reward, observation_, local_done)
                observation = observation_
                agent.learn()
            store_local.append(score/counter)
        print(store_local)
        score_history.append(np.mean(store_local))
        print('main counter: {}, part counter: {}, epsilon {}, avg score: {}'.format(n,counter,\
        agent.epsilon,np.mean(store_local)))

    ax[0].plot(test_action, label = 'Q leanring')
    ax[1].plot(output, label = 'output')
    ax1[0].plot(score_history, label = 'training history')
    test_history.append(test_score)
    ax1[1].plot(test_history, label = 'evaluation')
    plt.legend()
    plt.show()
    agent.save_model()

