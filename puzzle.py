from garden import Garden


class Puzzle:

    block_types = {
        'K': -1,  # Immovable obstacle
        'Z': -2,  # Yellow leaf
        'O': -3,  # Orange leaf
        'C': -4   # Red leaf
    }

    def __init__(self, file_name):
        self.garden = Garden()
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
        return self.garden.__str__()

    def load_garden(self, file):
        for y, line in enumerate(file.readlines()):
            self.garden.field.append([])
            for x, block in enumerate(line.split()):
                self.garden.field[y].append(Puzzle.block_types.get(block.upper(), 0))
                if block.upper() in Puzzle.block_types.keys():
                    self.add_obstacle(x, y)
        self.garden.width = len(self.garden.field)
        self.garden.length = len(self.garden.field[0])

    def add_obstacle(self, x, y):
        if self.garden.field[y][x] == -1:
            self.rocks.append((x, y))
        elif self.garden.field[y][x] == -2:
            self.yellow_leaves.append((x, y))
        elif self.garden.field[y][x] == -3:
            self.orange_leaves.append((x, y))
        elif self.garden.field[y][x] == -4:
            self.red_leaves.append((x, y))

    def reset_garden(self):
        for y in range(self.garden.width):
            for x in range(self.garden.length):
                self.garden.field[y][x] = 0
        for x, y in self.rocks:
            self.garden.field[y][x] = -1
        for x, y in self.yellow_leaves:
            self.garden.field[y][x] = -2
        for x, y in self.orange_leaves:
            self.garden.field[y][x] = -3
        for x, y in self.red_leaves:
            self.garden.field[y][x] = -4
