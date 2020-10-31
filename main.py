class Garden:

    block_values = {-1: 'K', -2: 'Z', -3: 'O', -4: 'C'}
    block_types = {
        'K': -1,  # Immovable obstacle
        'Z': -2,  # Yellow leaf
        'O': -3,  # Orange leaf
        'C': -4   # Red leaf
    }

    def __init__(self, file):
        self.width = 0
        self.length = 0
        self.field = []
        self.rocks = []
        self.yellow_leaves = []
        self.orange_leaves = []
        self.red_leaves = []
        self.load_field(file)

    def __repr__(self):
        return f'size({self.width} {self.length}) rocks({len(self.rocks)}) ' \
               f'leaves({len(self.yellow_leaves)}, {len(self.orange_leaves)}, {len(self.red_leaves)})'

    def __str__(self):
        s = "\n"
        for y in range(self.width):
            for x in range(self.length):
                s += f"{Garden.block_values.get(self.field[y][x], self.field[y][x])}".rjust(4, ' ')
            s += "\n"
        return s

    def load_field(self, file):
        with open(file, 'r') as f:
            for y, line in enumerate(f.readlines()):
                self.field.append([])
                for x, block in enumerate(line.split()):
                    self.field[y].append(Garden.block_types.get(block.upper(), 0))
                    if block.upper() in Garden.block_types.keys():
                        self.add_obstacle(x, y)
            self.width, self.length = y + 1, len(line.split())

    def add_obstacle(self, x, y):
        if self.field[y][x] == -1:
            self.rocks.append((x, y))
        elif self.field[y][x] == -2:
            self.yellow_leaves.append((x, y))
        elif self.field[y][x] == -3:
            self.orange_leaves.append((x, y))
        elif self.field[y][x] == -4:
            self.red_leaves.append((x, y))

    def reset_field(self):
        for y in range(self.width):
            for x in range(self.length):
                self.field[y][x] = 0
        for x, y in self.rocks:
            self.field[y][x] = -1
        for x, y in self.yellow_leaves:
            self.field[y][x] = -2
        for x, y in self.orange_leaves:
            self.field[y][x] = -3
        for x, y in self.red_leaves:
            self.field[y][x] = -4


class Monk:

    def __init__(self):
        pass

    def __repr__(self):
        pass


garden = Garden('garden_example1.txt')
print(garden)
