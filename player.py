import pygame
import math
import random
from NN import NN
from settings import *


class Vision(pygame.sprite.Sprite):

    def __init__(self, boat, type):
        pygame.sprite.Sprite.__init__(self)

        self.boat = boat

        self.image = pygame.image.load(PATH_X).convert_alpha()
        self.image = pygame.transform.scale(self.image, X_SCALE)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.d = MAX_VISION_DISTANCE

        if type == 1:
            self.angle = 90
        if type == 2:
            self.angle = 45
        if type == 3:
            self.angle = -45
        if type == 4:
            self.angle = -90
        if type == 5:
            self.angle = 0

        self.x = 0
        self.y = 0
        self.points = []

    def update(self, river):

        for i in range(self.d):
            p_x = self.boat.rect.center[0] - i * math.sin(math.radians(self.angle + self.boat.angle))
            p_y = self.boat.rect.center[1] - i * math.cos(math.radians(self.angle + self.boat.angle))
            self.rect.center = (p_x, p_y)
            col = pygame.sprite.collide_mask(river, self)
            if col:
                break
        self.x, self.y = self.rect.topleft

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        pygame.draw.line(screen, (255, 0, 0), self.boat.rect.center, self.rect.center)

    def distance(self, boat):
        return math.sqrt((boat.rect.center[0] - self.rect.center[0]) ** 2 +
                         (boat.rect.center[1] - self.rect.center[1]) ** 2) / self.d


class Player(object):

    def __init__(self, boat):
        self.boat = boat

        self.vision_1 = Vision(self.boat, 1)
        self.vision_2 = Vision(self.boat, 2)
        self.vision_3 = Vision(self.boat, 3)
        self.vision_4 = Vision(self.boat, 4)
        self.vision_5 = Vision(self.boat, 5)

        self.brain = NN()
        self.brain.init_weights()

    def draw(self, screen):
        self.vision_1.draw(screen)
        self.vision_2.draw(screen)
        self.vision_3.draw(screen)
        self.vision_4.draw(screen)
        self.vision_5.draw(screen)
        self.boat.draw(screen)

    def update(self, river):
        self.vision_1.update(river)
        self.vision_2.update(river)
        self.vision_3.update(river)
        self.vision_4.update(river)
        self.vision_5.update(river)

        self.set_f()

    def set_f(self):
        d1 = self.vision_1.distance(self.boat)
        d2 = self.vision_2.distance(self.boat)
        d3 = self.vision_3.distance(self.boat)
        d4 = self.vision_4.distance(self.boat)

        x = self.brain.forward([d1, d2, d3, d4])
        x = x.data.tolist()
        fe, fd = x
        self.boat.fe = fe
        self.boat.fd = fd
