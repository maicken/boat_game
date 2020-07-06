import pygame
from settings import *


class Camera(object):

    def __init__(self):

        self.camera_size = CAMERA_SIZE
        self.state = pygame.Rect(0, 0, self.camera_size[0], self.camera_size[1])
        self.move = False

    def check_boat_half(self, boat):
        self.move = boat.y < self.camera_size[1]/2

    def update(self, boat):
        self.state = None