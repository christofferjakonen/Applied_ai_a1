import math
from math import atan, cos, sin


def part_1_fitness_function(x1, x2):
    """Fitness function for part 2.1"""
    return math.pow(math.cos(x1) + math.sin(x2), 2) / (1 + abs(x1) + abs(x2))


def part_2_fitness_function(x1, x2):
    """Fitness function for part 3.1"""
    p1 = math.pow(math.e, -0.05 * (math.pow(x1, 2) + math.pow(x2, 2)))
    p2 = atan(x1) - atan(x2) + math.pow(math.e, -(x1**2 + x2**2)) * math.pow(cos(x1), 2) * math.pow(sin(x2), 2)
    return p1 * p2
