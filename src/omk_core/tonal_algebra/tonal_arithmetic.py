"""
Add and subtract intervals, chromae, notes.

These functions operate on tuples of the form `(d, c, o)`, where
`d` is a required integer representing a diatonic value,
`c` is a required integer representing a chromatic value,
`o` is an optional integer reprenting an octave designation.
"""

import itertools

from ..definitions.constants import D_LEN, C_LEN, MS
from ..utils import *

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

    >>> tonal_sum((6, 11, 1), (2, 4))
    (1, 3, 2)
    """

    if len(x) < len(y):
        raise TypeError("An octave designation cannot be added to an abstract tonal value.")

    sum = tuple(xval+yval for xval,yval in itertools.zip_longest(x,y, fillvalue=0))

    sum = _tonal_modulo(sum)

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

    >>> tonal_diff((0,1),(1,1))
    (6, 0)

    >>> tonal_diff((0,1,0), (6,10, -1))
    (1, 3, 0)

    >>> tonal_diff((0,0,0),(0,10,0))
    (0, 2, 0)

    """

    return tonal_sum(x, _negative_tuple(y))

def _negative_tuple(x):
    """
    >>> _negative_tuple((1, 1, 1))
    (-1, -1, -1)
    """

    return tuple(-m for m in x)


#@tonal_args
def tonal_invert(x, y=(0,0)):
    """Returns the inversion of x on y.

    The inversion is the value which is as far below y
    as x is above y.

    Examples
    --------

    >>> tonal_invert((2,4)) # The inversion of a Major Third is a Minor Sixth
    (5, 8)

    >>> tonal_invert((3,6)) # The inversion of a tritone is a tritone with a different name.
    (4, 6)

    >>> tonal_invert((4,7), (2,4)) # G is a min 3rd up from E. Down a min 3rd from E is C#.
    (0, 1)

    >>> tonal_invert((0,1,0))
    (0, 11, 0)

    """

    x, y = qualify_octave_as_needed(x, y)

    return tonal_diff(y, tonal_diff(x, y))


#@tonal_args
def _tonal_modulo(x):
    """Returns an octave-normalized rendering of x.

    Examples
    --------

    >>> _tonal_modulo((7, 12)) # C + 1 octave, no octave designation
    (0, 0)

    >>> _tonal_modulo((7, 12, 0)) # C + 1 octave
    (0, 0, 1)

    >>> _tonal_modulo((-1, -1)) # B - 1 octave
    (6, 11)

    >>> _tonal_modulo((-1, -1, 0)) # B - 1 octave
    (6, 11, -1)

    >>> _tonal_modulo((-1, 0))
    (6, 0)

    >>> _tonal_modulo((7, 12, 1))
    (0, 0, 2)

    """

    # From (0,0) to (6,11) (inclusive), no modulo is needed.
    if x[0] in range(D_LEN) and x[1] in range(C_LEN):
        return x

    d_val = x[0] % D_LEN # The normalized diatonic value.
    d_oct = x[0] // D_LEN # The additional diatonic octave.
    c_val = x[1] % C_LEN # The normalized chromatic value.
    
    if len(x) == 2:
        return (d_val, c_val)

    if len(x) == 3:
        return (d_val, c_val, (x[2] + d_oct))


def tonal_abs(x):
    """Returns the absolute distance in half steps from the origin (Middle C).
    >>> tonal_abs((6,11,-1))
    1

    >>> tonal_abs((0,1,0))
    1
    """

    return abs(tonal_int(x))

def tonal_int(x):
    """
    >>> tonal_int((4,7))
    7

    >>> tonal_int((4,7,2))
    31

    >>> tonal_int((6,11,-1))
    -1

    >>> tonal_int((0,-1,-1))
    -13

    >>> tonal_int((6,0,0))
    12

    >>> tonal_int((0,11,0))
    -1

    >>> tonal_int((0,11))
    -1

    >>> tonal_int((2, 0))
    0

    """

    if len(x) == 2:
        x = _tonal_unmodulo(x)
        return x[1]

    d = x[0]
    c = x[1]
    base_c = MS[d].c

    # Example: Cb --- base=0 c=11  c-base=11   11 - 12 = -1

    if c - base_c > 3:
        c = c - C_LEN

    # Example: B# --- base=11 c=0 c-base=-11        c+C_LEN =12
    if c - base_c < -3:
        c = c + C_LEN

    return c + x[2]*(C_LEN)

        

def tonal_greater_of(x,y):
    """
    >>> tonal_greater_of((0,0,0), (0,11,-1))
    (0, 0, 0)

    >>> tonal_greater_of((0,0,0),(0,10,0))
    (0, 0, 0)
    """
    if tonal_int(x) == tonal_int(y):
        if x[0] > y[0]:
            return x
        else:
            return y

    if tonal_int(x) > tonal_int(y):
        return x
    else:
        return y

def tonal_lesser_of(x,y):
    """
    >>> tonal_lesser_of((0,0,0), (0,11,-1))
    (0, 11, -1)

    >>> tonal_lesser_of((0,1,0),(0,10,0))
    (0, 10, 0)
    """
    x = _tonal_unmodulo(x)
    y = _tonal_unmodulo(y)

    if tonal_int(x) == tonal_int(y):
        if x[0] < y[0]:
            return x
        else:
            return y
    if tonal_int(x) < tonal_int(y):
        return _tonal_modulo(x)
    else:
        return _tonal_modulo(y)

def tonal_abs_val(x):
    """
    >>> tonal_abs_val((4,7))
    (3, 5)

    >>> tonal_abs_val((6,11,-1))
    (1, 1, 0)

    >>> tonal_abs_val((1,1,0))
    (1, 1, 0)

    >>> tonal_abs_val((6, 0, -1))
    (1, 0, 0)

    >>> tonal_abs_val((0,11,0))
    (0, 1, 0)
    """
    if len(x) == 2:
        y = tonal_invert(x)
        if x[0] == y[0]:
            if _tonal_unmodulo(x)[1] < 0:
                return y
            if _tonal_unmodulo(y)[1] < 0:
                return x

        return tonal_lesser_of(x, y)

    if len(x) == 3:
        y = tonal_invert(x)
        if x[2] < 0:
            return y
        if y[2] < 0:
            return x

        if x[0] == y[0] and x[2] == y[2] == 0:
            if _tonal_unmodulo(x)[1] < 0:
                return y
            if _tonal_unmodulo(y)[1] < 0:
                return x

        return tonal_lesser_of(x, y)
        


def tonal_abs_diff(x,y):
    """Returns an tuple representing the smallest difference between two tonal primitives.

    Examples
    --------

    >>> tonal_abs_diff((0,0),(5,9))
    (2, 3)

    >>> x, y = (0,0), (4,6)
    >>> tonal_abs_diff(x,y) == tonal_abs_diff(x,tonal_invert(y))
    True

    >>> tonal_abs_diff((0,0,0), (6,11,-1))
    (1, 1, 0)

    >>> tonal_abs_diff((6,0,0), (0,0,1))
    (1, 0, 0)

    >>> tonal_abs_diff((0,0,0),(0,11,0))
    (0, 1, 0)

    >>> tonal_abs_diff((0,0,0), (0,11,-1))
    (0, 1, 1)

    >>> tonal_abs_diff((0,0,0), (0,11,0))
    (0, 1, 0)

    >>> tonal_abs_diff((0, 0), (0, 1))
    (0, 1)

    >>> tonal_abs_diff((0, 0), (0,11))
    (0, 1)

    >>> tonal_abs_diff((1, 3), (3, 3))
    (2, 0)

    """
    x,y = qualify_octave_as_needed(x,y)
    #if len(x) == 3:
    #    return tonal_diff(tonal_greater_of(x,y), tonal_lesser_of(x,y))

    #return tonal_lesser_of(tonal_diff(x,y), tonal_diff(y,x))

    a = tonal_abs_val(tonal_diff(x,y))
    b = tonal_abs_val(tonal_diff(y,x))



    return _tonal_modulo(tonal_lesser_of(a, b))

def abs_int_diff(x, y):
    """
    >>> abs_int_diff((0,1,0),(0,11,0))
    2

    >>> abs_int_diff((0,1,0),(6,11,-1))
    2
    """
    x,y = qualify_octave_as_needed(x,y)

    if len(x) == 3:
        x = tonal_int(x)
        y = tonal_int(y)
        return abs(x-y)

    return tonal_int(tonal_abs_diff(x,y))


def tonal_nearest_instance(x,y):
    """Returns the location of y that is closest to x.
    >>> tonal_nearest_instance((0,0,0), (1,2,-1))
    (1, 2, 0)

    >>> tonal_nearest_instance((0,1,1), (6,10, -3))
    (6, 10, 0)

    >>> tonal_nearest_instance((0,0,0), (6,11,3))
    (6, 11, -1)

    >>> tonal_nearest_instance((0,0), (6,11,-1))
    (6, 11)

    >>> tonal_nearest_instance((0, 0, 0), (0, 11, 0))
    (0, 11, 0)
    """
    if len(x) == 2:
        return (y[0], y[1])

    d = y[0]
    c = y[1]
    o = x[2]

    o = [o, o-1, o+1]

    candidates = [(d,c,z) for z in o]
    diff_candidates = {abs_int_diff(x, z):z for z in candidates}

    return diff_candidates[min(diff_candidates.keys())]

def _tonal_unmodulo(x):
    """
    >>> _tonal_unmodulo((0,10,0))
    (0, -2, 0)

    >>> _tonal_unmodulo((6,0,0))
    (6, 12, 0)

    >>> _tonal_unmodulo((2, 0))
    (2, 0)
    """

    d = x[0]
    c = x[1]
    base_c = MS[d].c
    # Example: Cb --- base=0 c=11  c-base=11   11 - 12 = -1

    if c - base_c > 6:
        c = c - C_LEN

    # Example: B# --- base=11 c=0 c-base=-11        c+C_LEN =12
    if c - base_c < -6:
        c = c + C_LEN

    try:
        return (d, c, x[2])
    except:
        return (d, c)