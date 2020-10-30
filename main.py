class Garden:

    def __init__(self, file):
        self.field = []
        self.width = 0
        self.length = 0
        self.rock_count = 0
        with open(file, 'r') as f:
            for line in f.readlines():
                self.field.append([])
                self.field[self.width] = [*line.split()]
                self.rock_count += line.count('K')
                self.width += 1
            self.length = len(line.split())

    def __repr__(self):
        return f'size {self.width} x {self.length}\trocks = {self.rock_count}'

    def __str__(self):
        return '\n'.join((' '.join(self.field[i]) for i in range(self.width)))


class Monk:

    def __init__(self):
        pass

    def __repr__(self):
        pass


garden = Garden('garden_example1.txt')
print(garden)
