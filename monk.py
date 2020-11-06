from gene import *


class Monk:

    def __init__(self, garden):
        self.garden = garden
        self.chromosome = []
        self.fitness = 0
        self.n_collected = 0
        self.dead = False

    def __repr__(self):
        return f'\nMonk fitness {self.fitness}\n{str(self.garden)}\n\t' + \
               '\n\t'.join([str(i) + ': ' + str(gene) for i, gene in enumerate(self.chromosome)])

    def generate_genes(self, count):
        genes = []
        x, y = self.garden.length, self.garden.width
        positions = random.sample(range(2 * (x + y)), count)

        for _ in range(count):
            gene = Gene()
            gene.randomize(x, y, position=positions.pop())
            genes.append(gene)

        self.chromosome = genes

    def bury_garden(self):
        n_moves = 0

        for i, gene in enumerate(self.chromosome):
            if self.dead:  # Mnich sa zasekol v strede zahrady
                break

            x, y = gene.pos
            d = gene.dir
            if not self.garden.empty(x, y):  # Nie je mozne vsupit do zahrady
                continue

            turn_index = 0
            n_moves += 1
            while True:
                self.garden.field[y][x] = n_moves  # Vykoname pohyb dopredu
                x, y = self.move(x, y, d)

                if self.garden.is_outside(x, y):  # Dostali sme sa von zo zahrady a ideme na dalsi gen
                    break
                if self.garden.empty(x, y):  # Pokracujeme dalej rovno v ceste
                    continue
                if self.collectable(x, y):  # Ak mozme, tak pozbierame list a pokracujeme v ceste
                    self.n_collected += 1
                    continue

                x, y = self.move(x, y, d, forward=False)  # Ak je na ceste prekazka vratime sa o 1 policko
                d = self.turn(x, y, d, gene.turns[turn_index])  # Zmenime smer pohybu

                turn_index += 1
                turn_index %= len(gene.turns)
                if d is None:  # Zasekli sme sa v strede zahrady
                    self.dead = True
                    break

    @staticmethod
    def move(x, y, d, forward=True):
        if d == directions[0]:
            y = y + 1 if forward else y - 1  # dole
        elif d == directions[1]:
            x = x - 1 if forward else x + 1  # dolava
        elif d == directions[2]:
            y = y - 1 if forward else y + 1  # hore
        else:
            x = x + 1 if forward else x - 1  # doprava
        return x, y

    def turn(self, x, y, d, clockwise):
        # Ak je pohyb mnicha vertikalny, tak ho zmenime na horizontalny
        if d in directions[0::2]:
            return self.turn_horizontal(d, clockwise, self.garden.empty(x - 1, y) or x - 1 == -1,
                                        self.garden.empty(x + 1, y) or x + 1 == self.garden.length)
        else:  # A ak je horizontalny, tak ho zmenime na vertikalny
            return self.turn_vertical(d, clockwise, self.garden.empty(x, y - 1) or y - 1 == -1,
                                      self.garden.empty(x, y + 1) or y + 1 == self.garden.width)

    @staticmethod
    def turn_horizontal(d, clockwise, can_go_left, can_go_right):
        if can_go_right and can_go_left:
            if clockwise:
                if d == directions[0]:
                    return directions[1]
                else:
                    return directions[3]
            else:
                if d == directions[0]:
                    return directions[3]
                else:
                    return directions[1]
        elif can_go_right:
            return directions[3]
        elif can_go_left:
            return directions[1]
        return None

    @staticmethod
    def turn_vertical(d, clockwise, can_go_up, can_go_down):
        if can_go_up and can_go_down:
            if clockwise:
                if d == directions[1]:
                    return directions[2]
                else:
                    return directions[0]
            else:
                if d == directions[1]:
                    return directions[0]
                else:
                    return directions[2]
        elif can_go_up:
            return directions[2]
        elif can_go_down:
            return directions[0]
        return None

    def collectable(self, x, y):
        if not self.garden.is_leaf(x, y):
            return False

        block = self.garden.field[y][x]
        y, o, r = self.garden.n_yellow, self.garden.n_orange, self.garden.n_red

        return (block == -2 and self.n_collected < y) or \
               (block == -3 and y <= self.n_collected < y + o) or \
               (block == -4 and y + o <= self.n_collected < y + o + r)

    def calculate_fitness(self):
        self.fitness = 0
        for line in self.garden.field:
            for block in line:
                if block > 0:
                    self.fitness += 1

    def crossover(self, other, mode=0):
        child = Monk(self.garden.copy())

        if mode == 0:
            # Dedenie jednej casti genov od jedneho rodica a zvysku genov od druheho (napr. 0000111111)
            split = random.randrange(len(self.chromosome) + 1)
            child.chromosome = self.chromosome[:split] + other.chromosome[split:]
        elif mode == 1:
            # Dedenie nahodnych genov od oboch rodicov (napr. 0110100101)
            for i in range(len(self.chromosome)):
                child.chromosome.append(random.choice((self.chromosome[i], other.chromosome[i])))
        elif mode == 2:
            # Dedenie nahodne dlhych celkov chromozomu od oboch rodicov (napr. 0011110000)
            base, length = 0, 0
            new_chromosome = []
            while length != len(self.chromosome):
                length += random.randrange(len(self.chromosome) - length) + 1
                new_chromosome[base:length] = random.choice((self.chromosome[base:length],
                                                             other.chromosome[base:length]))
                base = length
            child.chromosome = new_chromosome
        else:
            # Dedenie vsetkych genov od jedneho rodica (napr. 0000000000)
            child.chromosome = random.choice((self.chromosome, other.chromosome))
            # Vysoka pravdepodobnost mutacie
            child.mutate(0.35)

        return child

    def mutate(self, mutation_rate=0.05, mode=0):
        for i in range(len(self.chromosome)):
            rand = random.random()

            if rand < mutation_rate:
                if mode == 0:
                    # Vytvorime novy gen
                    new_gene = Gene()
                    new_gene.randomize(self.garden.length, self.garden.width)
                    self.chromosome[i] = new_gene
                elif mode == 1:
                    # Vytvorime cely chromozom s novymi genmi
                    self.generate_genes(len(self.chromosome))
                    break
                else:
                    # Vytvorime nove rotacie v gene
                    gene = self.chromosome[i]
                    gene.generate_rotations(len(gene.turns))
