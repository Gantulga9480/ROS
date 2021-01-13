import rospy
import sys
import time
import random
import numpy as np
from DQN_functions.mobile_control import deep_mobile_control_goal

rospy.init_node('Test_ros_control',anonymous=True)
Robot=deep_mobile_control_goal()

def main():
    Robot.reset()
    i=0
    while(1):
        try:
            i=i+1
            Robot.set_goal_specific(i,i)
            time.sleep(4)
        except:
            pass

if __name__== "__main__":
    main()