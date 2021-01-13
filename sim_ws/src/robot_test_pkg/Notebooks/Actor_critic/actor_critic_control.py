#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 28 15:19:00 2019
@author: ganzobat
"""
## extra imports to set GPU options
import tensorflow as tf
from keras import backend as k

###################################
# TensorFlow wizardry
config = tf.ConfigProto() 
# Don't pre-allocate memory; allocate as-needed
config.gpu_options.allow_growth = True
# Only allow a total of half the GPU memory to be allocated
config.gpu_options.per_process_gpu_memory_fraction = 0.5
# Create a session with the above options specified.
k.tensorflow_backend.set_session(tf.Session(config=config))

import rospy
import numpy as np
import time
from tqdm import tqdm
import sys
from DQN_functions.mobile_control import deep_mobile_control_goal
from actor_critic_keras import Agent

gamma = 0.9
lr =0.03

num_iterations =8000
num_steps=32
epochs=10
delay_time=0.2
vels=[[1,0],[0.5,1],[0.5,-1],[0,1],[0,-1]]
legal_actions=len(vels)
reward_temp=0

rospy.init_node('Mobile_Control',anonymous=True)
Robot = deep_mobile_control_goal()

Robot.reset()
Robot.unpause()

def train_model():
    global reward_temp
    append_hist('reward_hist.txt',60)
    process_bar = tqdm(range(num_iterations))
    all_rewards=[]
    episode=0
    for episode in process_bar:
        done=False
        rewards=[]
        #values=[]
        states=[]
        new_states=[]
        steps=0
        actions=[]
        state=get_state()
        steps=0
        for steps in range(num_steps):
            states.append(state)
            #values.append(agent.critic.predict(state[None,:]))  
            action=choose_action(state)
            actions.append(action)
            perform_action(vels[action])
            rospy.sleep(delay_time)
            new_state=get_state()    
            new_states.append(new_state)
            state=new_state
            reward,done=get_reward()    
            rewards.append(reward)
            
            if done or steps==num_steps-1:

                all_rewards.append(np.sum(rewards))
                append_hist('reward_hist.txt',np.sum(rewards))
                
                if episode % 1 == 0:                    
                    sys.stdout.write("episode: {}, reward: {} \n".format(episode, np.sum(rewards)))
                break     
            
        agent.learn(np.array(states),np.array(actions),np.array(rewards),np.array(new_states))                
        if(episode%100==0):
            agent.critic.save('model_critic.h5')                     
            agent.actor.save('model_actor.h5')
            agent.policy.save('model_policy.h5')
    agent.critic.save('model_critic.h5')
    agent.actor.save('model_actor.h5')
    agent.policy.save('model_policy.h5')
def optimize_model():
    pass
    #append_hist('loss_history.txt',history.history['loss'][-1])
def choose_action(state):
    state=state[np.newaxis,:]
    probabilities=agent.actor.predict([state,np.arange(1)])
    action = np.random.choice(legal_actions, p=np.squeeze(probabilities))
    return action
def perform_action(a):
    Robot.vel.linear.x = a[0]
    Robot.vel.angular.z=a[1]
    Robot.cmd_vel.publish(Robot.vel)
def get_state():
    s_temp=Robot.data_laser
    ang_sp=Robot.odom_data.angular.z
    lin_sp=Robot.odom_data.linear.x
    return np.append(s_temp,[ang_sp,lin_sp])
def test_model():
    while (1):
        if (Robot.check_robot()):
            Robot.reset()
        s=get_state()
        a=choose_action(s)
        perform_action(a)
        try:           
            rospy.sleep(0.1)
        except:
            pass  
def append_hist(a,value):
    with open(a, 'a') as f:
        f.write("%s\n" % value)
def get_reward():
    if(Robot.check_robot()):
        Robot.reset()
        return -30, True        
    else:
        return max(Robot.odom_data.linear.x,0)*30,False # -np.sqrt((Robot.odom_pose.x-Robot.goals.x)**2+(Robot.odom_pose.y-Robot.goals.y)**2), False
if __name__== '__main__':
    agent=Agent(alpha=0.00001,n_actions=legal_actions,input_dims=7, beta=0.00005,first=False)
    train_model()   
    #test_model()
