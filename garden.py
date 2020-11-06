blocks = {-1: 'K', -2: 'Z', -3: 'O', -4: 'C'}


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
                s += f'{blocks.get(self.field[y][x], self.field[y][x])}'.rjust(4, ' ')
            s += '\n'
        return s

    def set_parameters(self, width, length, yellow, orange, red):
        self.width, self.length = width, length
        self.n_yellow, self.n_orange, self.n_red = yellow, orange, red

    def load(self, matrix):
        y, o, r = 0, 0, 0
        for line in matrix:
            y += line.count(-2)
            o += line.count(-3)
            r += line.count(-4)
        self.field = matrix
        self.set_parameters(len(matrix), len(matrix[0]), y, o, r)

    def copy(self):
        new_garden = Garden()
        new_garden.set_parameters(self.width, self.length,
                                  self.n_yellow, self.n_orange, self.n_red)
        for row in self.field:
            new_garden.field.append([0 if block > 0 else block for block in row])
        return new_garden

    def is_outside(self, x, y):
        return x < 0 or x >= self.length or y < 0 or y >= self.width

    def is_leaf(self, x, y):
        if self.is_outside(x, y):
            return False
        return self.field[y][x] != -1 and self.field[y][x] in blocks.keys()

    def empty(self, x, y):
        if self.is_outside(x, y):
            return False
        return self.field[y][x] == 0

    def clear(self):
        for y in range(self.width):
            for x in range(self.length):
                if self.field[y][x] > 0:
                    self.field[y][x] = 0
