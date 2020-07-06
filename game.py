import pygame
from settings import *
import sys
from boat import Boat
from river import River


class Game:

    def __init__(self):

        self.screen = pygame.display.set_mode(CAMERA_SIZE)
        pygame.display.set_caption(TITLE)
        icon = pygame.image.load(PATH_ICON)
        pygame.display.set_icon(icon)

        self.clock = pygame.time.Clock()
        self.boat_1 = Boat()
        self.group = []
        self.group.append(self.boat_1)
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

    def event(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                print("TODO")

    def draw(self):

        self.screen.fill(COLOR_RIVER)
        self.river.draw(self.screen)
        for boat in self.group:
            boat.draw(self.screen)


def main():

    g = Game()
    g.run()
    pygame.quit()


if __name__ == "__main__":
    pygame.init()
    main()