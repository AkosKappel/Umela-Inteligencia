from collections import deque
import time
import sys


def main():
    # Initialize vehicles
    # Vehicle('red', 2, 2, 1, 'h')
    # Vehicle('orange', 2, 0, 0, 'h')
    # Vehicle('yellow', 3, 1, 0, 'v')
    # Vehicle('purple', 2, 4, 0, 'v')
    # Vehicle('green', 3, 1, 3, 'v')
    # Vehicle('light blue', 3, 5, 2, 'h')
    # Vehicle('grey', 2, 4, 4, 'h')
    # Vehicle('blue', 3, 0, 5, 'v')

    Vehicle('red', 2, 2, 1, 'h')
    Vehicle('blue', 3, 1, 0, 'v')
    Vehicle('green', 3, 4, 3, 'h')
    Vehicle('yellow', 2, 1, 5, 'v')

    start = puzzle.get_state()
    breadth_first_search(start)
    depth_first_search(start)


def timer(function):
    def wrapper(args_for_function):
        start = time.time()
        function(args_for_function)
        end = time.time()
        print(f'Algorithm executed in {end - start:.3f} seconds.')
    return wrapper


@timer
def breadth_first_search(start_node):
    print('#' * 10, 'Breadth First Search', '#' * 10)
    puzzle.set_state(start_node)
    puzzle.show()
    solution = None
    visited_states = set()
    queue = deque()
    queue.append(start_node)
    while queue:
        current = queue.popleft()
        visited_states.add(current.state)
        puzzle.set_state(current)
        current.create_children()

        if puzzle.is_solved():
            solution = current
            break

        while current.has_children():
            child = current.children.pop()
            if child not in visited_states:
                queue.append(Node(child, parent=current))

    if not solution:
        print('Tento stav hry nemá riešenie!')
        return None
    path = get_path(solution)
    for move in path:
        print(*move)
    puzzle.set_state(solution)
    puzzle.show()
    return path


@timer
def depth_first_search(start_node):
    print('#' * 10, 'Depth First Search', '#' * 10)
    puzzle.set_state(start_node)
    start_node.create_children()
    puzzle.show()
    visited_states = set()
    current = start_node
    while True:
        if puzzle.is_solved():
            solution = current
            break

        visited_states.add(current.state)
        while current.has_children():
            child = current.children.pop()
            if child not in visited_states:
                current = Node(child, parent=current)
                puzzle.set_state(current)
                current.create_children()
                break

        if not current.has_children():
            if current.has_parent():
                current = current.parent
            else:
                print('Tento stav hry nemá riešenie!')
                return None
    path = get_path(solution)
    for move in path:
        print(*move)
    puzzle.set_state(solution)
    puzzle.show()
    return path


def get_path(final_node):
    moves = []
    current = final_node
    while current.has_parent():
        state_2 = current.state
        current = current.parent
        state_1 = current.state
        moves.append(get_move(state_1, state_2))
    moves.reverse()
    return moves


def get_move(first_state, second_state):
    for v_1, v_2 in zip(first_state, second_state):
        if v_1 != v_2:
            if v_1[4]:
                dif = v_2[2] - v_1[2]
                return (v_1[0], 'DOLE', dif) if dif > 0 else (v_1[0], 'HORE', -dif)
            dif = v_2[3] - v_1[3]
            return (v_1[0], 'VPRAVO', dif) if dif > 0 else (v_1[0], 'VLAVO', -dif)


STYLE = {  # Available vehicle colors:
    'white': '\33[30m',
    'red': '\33[31m',
    'orange': '\33[33m',
    'blue': '\33[34m',
    'purple': '\33[35m',
    'green': '\33[36m',
    'grey': '\33[37m',
    'black': '\33[90m',
    'yellow': '\33[93m',
    'light blue': '\33[94m',
    'pink': '\33[95m',
    'cyan': '\33[96m',
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

    def get_state(self):
        return Node(tuple([(v.id, v.length, v.y, v.x, v.is_vertical) for v in self.vehicles]))

    def set_state(self, s):
        self.clear_grid()
        for i, v in enumerate(self.vehicles):
            v.id, v.length, v.y, v.x, v.is_vertical = s.state[i]
            self.place_vehicle(v)

    def show(self):
        print('-' * (self.size * 2 + 3))
        for i in range(self.size):
            print('|', *self.grid[i], '|')
        print('-' * (self.size * 2 + 3))

    def place_vehicle(self, v):
        if not self.is_empty(v.x, v.y, v.is_vertical, v.length):
            print(v, 'is overlapping an existing vehicle', file=sys.stderr)
            exit(1)
        self.set_vehicle_cells(v, v.color + v.id + STYLE['END'] if v.color else v.id)

    def remove_vehicle(self, v):
        self.set_vehicle_cells(v, ' ')

    def set_vehicle_cells(self, v, cell_type):
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

    def clear_grid(self):
        for i in range(self.size):
            for j in range(self.size):
                self.grid[i][j] = ' '

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
        return self.parent is not None

    def has_children(self):
        return self.children != set()


puzzle = RushHour()
if __name__ == '__main__':
    main()
