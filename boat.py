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

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self, dt, mv_x, mv_y):
        x_r = self.x - self.v * math.sin(math.radians(self.angle)) * dt
        y_r = self.y - self.v * math.cos(math.radians(self.angle)) * dt
        if mv_x:
            self.x = x_r
        if mv_y:
            self.y = y_r
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        return x_r, y_r

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

    def update(self, dt, mv_x, mv_y):
        self.update_speed(dt)
        self.update_angular_speed(dt)
        self.rotate(dt)
        new_x, new_y = self.move(dt, mv_x, mv_y)
        return new_x, new_y

    def stop(self):
        self.v = 0
        self.w = 0
        self.fe = 0
        self.fd = 0