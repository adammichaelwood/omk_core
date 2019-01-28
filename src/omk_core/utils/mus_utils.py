def tonal_args(func):
    """Decorates a function that should only take valid tonal primitives as arguments.

    A tonal primitive is a tuple of two or three values,
    isomorphically representing either:

    - an interval (for example: :i:`Major 3`, :i:`Diminished 4`)
    - a chroma (a named pitch class; for example: :c:`C`, :c:`D#`)

    If there is a third value, it represents an octave designation.


    Tests
    -----

    >>> tonal_args(lambda x: x)((3,))
    Traceback (most recent call last):
    ...
    TypeError: Tonal primitives have two or three values.

    >>> tonal_args(lambda x: x)((3,2))
    (3, 2)

    >>> tonal_args(lambda x: x)((3,2,1))
    (3, 2, 1)

    >>> tonal_args(lambda x: x)((3, 2, 1, 0))
    Traceback (most recent call last):
    ...
    TypeError: Tonal primitives have two or three values.

    """

    def wrapper(*args, **kwargs):

        [err_if_not_tonal(arg) for arg in args]

        return func(*args, **kwargs)

    return wrapper


def err_if_not_tonal(x):
    # 2 or 3 values.
    if len(x) not in (2,3):
        raise TypeError("Tonal primitives have two or three values.")

    # Diatonic Value
    try:
        if x[0] not in range(D_LEN):
            raise ValueError("The Diatonic Value of a tonal primitive must be an integer in the range [0,6]")
    except TypeError:
        raise TypeError("The Diatonic Value of a tonal primitive must be an integer.")

    # Chromatic Value
    try:
        if x[1] < 0 or x[1] >= 12:
            raise ValueError("The Chromatic Value of a tonal primitive must be a number `c` where `0 <= c < 12`.")
    except TypeError:
        raise TypeError("The Chromatic Value of a tonal primitive must be a number.")

    # Octave Value
    try:
        if type(x[2]) is not int:
            raise TypeError("The Octave value of a tonal primitive must be an integer.")
    except IndexError: 
        pass

    return True

