from garden import Garden
from puzzle import Puzzle
from monk import Monk
from population import Population
import random

if __name__ == "__main__":
    puzzle = Puzzle('example_1.txt')
    print(puzzle)

    m = Monk(puzzle.garden.copy(), 12)
    m.bury_garden()
    # test = Population(1, puzzle)
    # print(repr(test))
    # print(test)
    print(m.garden)
