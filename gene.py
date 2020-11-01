import random


class Gene:

    orientation = ('down', 'left', 'up', 'right')

    def __init__(self, x, y):
        random.seed()
        idx = random.randrange(2 * (x + y))
        # TODO self.rotation = []
        if 0 <= idx < x:  # from top row going down
            self.start = (idx, 0)
            self.direction = Gene.orientation[0]
        elif x <= idx < x + y:  # from right side going left
            self.start = (x - 1, idx - x)
            self.direction = Gene.orientation[1]
        elif x + y <= idx < 2 * x + y:  # from bottom row going up
            self.start = (2 * x + y - 1 - idx, y - 1)
            self.direction = Gene.orientation[2]
        else:  # from left side going right
            self.start = (0, 2 * (x + y) - 1 - idx)
            self.direction = Gene.orientation[3]

    def __repr__(self):
        return f'{self.start}, {self.direction}'

    def __str__(self):
        return 'Gene: ' + f'start{self.start}, direction({self.direction})'
