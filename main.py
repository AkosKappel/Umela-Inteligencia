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
positions_ID = {}  # Zoznam vstupnych pozicii do zahrady [0, 2 * (x + y) - 1]
directions = ('down', 'left', 'up', 'right')  # Vsetky mozne smery pohybu po zahrade
length, width = 0, 0  # Rozmery zahrady
max_fitness = 0  # Maximalna ziskatelna fitnes
solved = False  # Urcuje, ci sa podarilo uspesne pohrabat celu zahradu

# Nastavitelne parametre:
population_size = 30  # Velkost populacie
selection_method = 'roulette'  # Metoda vyberu rodica (roulette, tournament)
tour_size = 3  # Pocet jedincov v turnaji
mutation_probability = 0.05  # Pravdepodobnost mutacie
fitness_penalty = 0.5  # Vyska penalizacie (0 ziadna penalizacia, 1 maximalna penalizacia)
new_blood_portion = 0.10  # Podiel novych jedincov v nasledujucej generacii
max_generation = 300  # Maximalna povolena generacia populacie


def main():
    # Inicializacia prvej generacie
    monks = Population(population_size)
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

# --------------------------------------------------------------------------------------------------------------


def load_puzzle(file_name):
    """
    Nacita zahradu z externeho textoveho suboru a nastavi pomocne globalne premenne.

    :param file_name: nazov suboru
    :return: objekt s nacitanou zahradou
    """
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

    # Vypocitame maximalnu ziskatelnu fitnes hodnotu a nastavime fitnes penalizaciu
    global max_fitness, fitness_penalty
    max_fitness = length * width - block_counter[-1] + 1
    fitness_penalty = 1 - fitness_penalty

    return garden


def init_positions_ID():
    """
    Spocita pocet kazdeho typu bloku v zahrade. Udaje sa ukladaju do premennej positions_ID.
    """
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

# --------------------------------------------------------------------------------------------------------------


class Garden:

    def __init__(self, matrix):
        """
        Zenova zahrada.

        :param matrix: matica reprezentujuca zahradu
        """
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
        Vytvori sa nova kopia zahrady.

        :return: nova zahrada
        """
        field = []

        for row in self.field:
            field.append([0 if block > 0 else block for block in row])

        return Garden(field)

    def empty(self, x, y):
        """
        Skontroluje, ci je policko (x, y) prazdne.

        :param x: x-ova suradnica policka
        :param y: y-ova suradnica policka
        :return: True ak je policko prazdne, inak False
        """
        if Garden.outside(x, y):
            return False
        return self.field[y][x] == 0

    def leaf(self, x, y):
        """
        Zisti, ci sa na policku nachadza list.

        :param x: x-ova suradnica policka
        :param y: y-ova suradnica policka
        :return: True ak na policku je list, inak False
        """
        if Garden.outside(x, y):
            return False
        return self.field[y][x] != -1 and self.field[y][x] in output_blocks.keys()

    @staticmethod
    def outside(x, y):
        """
        Overi, ci je pozicia (x, y) mimo zahrady.

        :param x: x-ova suradnica policka
        :param y: y-ova suradnica policka
        :return: True ak je policko mimo zahrady, inak False
        """
        return x < 0 or x >= length or y < 0 or y >= width

    @staticmethod
    def get_leaves_count():
        """
        Z premennej block_counter precita pocet zltych, oranzovych a cervenych listov v zahrade.

        :return: pocet vsetkych farieb listov v zahrade
        """
        return (block_counter[-2] if -2 in block_counter.keys() else 0,
                block_counter[-3] if -3 in block_counter.keys() else 0,
                block_counter[-4] if -4 in block_counter.keys() else 0)

# --------------------------------------------------------------------------------------------------------------


class Gene:

    def __init__(self, position, n_turns=6):
        """
        Gen tvoriaci chrmozom jedinca.

        :param position: vstupna pozicia do zahrady
        :param n_turns: pocet instrukcii na otocenie sa, ak na ceste je prekazka
        """
        self.position = position
        # Generujeme poradie, v akom sa otacame ak narazime na prekazku
        # 1 - otocenie v smere hodinovych ruciciek
        # 0 - otocenie v protismere hodinovych ruciciek
        rand = random.randrange(2 ** n_turns)
        self.turns = format(rand, f'0{n_turns}b')

    def __repr__(self):
        return f'{self.position} {self.turns} {positions_ID[self.position]} {self.get_direction()}'

    def __str__(self):
        return f'{positions_ID[self.position]} {self.get_direction()} {self.turns}'

    def __eq__(self, other):
        return self.position == other.position

    def __hash__(self):
        return hash(self.position)

    def get_direction(self):
        """
        Zisti informaciu o smere pohybu zo vstupnej pozicie do zahrady.
        """
        if 0 <= self.position < length:
            return directions[0]  # Pohyb z hornej casti smerom dole
        elif length <= self.position < length + width:
            return directions[1]  # Pohyb z pravej strany smerom dolava
        elif length + width <= self.position < 2 * length + width:
            return directions[2]  # Pohyb z dolnej casti smerom hore
        else:
            return directions[3]  # Pohyb z lavej strany smerom doprava

# --------------------------------------------------------------------------------------------------------------


class Individual:

    def __init__(self, garden):
        """
        Jedinec, ktory sa snazi vyriesit problem.

        :param garden: kopia povodnej zahrady
        """
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
        return f'{self.garden}\nfitness {self.fitness}, genes {len(self.chromosome)}\n\t' + \
               '\n\t'.join([f'{i:2}: ' + str(gene) for i, gene in enumerate(self.used_genes, start=1)])

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

        # Pridelime bonusovy bod pre jedinca, ktory uspesne vysiel zo zahrady
        # a bodovy postih pre jedinca, ktory sa zasekol v zahrade
        fitness = fitness + 1 if survived else int(fitness * fitness_penalty)

        if fitness >= max_fitness:  # Skontrolujeme, ci je cela zahrada uspesne pohrabana
            global solved
            solved = True

        return fitness

    def move(self, forward=True):
        """
        Jedinec vykona krok dopredu alebo dozadu o jedno policko v smere jeho pohyby.

        :param forward: ma sa vykonat pohyb dopredu
        :return: None
        """
        if self.direction == directions[0]:
            self.y = self.y + 1 if forward else self.y - 1  # Dole
        elif self.direction == directions[1]:
            self.x = self.x - 1 if forward else self.x + 1  # Dolava
        elif self.direction == directions[2]:
            self.y = self.y - 1 if forward else self.y + 1  # Hore
        else:
            self.x = self.x + 1 if forward else self.x - 1  # Doprava

    def turn(self, clockwise=True):
        """
        Jedninec zmeni smer svojho pohybu na taky smer, kde nie je pred nim ziadna prekazka.
        Ak taky smer neexistuje, smer sa nastavi na None, a ak sa vie otocit doprava aj dolava,
        rozhodne sa podla parametra clockwise.

        :param clockwise: otocenie v smere hodinovych ruciciek
        :return: None
        """
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
        """
        Zisti identifikatory tych zaciatocnych policok zahrady, ktore este nie su v chromozome jedinca.

        :return: zoznam vsetkych chybajucich identifikatorov usporiadanych v nahodnom poradi
        """
        used = [gene.position for gene in self.chromosome]
        missing = [position for position in positions_ID.keys() if position not in used]
        random.shuffle(missing)
        return missing

    def crossover(self, other):
        """
        Krizenie jedinca s dalsim jedincom.

        :param other: druhy jedinec
        :return: dieta, ktore vzniklo krizenim 2 rodicov
        """
        child = Individual(puzzle.copy())

        # Dedenie jednej casti genov od jedneho rodica a zvysku genov od druheho (napr. 0000111111)
        split = random.randrange(len(self.chromosome) + 1)
        child.chromosome = self.chromosome[:split]
        for gene in other.chromosome[split:]:
            if gene not in child.chromosome:  # Predideme viacnasobnemu dedeniu rovnakych genov
                child.chromosome.append(gene)  # (rovnaky gen == rovnaka zaciatocna pozicia)

        old_len = len(self.chromosome)
        missing = self.get_missing_positions()

        # Ak dieta dedi 2-krat ten isty gen, jeden z nich sa nahradi novym genom
        while old_len != len(child.chromosome):
            child.chromosome.append(Gene(missing.pop()))

        return child

    def mutate(self, mutation_rate=0.05):
        """
        Kazdy gen v chromozome jedinca sa s predvolenou pravdepodobnostou zmeni na novy gen.

        :param mutation_rate: pravdepodobnast mutacie
        :return: None
        """
        missing = self.get_missing_positions()

        for i, gene in enumerate(self.chromosome):
            if random.random() < mutation_rate:
                new_gene = Gene(missing.pop())
                self.chromosome[i] = new_gene

# --------------------------------------------------------------------------------------------------------------


class Population:

    def __init__(self, size):
        """
        Populacia tvorena rovnakymi jedincami.

        :param size: velkost populacie
        """
        self.size = size
        self.monks = self.create_monks(size)
        self.generation = 1
        self.fitness_sum = 0
        self.best, self.worst = None, None

    def __repr__(self):
        return f'Generation {self.generation}, Size {self.size}, Fitness sum {self.fitness_sum}'

    def __str__(self):
        return f'Gen {self.generation}, ' \
               f'Best {self.best.fitness}, Worst {self.worst.fitness}, ' \
               f'Avg {self.fitness_sum / self.size:.2f}, Sum {self.fitness_sum}'

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
        """
        Kazdy jedinec populacie pohrabe zahradu, vypocita sa ich fitnes hednota,
        zaroven sa spocita celkova fitnes populacie a urci sa najlepsi a najhorsi jedinec.

        :return: None
        """
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
        """
        Evolucia jednej generacie jedincov.

        :return: None
        """
        # Elitarizmus: najlepsi jedinec prechadza do dalsej generacie bez mutacie
        best_monk = Individual(puzzle.copy())
        best_monk.chromosome = self.best.chromosome
        new_monks, new_size = [best_monk], 1

        # Pridame novu krv do novej generacie
        n_new_blood = int(new_blood_portion * self.size)
        new_monks += self.create_monks(n_new_blood)

        while new_size < self.size:
            p1 = self.select_parent(selection_method, tour_size)  # Vyberieme si 2 rodicov
            p2 = self.select_parent(selection_method, tour_size)

            c1 = p1.crossover(p2)  # Vytvorime ich deti pomocou krizenia
            c2 = p2.crossover(p1)

            c1.mutate(mutation_probability)  # Mutujeme deti s prednastavenou pravdepodobnostou
            c2.mutate(mutation_probability)

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

    def show_all(self):  # Vypise vsetkych jedincov populacie
        for monk in self.monks:
            print(monk, '\n')

    def show_best(self):  # Vypise najlepsieho jedinca
        print(self.best, '\n')

    def show_worst(self):  # Vypise najhorsieho jedinca
        print(self.worst, '\n')


if __name__ == "__main__":
    puzzle = load_puzzle('test_gardens\\garden_1.txt')
    main()
