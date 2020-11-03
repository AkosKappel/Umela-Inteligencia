from monk import Monk
import random


class Population:

    def __init__(self, size, puzzle):
        self.generation = 1
        self.size = size
        self.puzzle = puzzle
        self.monks = self.create_monks(size)
        self.fitness_sum = 0

    def __repr__(self):
        return f'Generation({self.generation}), Fitness_sum({self.fitness_sum})'

    def __str__(self):
        return f'Generation({self.generation}), Fitness_sum({self.fitness_sum})'  # TODO remake

    def create_monks(self, size):
        n_genes = self.puzzle.garden.width + self.puzzle.garden.length + len(self.puzzle.rocks)
        return [Monk(self.puzzle.garden.copy(), n_genes) for _ in range(size)]

    def solve_puzzle(self):
        for m in self.monks:
            m.bury_garden()
        self.calculate_fitness()
        self.calculate_fitness_sum()

    def show(self):
        for m in self.monks:
            print(m.garden, '\n', m)

    def calculate_fitness(self):
        for m in self.monks:
            m.calculate_fitness()

    def calculate_fitness_sum(self):
        self.fitness_sum = 0
        for m in self.monks:
            self.fitness_sum += m.fitness

    def natural_selection(self):
        new_monks = []

        for _ in range(self.size // 2):
            # Vyberieme si 2 rodicov s metodou rulety podla ich fitness
            p1 = self.select_parent()
            p2 = self.select_parent()

            # Vytvorime ich deti pomocou krizenia
            new_monks.append(p1.get_child(p2))
            new_monks.append(p2.get_child(p1))

        self.monks = new_monks
        self.generation += 1

    def select_parent(self):
        roulette = random.randrange(self.fitness_sum)
        temp_sum = 0  # Stochasticky vyber (ruleta)
        for m in self.monks:
            temp_sum += m.fitness
            if temp_sum > roulette:
                return m

        print("ERROR YOU KNOW WHERE")
        return None  # Toto by sa nikdy nemalo stat

    def mutate_children(self):
        for m in self.monks:
            for g in m.genes:
                g.mutate()
