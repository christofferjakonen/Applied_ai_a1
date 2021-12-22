from part_1_utils import generate_population, fitness_function
from part_2_utils import get_distances
from matplotlib import pyplot as plt
import numpy as np
from part_1_utils import load_data
from sko.ACA import ACA_TSP
from sko.GA import GA_TSP
import multiprocessing as mp
import time


def random_search(part: int, display: bool = False):
    """
    Part 2.2 and 3.3 of the assignment (depending on the source of the distances).
    Random guessing at a solution.
    I might have misinterpreted what was wanted, but hey.
    :param part: Which part of the assignment to run; 1 or 2.
    :param display: Whether or not to create and display a histogram.
    """

    assert part in [1, 2]  # nobody is going to see this, but why not.

    if part == 1:
        distances = load_data()  # part 2.2, get distances from csv
    elif part == 2:
        distances = get_distances()  # part 3.3, download distances

    fitness_per_generation = []
    for _ in range(10_000):
        population = generate_population(list(distances.keys()), population_size=1)
        fitness_per_generation.append(fitness_function(population, distances))

    print(f"Shortest route traveled guessing randomly had distance {min(fitness_per_generation):_}")

    if display:
        plt.hist(fitness_per_generation)
        plt.xlabel("Distance")
        plt.ylabel("Generations")
        plt.show()


def aco_tsp(part: int):
    """
    Parts 2.3 and 3.6 of the assignment.
    ACO implementation of TSP, with max_iter = [50, 100, 150] or [100, 250, 500] for part 1 and 2 respectively.
    Side-note: the docs for scikit-opt are horrible.
    :param part: Which part of the assignment to run; 1 or 2.
    """

    assert part in [1, 2]  # nobody is going to see this, but why not.

    if part == 1:
        # part 2.3
        max_iter = [50, 100, 150]
        locations = load_data()  # read distances from csv
    elif part == 2:
        # part 3.6
        max_iter = [100, 250, 500]
        locations = get_distances()  # download distances

    def total_distance(routine):
        return sum([dist_mat[routine[i % 120], routine[(i + 1) % 120]] for i in range(120)])

    dist_mat = np.array([[dist for dist in destination.values()] for destination in locations.values()])

    for num in max_iter:
        aco = ACA_TSP(func=total_distance, n_dim=120,
                      size_pop=50, max_iter=num,
                      distance_matrix=dist_mat)
        best_x, best_y = aco.run()
        print(f"Shortest route traveled after {num} generations had distance {best_y:_}")


def greedy_tsp():
    """
    Part 3.4 of the assignment.
    Greedy implementation of TSP.
    Prints the cost of the route, for every starting location, if you always pick the closest next destination.
    """

    distances = get_distances()  # download distances
    costs = []
    for location in distances.keys():
        current = location
        visited = []
        while len(visited) != len(distances.keys()):
            visited.append(current)
            available = {place: value for place, value in distances[current].items() if place not in visited}
            if available:
                current = min(available.items(), key=lambda x: x[1])[0]
        costs.append(fitness_function(visited, distances))

    for start, cost in zip(distances.keys(), costs):
        print(f"Starting in {start} results in cost: {cost}")


def genetic_tsp(parallel: bool = False, output: bool = True, pool: mp.Queue = None):
    """
    For use in part 3.5 in the assignment.
    Genetic implementation of TSP.
    This should probably be in utils, but I'm leaving it here.
    :param parallel: Whether to run the function in parallel or serial.
    :param output: Whether or not to output the results to the console.
    :param pool: Pool used for multiprocessing. Only needed if parallel = True
    """

    def total_distance(routine):
        return sum([dist_mat[routine[i % 120], routine[(i + 1) % 120]] for i in range(120)])

    locations = load_data()
    dist_mat = np.array([[dist for dist in destination.values()] for destination in locations.values()])
    results = []
    for num in [100, 500, 1_000]:
        for mc in [0.001, 0.01, 0.05]:
            ga = GA_TSP(func=total_distance, n_dim=len(locations), size_pop=50, max_iter=num, prob_mut=mc)
            best_x, best_y = ga.run()
            results.append((num, mc, best_y[0]))

    if output:
        for result in results:
            num, mc, cost = result
            print(f"Shortest route traveled after {num} generations, "
                  f"with {mc:.1%} mutation rate, "
                  f"had distance {cost:_}")

    if parallel:
        pool.put(results)
    else:
        return results


def time_genetic_tsp():
    """
    Part 3.5 of the assignment.
    Comparing run time of genetic_TSP in parallel and serial processing.
    """

    mp.freeze_support()  # did not seem to need this, despite running windows. leaving it for safety.
    n_cores = mp.cpu_count()  # 12

    # timing multiprocessing
    start = time.perf_counter()

    qout = mp.Queue()
    processes = [mp.Process(target=genetic_tsp, args=(True, False, qout)) for _ in range(n_cores)]
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    results = [qout.get() for _ in processes]

    print(f"Time with multiprocessing {time.perf_counter() - start:.2f}s")  # ~95 sec

    # timing serial processing
    start = time.perf_counter()

    results = [genetic_tsp(output=False) for _ in range(n_cores)]

    print(f"Time with serial processing {time.perf_counter() - start:.2f}s")  # ~450 sec


def main():
    """You could run all of them at the same time, but I would not advise it."""

    # random_search(part=1)  # if part=1, part 2.2 from the assignment; if part=2, part 3.3 from the assignment.
    # aco_tsp(part=1)  # if part=1, part 2.3 from the assignment; if part=2, part 3.6 from the assignment.
    # greedy_tsp()  # part 3.4 of the assignment.
    time_genetic_tsp()  # part 3.5 of the assignment.


if __name__ == "__main__":
    main()
