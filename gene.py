import random
dimensions = ()


class Gene:

    directions = ('down', 'left', 'up', 'right')

    def __init__(self):
        self.pos, self.dir, self.turns = (0, 0), Gene.directions[0], [0]

    def __repr__(self):
        return f'{self.pos}, {self.dir}, {self.turns}'

    def randomize(self, x, y, n_rotations=6):
        global dimensions
        if not dimensions:
            dimensions = (x, y)
        random.seed()
        position = random.randrange(2 * (x + y))
        if 0 <= position < x:
            self.dir = Gene.directions[0]  # Pohyb z hornej casti smerom dole
            self.pos = (position, 0)
        elif x <= position < x + y:
            self.dir = Gene.directions[1]  # Pohyb z pravej strany smerom dolava
            self.pos = (x - 1, position - x)
        elif x + y <= position < 2 * x + y:
            self.dir = Gene.directions[2]  # Pohyb z dolnej casti smerom hore
            self.pos = (2 * x + y - 1 - position, y - 1)
        else:
            self.dir = Gene.directions[3]  # Pohyb z lavej strany smerom doprava
            self.pos = (0, 2 * (x + y) - 1 - position)

        # Zoznam otoceni ak sa najde prekazka na ceste
        # (1 - otocenie v smere hodinovych ruciciek, 0 - v protismere hodinovych ruciciek)
        n_clockwise_turns = random.randrange(n_rotations + 1)
        self.turns = [1] * n_clockwise_turns + [0] * (n_rotations - n_clockwise_turns)
        random.shuffle(self.turns)

    def crossover(self, other):
        new_gene = Gene()
        new_gene.pos, new_gene.dir = random.choice(((self.pos, self.dir), (other.pos, other.dir)))
        split = random.randrange(len(self.turns) + 1)
        new_gene.turns = self.turns[:split] + other.turns[split:]
        return new_gene

    def mutate(self):
        mutation_rate = 0.01
        rand = random.random()
        if rand < mutation_rate:
            self.randomize(*dimensions)
