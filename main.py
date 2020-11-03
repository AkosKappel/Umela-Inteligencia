from population import Population
from puzzle import Puzzle
import random
import time

if __name__ == "__main__":
    puzzle = Puzzle('example_1.txt')
    print(puzzle)

    # start = time.time()
    population = Population(100, puzzle)

    max_gen = 10
    while population.generation < max_gen:
        population.solve_puzzle()
        print(population)
        population.natural_selection()
        population.mutate_children()
    print(population)

    # end = time.time()
    # print(end - start)
    # population.show()
    # print(repr(population))
    # print(population)
