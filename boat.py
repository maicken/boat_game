from typing import Tuple

import pygame
import math
from settings import *


class Boat(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        p0 = BOAT_INITIAL_POSITION
        self.x = p0[0]
        self.y = p0[1]
        self.image = pygame.image.load(PATH_BOAT).convert_alpha()
        self.image = pygame.transform.scale(self.image, BOAT_SCALE)
        self.img_orig = pygame.transform.rotate(self.image, -90)

        self.angle = 0
        self.fe = 0
        self.fd = 0
        self.m = MASS
        self.l = LENGTH
        self.k = K
        self.fl = FORCE_LIMIT
        self.v = 0
        self.w = 0

        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=p0)
        self.movement = True

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        #pygame.draw.rect(screen, (255, 0, 0), self.rect)

    def move(self, dt):
        x_r = self.x - self.v * math.sin(math.radians(self.angle)) * dt
        y_r = self.y - self.v * math.cos(math.radians(self.angle)) * dt
        mv_n_x = x_r - self.x
        mv_n_y = y_r - self.y
        self.x = x_r
        self.y = y_r
        return mv_n_x, mv_n_y

    def update_rect_mask(self):
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

    def rotate(self, dt):
        self.angle = self.angle + self.w * dt
        self.image = pygame.transform.rotate(self.img_orig, self.angle)

    def update_speed(self, dt):
        self.v = self.v + (self.fe + self.fd) / self.m * dt - self.v ** 2 * self.k

    def update_angular_speed(self, dt):
        self.w = self.w + (-self.fe + self.fd) * self.l / 2 * dt
        if self.w < 0:
            self.w += self.w ** 2 * self.k
        else:
            self.w -= self.w ** 2 * self.k

    def update(self, dt):
        if self.movement:
            self.update_speed(dt)
            self.update_angular_speed(dt)
            self.rotate(dt)
            mv_n_x, mv_n_y = self.move(dt)
        else:
            mv_n_x = 0
            mv_n_y = 0
        return mv_n_x, mv_n_y

    def stop(self):
        self.movement = False