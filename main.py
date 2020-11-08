from population import Population
from puzzle import Puzzle
import time


if __name__ == "__main__":
    puzzle = Puzzle('example_1.txt')
    max_gen = 500

    # Inicializacia prvej generacie
    population = Population(100, puzzle)
    population.solve_puzzle()
    population.calculate_fitness()
    print(population)

    start = time.time()
    while population.gen < max_gen and not puzzle.solved:
        # Vytvorime novu generaciu
        population.natural_selection()

        # Pohrabeme zahradu
        population.solve_puzzle()

        # Vypocitame fitness
        population.calculate_fitness()

        # Vypiseme informacie o aktualnej generacii
        print(population)
    end = time.time()

    print(puzzle)
    population.show_best()
    print(f'{end - start:.3f} s')

    # TODO pridaj kroky a is_dead do fitness funkcie
