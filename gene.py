import random


class Gene:

    directions = ('down', 'left', 'up', 'right')

    def __init__(self, x, y):  # TODO add more turns
        random.seed()
        idx = random.randrange(2 * (x + y))
        if 0 <= idx < x:  # from top row going down
            self.pos = (idx, 0)
            self.dir = Gene.directions[0]
        elif x <= idx < x + y:  # from right side going left
            self.pos = (x - 1, idx - x)
            self.dir = Gene.directions[1]
        elif x + y <= idx < 2 * x + y:  # from bottom row going up
            self.pos = (2 * x + y - 1 - idx, y - 1)
            self.dir = Gene.directions[2]
        else:  # from left side going right
            self.pos = (0, 2 * (x + y) - 1 - idx)
            self.dir = Gene.directions[3]
        self.cw_turn = random.choice((True, False))

    def __repr__(self):
        return f'{self.pos}, {self.dir}, {self.cw_turn}'
