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
        mv_x = False
        mv_y = True
        for player in self.group:
            if player.boat.y < self.camera[1] / 2:
                mv_y = False
            new_x, new_y = player.boat.update(dt, mv_x, mv_y)
            if not mv_x:
                self.x -= new_x - player.boat.x
            if not mv_y:
                self.y -= new_y - player.boat.y
            self.rect.topleft = (self.x, self.y)
            col = pygame.sprite.collide_mask(self, player.boat)
            if col:
                player.boat.stop()

    def update(self, dt):

        mv_x = True
        mv_y = False

        new_x_l = []
        new_y_l = []

        for player in self.group:
            mv_n_x, mv_n_y = player.boat.update(dt)
            if player.boat.y < self.camera[1] / 2:
                mv_y = True
            new_x_l.append(mv_n_x)
            new_y_l.append(mv_n_y)

        new_y_max = max(new_y_l)
        new_y_min = min(new_y_l)

        if abs(new_y_max) > abs(new_y_min):
            new_y = new_y_max
        else:
            new_y = new_y_min
        new_x = new_x_l[new_y_l.index(new_y)]

        if mv_x:
            self.x -= new_x
        if mv_y:

            self.y -= new_y

        self.rect.topleft = (self.x, self.y)

        for player in self.group:
            if mv_x:
                player.boat.x -= new_x
            if mv_y:
                player.boat.y -= new_y
            col = player.boat.collision(self)
            if col:
                player.boat.stop()
            player.boat.update_rect_mask()