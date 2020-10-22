test_1 = (  # TEST 1 - Priklad zo zadania ulohy
    ('red', 2, 2, 1, 'h'),
    ('orange', 2, 0, 0, 'h'),
    ('yellow', 3, 1, 0, 'v'),
    ('purple', 2, 4, 0, 'v'),
    ('green', 3, 1, 3, 'v'),
    ('light blue', 3, 5, 2, 'h'),
    ('grey', 2, 4, 4, 'h'),
    ('blue', 3, 0, 5, 'v')
)

test_2 = (  # TEST 2 - Jednoduchy test na min 3 tahy
    ('red', 2, 2, 1, 'h'),
    ('blue', 3, 1, 0, 'v'),
    ('green', 3, 4, 3, 'h'),
    ('yellow', 2, 1, 5, 'v'),
    ('purple', 3, 0, 3, 'h')
)

test_3 = (  # TEST 3 - Kratky test na min 5 tahov
    ('red', 2, 3, 1, 'h'),
    ('blue', 2, 1, 2, 'h'),
    ('green', 3, 2, 3, 'v'),
    ('yellow', 3, 2, 0, 'h'),
    ('purple', 3, 3, 5, 'v'),
    ('black', 2, 3, 4, 'v')
)

test_4 = (  # TEST 4 - Cervene auto je vertikalne (6 tahov)
    ('red', 2, 1, 3, 'v'),
    ('yellow', 3, 3, 3, 'h'),
    ('pink', 2, 4, 4, 'v'),
    ('green', 3, 0, 0, 'h'),
    ('blue', 2, 2, 2, 'v'),
    ('white', 2, 5, 2, 'h'),
    ('purple', 3, 2, 0, 'v')
)

test_5 = (  # TEST 5 - Nema riesenie
    ('red', 2, 4, 0, 'h'),
    ('yellow', 3, 0, 4, 'v'),
    ('pink', 2, 4, 4, 'v'),
    ('green', 2, 1, 1, 'h'),
    ('blue', 2, 2, 2, 'v'),
    ('white', 2, 0, 2, 'h'),
    ('cyan', 3, 2, 5, 'v')
)

test_6 = (  # TEST 6 - Najnarocnejsia hra na 49 tahov
    ('red', 2, 2, 2, 'h'),
    ('white', 3, 0, 0, 'h'),
    ('orange', 2, 1, 0, 'v'),
    ('blue', 2, 3, 0, 'h'),
    ('purple', 2, 1, 1, 'h'),
    ('green', 2, 4, 1, 'v'),
    ('yellow', 3, 0, 4, 'v'),
    ('light blue', 3, 0, 5, 'v'),
    ('black', 2, 0, 3, 'v'),
    ('cyan', 2, 4, 4, 'h'),
    ('pink', 2, 3, 2, 'v'),
    ('grey', 2, 5, 2, 'h'),
    ('white', 2, 5, 4, 'h')
)

test_7 = (  # TEST 7 - Minimum 11 tahov
    ('red', 2, 1, 0, 'h'),
    ('yellow', 2, 0, 2, 'v'),
    ('green', 2, 0, 3, 'v'),
    ('black', 2, 0, 4, 'v'),
    ('white', 2, 0, 5, 'v'),
    ('cyan', 2, 2, 2, 'h'),
    ('blue', 2, 2, 4, 'h'),
    ('purple', 2, 2, 1, 'v'),
    ('pink', 3, 3, 2, 'h'),
    ('light blue', 2, 4, 0, 'h')
)

test_8 = (  # TEST 8 - Vertikalne cervene auto (min 9 tahov)
    ('red', 2, 0, 1, 'v'),
    ('yellow', 2, 2, 0, 'h'),
    ('pink', 2, 2, 3, 'h'),
    ('green', 2, 3, 0, 'h'),
    ('blue', 2, 3, 3, 'h'),
    ('black', 2, 4, 0, 'h'),
    ('cyan', 2, 4, 3, 'h'),
    ('white', 2, 5, 0, 'h'),
    ('grey', 2, 5, 3, 'h')
)

test_9 = (  # TEST 9 - Ziadna prekazka na ceste
    ('red', 2, 1, 0, 'h'),
    ('light blue', 2, 0, 4, 'h'),
    ('pink', 2, 2, 2, 'v'),
    ('yellow', 2, 4, 5, 'v'),
    ('green', 3, 4, 0, 'h'),
    ('cyan', 3, 3, 3, 'h')
)

test_10 = (  # TEST 10 - minimum 22 tahov
    ('red', 2, 0, 2, 'h'),
    ('light blue', 3, 0, 0, 'v'),
    ('blue', 3, 1, 5, 'v'),
    ('yellow', 2, 0, 1, 'v'),
    ('orange', 2, 5, 0, 'h'),
    ('white', 2, 4, 4, 'h'),
    ('pink', 3, 3, 0, 'h'),
    ('purple', 2, 2, 3, 'h'),
    ('cyan', 2, 1, 2, 'v'),
    ('black', 2, 4, 2, 'v'),
    ('grey', 2, 0, 4, 'v'),
    ('brown', 2, 3, 3, 'v'),
    ('blue', 2, 5, 3, 'h')
)

# Zoznam vsetkych testov
test = (test_1, test_2, test_3, test_4, test_5,
        test_6, test_7, test_8, test_9, test_10)
