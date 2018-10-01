"""
Add and subtract intervals, chromae, notes.

These functions operate on tuples of the form `(d, c, o)`, where
`d` is a required integer representing a diatonic value,
`c` is a required integer representing a chromatic value,
`o` is an optional integer reprenting an octave designation.
"""

import itertools

from . import *


def tonal_add(x, y):
    """Returns the value of x augmented by y.

    Examples
    --------

    >>> tonal_add((0, 0), (2, 3))
    (2, 3)

    >>> tonal_add((3, 6), (4, 6))
    (0, 0, 1)
    """

    if len(x) not in (2,3) or len(y) not in (2,3):
        TypeError("Tonal primitives have two or three values.")

    if len(x) < len(y):
        raise TypeError("An octave designation cannot be added to an abstract tonal value.")

    sum = tuple(xval+yval for xval,yval in itertools.zip_longest(x,y, fillvalue=0))

    sum = tonal_modulo(sum)

    return sum

def tonal_subtract(x, y):
    """Returns the value of x diminished by y.

    Examples
    --------

    >>> tonal_subtract((2, 3), (2, 3))
    (0, 0)

    >>> tonal_subtract((0,0), (1, 1))
    (6, 11, -1)
    """

    if len(x) not in (2,3) or len(y) not in (2,3):
        TypeError("Tonal primitives have two or three values.")

    return tonal_add(x, negative_tuple(y))




def tonal_modulo(x):
    """Returns an octave-normalized rendering of x.

    Examples
    --------

    >>> tonal_modulo((7, 12)) # C + 1 octave
    (0, 0, 1)

    >>> tonal_modulo((-1, -1)) # B - 1 octave
    (6, 11, -1)
    """

    if len(x) not in (2,3):
        raise TypeError("Tonal primitives have two or three values.")

    if x[0] in range(D_LEN) and x[1] in range(C_LEN):
        return x

    if len(x) == 2:
        x = (x[0], x[1], 0)

    d_val = x[0] % D_LEN
    d_oct = x[0] // D_LEN
    c_val = x[1] % C_LEN
    c_oct = x[1] // C_LEN

    if d_oct != c_oct:
        raise ValueError("Diatonic and chromatic values are not in the same octave.")

    oct_val = x[2] + d_oct

    normalized_x = (d_val, c_val, oct_val)

    return normalized_x


def negative_tuple(x):

    return tuple(-m for m in x)


