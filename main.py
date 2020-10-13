import sys


def main():
    # Initialize vehicles
    car_1 = Vehicle('red', 2, 2, 1, 'h')
    truck_1 = Vehicle('blue', 3, 1, 0, 'v')
    truck_2 = Vehicle('green', 3, 4, 3, 'h')
    car_2 = Vehicle('yellow', 2, 0, 5, 'v')

    # while not puzzle.is_solved():  # TODO or car.can_move()
    #     puzzle.show()
    #     car_1.go_forward()
    # puzzle.show()
    # Testing
    test_vehicle_movement()
    test_save_and_load_state()
    test_node_comparison()


def test_vehicle_movement():
    print(*Vehicle.all)
    puzzle.show()

    print('B move 2 down')
    Vehicle.all[1].go_forward(2)
    print(*Vehicle.all)
    puzzle.show()

    print('A move 2 right')
    Vehicle.all[0].go_forward(2)
    print(*Vehicle.all)
    puzzle.show()

    print('C move 1 left')
    Vehicle.all[2].go_backward(1)
    print(*Vehicle.all)
    puzzle.show()

    print('B move 3 up')
    Vehicle.all[1].go_backward(3)
    print(*Vehicle.all)
    puzzle.show()


def test_save_and_load_state():
    print('SAVE STATE 1')
    state_1 = puzzle.get_state()
    print(*Vehicle.all)
    puzzle.show()

    print('EMPTY GRID')
    puzzle.empty_grid()
    puzzle.show()

    print('LOAD STATE 1')
    puzzle.set_state(state_1)
    print(*Vehicle.all)
    puzzle.show()


def test_node_comparison():
    print('SAVED NODE 1')
    node_1 = Node(puzzle.get_state())
    puzzle.show()
    print(node_1)

    print('SAVED NODE 2')
    Vehicle.all[1].go_forward(1)
    node_2 = Node(puzzle.get_state())
    puzzle.show()
    print(node_2)

    print('SAVED NODE 3')
    Vehicle.all[1].go_backward(1)
    node_3 = Node(puzzle.get_state())
    puzzle.show()
    print(node_3)

    if node_1 == node_3:
        print('NODE 1 == NODE 2')
    if node_1 == node_2:
        print('ERROR: NODE 1 != NODE 2', file=sys.stderr)
    if node_3 != node_2:
        print('NODE 3 != NODE 2')


STYLE = {  # Available vehicle colors:
    'white': '\33[30m',
    'red': '\33[31m',
    'green': '\33[32m',
    'blue': '\33[34m',
    'purple': '\33[35m',
    'cyan': '\33[36m',
    'grey': '\33[37m',
    'black': '\33[90m',
    'yellow': '\33[93m',
    'light blue': '\33[94m',
    'pink': '\33[95m',
    'END': '\33[0m'
}


class Vehicle:
    all = []

    def __init__(self, color, length, y, x, direction):
        color = color.lower()
        self.color = STYLE[color] if color in STYLE.keys() else None
        self.id = chr(len(Vehicle.all) + 65)
        self.length = length
        self.x, self.y = x, y
        self.is_vertical = True if direction in 'Vv' else False
        Vehicle.all.append(self)
        self.game = puzzle
        self.game.place_vehicle(self)

    def __repr__(self):
        return f'({self.id} {self.length} {self.y} {self.x} ' + \
               ('v' if self.is_vertical else 'h') + ')'

    def go_forward(self, n=1):
        if self.is_vertical:
            if self.y + self.length + n <= self.game.size:  # down
                self.game.remove_vehicle(self)
                self.y += n
                self.game.place_vehicle(self)
                return True
        else:
            if self.x + self.length + n <= self.game.size:  # right
                self.game.remove_vehicle(self)
                self.x += n
                self.game.place_vehicle(self)
                return True
        return False

    def go_backward(self, n=1):
        if self.is_vertical:
            if self.y - n >= 0:  # up
                self.game.remove_vehicle(self)
                self.y -= n
                self.game.place_vehicle(self)
                return True
        else:
            if self.x - n >= 0:  # left
                self.game.remove_vehicle(self)
                self.x -= n
                self.game.place_vehicle(self)
                return True
        return False


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
            print('|', *self.grid[i], '|')
        print('-' * (self.size * 2 + 3))

    def get_state(self):  # TODO return node ?
        return tuple([(v.id, v.length, v.y, v.x, v.is_vertical) for v in self.vehicles])

    def set_state(self, s):
        self.empty_grid()
        for i, v in enumerate(self.vehicles):
            v.id, v.length, v.y, v.x, v.is_vertical = s[i]
            self.place_vehicle(v)

    def place_vehicle(self, v):
        if not self.is_empty(v.y, v.x, v.is_vertical, v.length):
            print(v, 'is overlapping an existing vehicle', file=sys.stderr)
            exit(1)
        self.set_block_of_vehicle(v, v.color + v.id + STYLE['END'] if v.color else v.id)

    def remove_vehicle(self, v):
        self.set_block_of_vehicle(v, ' ')

    def set_block_of_vehicle(self, v, cell_type):
        if v.is_vertical:
            for length in range(v.length):
                self.grid[v.y + length][v.x] = cell_type
        else:
            for length in range(v.length):
                self.grid[v.y][v.x + length] = cell_type

    def is_empty(self, x, y, is_vertical=None, length=1):
        if is_vertical and x + length <= self.size:
            return all(self.grid[x + i][y] == ' ' for i in range(length))
        elif not is_vertical and y + length <= self.size:
            return all(self.grid[x][y + i] == ' ' for i in range(length))
        elif is_vertical is None and x < self.size and y < self.size:
            return self.grid[x][y] == ' '
        print(f'Vehicle starting at ({x}, {y}) is outside the grid', file=sys.stderr)
        exit(2)

    def empty_grid(self):
        for i in range(self.size):
            for j in range(self.size):
                self.grid[i][j] = ' '

    def is_solved(self):
        v = self.vehicles[0]
        if v.is_vertical:
            return v.y + v.length == self.size
        return v.x + v.length == self.size


class Node:
    all = []
    # TODO add some kind of representation for all previous states

    def __init__(self, game_state):
        self.state = game_state
        self.id = len(Node.all)
        Node.all.append(self)

    def __repr__(self):
        return f'Node {self.id}: ' + \
               ' '.join([f'({v[0]} {v[1]} {v[2]} {v[3]} ' +
                         ('v' if v[4] else 'h') + ')' for v in self.state])

    def __eq__(self, other):
        return self.state == other.state


puzzle = RushHour()
if __name__ == '__main__':
    main()
