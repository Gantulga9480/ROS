#!/usr/bin/env python

# from __future__ import print_function
import numpy as np
from PIL import Image as ig
import pygame
import rospy
from sensor_msgs.msg import Image

WIDTH = 410
HEIGHT = 410


class ImgDisp:

    def __init__(self):
        pygame.init()
        self.fps = 60
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

    def callback1(self, msg):
        print(len(msg.data))
        print(ord(msg.data))

    def callback(self, msg):
        rgb_array = np.zeros((msg.width, msg.height, 3), dtype=np.uint8)
        for row in range(len(msg.data)/(msg.height*4)-1):
            for col in range(len(msg.data)/(msg.width*4)-1):
                # print(ord(msg.data[row*col]))
                rgb_array[row][col][0] = ord(msg.data[row*col+0])
                rgb_array[row][col][1] = 0
                rgb_array[row][col][2] = 0
                # rgb_array[row][col][2] = ord(msg.data[row*col+3])
                # print(ord(msg.data[row*col+3]))
        surf = pygame.surfarray.make_surface(rgb_array)
        self.win.blit(surf, (5, 5))
        pygame.display.flip()
        # self.clock.tick(self.fps)

    def main(self):
        rospy.init_node('im_disp_node')
        rospy.Subscriber('/camera/depth/image_raw', Image, self.callback)
        rospy.spin()


if __name__ == '__main__':
    img_disp = ImgDisp()
    img_disp.main()