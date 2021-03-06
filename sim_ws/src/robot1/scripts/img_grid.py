import numpy as np
from cv_bridge import CvBridge
import cv2
import pygame
import rospy
from sensor_msgs.msg import Image

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 177, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

NODE_RES = 10
PIXEL_SKIP_RATE = 2

OBS_HEIGHT = 0.3
CAMERA_HEIGHT = 2

WIN_WIDTH = 500
WIN_HEIGHT = 500


class ImgGrid:

    def __init__(self):
        pygame.init()
        self.bridge = CvBridge()
        self.clock = pygame.time.Clock()
        self.robot_pos = (30, 20)
        self.is_init = False
        self.grid = None
        self.win = None
        self.grid_height = 0
        self.grid_width = 0
        self.fps = 30
        self.shape = NODE_RES - 1
        self.vel = NODE_RES
        self.ground = None
        self.robot_color = None
        # self.pub = rospy.Publisher('/env_grid_data', board, queue_size=1)

    def draw_grid(self):
        for i in range(self.grid_width+1):
            pygame.draw.line(self.win, BLACK, (i*self.vel, 0),
                             (i*self.vel, self.grid_height*self.vel))
        for i in range(self.grid_height+1):
            pygame.draw.line(self.win, BLACK, (0, i*self.vel),
                             (self.grid_width*self.vel, i*self.vel))

    def draw_node(self, i, j, color):
        pygame.draw.rect(self.win, color,
                         (self.vel*i, self.vel*j,
                          self.vel, self.vel))

    def callback(self, msg):
        self.pygame_event()

        img_height = msg.height
        img_width = msg.width

        self.grid_height = img_height//NODE_RES
        self.grid_width = img_width//NODE_RES
        self.grid = np.zeros((self.grid_height, self.grid_width),
                             dtype=np.uint8)

        # msg to cv-img
        img = self.bridge.imgmsg_to_cv2(msg)

        # cv-img to np-ndarray
        image = np.array(img, dtype=np.float32)
        cv2.normalize(image, image, 0, 255, cv2.NORM_MINMAX)
        image = np.round(image).astype(np.uint8)
        image = image.T
        if not self.is_init:
            self.is_init = True
            self.ground = self.get_ground_data(image, (self.grid_width+4)//2,
                                               self.grid_height//2)
            self.robot_color = self.get_ground_data(image, self.grid_width//2-1,
                                                    self.grid_height//2-1)
            self.win = pygame.display.set_mode((img_width, img_height))
            pygame.display.set_caption("GRID {}x{}".format(self.grid_height,
                                                           self.grid_width))
            print(self.robot_color)
            print(self.ground)
        rgb_img = image[..., None].repeat(3, -1).astype("uint8")
        surf = pygame.surfarray.make_surface(rgb_img)
        self.win.blit(surf, (0, 0))
        # cv_img to grid_data
        max_pix_sum = (NODE_RES/(1+PIXEL_SKIP_RATE))**2 * 255
        # max pix_sum = 6375 with node_res=10, pixel_skip_rate = 1
        for i in range(self.grid_height):
            for j in range(self.grid_width):
                pix_sum = 0
                for pix_1 in range(j*NODE_RES, (j+1)*NODE_RES-1,
                                   1+PIXEL_SKIP_RATE):
                    for pix_2 in range(i*NODE_RES, (i+1)*NODE_RES-1,
                                       1+PIXEL_SKIP_RATE):
                        pix_sum += image[pix_2][pix_1]
                if self.robot_color - 10 <= pix_sum <= self.robot_color + 10:
                    self.draw_node(i, j, GREEN)
                elif self.ground - 5 <= pix_sum <= self.ground + 5:
                    # print("MAX at: {}, {}".format(i, j))
                    self.grid[i][j] = 0
                elif pix_sum <= 300:
                    self.grid[i][j] = 1
                    self.draw_node(i, j, RED)
                else:
                    pass

        self.draw_grid()
        pygame.display.flip()
        # self.clock.tick(self.fps)
        # self.pub.publish(self.grid.tobytes())

    def pygame_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rospy.signal_shutdown("EXIT")
                quit()
            elif event.type == pygame.KEYDOWN:
                pass

    def get_ground_data(self, img, w, h):
        pix_sum = 0 
        for pix_1 in range(h*NODE_RES,
                           (h+1)*NODE_RES-1,
                           1+PIXEL_SKIP_RATE):
            for pix_2 in range(w*NODE_RES,
                               (w+1)*NODE_RES-1,
                               1+PIXEL_SKIP_RATE):
                pix_sum += img[pix_1][pix_2]
        return pix_sum

    def get_dist(self, i, j):
        dx = 19.5 - i
        dy = 19.5 - j
        ground_y = 0


    def main(self):
        rospy.init_node('img_grid_node')
        rospy.Subscriber('/camera/depth/image_raw', Image, self.callback)
        rospy.spin()


if __name__ == '__main__':
    img_grid = ImgGrid()
    img_grid.main()
