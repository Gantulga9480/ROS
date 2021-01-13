import rospy
import numpy as np
import sys
import time
from tqdm import tqdm
import random
import csv
from DQN_functions.mobile_control import deep_mobile_control
from DQN_functions.ReplayMemory import ReplayMemory

from keras import Sequential
from keras.layers import Dense,Dropout
from keras.optimizers import Adam,SGD,RMSprop
from keras.models import load_model
from keras.callbacks.callbacks import EarlyStopping

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
lr =0.01
lr_decay=0.5
num_iterations =50000
epochs=10
epsilon =0.5
epsilon_decay =0.9999
min_epsilon=0.1
delay_time=0.5
vels=[[0.8,0],[0.3,0.7],[0.3,-0.7],[0,0.7],[0,-0.7],[-0.5,0]]
legal_actions=len(vels)
batch_size=64
memory_size=4000
avg_speed=0
reward_temp=0
patience=6
rospy.init_node('Control',anonymous=True)
Robot = deep_mobile_control()
memory=ReplayMemory(memory_size)

Robot.reset()
Robot.unpause()
optimizer=Adam(learning_rate=lr, beta_1=0.9, beta_2=0.999, amsgrad=False)
#optimizer=RMSprop(lr=0.001,rho=0.9)
#optimizer=SGD(learning_rate=0.001,momentum=0.9)

model1=load_model('model_1.h5')
model2=load_model('model_2.h5')

early_stop=EarlyStopping(monitor='loss', min_delta=0, patience=patience, verbose=0, mode='auto', baseline=None, restore_best_weights=True)
model1.compile(loss='mean_squared_error',optimizer=optimizer)
model2.compile(loss='mean_squared_error',optimizer=optimizer)

def main():    
    try:

        a=Robot.data_laser
        a=Robot.imu_x
        a=Robot.odom_data
        print(a)
        #test_model()

    except:
        print("Error occured. Can't subscribe sensor info")
    #store_transition(delay_time)
    #train_model()   
    test_model()
def train_model():
    global lr,reward_temp,avg_speed

    process_bar = tqdm(range(num_iterations))
    for i in process_bar:
        if(i%1000==0):
            model1.save('model_1.h5')
            model1.save_weights('model_1_weights.h5')
            model2.save('model_2.h5')
            model2.save_weights('model_2_weights.h5')

            #lr=lr*lr_decay
        if(i%100==0):
            print('eps:',epsilon)
            with open(r'reward.csv','a') as f:
                writer=csv.writer(f)
                writer.writerow([i,reward_temp/100,epsilon,avg_speed/100])
            reward_temp=0
            avg_speed=0
        check_robot()
        store_transition(delay_time)
        optimize_model()
        #Robot.pause()
        #Robot.unpause()
        with open(r'pose.csv', 'a') as f:
            writer=csv.writer(f)
            writer.writerow([Robot.odom_pose.x,Robot.odom_pose.y])
        
    model1.save('model_1.h5')
    model1.save_weights('model_1_weights.h5')
    model2.save('model_2.h5')
    model2.save_weights('model_2_weights.h5')

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
        Q = (model1.predict(np.array([s]))+model2.predict(np.array([s])))/2
        
        a =vels[np.argmax(Q)]
        print(Q)
    return a
def get_state():
    s_temp=Robot.data_laser
    ang_sp=Robot.odom_data.angular.z
    lin_sp=Robot.odom_data.linear.x
    s_temp=np.append(s_temp,[ang_sp,lin_sp])
    return s_temp
def test_model():
    global epsilon
    epsilon=0.1
    while (1):
        check_robot()
        s=get_state()
        #print('eps:',epsilon)
        a=choose_action(s)
        #print(a)
        perform_action(a)
        try:           
            rospy.sleep(0.1)
        except:
            pass
def check_robot():
    if(abs(Robot.imu_x)>0.2 or abs(Robot.imu_y)>0.2):
        Robot.reset()
    if(abs(Robot.odom_pose.x)>10 or abs(Robot.odom_pose.y)>10):
        Robot.reset()
    if(abs(Robot.odom_data.angular.z)>10 or abs(Robot.odom_data.linear.x)>10):
        Robot.reset()    
def append_hist(a,value):
    with open(a, 'a') as f:
        f.write("%s\n" % value)
def store_transition(delay_time):
        global reward_temp,avg_speed
        s=get_state()
        a=choose_action(s)
        perform_action(a)
        try:
            rospy.sleep(delay_time)
        except:
            pass    
        s1=get_state()
        reward=Robot.odom_data.linear.x*30+0.5*(s1[0]+s1[4])+(s1[1]+s1[3])+2*s1[2]-10
        experience=(s,reward,a,s1)
        memory.append(experience)
        
        reward_temp=reward_temp+reward
        avg_speed=avg_speed+Robot.odom_data.linear.x
        
def optimize_model():
    global reward_temp
    if memory.__len__()>batch_size: 
        size=batch_size
    else:
        size=memory.__len__()
    batches=memory.sample(size)
    states= np.array([batch[0] for batch in batches])
    rewards= np.array([batch[1] for batch in batches])
    actions= np.array([batch[2] for batch in batches])
    new_states= np.array([batch[3] for batch in batches])
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
    
        next_state_value=np.squeeze(temp_model2.predict(new_states[i].reshape(1,-1)))[next_state_action_index]
        Qs[i][action_index]= rewards[i]+gamma*next_state_value

    history=temp_model1.fit(states,Qs,batch_size=len(batches),callbacks=[early_stop],epochs =epochs )
    
if __name__== "__main__":
    main()