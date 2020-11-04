from monk import Monk
import random


class Population:

    def __init__(self, size, puzzle):
        self.size, self.puzzle = size, puzzle
        self.monks = self.create_monks(size)
        self.gen = 1
        self.fitness_sum = 0
        self.max_fitness = sum(row.count(0) for row in puzzle.garden.field)
        self.best = self.monks[0]

    def __repr__(self):  # TODO redo stats
        return f'Gen {self.gen:2d}: Size {self.size}, BestF {self.best.fitness if self.best else 0:3d}, ' \
               f'AvgF {self.fitness_sum / self.size:.2f}, MaxF {self.max_fitness:3d}'

    def create_monks(self, size):
        n_genes = self.puzzle.garden.width + self.puzzle.garden.length + len(self.puzzle.rocks)
        monks = []

        for _ in range(size):
            monk = Monk(self.puzzle.garden.copy())
            monk.generate_genes(n_genes)
            monks.append(monk)

        return monks

    def solve_puzzle(self):
        for m in self.monks:
            m.bury_garden()

    def show_all(self):
        for m in self.monks:
            print(m, '\n')

    def show_best(self):
        print(self.best, '\n')

    def calculate_fitness(self):
        max_fitness = 0
        self.fitness_sum = 0

        for m in self.monks:
            m.calculate_fitness()  # Zistime fitness kazdeho jedinca
            self.fitness_sum += m.fitness  # Spocitame sucet vsetkych fitness hodnot
            if m.fitness > max_fitness:  # Najdeme najlepsieho jedinca
                max_fitness = m.fitness
                self.best = m

        if self.best.fitness >= self.max_fitness:  # Skontrolujeme, ci je uloha vyriesena
            self.puzzle.solved = True

    def natural_selection(self):
        self.best.garden.clear()
        new_monks, new_size = [self.best], 1

        while new_size < self.size:
            # Vyberieme si 2 rodicov s metodou rulety podla ich fitness
            p1 = self.select_parent()
            p2 = self.select_parent()

            # Vytvorime ich deti pomocou krizenia
            c1 = p1.crossover(p2)
            c2 = p2.crossover(p1)

            # Mutujeme deti s predvolenou pravdepodobnostou
            c1.mutate()
            c2.mutate()

            # Pridame deti do nasledujucej generacie
            new_monks.extend((c1, c2))
            new_size += 2

        if new_size != self.size:
            new_monks.pop()
            new_size -= 1

        self.monks, self.size = new_monks, new_size
        self.gen += 1

    def select_parent(self):
        roulette = random.randrange(self.fitness_sum)
        temp_sum = 0  # Stochasticky vyber (ruleta)
        for m in self.monks:
            temp_sum += m.fitness
            if temp_sum > roulette:
                return m

        return None  # Toto by sa nikdy nemalo stat
