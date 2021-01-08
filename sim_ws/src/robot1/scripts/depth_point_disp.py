#!/usr/bin/env python

# from __future__ import print_function

import rospy
from sensor_msgs.msg import PointCloud2


def callback(msg):
    print("data len:", len(msg.data))
    print("div height:", len(msg.data)/(msg.height*8))
    # print("div width:", len(msg.data)/msg.width)


def main():

    rospy.init_node('depth_point_disp')
    rospy.Subscriber('/camera/depth/points', PointCloud2, callback)
    rospy.spin()


if __name__ == '__main__':
    main()