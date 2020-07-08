import pygame
from settings import *
import sys
from boat import Boat
from river import River
from player import Player


class Game:

    def __init__(self):

        self.screen = pygame.display.set_mode(CAMERA_SIZE)
        pygame.display.set_caption(TITLE)
        icon = pygame.image.load(PATH_ICON)
        pygame.display.set_icon(icon)
        self.clock = pygame.time.Clock()

        self.group = []

        for i in range(NUM_PLAYER):
            boat = Boat()
            player = Player(boat)
            self.group.append(player)

        self.river = River(self.group)

        self.running = True

    def run(self):
        while self.running:
            self.event()
            self.update()
            self.draw()

            pygame.display.update()

    def update(self):
        dt = self.clock.tick(FPS)
        self.river.update(dt)
        for player in self.group:
            player.update(self.river)

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


def main():

    g = Game()
    g.run()
    pygame.quit()


if __name__ == "__main__":
    pygame.init()
    main()