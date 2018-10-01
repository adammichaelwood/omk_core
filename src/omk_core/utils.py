def tonal_args(func):
    """Decorates a function that should only take valid tonal primitives as arguments.

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
    if len(x) not in (2,3):
        raise TypeError("Tonal primitives have two or three values.")
    return True
