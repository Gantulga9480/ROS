#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 17:54:19 2019

@author: luu
"""

from keras import backend as K
from keras.layers import Dense, Input
from keras.models import Model,load_model
from keras.optimizers import Adam
import numpy as np

class Agent(object):
    def __init__(self,alpha, beta, gamma=0.99, n_actions=4, layer1_size=100, layer2_size=50,layer3_size=20, input_dims=8,first=True):
        
        self.gamma=gamma
        self.alpha=alpha
        self.beta=beta
        self.input_dims=input_dims
        self.fc1_dims=layer1_size
        self.fc2_dims=layer2_size
        self.fc3_dims=layer3_size
        self.n_actions=n_actions
        self.first=first

        self.actor, self.critic, self.policy = self.build_actor_critic_network()
        self.action_space=[i for i  in range(self.n_actions)]
        
    def build_actor_critic_network(self):
        input_=Input(shape=(self.input_dims,))
        delta=Input(shape=(1,))
        dense1=Dense(self.fc1_dims,activation='relu')(input_)
        dense2=Dense(self.fc2_dims,activation='relu')(dense1)
        dense3=Dense(self.fc3_dims,activation='relu')(dense2)
        probs=Dense(self.n_actions,activation='softmax')(dense3)

        input_critic=Input(shape=(self.input_dims,))
        dense1_critic=Dense(self.fc1_dims,activation='relu')(input_critic)
        dense2_critic=Dense(self.fc2_dims,activation='relu')(dense1_critic)
        dense3_critic=Dense(self.fc3_dims,activation='relu')(dense2_critic)
        values=Dense(1,activation='linear')(dense3_critic)
        
        def custom_loss(y_true,y_pred):
            out=K.clip(y_pred,1e-8,1-1e-8)
            log_lik=K.sum(y_true*K.log(out),axis=1)
            
            return K.sum(-log_lik*delta)
        if self.first:
        
            actor=Model(input=[input_,delta],output=[probs])
            actor.compile(optimizer=Adam(lr=self.alpha),loss=custom_loss)
            
            critic=Model(input=[input_critic],output=[values])
            critic.compile(optimizer=Adam(lr=self.beta),loss='mean_squared_error')
            
            policy=Model(input=[input_],output=[probs])
        else:
            actor=load_model('model_actor.h5')
            critic=load_model('model_critic.h5')
            policy=load_model('model_policy.h5')

        return actor, critic, policy
    def choose_action(self, observation):
        state= observation[np.newaxis,:]
        probabilities=self.policy.predict(state)[0]
        action=np.random.choice(self.action_space,p=probabilities)
        return action

    def learn (self, states, actions, rewards, new_states):
        #states=states[np.newaxis,:]
        #new_states=new_states[np.newaxis,:]
        
        critic_value_=self.critic.predict(new_states)
        critic_value=self.critic.predict(states)

        actions_temp=np.zeros([len(actions),self.n_actions])

#        for q in reversed(range(len(rewards))):
        target=rewards +self.gamma*critic_value_.squeeze()
        delta=target[:,None]-critic_value
        

        actions_temp[np.arange(len(actions)),actions]=1.0
        
        self.actor.fit([states,delta[:]],actions_temp,epochs=10,batch_size=128,verbose=1)
        self.critic.fit(states,target, verbose=1,epochs=10,batch_size=128)
        #critic_value_=agent.critic.predict(np.array(new_states))
        #critic_value=agent.critic.predict(np.array(states))
        #actions_temp=np.zeros([len(np.array(actions)),legal_actions])
        #target=np.array(rewards+agent.gamma*critic_value_.squeeze())
        #delta=target[:,None]-critic_value
        #actions_temp[np.arange(len(actions)),actions]=1.0
        
