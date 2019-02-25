import pytest

from test_fixtures import *
import omk_core as omk

def test_add_subtract(tonal_vectors, tonal_oct_vectors):
    for x in tonal_vectors:
        for y in tonal_vectors:
            assert x + y - y == x
