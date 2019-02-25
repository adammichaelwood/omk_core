import pytest
from hypothesis import given
from hypothesis.strategies import sampled_from


import omk_core as omk





_MS = [
    (0, 0),
    (1, 2),
    (2, 4),
    (3, 5), 
    (4, 7), 
    (5, 9),
    (6,11)
]

tonal_tuples = [(x[0],(x[1]+m)%12) for m in [0,1,-1] for x in _MS]

tonal_vectors = [omk.TonalVector(x) for x in tonal_tuples]

tonal_oct_tuples = [(x[0], x[1], y) for y in [0,1,2,-1,-2] for x in tonal_tuples]

tonal_oct_vectors = [omk.TonalVector(x) for x in tonal_oct_tuples]





@given(sampled_from(tonal_vectors), sampled_from(tonal_vectors))
def test_add_subtract_vectors(x, y):
    assert x + y - y == x

#   This does not work if double aug and doubl dim are included in test set.
#   That is, in theory, ok --- but I really don't like the traceback:
#   (1, 4) + (2, 6) = (3, 10)
#   TV(3, 10)
#   File "/Users/adamwood/omk/omk_core/src/omk_core/tonal_algebra/interval_quality.py", line 127, in _
#    return qualities[q]
#   KeyError: -7
#
#   Should be KeyError 5 (I think) ?
