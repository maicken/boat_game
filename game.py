import pygame
from settings import *
import sys
from boat import Boat
from river import River
from player import Player


class Game:

    def __init__(self, group, screen):

        self.screen = screen
        self.clock = pygame.time.Clock()
        self.group = group
        self.river = River(self.group)

        self.running = True
        self.time_run = 0

    def run(self):
        while self.running:
            self.event()
            self.update()
            self.draw()

            pygame.display.update()

    def update(self):
        dt = self.clock.tick(FPS)
        self.time_run += dt
        self.river.update(dt)

        end = True
        for player in self.group:
            player.update(self.river)
            if player.boat.movement:
                end = False
        if end or self.time_run > TIME_MAX * 1000:
            for player in self.group:
                player.calculate_fitness()
            self.running = False

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                sys.exit()

    def draw(self):
        self.screen.fill(COLOR_RIVER)
        self.river.draw(self.screen)
        for player in self.group:
            player.draw(self.screen)
