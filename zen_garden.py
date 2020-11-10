blocks = {  # Reprezentacia blokov pri vypisovani zahrady
    -1: '\33[30mK\33[0m',
    -2: '\33[93mZ\33[0m',
    -3: '\33[33mO\33[0m',
    -4: '\33[31mC\33[0m'
}


class Puzzle:

    # Reprezentacia blokov pri nacitavani zahrady z textoveho suboru
    block_types = {
        'K': -1,  # Kamene
        'Z': -2,  # Zlte listy
        'O': -3,  # Oranzove listy
        'C': -4   # Cervene listy
    }

    def __init__(self, file_name):
        self.garden = Garden()
        self.solved = False
        self.rocks = []
        self.yellow_leaves = []
        self.orange_leaves = []
        self.red_leaves = []
        with open(file_name, 'r') as file:
            self.load_garden(file)

    def __repr__(self):
        return f'size({self.garden.length}, {self.garden.width}) rocks({len(self.rocks)}) ' \
               f'leaves({len(self.yellow_leaves)}, {len(self.orange_leaves)}, {len(self.red_leaves)})'

    def __str__(self):
        return str(self.garden)

    def load_garden(self, file):
        """
        Nacitanie zahrady z externeho textoveho suboru.

        :param file: nazov suboru
        :return: None
        """
        for y, line in enumerate(file.readlines()):
            self.garden.field.append([])
            for x, block in enumerate(line.split()):
                self.garden.field[y].append(Puzzle.block_types.get(block.upper(), 0))

                # Ak sa na policku nachadza nejaky predmet (napr. kamen), zapiseme si jeho suradnice do zoznamu
                if block.upper() in Puzzle.block_types.keys():
                    if self.garden.field[y][x] == -1:
                        self.rocks.append((x, y))
                    elif self.garden.field[y][x] == -2:
                        self.yellow_leaves.append((x, y))
                    elif self.garden.field[y][x] == -3:
                        self.orange_leaves.append((x, y))
                    elif self.garden.field[y][x] == -4:
                        self.red_leaves.append((x, y))

        # Nastavenie dlzky, sirky a poctu listov v zahrade
        self.garden.set_parameters(len(self.garden.field), len(self.garden.field[0]),
                                   len(self.yellow_leaves), len(self.orange_leaves),
                                   len(self.red_leaves))

    def reset_garden(self):
        # Odstranime vykonane kroky po zahrade
        self.garden.clear()

        # Znovu umiestnime predmety
        for x, y in self.rocks:
            self.garden.field[y][x] = -1
        for x, y in self.yellow_leaves:
            self.garden.field[y][x] = -2
        for x, y in self.orange_leaves:
            self.garden.field[y][x] = -3
        for x, y in self.red_leaves:
            self.garden.field[y][x] = -4


class Garden:

    def __init__(self):
        self.width = 0
        self.length = 0
        self.field = []
        self.n_yellow = 0
        self.n_orange = 0
        self.n_red = 0

    def __repr__(self):
        return f'garden_size({self.length}, {self.width}), ' \
               f'leaves({self.n_yellow}, {self.n_orange}, {self.n_red})'

    def __str__(self):
        s = '\n'
        for y in range(self.width):
            for x in range(self.length):
                if self.field[y][x] in blocks.keys():
                    s += f'   {blocks.get(self.field[y][x])}'
                else:
                    s += f'{self.field[y][x]}'.rjust(4, ' ')
            s += '\n'
        return s

    def set_parameters(self, width, length, yellow, orange, red):
        """
        Nastavenie zakladnych parametrov zahrady.

        :param width: sirka
        :param length: dlzka
        :param yellow: pocet zltych listov
        :param orange: pocet oranzovych listov
        :param red: pocet cervenych listov
        :return: None
        """
        self.width, self.length = width, length
        self.n_yellow, self.n_orange, self.n_red = yellow, orange, red

    def load(self, matrix):
        """
        Nacitanie zahrady z matice.

        :param matrix: matica so zahradou
        :return: None
        """
        y, o, r = 0, 0, 0
        for line in matrix:
            y += line.count(-2)
            o += line.count(-3)
            r += line.count(-4)
        self.field = matrix
        self.set_parameters(len(matrix), len(matrix[0]), y, o, r)

    def copy(self):
        """
        Vytvorenie novej kopie zahrady, na ktorej nie su vykonane este ziadne kroky.

        :return: kopia zahrady
        """
        new_garden = Garden()
        new_garden.set_parameters(self.width, self.length,
                                  self.n_yellow, self.n_orange, self.n_red)
        for row in self.field:
            new_garden.field.append([0 if block > 0 else block for block in row])
        return new_garden

    def is_outside(self, x, y):  # Overenie, ci pozicia je mimo zahrady
        return x < 0 or x >= self.length or y < 0 or y >= self.width

    def is_leaf(self, x, y):  # Zisti, ci policko obsahuje list
        if self.is_outside(x, y):
            return False
        return self.field[y][x] != -1 and self.field[y][x] in blocks.keys()

    def empty(self, x, y):  # Skontroluje, ci mozeme navstivit dane policko
        if self.is_outside(x, y):
            return False
        return self.field[y][x] == 0

    def clear(self):  # Odstrani vykonane kroky
        for y in range(self.width):
            for x in range(self.length):
                if self.field[y][x] > 0:
                    self.field[y][x] = 0
