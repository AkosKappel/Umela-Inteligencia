class Garden:

    def __init__(self):
        self.width = 0
        self.length = 0
        self.field = []

    def __repr__(self):
        return f'garden_size({self.length}, {self.width})'

    def __str__(self):
        s = '\n'
        for y in range(self.width):
            for x in range(self.length):
                s += f'{block_repr.get(self.field[y][x], self.field[y][x])}'.rjust(4, ' ')
            s += '\n'
        return s

    def copy(self):
        new_garden = Garden()
        new_garden.width, new_garden.length = self.width, self.length
        for row in self.field:
            new_garden.field.append(row.copy())
        return new_garden


block_repr = {-1: 'K', -2: 'Z', -3: 'O', -4: 'C'}
