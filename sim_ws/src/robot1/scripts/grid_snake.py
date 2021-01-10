#!/usr/bin/env python

import numpy as np
import rospy
from robot1.msg import board


class Snake:

    def __init__(self):
        self.grid = None

    def callback(self, msg):
        print(type(msg.table))

    def main(self):
        rospy.init_node('snake_grid_node')
        rospy.Subscriber('/env_grid_data', board, self.callback)
        rospy.spin()


if __name__ == '__main__':
    game = Snake()
    game.main()
