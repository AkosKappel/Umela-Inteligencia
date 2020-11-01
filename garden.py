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
               f'leaves({self.n_yellow}, {self.is_outside()}, {self.n_red})'

    def __str__(self):
        s = '\n'
        for y in range(self.width):
            for x in range(self.length):
                s += f'{block_repr.get(self.field[y][x], self.field[y][x])}'.rjust(4, ' ')
            s += '\n'
        return s

    def set_parameters(self, width, length, yellow, orange, red):
        self.width, self.length = width, length
        self.n_yellow, self.n_orange, self.n_red = yellow, orange, red

    def copy(self):
        new_garden = Garden()
        new_garden.set_parameters(self.width, self.length,
                                  self.n_yellow, self.n_orange,
                                  self.n_red)
        for row in self.field:
            new_garden.field.append(row.copy())
        return new_garden

    def is_outside(self, x, y):
        return x < 0 or x >= self.length or y < 0 or y >= self.width

    def empty(self, x, y):
        if self.is_outside(x, y):
            return False
        return self.field[y][x] == 0  # TODO add leaves recognition logic


block_repr = {-1: 'K', -2: 'Z', -3: 'O', -4: 'C'}
