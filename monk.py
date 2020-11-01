from gene import Gene


class Monk:

    def __init__(self, garden, gene_count):
        self.garden = garden
        self.genes = [Gene(garden.length, garden.width) for _ in range(gene_count)]
        self.dead = False
        # TODO self.fitness = 0

    def __repr__(self):
        return ' | '.join([repr(gene) for gene in self.genes])

    def __str__(self):
        return 'Monk:\n\t' + '\n\t'.join([str(gene) for gene in self.genes])

    def bury_garden(self):
        n_moves = 0
        for gene in self.genes:
            if self.dead:  # Mnich sa zasekol v strede zahrady
                break

            x, y = gene.pos
            d = gene.dir
            if not self.garden.empty(x, y):  # Nie je mozne vsupit do zahrady
                continue

            n_moves += 1
            while True:
                self.garden.field[y][x] = n_moves  # Vykoname pohyb
                x, y = self.move(x, y, d)
                if self.garden.is_outside(x, y):  # Mimo zahrady ... ideme na dalsi gen
                    break
                if self.garden.empty(x, y):  # Pokracujeme rovno v ceste
                    continue
                x, y = self.move(x, y, d, forward=False)  # Vratime sa o 1 policko
                d = self.turn(d, x, y, gene.cw_turn)  # Zmenime smer pohybu
                if d is None:
                    break

        # TODO self.set_fitness()

    @staticmethod
    def move(x, y, d, forward=True):
        if d == Gene.directions[0]:
            y = y + 1 if forward else y - 1
        elif d == Gene.directions[1]:
            x = x - 1 if forward else x + 1
        elif d == Gene.directions[2]:
            y = y - 1 if forward else y + 1
        else:
            x = x + 1 if forward else x - 1
        return x, y

    def turn(self, d, x, y, clockwise):
        if d in Gene.directions[0::2]:  # Pohyb hore a dole
            return self.turn_to_horizontal(d, self.garden.empty(x + 1, y),
                                           self.garden.empty(x - 1, y), clockwise)
        else:  # Pohyb doprava a dolava
            return self.turn_to_vertical(d, self.garden.empty(x, y - 1),
                                         self.garden.empty(x, y + 1), clockwise)

    def turn_to_horizontal(self, d, can_go_right, can_go_left, clockwise):
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

    def turn_to_vertical(self, d, can_go_up, can_go_down, clockwise):
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

    def set_fitness(self):
        pass  # TODO
