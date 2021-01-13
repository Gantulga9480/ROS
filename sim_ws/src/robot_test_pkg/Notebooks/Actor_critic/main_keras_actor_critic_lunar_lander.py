#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 18:13:01 2019

@author: luu
"""

import gym 
from actor_critic_keras import Agent
#from utils import plotLearning
import numpy as np

if __name__== '__main__':
    env=gym.make('LunarLander-v2')

    agent=Agent(alpha=0.00001,n_actions=env.action_space.n,input_dims=env.observation_space.shape[0], beta=0.00005)
    score_history= []
    num_episodes=2000
    for i in range(num_episodes):
        done=False
        score=0 
        observation= env.reset()
        
        while not done:
            action=agent.choose_action(observation)
            observation_, reward, done, info =env.step(action)
            agent.learn(observation, action, reward, observation_, done)
            observation=observation_
            score += reward
        
        score_history.append(score)
        avg_score = np.mean(score_history[-100:])
        print('episode ',i , 'score: %.2f average score %.2f' % \
              (score,avg_score))
    
    filename= 'lunar-lander-actor-critic.png'
