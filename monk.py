from gene import Gene


class Monk:

    def __init__(self, garden, gene_count=0):
        self.garden = garden
        self.genes = []
        for _ in range(gene_count):
            gene = Gene()
            gene.randomize(garden.length, garden.width)
            self.genes.append(gene)
        self.fitness = 0
        self.dead = False

    def __repr__(self):
        return f'fitness({self.fitness}) - ' + ' | '.join([repr(gene) for gene in self.genes])

    def __str__(self):
        return f'Monk: fitness({self.fitness})\n\t' + '\n\t'.join([str(gene) for gene in self.genes])

    def bury_garden(self, show_moves=False):
        n_moves = 0
        for i, gene in enumerate(self.genes):
            if self.dead:  # Mnich sa zasekol v strede zahrady
                break

            x, y = gene.pos
            d = gene.dir
            if not self.garden.empty(x, y):  # Nie je mozne vsupit do zahrady
                continue

            turn_index = 0
            n_moves += 1
            while True:
                self.garden.field[y][x] = n_moves  # Vykoname pohyb
                x, y = self.move(x, y, d)

                if self.garden.is_outside(x, y):  # Mimo zahrady ... ideme na dalsi gen
                    break
                if self.garden.empty(x, y):  # Pokracujeme rovno v ceste
                    continue

                x, y = self.move(x, y, d, forward=False)  # Vratime sa o 1 policko
                d = self.turn(x, y, d, gene.turns[turn_index])  # Zmenime smer pohybu

                turn_index += 1
                turn_index %= len(gene.turns)
                if d is None:
                    break
            if show_moves:
                print(i, gene)
                print(self.garden)

    @staticmethod
    def move(x, y, d, forward=True):
        if d == Gene.directions[0]:
            y = y + 1 if forward else y - 1  # dole
        elif d == Gene.directions[1]:
            x = x - 1 if forward else x + 1  # dolava
        elif d == Gene.directions[2]:
            y = y - 1 if forward else y + 1  # hore
        else:
            x = x + 1 if forward else x - 1  # doprava
        return x, y

    def turn(self, x, y, d, clockwise):
        # Ak je pohyb mnicha vertikalny, tak ho zmenime na horizontalny
        if d in Gene.directions[0::2]:
            return self.turn_horizontal(d, clockwise, self.garden.empty(x - 1, y) or x - 1 == -1,
                                        self.garden.empty(x + 1, y) or x + 1 == self.garden.length)
        else:  # A ak je horizontalny, tak ho zmenime na vertikalny
            return self.turn_vertical(d, clockwise, self.garden.empty(x, y - 1) or y - 1 == -1,
                                      self.garden.empty(x, y + 1) or y + 1 == self.garden.width)

    def turn_horizontal(self, d, clockwise, can_go_left, can_go_right):
        if can_go_right and can_go_left:
            if clockwise:
                if d == Gene.directions[0]:
                    return Gene.directions[1]
                else:
                    return Gene.directions[3]
            else:
                if d == Gene.directions[0]:
                    return Gene.directions[3]
                else:
                    return Gene.directions[1]
        elif can_go_right:
            return Gene.directions[3]
        elif can_go_left:
            return Gene.directions[1]
        self.dead = True
        return None

    def turn_vertical(self, d, clockwise, can_go_up, can_go_down):
        if can_go_up and can_go_down:
            if clockwise:
                if d == Gene.directions[1]:
                    return Gene.directions[2]
                else:
                    return Gene.directions[0]
            else:
                if d == Gene.directions[1]:
                    return Gene.directions[0]
                else:
                    return Gene.directions[2]
        elif can_go_up:
            return Gene.directions[2]
        elif can_go_down:
            return Gene.directions[0]
        self.dead = True
        return None

    def calculate_fitness(self):
        self.fitness = 0
        for line in self.garden.field:
            for block in line:
                if block > 0:
                    self.fitness += 1

    def get_child(self, other):
        baby = Monk(self.garden.copy())
        for i in range(len(self.genes)):
            baby.genes.append(self.genes[i].crossover(other.genes[i]))
        return baby
