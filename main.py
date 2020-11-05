from population import Population
from puzzle import Puzzle
import time


if __name__ == "__main__":
    puzzle = Puzzle('example_1.txt')
    max_gen = 700
    start = time.time()

    # Inicializacia prvej generacie
    population = Population(100, puzzle)
    population.solve_puzzle()
    population.calculate_fitness()
    print(population)

    while population.gen < max_gen and not puzzle.solved:
        # Vytvorime novu generaciu
        population.natural_selection()

        # Pohrabeme zahradu
        population.solve_puzzle()

        # Vypocitame fitness
        population.calculate_fitness()
        print(population)

    population.show_best()
    end = time.time()
    print(f'{end - start:.3f} s')

    # TODO pridaj cislovanie genov (ID) a vypis iba pouzite
    # TODO pridaj kroky a is_dead do fitness funkcie
