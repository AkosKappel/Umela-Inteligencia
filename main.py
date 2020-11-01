from garden import Garden
from puzzle import Puzzle
from population import Population
import random

if __name__ == "__main__":
    puzzle = Puzzle('example_1.txt')
    print(puzzle)
    test = Population(3, puzzle)
    print(repr(test))
    print(test)
