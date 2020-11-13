import random
import time

# Pomocne globalne premenne:
block_counter = {}  # Pocetnost roznych typov blokov v zahrade
input_blocks = {  # Reprezentacia blokov pri nacitavani zahrady z textoveho suboru
    'K': -1,  # Kamene
    'Z': -2,  # Zlte listy
    'O': -3,  # Oranzove listy
    'C': -4   # Cervene listy
}
output_blocks = {  # Reprezentacia blokov pri vypisovani zahrady
    -1: '\33[30mK\33[0m',
    -2: '\33[93mZ\33[0m',
    -3: '\33[33mO\33[0m',
    -4: '\33[31mC\33[0m'
}
positions_ID = {}  # Zoznam identifikatorov vstupnych pozicii do zahrady
directions = ('down', 'left', 'up', 'right')  # Vsetky mozne smery pohybu po zahrade
length, width = 0, 0  # Rozmery zahrady
max_fitness = 0  # Maximalna ziskatelna fitnes
solved = False  # Urcuje, ci sa podarilo uspesne pohrabat celu zahradu

# Nastavitelne parametre:
max_generation = 300


def main():
    # Inicializacia prvej generacie
    monks = Population(50)
    monks.solve_puzzle()
    print(monks)

    start = time.time()
    while monks.generation < max_generation and not solved:
        monks.natural_selection()  # Vytvorime novu generaciu
        monks.solve_puzzle()  # Pohrabeme zahradu
        print(monks)  # Vypiseme informacie o aktualnej generacii
    end = time.time()

    print(puzzle)
    monks.show_best()
    print(f'{end - start:.3f} s')

# ----------------------------------------------------------------------------------------------------


def load_puzzle(file_name):
    field = []
    garden = Garden(field)

    # Nacitame zahradu z externeho suboru
    with open(file_name, 'r') as file:

        for i, line in enumerate(file.readlines()):
            field.append([])

            for block in line.split():
                block = input_blocks.get(block.upper(), 0)
                block_counter.setdefault(block, 0)

                # Spocitame pocet kazdeho bloku v zahrade
                block_counter[block] += 1
                field[i].append(block)

    # Zapiseme si rozmery zahrady
    global width, length
    width = len(field)
    length = len(field[0])

    # Kazdemu moznemu vstupu do zahrady priradime identifikacne cislo
    init_positions_ID()

    # Vypocitame maximalnu ziskatelnu fitnes hodnotu
    global max_fitness
    max_fitness = length * width - block_counter[-1] + 1

    return garden


def init_positions_ID():
    # Kazdemu vstupu do zahrady priradime unikatnu hodnotu na jej identifikaciu.
    # Napriklad pre zahradu 3 x 4 by sme pridelili tieto hodnoty:
    #       0  1  2  3
    #   13  .  .  .  .  4
    #   12  .  .  .  .  5
    #   11  .  .  .  .  6
    #      10  9  8  7

    for num in range(2 * (length + width)):
        if 0 <= num < length:
            mapping = {num: (num, 0)}
        elif length <= num < length + width:
            mapping = {num: (length - 1, num - length)}
        elif length + width <= num < 2 * length + width:
            mapping = {num: (2 * length + width - 1 - num, width - 1)}
        else:
            mapping = {num: (0, 2 * (length + width) - 1 - num)}
        positions_ID.update(mapping)

# ----------------------------------------------------------------------------------------------------


class Garden:

    def __init__(self, matrix):
        self.field = matrix

    def __repr__(self):
        return f'size({width}, {length}), ' \
               f'rocks({block_counter[-1] if -1 in block_counter.keys() else 0}) ' \
               f'leaves{self.get_leaves_count()}'

    def __str__(self):
        s = '\n'
        for y in range(width):
            for x in range(length):
                if self.field[y][x] in output_blocks.keys():
                    s += f'   {output_blocks.get(self.field[y][x])}'
                else:
                    s += f'{self.field[y][x]}'.rjust(4, ' ')
            s += '\n'
        return s

    def copy(self):
        """
        Vytvori novu kopiu zahrady.

        :return: nova zahrada
        """
        field = []

        for row in self.field:
            field.append([0 if block > 0 else block for block in row])

        return Garden(field)

    def empty(self, x, y):  # Skontroluje, ci dane policko je prazdne
        if Garden.outside(x, y):
            return False
        return self.field[y][x] == 0

    def leaf(self, x, y):  # Zisti, ci policko obsahuje list
        if Garden.outside(x, y):
            return False
        return self.field[y][x] != -1 and self.field[y][x] in output_blocks.keys()

    @staticmethod
    def outside(x, y):  # Overi, ci pozicia je mimo zahrady
        return x < 0 or x >= length or y < 0 or y >= width

    @staticmethod
    def get_leaves_count():  # Vrati pocet vsetkych farieb listov v zahrade
        return (block_counter[-2] if -2 in block_counter.keys() else 0,
                block_counter[-3] if -3 in block_counter.keys() else 0,
                block_counter[-4] if -4 in block_counter.keys() else 0)

# ----------------------------------------------------------------------------------------------------


class Gene:

    def __init__(self, position, n_turns=6):
        self.position = position
        # Generujeme poradie, v akom sa otacame ak narazime na prekazku
        # 1 - otocenie v smere hodinovych ruciciek
        # 0 - otocenie v protismere hodinovych ruciciek
        rand = random.randrange(2 ** n_turns)
        self.turns = format(rand, f'0{n_turns}b')

    def __repr__(self):
        return f'{self.position} {self.turns} {positions_ID[self.position]} {self.get_direction()}'

    def __str__(self):
        return f'{self.position} {self.turns} {positions_ID[self.position]} {self.get_direction()}'

    def __eq__(self, other):
        return self.position == other.position

    def __hash__(self):
        return hash(self.position)

    def get_direction(self):  # Zisti smer pohybu zo zaciatocnej pozicie zahrady
        if 0 <= self.position < length:
            return directions[0]  # Pohyb z hornej casti smerom dole
        elif length <= self.position < length + width:
            return directions[1]  # Pohyb z pravej strany smerom dolava
        elif length + width <= self.position < 2 * length + width:
            return directions[2]  # Pohyb z dolnej casti smerom hore
        else:
            return directions[3]  # Pohyb z lavej strany smerom doprava

# ----------------------------------------------------------------------------------------------------


class Individual:

    def __init__(self, garden):
        self.garden = garden
        self.chromosome = []  # Zoznam genov
        self.fitness = 0
        self.collected = 0  # Pocet pozbieranych listov
        self.used_genes = []
        self.x, self.y = None, None
        self.direction = None

    def __repr__(self):
        return f'fitness {self.fitness}, genes {len(self.chromosome)}, collected {self.collected}'

    def __str__(self):
        return f'{str(self.garden)}\nfitness {self.fitness}, genes {len(self.chromosome)}\n\t' + \
               '\n\t'.join([str(i + 1) + ': ' + repr(gene) for i, gene in enumerate(self.used_genes)])

    @staticmethod
    def create_genes(count):
        """
        Vytvori novy chromozom so zadanym poctom genov.

        :param count: pocet genov
        :return: None
        """
        return [Gene(pos_id) for pos_id in random.sample(range(2 * (length + width)), count)]

    def calculate_fitness(self):
        """
        Vypocita fitnes hodnotu daneho jedinca.

        :return: fitnes jedinca
        """
        fitness = 0

        for line in self.garden.field:
            for block in line:
                if block > 0:
                    fitness += 1

        return fitness

    def solve_garden(self):
        """
        Jedinec pohrabe zahradu podla instrukcii v chromozome. Pocas prehrabavania zahrady
        sa vypocita aj fitnes jedinca.

        :return: fitnes hodnota jedinca
        """
        fitness = 0
        survived = True
        move_counter = 0

        for gene in self.chromosome:
            if not survived:
                break

            self.x, self.y = positions_ID[gene.position]
            if not self.garden.empty(self.x, self.y):  # Nie je mozne vsupit do zahrady
                continue

            self.direction = gene.get_direction()
            self.used_genes.append(gene)
            turn_index = 0
            move_counter += 1

            while True:
                self.garden.field[self.y][self.x] = move_counter  # Vykoname pohyb dopredu
                fitness += 1
                self.move()

                if self.garden.outside(self.x, self.y):  # Dostali sme sa von zo zahrady a ideme na dalsi gen
                    break
                if self.garden.empty(self.x, self.y):  # Pokracujeme dalej rovno v ceste
                    continue
                if self.can_collect():  # Ak mozeme, tak pozbierame list a pokracujeme v ceste
                    self.collected += 1
                    continue

                fitness -= 1
                self.move(forward=False)  # Ak je na ceste prekazka vratime sa o 1 policko
                self.turn(bool(int(gene.turns[turn_index])))  # Zmenime smer pohybu

                turn_index += 1
                turn_index %= len(gene.turns)

                if self.direction is None:  # Zasekli sme sa v strede zahrady
                    survived = False
                    fitness += 1
                    break

        if survived:
            fitness += 1
        else:  # Bodovy postih pre jedinca, ktory sa zasekol v zahrade
            fitness *= 0.5
            fitness = int(fitness)

        if fitness >= max_fitness:
            global solved
            solved = True

        return fitness

    def move(self, forward=True):
        if self.direction == directions[0]:
            self.y = self.y + 1 if forward else self.y - 1  # Dole
        elif self.direction == directions[1]:
            self.x = self.x - 1 if forward else self.x + 1  # Dolava
        elif self.direction == directions[2]:
            self.y = self.y - 1 if forward else self.y + 1  # Hore
        else:
            self.x = self.x + 1 if forward else self.x - 1  # Doprava

    def turn(self, clockwise=True):
        if self.direction in directions[0::2]:  # Vertikalny pohyb zmenime na horizontalny
            can_go_left = self.garden.empty(self.x - 1, self.y) or self.x == 0
            can_go_right = self.garden.empty(self.x + 1, self.y) or self.x + 1 == length

            if can_go_right and can_go_left:  # Ak mame na vyber, rozhodne informacia v gene
                if clockwise:
                    self.direction = directions[1] if self.direction == directions[0] else directions[3]
                else:
                    self.direction = directions[3] if self.direction == directions[0] else directions[1]
            elif can_go_right:
                self.direction = directions[3]
            elif can_go_left:
                self.direction = directions[1]
            else:
                self.direction = None  # Zasekli sme sa v zahrade
        else:  # Horizontalny pohyb zmenime na vertikalny
            can_go_up = self.garden.empty(self.x, self.y - 1) or self.y == 0
            can_go_down = self.garden.empty(self.x, self.y + 1) or self.y + 1 == width

            if can_go_up and can_go_down:  # Ak mame na vyber, rozhodne informacia v gene
                if clockwise:
                    self.direction = directions[2] if self.direction == directions[1] else directions[0]
                else:
                    self.direction = directions[0] if self.direction == directions[1] else directions[2]
            elif can_go_up:
                self.direction = directions[2]
            elif can_go_down:
                self.direction = directions[0]
            else:
                self.direction = None  # Zasekli sme sa v zahrade

    def can_collect(self):
        """
        Zisti, ci sa na policku nachadza list a ci ho mozeme zobrat.

        :return: True ak list mozeme zobrat, inak False
        """
        if not self.garden.leaf(self.x, self.y):  # Skontrolujeme, ci dane policko obsahuje list
            return False

        block = self.garden.field[self.y][self.x]
        y, o, r = self.garden.get_leaves_count()

        # Zistime, ci mozeme pozbierat list na danom policku
        return (block == -2 and self.collected < y) or \
               (block == -3 and y <= self.collected < y + o) or \
               (block == -4 and y + o <= self.collected < y + o + r)

    def get_missing_positions(self):
        used = [gene.position for gene in self.chromosome]
        missing = [position for position in positions_ID.keys() if position not in used]
        random.shuffle(missing)
        return missing

    def crossover(self, other):
        child = Individual(puzzle.copy())

        split = random.randrange(len(self.chromosome) + 1)
        child.chromosome = self.chromosome[:split]
        for gene in other.chromosome[split:]:
            if gene not in child.chromosome:
                child.chromosome.append(gene)

        old_len = len(self.chromosome)
        missing = self.get_missing_positions()

        while old_len != len(child.chromosome):
            child.chromosome.append(Gene(missing.pop()))

        return child

    def mutate(self, mutation_rate=0.05):
        missing = self.get_missing_positions()

        for i, gene in enumerate(self.chromosome):
            if random.random() < mutation_rate:
                new_gene = Gene(missing.pop())
                self.chromosome[i] = new_gene

# ----------------------------------------------------------------------------------------------------


class Population:

    def __init__(self, size):
        self.size = size
        self.monks = self.create_monks(size)
        self.generation = 1
        self.fitness_sum = 0
        self.best, self.worst = None, None

    def __repr__(self):
        return f'{self.generation} {self.size} {self.fitness_sum}'

    def __str__(self):
        return f'Gen {self.generation}, ' \
               f'Best {self.best.fitness}, Worst {self.worst.fitness}, ' \
               f'Avg {self.fitness_sum / self.size}, Sum {self.fitness_sum}'

    @staticmethod
    def create_monks(size):
        """
        Vytvori populaciu so zadanym poctom jedincov.

        :param size: mnozstvo jedincov
        :return: zoznam jedincov
        """
        monks = []
        gene_count = width + length + block_counter[-1]

        for _ in range(size):
            monk = Individual(puzzle.copy())
            monk.chromosome = monk.create_genes(gene_count)
            monks.append(monk)

        return monks

    def solve_puzzle(self):
        total_fitness = 0
        temp_min = max_fitness
        temp_max = 0

        for monk in self.monks:
            fitness = monk.solve_garden()
            monk.fitness = fitness
            total_fitness += fitness

            if monk.fitness > temp_max:  # Najdeme najlepsieho jedinca
                temp_max = monk.fitness
                self.best = monk

            if monk.fitness < temp_min:  # Najdeme najhorsieho jedinca
                temp_min = monk.fitness
                self.worst = monk

        self.fitness_sum = total_fitness

    def natural_selection(self):
        # Elitarizmus: najlepsi jedinec prechadza do dalsej generacie bez mutacie
        best_monk = Individual(puzzle.copy())
        best_monk.chromosome = self.best.chromosome
        new_monks, new_size = [best_monk], 1

        # Pridame novu krv do novej generacie
        n_new_blood = int(0.10 * self.size)
        new_monks += self.create_monks(n_new_blood)

        while new_size < self.size:
            p1 = self.select_parent()  # Vyberieme si 2 rodicov
            p2 = self.select_parent()

            c1 = p1.crossover(p2)  # Vytvorime ich deti pomocou krizenia
            c2 = p2.crossover(p1)

            c1.mutate()  # Mutujeme deti s prednastavenou pravdepodobnostou
            c2.mutate()

            new_monks.extend((c1, c2))  # Pridame deti do nasledujucej generacie
            new_size += 2

        if new_size != self.size:
            new_monks.pop()
            new_size -= 1

        self.monks, self.size = new_monks, new_size
        self.generation += 1

    def select_parent(self, mode='roulette', k=3):
        """
        Vyberie rodica z aktualnej populacie.

        :param mode: sposob vyberu (tournament, roulette)
        :param k: pocet jedincov v turnaji
        :return: zvoleny jedinec
        """
        if mode == 'tournament':  # Vyber rodica pouzitim turnaja
            tour = random.sample(self.monks, k)
            tour = sorted(tour, key=lambda x: x.fitness, reverse=True)
            return tour[0]
        elif mode == 'roulette':  # Vyber rodica pouzitim rulety
            temp_sum = 0
            rand = random.randrange(self.fitness_sum)

            for monk in self.monks:
                temp_sum += monk.fitness
                if temp_sum > rand:
                    return monk

            return None  # Toto by sa nikdy nemalo stat

    def show_all(self):
        for monk in self.monks:
            print(monk, '\n')

    def show_best(self):
        print(self.best, '\n')

    def show_worst(self):
        print(self.worst, '\n')


if __name__ == "__main__":
    puzzle = load_puzzle('example_1.txt')
    main()
