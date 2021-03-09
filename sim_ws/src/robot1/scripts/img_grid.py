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

NODE_RES = 20
PIXEL_SKIP_RATE = 10

OBS_HEIGHT = 0.5
CAMERA_HEIGHT = 3

WIN_WIDTH = 640
WIN_HEIGHT = 480


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
        self.robot_cor = [0, 0]

    def main(self):
        rospy.init_node('img_depth_node')
        rospy.Subscriber('/camera/depth/image_raw', Image, self.callback)
        rospy.sleep(1)
        rospy.Subscriber('/camera/color/image_raw', Image, self.rgb_callback)
        rospy.spin()

    def rgb_callback(self, msg):
        img = self.bridge.imgmsg_to_cv2(msg)
        image = np.array(img, dtype=np.float32)
        cv2.normalize(image, image, 0, 255, cv2.NORM_MINMAX)
        image = np.round(image).astype(np.uint8)
        image = np.swapaxes(image, 0, 1)
        self.max_sum = 0
        self.robot_cor = [0, 0]
        for i in range(self.grid_width):
            for j in range(self.grid_height):
                pix_sum = self.get_img(image, i, j)
                if pix_sum > self.max_sum:
                    if i != 0 and j != 0:
                        self.max_sum = pix_sum
                        self.robot_cor[0] = i
                        self.robot_cor[1] = j

    def callback(self, msg):
        self.pygame_event()

        self.grid_height = msg.height//NODE_RES
        self.grid_width = msg.width//NODE_RES
        self.grid = np.zeros((self.grid_height, self.grid_width),
                             dtype=np.uint8)
        # max pix_sum = 6375 with node_res=10, pixel_skip_rate = 1
        max_pix_sum = (NODE_RES//(1 + PIXEL_SKIP_RATE))**2 * 255

        # msg to cv-img
        img = self.bridge.imgmsg_to_cv2(msg)

        # cv-img to np-ndarray
        image = np.array(img, dtype=np.float32)
        cv2.normalize(image, image, 0, 255, cv2.NORM_MINMAX)
        image = np.round(image).astype(np.uint8)
        image = image.T
        if not self.is_init:
            self.is_init = True
            self.ground = self.get_data(image, self.grid_width//2,
                                        self.grid_height//2)
            self.ground /= max_pix_sum
            print('ground color', self.ground)
            self.win = pygame.display.set_mode((msg.width, msg.height))
            pygame.display.set_caption("GRID {}x{}".format(self.grid_width,
                                                           self.grid_height))
        img = image[..., None].repeat(3, -1).astype("uint8")
        surf = pygame.surfarray.make_surface(img)
        self.win.blit(surf, (0, 0))
        # cv_img to grid_data
        for i in range(self.grid_height):
            for j in range(self.grid_width):
                pix_sum = self.get_data(image, j, i) / max_pix_sum
                if self.ground - 0.2 <= pix_sum <= self.ground + 0.06:
                    self.draw_node(i, j, GREEN)
                    self.grid[i][j] = 0
                else:
                    self.grid[i][j] = 1
                    # self.draw_node(i, j, RED)
        self.draw_node(self.robot_cor[1], self.robot_cor[0], BLUE)
        self.draw_grid()
        pygame.display.flip()
        # self.clock.tick(self.fps)

    def pygame_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rospy.signal_shutdown("EXIT")
                quit()
            elif event.type == pygame.KEYDOWN:
                pass

    def get_data(self, img, w, h):
        pix_sum = 0
        for pix_1 in range(w*NODE_RES,
                           (w+1)*NODE_RES-1,
                           1+PIXEL_SKIP_RATE):
            for pix_2 in range(h*NODE_RES,
                               (h+1)*NODE_RES-1,
                               1+PIXEL_SKIP_RATE):
                pix_sum += img[pix_1][pix_2]
        return pix_sum

    def get_img(self, array, w, h):
        pix_sum = 0
        for pix_1 in range(w*NODE_RES,
                           (w+1)*NODE_RES-1,
                           1+PIXEL_SKIP_RATE):
            for pix_2 in range(h*NODE_RES,
                               (h+1)*NODE_RES-1,
                               1+PIXEL_SKIP_RATE):
                pix_sum += np.mean(array[pix_1][pix_2])
                # self.win.set_at((pix_1, pix_2), array[pix_1][pix_2])
        return pix_sum

    def draw_grid(self):
        for i in range(self.grid_width+1):
            pygame.draw.line(self.win, BLACK, (i*self.vel, 0),
                             (i*self.vel, self.grid_height*self.vel))
        for i in range(self.grid_height+1):
            pygame.draw.line(self.win, BLACK, (0, i*self.vel),
                             (self.grid_width*self.vel, i*self.vel))

    def draw_node(self, i, j, color):
        pygame.draw.rect(self.win, color,
                         (self.vel*j, self.vel*i,
                          self.vel, self.vel))


if __name__ == '__main__':
    img_grid = ImgGrid()
    img_grid.main()
