import sys


def main():
    # Initialize vehicles
    Vehicle('red', 2, 2, 1, 'h')
    Vehicle('orange', 2, 0, 0, 'h')
    Vehicle('yellow', 3, 1, 0, 'v')
    Vehicle('purple', 2, 4, 0, 'v')
    Vehicle('green', 3, 1, 3, 'v')
    Vehicle('light blue', 3, 5, 2, 'h')
    Vehicle('grey', 2, 4, 4, 'h')
    Vehicle('blue', 3, 0, 5, 'v')

    start = puzzle.get_state()
    depth_first_search(start)
    breadth_first_search(start)


def breadth_first_search(start_state):
    solution = None
    # TODO finish algorithm


def depth_first_search(start_state):
    solution = None
    visited_nodes = set()

    current = start_state
    puzzle.set_state(current)
    current.create_children()
    total_steps = 0
    puzzle.show()
    while True:
        visited_nodes.add(current.state)
        if puzzle.is_solved():
            print('SOLVED')  # TODO remove
            solution = current
            break

        while current.has_children():
            child = current.children.pop()
            if child not in visited_nodes:
                current = Node(child, parent=current)
                puzzle.set_state(current)
                current.create_children()
                total_steps += 1
                # puzzle.show()
                break

        if not current.has_children():
            if current.has_parent():
                current = current.parent
            else:
                print('UNSOLVABLE')  # TODO remove
                break

    if solution:
        print(solution.state)
    print('Total steps', total_steps)
    puzzle.set_state(solution)
    puzzle.show()
    # while solution.has_parent():
    #     print(solution.parent.state)
    #     solution = solution.parent


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
                return self.game.get_state()
        else:
            if self.x + self.length + n <= self.game.size:  # right
                self.game.remove_vehicle(self)
                self.x += n
                self.game.place_vehicle(self)
                return self.game.get_state()
        return None

    def go_backward(self, n=1):
        if self.is_vertical:
            if self.y - n >= 0:  # up
                self.game.remove_vehicle(self)
                self.y -= n
                self.game.place_vehicle(self)
                return self.game.get_state()
        else:
            if self.x - n >= 0:  # left
                self.game.remove_vehicle(self)
                self.x -= n
                self.game.place_vehicle(self)
                return self.game.get_state()
        return None

    def can_go_forward(self):
        if self.is_vertical and self.y + self.length < self.game.size and \
                self.game.is_empty(self.x, self.y + self.length):
            return True
        elif not self.is_vertical and self.x + self.length < self.game.size and \
                self.game.is_empty(self.x + self.length, self.y):
            return True
        return False

    def can_go_backward(self):
        if self.is_vertical and self.y - 1 >= 0 and self.game.is_empty(self.x, self.y - 1):
            return True
        elif not self.is_vertical and self.x - 1 >= 0 and self.game.is_empty(self.x - 1, self.y):
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

    def get_state(self):
        return Node(tuple([(v.id, v.length, v.y, v.x, v.is_vertical) for v in self.vehicles]))

    def set_state(self, s):
        self.empty_grid()
        for i, v in enumerate(self.vehicles):
            v.id, v.length, v.y, v.x, v.is_vertical = s.state[i]
            self.place_vehicle(v)

    def place_vehicle(self, v):
        if not self.is_empty(v.x, v.y, v.is_vertical, v.length):
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
        if is_vertical and y + length <= self.size:
            return all(self.grid[y + i][x] == ' ' for i in range(length))
        elif not is_vertical and x + length <= self.size:
            return all(self.grid[y][x + i] == ' ' for i in range(length))
        elif 0 <= x < self.size and 0 <= y < self.size:
            return self.grid[y][x] == ' '
        print(f'Point ({x}, {y}) is outside the grid', file=sys.stderr)
        exit(2)

    def empty_grid(self):
        for i in range(self.size):
            for j in range(self.size):
                self.grid[i][j] = ' '

    # @property
    def is_solved(self):
        v = self.vehicles[0]
        if v.is_vertical:
            return v.y + v.length == self.size
        return v.x + v.length == self.size


class Node:

    def __init__(self, game_state, parent=None):
        self.state = game_state
        self.parent = parent
        self.children = set()

    def __repr__(self):
        return f'Node parent({self.parent}), children({self.children.__repr__()}):\n' + \
               ' '.join([f'({v[0]} {v[1]} {v[2]} {v[3]} ' +
                         ('v' if v[4] else 'h') + ')' for v in self.state])

    def __eq__(self, other):
        return self.state == other.state

    def create_children(self):
        temp_state = puzzle.get_state()
        for v in Vehicle.all:
            while v.can_go_forward():
                self.children.add(v.go_forward().state)
            while v.can_go_backward():
                self.children.add(v.go_backward().state)
            puzzle.set_state(temp_state)

    def has_parent(self):
        return self.parent

    def has_children(self):
        return self.children != set()


puzzle = RushHour()
if __name__ == '__main__':
    main()
