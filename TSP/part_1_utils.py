from random import shuffle
from copy import copy
import csv
from collections import defaultdict


def load_data() -> defaultdict:
    """
    Load distances from csv file and format it as something more workable.
    :return: Dict containing dicts containing distances. It's a distance matrix in dict form, if you will.
    """

    with open("../data/distances.csv", "r") as file:
        distances = defaultdict(dict)
        for row in csv.DictReader(file):
            distances[row["Start"]][row["Target"]] = int(row["Distance"])
    return distances


def generate_population(destinations: list[str], population_size: int = 20):
    """
    Generates a population of given size containing legal routes (no repeats) between given locations.
    :param destinations: List of the locations to be included in the solutions.
    :param population_size: How many solutions to generate.
    :return: List of generated solutions.
    """

    assert population_size > 0
    population = [copy(destinations) for _ in range(population_size)]
    for genome in population:
        shuffle(genome)

    return population if population_size > 1 else population[0]


def fitness_function(solution: list[str], distances: defaultdict) -> int:
    """
    Fitness function for evaluating solutions.
    Was going to make something nicer until I saw that we were supposed to use scikit-opt for most of the assignment.
    :param solution: List of the names of locations.
    :param distances: Dict with the distanced between the locations.
    :return: Sum distance/cost of a solution.
    """

    distance = 0
    for i in range(1, len(solution)):
        distance += distances[solution[i-1]][solution[i]]

    return distance
