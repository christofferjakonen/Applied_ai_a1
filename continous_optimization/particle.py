import numpy as np
import sys


class Particle(object):
    global_highest_fitness = -sys.maxsize
    global_lowest_fitness = sys.maxsize
    global_highest_position = []
    global_lowest_position = []
    bounds = []

    def __init__(self, minmax: int, nv: int, fitness_func):
        """
        Particle object used in PSO for either maximization or minimization of a given function.
        :param minmax: if maximization, set to 1; if minimization, set to -1.
        :param nv: number of variables / particle.
        :param fitness_func: function to use for evaluation.
        """
        self.minmax = minmax
        self.nv = nv
        self.fitness_function = fitness_func
        self.velocity = []
        self.position = []
        self.local_best_position = []

        if self.minmax == 1:
            self.fitness = -sys.maxsize
            self.local_best_fitness = -sys.maxsize
        elif self.minmax == -1:
            self.fitness = sys.maxsize
            self.local_best_fitness = sys.maxsize
        else:
            raise Exception("Neither maximization or minimization was set.")

        for i in range(self.nv):
            self.position.append(np.random.uniform(*Particle.bounds[i]))
            self.velocity.append(np.random.uniform(-1, 1))

    def evaluate(self):
        self.fitness = self.fitness_function(*self.position)

        if self.minmax == 1:
            if self.fitness > self.local_best_fitness:
                self.local_best_fitness = self.fitness
                self.local_best_position = self.position

            if self.fitness > Particle.global_highest_fitness:
                Particle.global_highest_fitness = self.fitness
                Particle.global_highest_position = list(self.position)

        elif self.minmax == -1:
            if self.fitness < self.local_best_fitness:
                self.local_best_fitness = self.fitness
                self.local_best_position = self.position

            if self.fitness < Particle.global_lowest_fitness:
                Particle.global_lowest_fitness = self.fitness
                Particle.global_lowest_position = list(self.position)

    def update_velocity(self, c1, c2, w):
        for i in range(self.nv):
            r1 = np.random.random()
            r2 = np.random.random()

            cognitive_velocity = c1 * r1 * (self.local_best_position[i] - self.position[i])

            if self.minmax == 1:
                social_velocity = c2 * r2 * (Particle.global_highest_position[i] - self.position[i])

            elif self.minmax == -1:
                social_velocity = c2 * r2 * (Particle.global_lowest_position[i] - self.position[i])

            self.velocity[i] = w * self.velocity[i] + cognitive_velocity + social_velocity

    def update_position(self):
        for i in range(self.nv):
            self.position[i] += self.velocity[i]

            if self.position[i] > Particle.bounds[i][1]:
                self.position[i] = Particle.bounds[i][1]
            elif self.position[i] < Particle.bounds[i][0]:
                self.position[i] = Particle.bounds[i][0]
