import random
directions = ('down', 'left', 'up', 'right')


class Gene:

    def __init__(self):
        self.pos, self.dir, self.turns = (0, 0), directions[0], [0]

    def __repr__(self):
        return f'{self.pos}, {self.dir}, {self.turns}'

    def randomize(self, x, y, n_rotations=6):
        random.seed()
        position = random.randrange(2 * (x + y))

        # Vygenerujeme suradnice zaciatocnej pozicie a smer pohybu
        if 0 <= position < x:
            # Pohyb z hornej casti smerom dole
            self.dir = directions[0]
            self.pos = (position, 0)
        elif x <= position < x + y:
            # Pohyb z pravej strany smerom dolava
            self.dir = directions[1]
            self.pos = (x - 1, position - x)
        elif x + y <= position < 2 * x + y:
            # Pohyb z dolnej casti smerom hore
            self.dir = directions[2]
            self.pos = (2 * x + y - 1 - position, y - 1)
        else:
            # Pohyb z lavej strany smerom doprava
            self.dir = directions[3]
            self.pos = (0, 2 * (x + y) - 1 - position)

        # Generujeme poradie, v akom sa otacame, ak narazime na prekazku
        # 1 - otocenie v smere hod. ruciciek
        # 0 - otocenie v protismere hod. ruciciek
        n_clockwise_turns = random.randrange(n_rotations + 1)
        self.turns = [1] * n_clockwise_turns + [0] * (n_rotations - n_clockwise_turns)
        random.shuffle(self.turns)
