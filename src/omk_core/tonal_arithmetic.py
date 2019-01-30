"""
Add and subtract intervals, chromae, notes.

These functions operate on tuples of the form `(d, c, o)`, where
`d` is a required integer representing a diatonic value,
`c` is a required integer representing a chromatic value,
`o` is an optional integer reprenting an octave designation.
"""

import itertools

from constants import D_LEN, C_LEN
from utils import *

#@mus_utils.tonal_args
def tonal_sum(x, y):
    """Returns the value of x augmented by y.

    Examples
    --------

    >>> tonal_sum((0, 0), (2, 3))
    (2, 3)

    >>> tonal_sum((3, 6), (4, 6))
    (0, 0)

    >>> tonal_sum((0, 0, 0), (2, 3))
    (2, 3, 0)

    >>> tonal_sum((3, 6, 0), (4, 6))
    (0, 0, 1)
    """

    if len(x) < len(y):
        raise TypeError("An octave designation cannot be added to an abstract tonal value.")

    sum = tuple(xval+yval for xval,yval in itertools.zip_longest(x,y, fillvalue=0))

    sum = tonal_modulo(sum)

    return sum

# @tonal_args
def tonal_diff(x, y):
    """Returns the value of x diminished by y.

    Examples
    --------

    >>> tonal_diff((2, 3), (2, 3))
    (0, 0)

    >>> tonal_diff((0, 0), (1, 1))
    (6, 11)

    >>> tonal_diff((0, 0, 0), (1, 1))
    (6, 11, -1)
    """


    return tonal_sum(x, negative_tuple(y))

#@tonal_args
def tonal_invert(x, y=(0,0)):
    """Returns the inversion of x on y.

    The inversion is the value which is as far below x
    as y is above x.

    Examples
    --------

    >>> tonal_invert((2,4)) # The inversion of a Major Third is a Minor Sixth
    (5, 8)

    >>> tonal_invert((3,6)) # The inversion of a tritone is a tritone with a different name.
    (4, 6)

    >>> tonal_invert((4,7), (2,4)) # G is a min 3rd up from E. Down a min 3rd from E is C#.
    (0, 1)
    """

    return tonal_diff(y, tonal_diff(x, y))


#@tonal_args
def tonal_modulo(x):
    """Returns an octave-normalized rendering of x.

    Examples
    --------

    >>> tonal_modulo((7, 12)) # C + 1 octave, no octave designation
    (0, 0)

    >>> tonal_modulo((7, 12, 0)) # C + 1 octave
    (0, 0, 1)

    >>> tonal_modulo((-1, -1)) # B - 1 octave
    (6, 11)

    >>> tonal_modulo((-1, -1, 0)) # B - 1 octave
    (6, 11, -1)

    """

    # From (0,0) to (6.11) (inclusive), no modulo is needed.
    if x[0] in range(D_LEN) and x[1] in range(C_LEN):
        return x

    #if len(x) == 2:
    #    x = (x[0], x[1], 0)

    d_val = x[0] % D_LEN # The normalized diatonic value.
    d_oct = x[0] // D_LEN # The additional diatonic octave.
    c_val = x[1] % C_LEN # The normalized chromatic value.
    c_oct = x[1] // C_LEN # The additional chromatic ocatve.

    # The diatonic and chromatic additional octaves should be the same,
    # otherwise there was some problem further up.
    if d_oct != c_oct:
        raise ValueError("Diatonic and chromatic values are not in the same octave.")

    if len(x) == 2:
        return (d_val, c_val)

    if len(x) == 3:
        return (d_val, c_val, d_oct)


def negative_tuple(x):

    return tuple(-m for m in x)

def tonal_abs(x):
    """Returns the distance from the origin (Middle C).
    """

    return abs(tonal_int(x))

def tonal_int(x):

    try:
        return x[1] + x[2]*(C_LEN)
    except IndexError:
        return x[1]

def tonal_greater_of(x,y):
    if tonal_int(x) > tonal_int(y):
        return x
    else:
        return y

def tonal_lesser_of(x,y):
    if tonal_int(x) < tonal_int(y):
        return x
    else:
        return y


if __name__ == "__main__":
    import doctest
    doctest.testmod()
