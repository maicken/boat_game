from typing import List, Tuple

from NN import NN
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
import random
import math
import os
import torch

class MainWindows(object):

    def __init__(self):
        self.screen = pygame.display.set_mode(CAMERA_SIZE)
        pygame.display.set_caption(TITLE)
        icon = pygame.image.load(PATH_ICON)
        pygame.display.set_icon(icon)

        self.gen = Generation(self.screen)

    def run(self):
        for i in range(END_GENERATION):
            self.gen.run()
            self.gen.update()
        self.gen.save()


class Generation(object):

    def __init__(self, screen):
        self.screen = screen

        # LOAD POPULATION
        self.group = []
        self.load()
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
        self._SBX_eta = self.cfg['SBX_eta']
        self._mutation_rate = self.cfg['mutation_rate']
        self._next_gen_size = self.cfg['num_offspring']
        self.current_generation = 0

    def save(self):
        os.makedirs(SAVE_PATH, exist_ok=True)
        save_dict = {'generation': self.current_generation}
        for i, ind in enumerate(self.population.individuals):
            str_ind = 'ind_'+str(i)
            save_dict[str_ind] = ind.brain.state_dict()
        torch.save(save_dict, os.path.join(SAVE_PATH, SAVE_NAME))

    def load(self):
        self.group = []
        for i in range(NUM_PLAYER):
            boat = Boat()
            brain = NN()
            brain.init_weights()
            player = Player(brain, boat)
            self.group.append(player)

        if LOAD_PATH is not None:
            checkpoint = torch.load(LOAD_PATH)
            self.current_generation = checkpoint['generation']
            for i, ind in enumerate(self.group):
                str_ind = 'ind_' + str(i)
                ind.brain.load_state_dict(checkpoint[str_ind])
                ind.brain.eval()

    def run(self):
        self.game.run()

    def update(self):
        print('======================= Generation {} ======================='.format(self.current_generation))
        print('----Max fitness:', self.population.fittest_individual)
        print('----Best Score:', self.population.fittest_individual.score)
        print('----Average fitness:', self.population.average_fitness)
        self.next_generation()
        self.game = Game(self.group, self.screen)

    def next_generation(self):
        self._increment_generation()
        # Calculate fitness of individuals
        for individual in self.population.individuals:
            individual.calculate_fitness()

        self.population.individuals = elitism_selection(self.population, self.cfg['num_parents'])
        random.shuffle(self.population.individuals)

        next_pop: List[Player] = []
        while len(next_pop) < self._next_gen_size:
            p1, p2 = roulette_wheel_selection(self.population, 2)

            L = p1.brain.layer_nodes
            c1_params = {}
            c2_params = {}

            # Each W_l and b_l are treated as their own chromosome.
            # Because of this I need to perform crossover/mutation on each chromosome between parents
            for l in range(0, L, 2):
                p1_W_l = p1.brain.net[l].weight.data.numpy()
                p2_W_l = p2.brain.net[l].weight.data.numpy()
                p1_b_l = np.array([p1.brain.net[l].bias.data.numpy()])
                p2_b_l = np.array([p2.brain.net[l].bias.data.numpy()])

                # Crossover
                # @NOTE: I am choosing to perform the same type of crossover on the weights and the bias.
                c1_W_l, c2_W_l, c1_b_l, c2_b_l = self._crossover(p1_W_l, p2_W_l, p1_b_l, p2_b_l)

                # Mutation
                # @NOTE: I am choosing to perform the same type of mutation on the weights and the bias.
                self._mutation(c1_W_l, c2_W_l, c1_b_l, c2_b_l)

                # Assign children from crossover/mutation
                c1_params['W' + str(l)] = c1_W_l
                c2_params['W' + str(l)] = c2_W_l
                c1_params['b' + str(l)] = c1_b_l
                c2_params['b' + str(l)] = c2_b_l

                # Clip to [-1, 1]
                np.clip(c1_params['W' + str(l)], -1, 1, out=c1_params['W' + str(l)])
                np.clip(c2_params['W' + str(l)], -1, 1, out=c2_params['W' + str(l)])
                np.clip(c1_params['b' + str(l)], -1, 1, out=c1_params['b' + str(l)])
                np.clip(c2_params['b' + str(l)], -1, 1, out=c2_params['b' + str(l)])

            # Create children from chromosomes generated above
            brain = NN()
            boat = Boat()
            brain.transform_weights(c1_params)
            p1 = Player(brain, boat)

            brain = NN()
            boat = Boat()
            brain.transform_weights(c2_params)
            p2 = Player(brain, boat)

            # Add children to the next generation
            next_pop.extend([p1, p2])

        # Set the next generation
        random.shuffle(next_pop)
        self.group = next_pop
        self.population = Population(self.group)

    def _increment_generation(self):
        self.current_generation += 1

    def _crossover(self, parent1_weights: np.ndarray, parent2_weights: np.ndarray, parent1_bias: np.ndarray,
                   parent2_bias: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:

        rand_crossover = random.random()
        crossover_bucket = np.digitize(rand_crossover, self._crossover_bins)
        child1_weights, child2_weights = None, None
        child1_bias, child2_bias = None, None

        # SBX
        if crossover_bucket == 0:
            child1_weights, child2_weights = SBX(parent1_weights, parent2_weights, self._SBX_eta)
            child1_bias, child2_bias = SBX(parent1_bias, parent2_bias, self._SBX_eta)

        # Single point binary crossover (SPBX)
        elif crossover_bucket == 1:
            child1_weights, child2_weights = single_point_binary_crossover(parent1_weights, parent2_weights,
                                                                           major=self._SPBX_type)
            child1_bias, child2_bias = single_point_binary_crossover(parent1_bias, parent2_bias, major=self._SPBX_type)

        else:
            raise Exception('Unable to determine valid crossover based off probabilities')

        return child1_weights, child2_weights, child1_bias, child2_bias

    def _mutation(self, child1_weights: np.ndarray, child2_weights: np.ndarray,
                  child1_bias: np.ndarray, child2_bias: np.ndarray) -> None:
        scale = .2
        rand_mutation = random.random()
        mutation_bucket = np.digitize(rand_mutation, self._mutation_bins)

        mutation_rate = self._mutation_rate
        if self.cfg['mutation_rate_type'].lower() == 'decaying':
            mutation_rate = mutation_rate / math.sqrt(self.current_generation + 1)

        # Gaussian
        if mutation_bucket == 0:
            # Mutate weights
            gaussian_mutation(child1_weights, mutation_rate, scale=scale)
            gaussian_mutation(child2_weights, mutation_rate, scale=scale)

            # Mutate bias
            gaussian_mutation(child1_bias, mutation_rate, scale=scale)
            gaussian_mutation(child2_bias, mutation_rate, scale=scale)

        # Uniform random
        elif mutation_bucket == 1:
            # Mutate weights
            random_uniform_mutation(child1_weights, mutation_rate, -1, 1)
            random_uniform_mutation(child2_weights, mutation_rate, -1, 1)

            # Mutate bias
            random_uniform_mutation(child1_bias, mutation_rate, -1, 1)
            random_uniform_mutation(child2_bias, mutation_rate, -1, 1)

        else:
            raise Exception('Unable to determine valid mutation based off probabilities.')

def main():
    mw = MainWindows()
    mw.run()
    pygame.quit()


if __name__ == "__main__":
    pygame.init()
    main()
