from particle import Particle
import utils


def part_1(swarm_size: int, epochs: int, w: float, c1: float, c2: float):
    """
    Part 2.1 of the assignment.
    :param swarm_size: How many particles to use in a simulation.
    :param epochs: How many generations to run a simulation for.
    :param w: Inertia constant; how much of a particles speed to carry over between epochs, between 0 - 1.
    :param c1: Cognitive coefficient; how much a particle pull towards its personal best found state, between 0 - 1.
    :param c2: Swarm coefficient; how much a particle pull towards the global best found state, between 0 - 1.
    """

    swarm = [Particle(minmax=1, nv=2, fitness_func=utils.part_1_fitness_function) for _ in range(swarm_size)]

    for _ in range(epochs):
        for particle in swarm:
            particle.evaluate()

        for particle in swarm:
            particle.update_velocity(c1, c2, w)
            particle.update_position()

    print("Part 1")
    print(f"Maximum solution: {list(map(lambda x: round(x, 6), Particle.global_highest_position))}\n"
          f"Maximum fitness: {round(Particle.global_highest_fitness, 6)}\n")


def part_2(swarm_size: int, epochs: int, w: float, c1: float, c2: float):
    """
    Part 3.1 of the assignment.
    :param swarm_size: How many particles to use in a simulation.
    :param epochs: How many generations to run a simulation for.
    :param w: Inertia constant; how much of a particles speed to carry over between epochs, between 0 - 1.
    :param c1: Cognitive coefficient; how much a particle pull towards its personal best found state, between 0 - 1.
    :param c2: Swarm coefficient; how much a particle pull towards the global best found state, between 0 - 1.
    """

    swarm = []
    swarm += [Particle(minmax=1, nv=2, fitness_func=utils.part_2_fitness_function) for _ in range(swarm_size)]
    swarm += [Particle(minmax=-1, nv=2, fitness_func=utils.part_2_fitness_function) for _ in range(swarm_size)]

    for _ in range(epochs):
        for particle in swarm:
            particle.evaluate()

        for particle in swarm:
            particle.update_position()
            particle.update_velocity(c1, c2, w)

    print("Part 2")
    print(f"Maximum solution: {list(map(lambda x: round(x, 6), Particle.global_highest_position))}\n"
          f"Maximum fitness: {round(Particle.global_highest_fitness, 6)}\n"
          f"\n"
          f"Minimum solution: {list(map(lambda x: round(x, 6), Particle.global_lowest_position))}\n"
          f"Minimum fitness: {round(Particle.global_lowest_fitness, 6)}")


def main():
    """
    Setting up constants.
    Only run one part at a time, i didn't bother resetting the results in between.
    """

    # constants set here were the same for both parts.
    Particle.bounds = [(-5.0, 5.0), (-5.0, 5.0)]  # upper and lower bounds of variables
    swarm_size = 50  # number of particles
    epochs = 2_500  # probably a little high but it's not heavy computation so no big time waste.
    w = 0.75  # inertia constant
    c1 = 0.5  # cognitive coefficient
    c2 = 0.75  # swarm coefficient

    # part_1(swarm_size, epochs, w, c1, c2)
    part_2(swarm_size, epochs, w, c1, c2)


if __name__ == "__main__":
    main()
