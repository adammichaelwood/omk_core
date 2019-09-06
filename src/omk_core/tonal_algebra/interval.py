import re

from ..definitions.constants import MS
from . import tonal_vector as tv
from . import interval_quality as iq

_interval_parser = re.compile("([apmdAPMD][a-zA-Z]*)\s?(\d+)\,?\s?([+\-]?\d*)")


def Interval(istr):
    """Returns a tonal vector from a human-readable string representing an interval.
    
    Examples
    --------

    >>> Interval('P5')
    TonalVector((4, 7))

    >>> Interval('aug2, +1')
    TonalVector((1, 3, 1))

    >>> Interval('maj 7 -3')
    TonalVector((6, 11, -3))

    >>> Interval('m6+2')
    TonalVector((5, 8, 2))

    >>> Interval('aug 3, +4')
    TonalVector((2, 5, 4))

    >>> Interval('d2, -1')
    TonalVector((1, 0, -1))

    >>> Interval('dim7, -1')
    TonalVector((6, 9, -1))

    >>> Interval('min 2, -1')
    TonalVector((1, 1, -1))
    
    """

    return tv.TonalVector(interval_to_tuple(istr))

def interval_to_tuple(istr):

    i_re = _interval_parser.fullmatch(istr)

    if i_re is None:
        raise ValueError("Interval string representation is malformed.")

    n = int(i_re[2]) # name
    d = n - 1 # diatonic value


    # determine chromatic value from difference between "natural" quality and given quality
    
    qn = i_re[1]  
    q = iq._get_quality(qn, d)
    
    c = MS[d].c + q.chromatic_modifier


    try:
        o = int(i_re[3]) # octave
    except ValueError:
        return (d, c)
    else:
        return(d, c, o)


if __name__ == "__main__":
    import doctest
    doctest.testmod()




    

    