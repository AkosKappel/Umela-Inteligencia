import random
directions = ('down', 'left', 'up', 'right')  # Vsetky mozne smery pohybu po zahrade
positions_map = {}


class Population:

    puzzle = None

    def __init__(self, size, puzzle):
        self.size, Population.puzzle = size, puzzle
        Gene.create_mapping(puzzle.garden.length, puzzle.garden.width)
        self.monks = self.create_monks(size)
        self.gen = 1
        self.total_fitness = 0
        self.best, self.worst = self.monks[0], self.monks[-1]
        self.max_fitness = sum(row.count(0) for row in puzzle.garden.field)
        self.max_fitness += puzzle.garden.n_yellow + puzzle.garden.n_orange + puzzle.garden.n_red

    def __repr__(self):  # TODO redo stats
        return f'Gen {self.gen:2d}: Size {self.size}, BestF {self.best.fitness if self.best else 0:3d}, ' \
               f'AvgF {self.total_fitness / self.size:.2f}, MaxF {self.max_fitness:3d}'

    @staticmethod
    def create_monks(size):
        """
        Vytvori populaciu s danym poctom jedincov.

        :param size: mnozstvo jedincov
        :return: zoznam jedincov
        """
        monks = []
        garden = Population.puzzle.garden
        n = garden.width + garden.length + len(Population.puzzle.rocks)

        for _ in range(size):
            monk = Monk(garden.copy())
            monk.chromosome = monk.generate_genes(n)
            monks.append(monk)

        return monks

    def solve_puzzle(self):  # Kazdy mnich pohrabe zahradu
        for m in self.monks:
            m.solve()

    def show_all(self):  # Vypis vsetkych mnichov v aktualnej populacii
        for m in self.monks:
            print(m, '\n')

    def show_best(self):  # Vypis najlepsieho mnicha v aktualnej populacii
        print(self.best, '\n')

    def calculate_fitness(self):
        """
        Vypocita fitnes kazdeho jedinca, zisti celkovu fitnes populacie
        a urci najlepsieho a najhorsieho jedinca v aktualnej generacii.

        :return: None
        """
        min_fitness = self.max_fitness
        max_fitness = 0
        self.total_fitness = 0

        for m in self.monks:
            m.calculate_fitness()  # Zistime fitness kazdeho jedinca
            self.total_fitness += m.fitness  # Spocitame sucet vsetkych fitness hodnot

            if m.fitness > max_fitness:  # Najdeme najlepsieho jedinca
                max_fitness = m.fitness
                self.best = m

            if m.fitness < min_fitness:  # Najdeme najhorsieho jedinca
                min_fitness = m.fitness
                self.worst = m

        # TODO monk must be alive for solution
        if self.best.fitness >= self.max_fitness:  # Skontrolujeme, ci je uloha vyriesena
            Population.puzzle.solved = True

    def natural_selection(self):
        # Elitarizmus = najlepsi jedinec prechadza do dalsej generacie bez mutacie
        best_monk = Monk(Population.puzzle.garden.copy())
        best_monk.chromosome = self.best.chromosome
        new_monks, new_size = [best_monk], 1  # TODO remove elitarism ?

        # Pridame novu krv do novej generacie
        n_new_blood = int(0.10 * self.size)
        new_monks += self.create_monks(n_new_blood)

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
        roulette = random.randrange(self.total_fitness)
        temp_sum = 0  # Stochasticky vyber (ruleta)
        for m in self.monks:
            temp_sum += m.fitness
            if temp_sum > roulette:
                return m

        return None  # Toto by sa nikdy nemalo stat


class Monk:

    def __init__(self, garden):
        self.garden = garden
        self.chromosome = []
        self.fitness = 0
        self.n_collected = 0  # Pocet pozbieranych listov
        self.used_genes = []
        self.dead = False

    def __repr__(self):
        return f'{str(self.garden)}\nMonk - fitness {self.fitness}, genes {len(self.chromosome)}\n\t' + \
               '\n\t'.join([str(i + 1) + ': ' + str(gene) for i, gene in enumerate(self.used_genes)])

    def generate_genes(self, count):
        """
        Vytvori novy chromozom s danym poctom genov.

        :param count: pocet genov
        :return: None
        """
        return [Gene(position) for position in random.sample(
            range(2 * (self.garden.length + self.garden.width)), count)]

    def solve(self):
        """
        Hlavna funkcia na pohrabanie zahrady.

        :return: None
        """
        n_moves = 0

        for gene in self.chromosome:
            if self.dead:  # Mnich sa zasekol v strede zahrady
                break

            x, y = positions_map[gene.pos]
            d = gene.get_direction()
            if not self.garden.empty(x, y):  # Nie je mozne vsupit do zahrady
                continue

            self.used_genes.append(gene)
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
        """
        Zisti, ci sa na policku nachadza list a ci ho moze zobrat.

        :param x: x-ova suradnica policka
        :param y: y-ova suradnica policka
        :return: True ak list mozme zobrat, inak False
        """
        if not self.garden.is_leaf(x, y):  # Skontrolujeme, ci dane policko obsahuje list
            return False

        block = self.garden.field[y][x]
        y, o, r = self.garden.n_yellow, self.garden.n_orange, self.garden.n_red

        # Zistime, ci mozeme pozbierat list na danom policku
        return (block == -2 and self.n_collected < y) or \
               (block == -3 and y <= self.n_collected < y + o) or \
               (block == -4 and y + o <= self.n_collected < y + o + r)

    def calculate_fitness(self):
        """
        Vypocita fitnes hodnotu jedinca.

        :return: None
        """
        self.fitness = 0
        for line in self.garden.field:
            for block in line:
                if block > 0:
                    self.fitness += 1

    def crossover(self, other, mode=0):
        """
        Krizenie jedincov.

        :param other: druhy jedinec
        :param mode: sposob krizenia (0, 1, 2, 3)
        :return: novy jedinec
        """
        child = Monk(Population.puzzle.garden.copy())

        if mode == 0:
            # Dedenie jednej casti genov od jedneho rodica a zvysku genov od druheho (napr. 0000111111)
            split = random.randrange(len(self.chromosome) + 1)
            child.chromosome = self.chromosome[:split] + other.chromosome[split:]
            # if len(set(child.chromosome)) != len(child.chromosome):
            #     print('ERROR')  # TODO continue
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
        elif mode == 3:
            # Dedenie vsetkych genov od jedneho rodica (napr. 0000000000)
            child.chromosome = random.choice((self.chromosome, other.chromosome))
            # Ziadne krizenie iba mutacia
            child.mutate(1.00)

        return child

    def mutate(self, mutation_rate=0.05, mode=0):
        """
        Mutacia jedinca.

        :param mutation_rate: pravdepodobnost mutacie
        :param mode: sposob mutacie (0, 1, 2, 3)
        :return: None
        """
        if mode == 0:
            # Niektore geny zmenime na nove
            for i in range(len(self.chromosome)):
                if random.random() < mutation_rate:
                    new_gene = Gene()
                    self.chromosome[i] = new_gene
        elif mode == 1:
            # Vytvorime nove rotacie v gene
            for i in range(len(self.chromosome)):
                if random.random() < mutation_rate:
                    gene = self.chromosome[i]
                    gene.generate_turns(len(gene.turns))
        elif mode == 2:
            # Vytvorime cely chromozom s novymi genmi
            if random.random() < mutation_rate:
                self.chromosome = self.generate_genes(len(self.chromosome))
        elif mode == 3:
            # Zamenime poradie genov v chromozome
            if random.random() < mutation_rate:
                random.shuffle(self.chromosome)


class Gene:

    length, width = 0, 0

    def __init__(self, position=None, n_turns=6):
        random.seed()
        if not position:
            position = random.randrange(2 * (Gene.length + Gene.width))

        self.pos = position  # Nastavime zaciatocnu polohu, kde ma mnich vstupit do zahrady
        # Vygenerujeme nahodne otacania pre pripad, ak mnich narazi na prekazku v ceste
        self.turns = self.generate_turns(n_turns)

    def __repr__(self):
        return f'{positions_map[self.pos]}, {self.get_direction()}, {self.turns}'

    def __eq__(self, other):
        return self.pos == other.pos

    def __hash__(self):
        return hash(self.pos)

    def get_direction(self):
        if 0 <= self.pos < Gene.length:
            return directions[0]  # Pohyb z hornej casti smerom dole
        elif Gene.length <= self.pos < Gene.length + Gene.width:
            return directions[1]  # Pohyb z pravej strany smerom dolava
        elif Gene.length + Gene.width <= self.pos < 2 * Gene.length + Gene.width:
            return directions[2]  # Pohyb z dolnej casti smerom hore
        else:
            return directions[3]  # Pohyb z lavej strany smerom doprava

    @staticmethod
    def create_mapping(length, width):
        # Kazdemu moznemu vstupu do zahrady priradime unikatnu hodnotu na jej identifikaciu, napr.:
        #      0  1  2  3
        #   13 .  .  .  . 4
        #   12 .  .  .  . 5
        #   11 .  .  .  . 6
        #     10  9  8  7
        Gene.length, Gene.width = length, width
        for num in range(2 * (length + width)):
            if 0 <= num < length:
                d = {num: (num, 0)}
            elif length <= num < length + width:
                d = {num: (length - 1, num - length)}
            elif length + width <= num < 2 * length + width:
                d = {num: (2 * length + width - 1 - num, width - 1)}
            else:
                d = {num: (0, 2 * (length + width) - 1 - num)}
            positions_map.update(d)

    @staticmethod
    def generate_turns(count):
        # Generujeme poradie, v akom sa otacame ak narazime na prekazku
        # 1 - otocenie v smere hodinovych ruciciek
        # 0 - otocenie v protismere hodinovych ruciciek
        n_clockwise_turns = random.randrange(count + 1)
        turns = [1] * n_clockwise_turns + [0] * (count - n_clockwise_turns)
        random.shuffle(turns)
        return turns
