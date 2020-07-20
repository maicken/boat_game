import pygame
from pygame.math import Vector2
import math
from settings import *


class Paddle(pygame.sprite.Sprite):

    def __init__(self, side, boat):
        pygame.sprite.Sprite.__init__(self)

        self.side = side
        self.boat = boat
        self.width = PADDLE_SCALE[0]
        self.height = PADDLE_SCALE[1]

        self.green = pygame.image.load(PATH_PADDLE_GREEN).convert_alpha()
        self.green = pygame.transform.scale(self.green, PADDLE_SCALE)
        self.red = pygame.image.load(PATH_PADDLE_RED).convert_alpha()
        self.red = pygame.transform.scale(self.red, PADDLE_SCALE)
        self.rect = self.red.get_rect()

        self.image = self.red
        self.img_orig_green = self.green.copy()
        self.img_orig_red = self.red.copy()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.x = 0
        self.y = 0
        self.angle = 0

        self.water = True
        self.mov = True

        self.m = MASS_PADDER
        self.l = LENGTH_PADDER_BOAT
        self.f = 0

    def rotate(self, dt):
        pass

    def update_rect_mask(self):
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def collision(self, river):
        if pygame.sprite.collide_mask(river, self):
            return True
        return False

    def move(self, dt):
        pass


class PaddleLeft(Paddle):

    def __init__(self, boat):
        super().__init__('left', boat)
        self.rect.centerx = self.boat.rect.centerx + self.width / 2
        self.rect.centery = self.boat.rect.centery
        self.x, self.y = self.rect.topleft

        self.angle = 0
        self.max_angle = self.angle + MAX_ANGLE
        self.min_angle = self.angle - MAX_ANGLE

    def update(self, dt):
        self.move(dt)
        self.rect.bottomright = self.boat.rect.center
        self.rotate(dt)
        self.x, self.y = self.rect.topleft

    def rotate(self, dt):
        pivot = Vector2(self.boat.rect.center)
        size = self.width/2
        offset = pivot + size * Vector2(-math.cos(math.radians(self.angle + self.boat.angle)), math.sin(math.radians(self.angle + self.boat.angle)))
        if self.water:
            self.image = pygame.transform.rotate(self.img_orig_green, self.angle + self.boat.angle)
        else:
            self.image = pygame.transform.rotate(self.img_orig_red, self.angle + self.boat.angle)
        self.rect.center = offset

    def move(self, dt):
        self.mov = False
        if self.min_angle <= self.angle + self.f * self.l / self.m <= self.max_angle:
            self.angle = self.angle + self.f * self.l / self.m
            self.mov = True


class PaddleRight(Paddle):

    def __init__(self, boat):
        super().__init__('right', boat)
        self.rect.centerx = self.boat.rect.centerx - self.width / 2
        self.rect.centery = self.boat.rect.centery
        self.x, self.y = self.rect.topleft

        self.angle = 180
        self.max_angle = self.angle + MAX_ANGLE
        self.min_angle = self.angle - MAX_ANGLE

    def update(self, dt):
        self.move(dt)
        self.rect.bottomleft = self.boat.rect.center
        self.rotate(dt)
        self.x, self.y = self.rect.topleft

    def rotate(self, dt):
        pivot = Vector2(self.boat.rect.center)
        size = self.width/2
        offset = pivot + size * Vector2(-math.cos(math.radians(self.angle + self.boat.angle)), math.sin(math.radians(self.angle + self.boat.angle)))
        if self.water:
            self.image = pygame.transform.rotate(self.img_orig_green, self.angle + self.boat.angle)
        else:
            self.image = pygame.transform.rotate(self.img_orig_red, self.angle + self.boat.angle)
        self.rect.center = offset

    def move(self, dt):
        self.mov = False
        if self.min_angle <= self.angle - self.f * self.l / self.m <= self.max_angle:
            self.angle = self.angle - self.f * self.l / self.m
            self.mov = True
