"""Pitch is constructor for a TonalVector.

>>> Pitch('gsharp')
TonalVector((4, 8))


>>> Pitch('Bb')
TonalVector((6, 10))

>>> Pitch('C#')
TonalVector((0, 1))

>>> Pitch('eis')
TonalVector((2, 3))

>>> Pitch('Db3')
TonalVector((1, 1, 3))

# >>> C0 = Pitch('c0')
# >>> Pitch("a'", C0)
# TonalVector((5, 9))

"""

import re

import tonal_vector as tv


note_parser = re.compile('([a-gA-G])\s*([^-\d\s]*)\s*(-?[0-9]*)')

def int_or_none(x):
    try:
        return int(x)
    except:
        None

def pitch_to_tuple(nstr):
    note_re = note_parser.fullmatch(nstr)
    n, m, o = note_re[1].lower(), note_re[2].lower(), int_or_none(note_re[3])
    
    s = [x for x in tv.MS if x.ln == n][0]
    
    d = s.d
    
    m_key = [key for key,strs in tv.AC.items() if m in strs.values()][0]
    
    c = s.c + m_key
    
    if o is not None:
        return (d, c, o)
    return (d, c)

def Pitch(nstr):
    return tv.TonalVector(pitch_to_tuple(nstr))
    

if __name__ == "__main__":
    import doctest
    doctest.testmod()