import numpy as np
import rospy
import sys
import time
from tqdm import tqdm
import random
import keyboard
#import Mobile_Control

from mobile_control import mobile_control as Mobile_Control

#Hyperparameters
gamma = 0.9
lr =0.4
lr_decay=0.999
num_episodes =500
epsilon =0.6
epsilon_decay =0.99999
min_epsilon=0.3
delay_time=0.01
vels=[[1,0],[0.5,1],[0.5,-1],[0,2],[0,-2],[-1.5,0]]
legal_actions=len(vels)
s=np.zeros([3,3,3,3,3,3,3])   
#Q=np.zeros((3,3,3,3,3,3
#Q=np.zeros((s.size,legal_actions))
Q=np.load('Q-table-sp-goal.npy')

Robot = Mobile_Control()
Robot.reset()


def main():
    rospy.init_node('Mobile_Control',anonymous=True)
    try:
        a=Robot.data_laser
        a=Robot.imu_x
        a=Robot.odom_data
        print(a)
    except:
        print("Error occured. Can't subscribe sensor info")
    print(legal_actions)
    print(s.size)
    print(Q.shape)
    #train_model()   
    test_model()

def train_model():
    global epsilon
    global lr
    process_bar = tqdm(range(num_episodes))
    for i in process_bar:
        if(i%1000==0):
            print('eps:',epsilon)
            if(lr>0.2):               
                lr=lr*lr_decay
                print('lr:',lr)

        check_robot()
        s=get_state()

        s0=(int)(s[0]*81+s[1]*27+s[2]*9+s[3]*3+s[4]+243*s[5]+729*s[6])
        action_index=choose_action(s0)
        take_action(vels[action_index])

        time.sleep(delay_time)

        ss=get_state()        
        print('ss:',ss)
        # next state index
        j=(int)(ss[0]*81+ss[1]*27+ss[2]*9+ss[3]*3+ss[4]+ss[5]*243+ss[6]*729)
        reward=max(Robot.odom_data.linear.x,0)
        print('reward:',reward)
        Q[s0,action_index]= (1-lr)*Q[s0,action_index]+ lr*(reward+gamma*np.max(Q[j,:]))
        if (i%1000==0):  #Save model in every 1000 iterations
            np.save('Q-table-sp-goal.npy',Q)
    np.save('Q-table-sp-goal.npy',Q)
def test_model():
    Q=np.load('Q-table-sp-goal.npy')
    
    while True:
    #if keyboard.is_pressed('q'):
        #   break
        check_robot()

        s=get_state()

        s0=(int)(s[0]*81+s[1]*27+s[2]*9+s[3]*3+s[4]+243*s[5]+729*s[6])
        action_index=choose_action(s0)
        take_action(vels[action_index])

def take_action(a):
    Robot.vel.linear.x = a[0]
    Robot.vel.angular.z=a[1]
    Robot.cmd_vel.publish(Robot.vel)
def choose_action(s):
    global epsilon,min_epsilon
        #epsilon greedy. to choose random actions initially when Q is all zeros
    if np.random.random()<epsilon:
        action_index=np.random.randint(0,legal_actions)
        if epsilon>min_epsilon:
            epsilon = epsilon*epsilon_decay
        #print('Took random action')
    else:
        action_index=np.argmax(Q[s,:])
    return action_index
def get_state():
    s_temp=Robot.data_laser
    sp_ang=Robot.odom_data.angular.z
    if(sp_ang<-0.2):
        ang_sp=0
    elif(sp_ang>0.2):
        ang_sp=1
    else:
        ang_sp=2    
    sp_lin=Robot.odom_data.linear.x
    if(sp_lin<-0.2):
        lin_sp=0
    elif(sp_lin>0.2):
        lin_sp=1
    else:
        lin_sp=2
    s_temp=np.append(s_temp,[ang_sp,lin_sp])
    return s_temp
def check_robot():
        if(abs(Robot.imu_x)>0.1 or abs(Robot.imu_y)>0.1):
            Robot.reset()
        if(abs(Robot.odom_data.linear.x)>4 or abs(Robot.odom_data.angular.z)>4):
            Robot.reset()

if __name__== "__main__":
    main()