import sys


def main():
    # Init
    puzzle = RushHour()
    car_1 = Vehicle('red', 2, 2, 1, 'h', puzzle)
    truck_1 = Vehicle('blue', 3, 1, 0, 'v', puzzle)
    truck_2 = Vehicle('green', 3, 4, 3, 'h', puzzle)

    # Printing game phases for testing movement
    print(*Vehicle.all)
    puzzle.show()
    truck_1.go_down(2)
    print(*Vehicle.all)
    puzzle.show()
    car_1.go_right(2)
    print(*Vehicle.all)
    puzzle.show()
    truck_2.go_left(1)
    print(*Vehicle.all)
    puzzle.show()
    truck_1.go_up(3)
    print(*Vehicle.all)
    puzzle.show()


class Vehicle:
    all = []

    def __init__(self, color, length, x, y, direction, game):
        color = color[0].lower()
        if color in STYLE.keys():
            color = STYLE[color] + str(len(Vehicle.all)) + STYLE['END']
        self.id = color
        self.length = length
        self.x, self.y = x, y
        self.is_vertical = True if direction in 'Vv' else False
        self.game = game
        Vehicle.all.append(self)
        game.place_vehicle(self)

    def __repr__(self):
        return f'({self.id} {self.length} {self.x} {self.y} ' + \
               ('v' if self.is_vertical else 'h') + ')'

    def go_up(self, n):
        if self.is_vertical and self.x - n >= 0:
            self.game.remove_vehicle(self)
            self.x -= n
            self.game.place_vehicle(self)

    def go_down(self, n):
        if self.is_vertical and self.x + self.length + n <= self.game.size:
            self.game.remove_vehicle(self)
            self.x += n
            self.game.place_vehicle(self)

    def go_left(self, n):
        if not self.is_vertical and self.y - n >= 0:
            self.game.remove_vehicle(self)
            self.y -= n
            self.game.place_vehicle(self)

    def go_right(self, n):
        if not self.is_vertical and self.y + self.length + n <= self.game.size:
            self.game.remove_vehicle(self)
            self.y += n
            self.game.place_vehicle(self)


class RushHour:

    def __init__(self):
        self.size = 6
        self.grid = [[' ' for _ in range(self.size)] for _ in range(self.size)]
        self.vehicles = Vehicle.all

    def __repr__(self):
        return 'Size: ' + str(self.size) + '\n' + \
               'Vehicles: ' + self.vehicles.__repr__() + '\n' + \
               'Grid: ' + self.grid.__repr__()

    def __str__(self):
        return '\n'.join(' '.join(self.grid[i]) for i in range(self.size))

    def show(self):
        print('-' * (self.size * 2 + 3))
        for i in range(self.size):
            if i != (self.size - 1) // 2:
                print('|', *self.grid[i], '|')
            else:
                print('|', *self.grid[i], '->')
        print('-' * (self.size * 2 + 3))

    def place_vehicle(self, v):
        if not self.is_empty(v.x, v.y, v.is_vertical, v.length):
            print(v, 'is overlapping an existing vehicle', file=sys.stderr)
            exit(1)
        self.set_vehicle(v, v.id)

    def remove_vehicle(self, v):
        self.set_vehicle(v, ' ')

    def set_vehicle(self, v, cell_type):
        if v.is_vertical:
            for length in range(v.length):
                self.grid[v.x + length][v.y] = cell_type
        else:
            for length in range(v.length):
                self.grid[v.x][v.y + length] = cell_type

    def is_empty(self, x, y, is_vertical=None, length=1):
        if is_vertical and x + length <= self.size:
            return all(self.grid[x + i][y] == ' ' for i in range(length))
        elif not is_vertical and y + length <= self.size:
            return all(self.grid[x][y + i] == ' ' for i in range(length))
        elif is_vertical is None and x < self.size and y < self.size:
            return self.grid[x][y] == ' '
        print(f'Position ({x}, {y}) is outside the grid', file=sys.stderr)
        exit(2)

    def empty_grid(self):
        for i in range(self.size):
            for j in range(self.size):
                self.grid[i][j] = ' '


STYLE = {
    'w': '\33[30m',  # white
    'r': '\33[31m',  # red
    'b': '\33[34m',  # blue
    'g': '\33[36m',  # green
    'y': '\033[93m',  # yellow
    'p': '\033[95m',  # pink
    'k': '\33[90m',  # black
    'l': '\033[94m',  # light blue
    'END': '\033[0m'  # normal
}


if __name__ == '__main__':
    main()
