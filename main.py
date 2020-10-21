from collections import deque
from tests import *
import time
import sys


def main():
    while True:
        num = int(input('Zadaj číslo testu: ')) - 1
        if 0 <= num < len(test):
            break
        print(f'Nesprávne číslo! Číslo musí byť z intervalu <1, {len(test)}>.')

    for v in test[num]:  # Tu treba zmenit cislo testu
        Vehicle(v[0], v[1], v[2], v[3], v[4])

    start = puzzle.get_state()
    breadth_first_search(start)
    depth_first_search(start)


def timer(function):
    def wrapper(args_for_function):
        start = time.time()
        function(args_for_function)
        end = time.time()
        print(f'Algoritmus bol vykonaný za {end - start:.3f} sekúnd.\n')
    return wrapper


@timer
def breadth_first_search(start_state):
    print('#' * 10, 'Prehľadávanie do šírky', '#' * 10)
    state_counter = 0
    solution = None
    visited = set()
    queue = deque()
    queue.append(Node(start_state))
    visited.add(hash(str(start_state)))
    puzzle.set_state(start_state)
    print(puzzle)
    while queue:
        state_counter += 1
        current = queue.popleft()
        puzzle.set_state(current.state)
        if puzzle.is_solved():
            solution = current
            break
        for state in current.get_possible_states():
            if hash(str(state)) not in visited:
                queue.append(Node(state, parent=current))
                visited.add(hash(str(state)))
    if solution:
        path = get_path(solution)
        puzzle.set_state(solution.state)
        print(puzzle)
        print('Množstvo potrebných ťahov', len(path))
        print('Počet navštívených stavov:', state_counter)
        return path
    print('Tento stav hry nemá riešenie!')
    print('Počet navštívených stavov:', state_counter)
    return None


@timer
def depth_first_search(start_state):
    print('#' * 10, 'Prehľadávanie do hĺbky', '#' * 10)
    visited = set()
    current = Node(start_state)
    puzzle.set_state(start_state)
    current.create_children()
    print(puzzle)
    while True:
        visited.add(hash(current))
        if puzzle.is_solved():
            solution = current
            break
        while len(current.children) > 0:
            child = current.children.pop()
            if hash(str(child)) not in visited:
                current = Node(child, parent=current)
                puzzle.set_state(child)
                current.create_children()
                break
        if len(current.children) == 0:
            if current.parent is not None:
                current = current.parent
            else:
                print('Tento stav hry nemá riešenie!')
                print('Počet navštívených stavov:', len(visited))
                return None
    path = get_path(solution)
    puzzle.set_state(solution.state)
    print(puzzle)
    print('Množstvo potrebných ťahov', len(path))
    print('Počet navštívených stavov:', len(visited))
    return path


def get_path(final_node):
    moves = []
    current = final_node
    while current.parent is not None:
        state_2 = current.state
        current = current.parent
        state_1 = current.state
        moves.append(get_move(state_1, state_2))
    moves.reverse()
    for move in moves:
        print(*move)
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
        return f'({self.id} {self.length} {self.y} {self.x} {self.is_vertical})'

    def __str__(self):
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
        return f'Size: {self.size}\n' + \
               f'Vehicles: {self.vehicles.__repr__()}\n' + \
               f'Grid: {self.grid.__repr__()}'

    def __str__(self):
        return '\n'.join(('-' * (self.size * 2 + 3),
                          *['| ' + ' '.join(self.grid[i]) + ' |' for i in range(self.size)],
                          '-' * (self.size * 2 + 3)))

    def get_state(self):
        return tuple([(v.id, v.length, v.y, v.x, v.is_vertical) for v in self.vehicles])

    def set_state(self, s):
        self.clear_grid()
        for i, v in enumerate(self.vehicles):
            v.id, v.length, v.y, v.x, v.is_vertical = s[i]
            self.place_vehicle(v)

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
        for v in self.vehicles:
            self.remove_vehicle(v)

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
        return "Node: " + ' '.join([f'({v[0]} {v[1]} {v[2]} {v[3]} {v[4]})' for v in self.state]) + \
               f"\nparent = {self.parent.state if self.parent else None}" \
               f"\nchildren({len(self.children)}) = {self.children.__repr__()}\n"

    def __str__(self):
        return "Node: " + ' '.join([f'({v[0]} {v[1]} {v[2]} {v[3]} ' +
                                    ('v' if v[4] else 'h') + ')' for v in self.state]) + \
               f"\nparent = {self.parent.state if self.parent else None}" \
               f"\nchildren count = {len(self.children)}"

    def __eq__(self, other):
        return self.state == other.state

    def __hash__(self):
        return hash(str(self.state))

    def get_possible_states(self):
        temp_state = puzzle.get_state()
        moves = set()
        for v in Vehicle.all:
            while v.can_go_forward():
                moves.add(v.go_forward())
            while v.can_go_backward():
                moves.add(v.go_backward())
            puzzle.set_state(temp_state)
        return moves

    def create_children(self):
        temp_state = puzzle.get_state()
        for v in Vehicle.all:
            while v.can_go_forward():
                self.children.add(v.go_forward())
            while v.can_go_backward():
                self.children.add(v.go_backward())
            puzzle.set_state(temp_state)


if __name__ == '__main__':
    puzzle = RushHour()
    main()
