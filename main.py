from game import Game
from genetic_algorithm.population import Population
from genetic_algorithm.selection import elitism_selection, roulette_wheel_selection, tournament_selection
from genetic_algorithm.mutation import gaussian_mutation, random_uniform_mutation
from genetic_algorithm.crossover import simulated_binary_crossover as SBX
from genetic_algorithm.crossover import uniform_binary_crossover, single_point_binary_crossover
from settings import *
import pygame
from boat import Boat
from river import River
from player import Player


class MainWindows(object):

    def __init__(self):
        self.screen = pygame.display.set_mode(CAMERA_SIZE)
        pygame.display.set_caption(TITLE)
        icon = pygame.image.load(PATH_ICON)
        pygame.display.set_icon(icon)

        self.gen = Generation(self.screen)

    def run(self):
        for i in range(2):
            self.gen.run()
            self.gen.update()


class Generation(object):

    def __init__(self, screen):
        self.screen = screen

        # LOAD POPULATION
        self.group = []
        self.load(LOAD_PATH)
        self.population = Population(self.group)
        self.game = Game(self.group, self.screen)

        self.cfg = GA_SETTINGS
        self._mutation_bins = np.cumsum([self.cfg['probability_gaussian'],
                                         self.cfg['probability_random_uniform']
                                         ])
        self._crossover_bins = np.cumsum([self.cfg['probability_SBX'],
                                          self.cfg['probability_SPBX']
                                          ])
        self._SPBX_type = self.cfg['SPBX_type'].lower()
        self._mutation_rate = self.cfg['mutation_rate']
        self._next_gen_size = self.cfg['num_offspring']
        self.current_generation = 0

    def save(self, path):
        # TODO
        pass

    def load(self, path):
        self.group = []
        if path is None:
            for i in range(NUM_PLAYER):
                boat = Boat()
                player = Player(boat)
                self.group.append(player)
        else:
            # TODO
            raise Exception("Load not implemented")

    def run(self):
        self.game.run()

    def update(self):
        print('======================= Generation {} ======================='.format(self.current_generation))
        print('----Max fitness:', self.population.fittest_individual)
        print('----Best Score:', self.population.fittest_individual.score)
        print('----Average fitness:', self.population.average_fitness)
        self.load(None)
        self.game = Game(self.group, self.screen)

    def next_generation(self):
        pass
    
    def _increment_generation(self):
        self.current_generation += 1

def main():
    mw = MainWindows()
    mw.run()
    pygame.quit()


if __name__ == "__main__":
    pygame.init()
    main()
