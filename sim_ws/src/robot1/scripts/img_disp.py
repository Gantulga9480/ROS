#!/usr/bin/env python

# from __future__ import print_function
import numpy as np
from cv_bridge import CvBridge
import cv2
import rospy
from sensor_msgs.msg import Image


class ImgDisp:

    def __init__(self):
        self.bridge = CvBridge()
        self.pub = rospy.Publisher('cv2_depth_img_raw', Image, queue_size=1)

    def callback1(self, msg):
        print(len(msg.data))
        # print(ord(msg.data))

    def callback(self, msg):
        img = self.bridge.imgmsg_to_cv2(msg)
        image = np.array(img, dtype=np.float32)
        cv2.normalize(image, image, 0, 255, cv2.NORM_MINMAX)
        # round to integer values
        image = np.round(image).astype(np.uint8)
        cv2.imshow('dst_rt', image)
        cv2.waitKey(1)

    def main(self):
        rospy.init_node('im_disp_node')
        rospy.Subscriber('/camera/depth/image_raw', Image, self.callback)
        rospy.spin()


if __name__ == '__main__':
    img_disp = ImgDisp()
    img_disp.main()
