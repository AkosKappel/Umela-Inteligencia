from gene import Gene


class Monk:

    def __init__(self, garden, gene_count):
        self.garden = garden
        self.genes = [Gene(garden.length, garden.width) for _ in range(gene_count)]
        # TODO self.fitness = 0

    def __repr__(self):
        return ' | '.join([repr(gene) for gene in self.genes])

    def __str__(self):
        return 'Monk:\n\t' + '\n\t'.join([str(gene) for gene in self.genes])

    def bury_garden(self):
        pass  # TODO
