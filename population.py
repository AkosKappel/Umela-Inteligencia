from monk import Monk


class Population:

    def __init__(self, size, puzzle):
        self.generation = 1
        n_genes = puzzle.garden.width + puzzle.garden.length + len(puzzle.rocks)
        self.monks = [Monk(puzzle.garden.copy(), n_genes) for _ in range(size)]

    def __repr__(self):
        return f'Generation: {self.generation}\n' + '\n'.join(repr(m) for m in self.monks)

    def __str__(self):
        return f'Generation: {self.generation}\n' + '\n'.join(str(m) for m in self.monks)  # TODO remake
