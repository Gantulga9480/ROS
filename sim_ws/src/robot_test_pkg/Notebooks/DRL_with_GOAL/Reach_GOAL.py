import rospy
import numpy as np
import sys
import time
from tqdm import tqdm
import random

#from DQN_functions.mobile_control import deep_mobile_control_goal
#from DQN_functions.ReplayMemory import ReplayMemory
from mobile_control import deep_mobile_control_goal
from ReplayMemory import ReplayMemory

from keras import Sequential
from keras.layers import Dense,Dropout,Input,concatenate
from keras.optimizers import Adam
from keras.models import Model, load_model
from keras.callbacks.callbacks import EarlyStopping
from keras import regularizers
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


gamma = 0.9
lr =0.03
lr_decay=0.5

num_iterations =80000
epochs=10

epsilon =0.9
initial_epsilon=epsilon

epsilon_decay =0.9999
min_epsilon=0.1
delay_time=0.5
vels=[[1,0],[0.5,1],[0.5,-1],[0,1],[0,-1]]
legal_actions=len(vels)
batch_size=64
memory_size=4000
reward_temp=0
patience=6
threshold=0.7 # Threshold to assume reached to the goal

rospy.init_node('Mobile_Control',anonymous=True)
Robot = deep_mobile_control_goal()
memory=ReplayMemory(memory_size)

Robot.reset()
Robot.unpause()
'''
inp_laser=Input(shape=(20,))
x=Dense(50,activation='relu',kernel_initializer='random_uniform',use_bias='True',activity_regularizer=regularizers.l2(0.0001))(inp_laser)
#x=Dense(20,activation='sigmoid')(x)
x=Dense(10,activation='relu',kernel_initializer='random_uniform',use_bias='True',activity_regularizer=regularizers.l2(0.0001))(x)
inp_speed=Input(shape=(3,))
merged=concatenate([x,inp_speed])
merged=Dense(20,activation='relu',kernel_initializer='random_uniform',use_bias='True',activity_regularizer=regularizers.l2(0.0001))(merged)
inp_goal=Input(shape=(2,))
inp_pose=Input(shape=(2,))
merged=concatenate([merged,inp_goal,inp_pose])
merged=Dense(50,activation='relu',kernel_initializer='random_uniform',use_bias='True',activity_regularizer=regularizers.l2(0.0001))(merged)
merged=Dense(30,activation='relu',kernel_initializer='random_uniform',use_bias='True',activity_regularizer=regularizers.l2(0.0001))(merged)
merged=Dense(20,activation='relu',kernel_initializer='random_uniform',use_bias='True',activity_regularizer=regularizers.l2(0.0001))(merged)
merged=Dense(10,activation='relu',kernel_initializer='random_uniform',use_bias='True',activity_regularizer=regularizers.l2(0.0001))(merged)

out=Dense(5,activation='linear',kernel_initializer='random_uniform',use_bias='True',activity_regularizer=regularizers.l2(0.0001))(merged)

model=Model(inputs=[inp_laser,inp_speed,inp_goal,inp_pose],outputs=out)

optimizer=Adam(learning_rate=lr, beta_1=0.9, beta_2=0.999, amsgrad=False)
model.compile(loss='huber_loss',optimizer=optimizer)
model.summary()
model.save('model_1.h5')
model.compile(loss='mse',optimizer=optimizer)
model.save('model_2.h5')
'''
model1=load_model('model_1.h5')
model2=load_model('model_2.h5')
#early_stop=EarlyStopping(monitor='loss', min_delta=0, patience=patience, verbose=0, mode='auto', baseline=None, restore_best_weights=True)
#model1.compile(loss='mean_squared_error',optimizer=optimizer)
#model2.compile(loss='mean_squared_error',optimizer=optimizer)
goal_x=5
goal_y=5
#Robot.goals.x=goal_x
#Robot.goals.y=goal_y
i=1
def main():
    global i    
    Robot.set_goal()    
    while Robot.goals is None:
        Robot.set_goal()
    store_transition(delay_time)
    train_model()   
    test_model()
def train_model():
    global lr,reward_temp
    append_hist('loss_history.txt',1000)
    append_hist('reward_hist.txt',30)

    process_bar = tqdm(range(num_iterations))
    for i in process_bar:
        if(i%1000==0):
            model1.save('model_1.h5')
            model2.save('model_2.h5')
            lr=lr*lr_decay
        if(i%100==0):
            print('eps:',epsilon)
            append_hist('reward_hist.txt',reward_temp/100)
            reward_temp=0
        store_transition(delay_time)
        #Robot.pause()
        optimize_model()
        #Robot.unpause()
    model1.save('model_1.h5')
    model2.save('model_2.h5')

def perform_action(a):
    Robot.vel.linear.x = a[0]
    Robot.vel.angular.z=a[1]
    Robot.cmd_vel.publish(Robot.vel)
def choose_action(s):
    global epsilon,min_epsilon
        #epsilon greedy. to choose random actions initially when Q is all zeros
    if np.random.random()<epsilon:
        action_index=np.random.randint(0,legal_actions)
        a =vels[action_index]
        if epsilon>min_epsilon:
            epsilon = epsilon*epsilon_decay
        print('Took random action')
    else:
        Q = (model1.predict( s)+model2.predict(s ))/2
        
        a =vels[np.argmax(Q)]
        print(Q)
    return a
def get_state():
    s_temp=Robot.data_laser
    ang_sp=Robot.odom_data.angular.z
    lin_sp=Robot.odom_data.linear.x
#    sp=np.array(ang_sp,lin_sp)
    #pose_x=Robot.odom_pose.x
    #pose_y=Robot.odom_pose.y
    #s_temp=np.append(s_temp,[ang_sp,lin_sp])
    return [np.array([s_temp]),np.array([[ang_sp,lin_sp,Robot.odom_yaw]]),np.array([[Robot.odom_pose.x,Robot.odom_pose.y]]),
                          np.array([[Robot.goals.x,Robot.goals.y]])]
def test_model():
    global epsilon
    epsilon=0.1
    while (1):
        Robot.check_robot()
        s=get_state()
        #print('eps:',epsilon)
        a=choose_action(s)
        #print(a)
        perform_action(a)
        try:           
            rospy.sleep(0.1)
        except:
            pass  
def append_hist(a,value):
    with open(a, 'a') as f:
        f.write("%s\n" % value)
def store_transition(delay_time):
        global reward_temp
        s=get_state()
        #print('s:',s)
        a=choose_action(s)
        perform_action(a)
        try:
            rospy.sleep(delay_time)
        except:
            pass    
        s1=get_state()
        reward,is_terminal=get_reward()
        experience=(s,reward,a,s1,is_terminal)
        memory.append(experience)
        
        reward_temp=reward_temp+reward

def optimize_model():
    global reward_temp
    if memory.__len__()>batch_size: 
        size=batch_size
    else:
        size=memory.__len__()
    batches=memory.sample(size)
#    batch=batches[0]
    states=list_to_array_states([batch[0] for batch in batches])
    
    rewards= np.array([batch[1] for batch in batches])
    actions= np.array([batch[2] for batch in batches])
    
    new_states=list_to_array_states( [batch[3] for batch in batches])
    terminal=[batch[4] for batch in batches]
    if np.random.random()<0.5:
        temp_model1=model1
        temp_model2=model2
    else:
        temp_model1=model2  
        temp_model2=model1
    #print(actions)
    Qs =temp_model1.predict(states)
    next_state_Qs = temp_model1.predict(new_states)
    next_state_actions=np.argmax(next_state_Qs,axis=1)

    for i in range(len(rewards)):
        action_index=vels.index(list(actions[i]))
        next_state_action_index=next_state_actions[i]
    
        next_state_value=np.squeeze(temp_model2.predict([new_state[i].reshape(1,-1) for new_state in new_states]))[next_state_action_index]
        if terminal[i]:
            Qs[i][action_index]= rewards[i]
        else:    
            Qs[i][action_index]= rewards[i]+gamma*next_state_value

    history=temp_model1.fit(states,Qs,batch_size=len(batches),epochs =epochs )
    append_hist('loss_history.txt',history.history['loss'][-1])
def get_reward():
    global threshold
    if(Robot.isFinal(Robot.goals.x,Robot.goals.y,threshold)):
        Robot.reset()
        Robot.set_goal()
        
        return 100 ,True
        
    elif(Robot.check_robot()):
        Robot.reset()
        Robot.set_goal()
        return -10, True
        
    else:
        return -np.sqrt((Robot.odom_pose.x-Robot.goals.x)**2+(Robot.odom_pose.y-Robot.goals.y)**2), False
def list_to_array_states(states):
    
    #a_1=[]
    #a_2=[]
    #a_3=[]
    #a_4=[]
    a_1=np.squeeze(np.array([state[0] for state in states]),axis=1)
    a_2=np.squeeze(np.array([state[1] for state in states]),axis=1)
    a_3=np.squeeze(np.array([state[2] for state in states]),axis=1)
    a_4=np.squeeze(np.array([state[3] for state in states]),axis=1)
    return [a_1,a_2,a_3,a_4]
   #return [np.array(a_1),np.array(a_2),np.array(a_3),np.array(a_4)]               
if __name__== "__main__":
    main()