import pytest
from hypothesis import given, assume
from hypothesis.strategies import sampled_from, decimals, floats, fractions, integers

from fractions import Fraction as Frac
import omk_core as omk

denominators = [2**n for n in range(1, 10)]

@given(integers(1,100), sampled_from(denominators))
def test_str(n, d):

    assert omk.TimeSignature(n, d)._str == "{}/{}".format(n, d)

@given(integers(1,100), integers(1,100), sampled_from(denominators))
def test_add_same_denom(n1, n2, d):

    assert (omk.TimeSignature(n1,d) + omk.TimeSignature(n2,d))._d == d

@given(integers(1,100), integers(1,100), sampled_from(denominators), sampled_from(denominators))
def test_add_different_denom(n1, n2, d1, d2):

    x = omk.TimeSignature(n1, d1)
    y = omk.TimeSignature(n2, d2)
    assert (x + y)._d == max([d1, d2]) # True for powers of two

@given(integers(1,100), integers(1,100), sampled_from(denominators), sampled_from(denominators))
def test_add_commutative(n1, n2, d1, d2):

    x = omk.TimeSignature(n1, d1)
    y = omk.TimeSignature(n2, d2)
    assert x + y == y + x

    z = Frac(n2, d2)
    assert x + z == z + x

    i = n2
    assert x + i == i + x

@given(integers(1,100), integers(1,100), sampled_from(denominators), sampled_from(denominators))
def test_sub_commutative(n1, n2, d1, d2):

    x = omk.TimeSignature(n1, d1)
    y = omk.TimeSignature(n2, d2)
    assert (x - y) + y == x
    assert (y - x) + x == y

    z = Frac(n2, d2)
    assert (x - z) + z == x
    assert (z - x) + x == z

    i = n2
    assert (x - i) + i == x
    assert (i - x) + x == i

@given(integers(1,100), integers(1,100), sampled_from(denominators), sampled_from(denominators))
def test_mul_calculation(n1, n2, d1, d2):
    xt = omk.TimeSignature(n1, d1)
    yt = omk.TimeSignature(n2, d2)

    xf = Frac(n1, d1)
    yf = Frac(n2, d2)

    assert xt * yt == xf * yf

@given(integers(1,100), integers(1,100), sampled_from(denominators), sampled_from(denominators))
def test_mul_commutative(n1, n2, d1, d2):

    x = omk.TimeSignature(n1, d1)
    y = omk.TimeSignature(n2, d2)
    assert x * y == y * x

    z = Frac(n2, d2)
    assert x * z == z * x
    
    i = n2
    assert x * i == i * x

@given(integers(1,100), integers(1,100), sampled_from(denominators), sampled_from(denominators))
def test_true_div(n1, n2, d1, d2):

    x = omk.TimeSignature(n1, d1)
    y = omk.TimeSignature(n2, d2)
    assert (x / y) * y == x
    assert (y / x) * x == y

    z = Frac(n2, d2)
    assert (x / z) * z == x
    assert (z / x) * x == z
    
    i = n2
    assert (x / i) * i == x
    assert (i / x) * x == i