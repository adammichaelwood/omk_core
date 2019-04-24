import pytest
from hypothesis import given
from hypothesis.strategies import sampled_from

import omk_core as omk

from test_set import tonal_vectors, tonal_oct_vectors, tonal_tuples, tonal_oct_tuples


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
#
#   This traceback tells me that there is something going on here that I don't understand.
#
#   Note --- It's happening because 
#   get_quality attempts to normalize out-of-range indexes by adding/subtracting 12

@given(sampled_from(tonal_oct_vectors), sampled_from(tonal_oct_vectors))
def test_add_subtract_oct_vectors(x, y):
    assert x + y - y == x

@given(sampled_from(tonal_vectors), sampled_from(tonal_vectors))
def test_vector_distance(x, y):
    assert x.distance(y) == y.distance(x)
    assert abs(x.distance(y)) < 7

@given(sampled_from(tonal_oct_vectors), sampled_from(tonal_oct_vectors))
def test_oct_vector_distance(x, y):
    assert x.distance(y) == y.distance(x)

@given(sampled_from(tonal_vectors), sampled_from(tonal_oct_vectors))
def test_nearest_instance(x, y):
    assert abs(x.nearest_instance(y).distance(x)) < 7

@given(sampled_from(tonal_oct_vectors), sampled_from(tonal_vectors+tonal_oct_vectors))
def test_oct_nearest_instance(x, y):
    assert abs(x.nearest_instance(y).distance(x)) < 7

@given(sampled_from(tonal_vectors), sampled_from(tonal_vectors))
def test_inversion(x,y):
    assert x.inversion().inversion() == x
    assert x.inversion(y).inversion(y) == x
    assert x.distance(y) == x.inversion(y).distance(y)

@given(sampled_from(tonal_oct_vectors), sampled_from(tonal_oct_vectors))
def test_oct_inversion(x,y):
    assert x.inversion().inversion() == x
    assert x.inversion(y).inversion(y) == x
    assert x.distance(y) == x.inversion(y).distance(y)

@given(sampled_from(tonal_tuples+tonal_oct_tuples))
def test_hash_and_eq(x):
    y = omk.TonalVector(x)
    assert x == y
    assert len(set([x, y]))


## TonalVector.Note
## TonalVector.Interval
## Probably best approach is to test along with Pitch and Interval parsing.
