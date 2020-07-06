from typing import Tuple

import pygame
from settings import *


class River(pygame.sprite.Sprite):

    def __init__(self, group):

        pygame.sprite.Sprite.__init__(self)

        self.group = group

        self.camera = CAMERA_SIZE
        self.map = RIVER_SCALE

        self.x = -self.map[0] + self.camera[0]
        self.y = -self.map[1] + self.camera[1]

        self.image = pygame.image.load(PATH_RIVER).convert_alpha()
        self.image = pygame.transform.scale(self.image, self.map)

        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def update(self, dt):
        mv_x = True
        mv_y = False
        for boat in self.group:
            if boat.y < self.camera[1] / 2:
                mv_y = True
            new_x, new_y = boat.update(dt, mv_x, mv_y)
            if not mv_x:
                self.x -= new_x - boat.x
            if not mv_y:
                self.y -= new_y - boat.y
            self.rect.topleft = (self.x, self.y)
            col = pygame.sprite.collide_mask(self, boat)
            if col:
                boat.v = 0
                boat.w = 0
                boat.fe = 0
                boat.fd = 0
