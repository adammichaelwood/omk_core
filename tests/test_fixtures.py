import pytest

import omk_core as omk 

@pytest.fixture
def tonal_tuples():
    MS = [
        (0, 0),
        (1, 2),
        (2, 4),
        (3, 5), 
        (4, 7), 
        (5, 9),
        (6,11)
    ]

    return [(x[0],(x[1]+m)%12) for m in [0,1,2,-1,-2] for x in MS]

@pytest.fixture
def tonal_vectors(tonal_tuples):
    return [omk.TonalVector(x) for x in tonal_tuples]

@pytest.fixture
def tonal_oct_tuples(tonal_tuples):
    return [(x[0], x[1], y) for y in [0,1,2,-1,-2] for x in tonal_tuples]

@pytest.fixture
def tonal_oct_vectors(tonal_oct_tuples):
    return [omk.TonalVector(x) for x in tonal_oct_tuples]