from typing import Tuple

import pygame
from pygame.math import Vector2
import math
from settings import *
from paddle import PaddleRight, PaddleLeft


class Boat(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        p0 = BOAT_INITIAL_POSITION
        self.width = BOAT_SCALE[0]
        self.height = BOAT_SCALE[1]
        self.x = p0[0]
        self.y = p0[1]
        self.image = pygame.image.load(PATH_BOAT).convert_alpha()
        self.image = pygame.transform.scale(self.image, BOAT_SCALE)
        self.img_orig = pygame.transform.rotate(self.image, -90)

        self.angle = 0
        self.fe = 0
        self.fr = 0

        self.m = MASS
        self.A = AREA_BOAT
        self.lb = LENGTH_BOAT
        self.lp = LENGTH_PADDER
        self.u = VISCOSITY
        self.fl = FORCE_LIMIT
        self.H = HEIGHT

        self.v = 0
        self.w = 0

        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=p0)
        self.movement = True

        self.paddle_l = PaddleLeft(self)
        self.paddle_r = PaddleRight(self)

        self.points = [[0, 0]]

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        self.paddle_l.draw(screen)
        self.paddle_r.draw(screen)

    def move(self, dt):
        x_r = self.x - self.v * math.sin(math.radians(self.angle)) * dt
        y_r = self.y - self.v * math.cos(math.radians(self.angle)) * dt
        mv_n_x = x_r - self.x
        mv_n_y = y_r - self.y
        self.x = x_r
        self.y = y_r
        self.points.append([x + y for x, y in zip(self.points[-1], [mv_n_x, mv_n_y])])

        return mv_n_x, mv_n_y

    def update_rect_mask(self):
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.paddle_l.update_rect_mask()
        self.paddle_r.update_rect_mask()

    def rotate(self, dt):
        self.angle = self.angle + self.w * dt
        self.image = pygame.transform.rotate(self.img_orig, self.angle)

    def update_speed(self, dt):
        try:
            self.v = self.v + (self.fe + self.fr) / self.m * dt - self.u * math.sqrt(self.v) * self.A / self.H * dt
        except:
            self.v = self.v + (self.fe + self.fr) / self.m * dt

    def update_angular_speed(self, dt):
        self.w = self.w + (-self.fe + self.fr) * self.lp * dt
        at = self.u * self.w * self.lb * self.A / self.lb * self.lb / self.H
        at = abs(at)
        if self.w < 0:
            self.w += at
        else:
            self.w -= at

    def update(self, dt):
        if self.movement:
            self.update_speed(dt)
            self.update_angular_speed(dt)
            self.rotate(dt)
            self.paddle_l.update(dt)
            self.paddle_r.update(dt)
            self.update_force()
            mv_n_x, mv_n_y = self.move(dt)
        else:
            mv_n_x = 0
            mv_n_y = 0
        return mv_n_x, mv_n_y

    def stop(self):
        self.movement = False

    def collision(self, river):
        col_boat = pygame.sprite.collide_mask(river, self)
        col_paddle_l = self.paddle_l.collision(river)
        col_paddle_r = self.paddle_l.collision(river)

        return col_boat or col_paddle_l or col_paddle_r

    def update_force(self):
        self.fe = self.paddle_l.f
        self.fr = self.paddle_r.f
        if not self.paddle_l.water or not self.paddle_l.mov:
            self.fe = 0
        if not self.paddle_r.water or not self.paddle_r.mov:
            self.fr = 0
