import sys


class Vehicle:

    def __init__(self, color, length, x, y, direction):
        if color in STYLE.keys():
            color = STYLE[color] + color + STYLE['END']
        self.color = color
        self.length = length
        self.x, self.y = x, y
        self.direction = direction

    def __repr__(self):
        return f'({self.color} {self.length} {self.x} {self.y} {self.direction})'


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


class RushHour:

    def __init__(self, *vehicles):
        self.size = 6
        self.grid = [[' ' for _ in range(self.size)] for _ in range(self.size)]
        self.vehicles = [*vehicles]
        self.place_vehicles()  # Put all vehicles on the grid.

    def __repr__(self):
        return 'Size: ' + str(self.size) + '\n' + \
               'Vehicles: ' + self.vehicles.__repr__() + '\n' + \
               'Grid: ' + self.grid.__repr__()

    def __str__(self):
        return '\n'.join(' '.join(self.grid[i]) for i in range(self.size))

    def show(self):
        print('-' * (self.size * 2 + 3))
        for i in range(self.size):
            print('|', *self.grid[i], '|')
        print('-' * (self.size * 2 + 3))

    def place_vehicles(self):
        for v in self.vehicles:
            if not self.is_free(v.x, v.y, v):
                print('Incorrect vehicle position', repr(v), file=sys.stderr)
                exit(1)

            if v.direction in 'Vv':  # Vertical
                for length in range(v.length):
                    self.grid[v.x + length][v.y] = v.color
            elif v.direction in 'Hh':  # Horizontal
                for length in range(v.length):
                    self.grid[v.x][v.y + length] = v.color

    def is_free(self, x, y, vehicle=None):
        if vehicle:
            if vehicle.direction in 'Vv':
                return all(self.grid[x + i][y] == ' ' for i in range(vehicle.length))
            elif vehicle.direction in 'Hh':
                return all(self.grid[x][y + i] == ' ' for i in range(vehicle.length))
        else:
            return self.grid[x][y] == ' '


def main():
    car = Vehicle('r', 2, 2, 1, 'h')
    truck = Vehicle('b', 3, 1, 0, 'v')
    puzzle = RushHour(car, truck)
    print(*puzzle.vehicles)
    puzzle.show()


if __name__ == '__main__':
    main()
