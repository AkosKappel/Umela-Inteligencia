import random


class Gene:

    orientation = ("down", "left", "up", "right")

    def __init__(self, x, y):
        random.seed()
        idx = random.randrange(2 * (x + y))
        # TODO self.rotation = []
        if 0 <= idx < x:  # from up going down
            self.start = (idx, 0)
            self.direction = Gene.orientation[0]
        elif x <= idx < x + y:  # from right side to left
            self.start = (x - 1, idx - x)
            self.direction = Gene.orientation[1]
        elif x + y <= idx < 2 * x + y:  # from down going up
            self.start = (2 * x + y - 1 - idx, y - 1)
            self.direction = Gene.orientation[2]
        else:  # from left side to right
            self.start = (0, 2 * (x + y) - 1 - idx)
            self.direction = Gene.orientation[3]
