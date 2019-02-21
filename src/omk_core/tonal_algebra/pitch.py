import re

from . import tonal_arithmetic as ta
from . import tonal_vector as tv


def Pitch(nstr, octave_context=None):
    """Returns a TonalVector from a human readable string representing a note.

    Parameters
    ----------

    nstr : str
        A human readable string representing a note, with or without an octave designation.
        Accepts:

        - letter names a-b (case insensitive)

        - modifiers/accidentals
        
          - spelled out (sharp, flat)
          - ascii (#, b)
          - unicode (♯, ♭)
          - ly (es, is)

        - octave designations

          - int
          - ly (''' ,,,)

        
        Examples: cflat; D#; Ab3; bes'; gis,,

    octave_context : tonal object or 'c4'
        If nstr is a lilypond representation using relative octaves,
        octave_context is the preceding note.

        If nstr is an int,
        octave_context may be the string c4,
        indicating that the nstr is written using c4 octave designations.

    
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

    >>> C0 = Pitch('c4', 'c4')
    >>> Pitch("a'", C0)
    TonalVector((5, 9, 0))

    """
    return tv.TonalVector(pitch_to_tuple(nstr, octave_context))
    

def pitch_to_tuple(nstr, octave_context=None):
    """Returns a tonal primitive (a tuple) from a human readble note string.

    This function implements the arithmetic for Pitch().

    Parameters
    ----------

    nstr : str
        A human readable string representing a note, with or without an octave designation.
        Accepts:

        - letter names a-b (case insensitive)

        - modifiers/accidentals
        
          - spelled out (sharp, flat)
          - ascii (#, b)
          - unicode (♯, ♭)
          - ly (es, is)

        - octave designations

          - int
          - ly (''' ,,,)

        
        Examples: cflat; D#; Ab3; bes'; gis,,

    octave_context : tonal object or 'c4'
        If nstr is a lilypond representation using relative octaves,
        octave_context is the preceding note.

        If nstr is an int,
        octave_context may be the string c4,
        indicating that the nstr is written using c4 octave designations.

    Examples
    --------

    >>> pitch_to_tuple('F#')
    (3, 6)

    >>> pitch_to_tuple('Bb')
    (6, 10)

    >>> pitch_to_tuple('a-1')
    (5, 9, -1)

    >>> pitch_to_tuple("e'''")
    (2, 4, 3)

    >>> c1 = pitch_to_tuple('c5', 'c4')
    >>> pitch_to_tuple("bis'", c1)
    (6, 10, 1)

    >>> pitch_to_tuple('q#-1')
    Traceback (most recent call last):
    ...
    ValueError: Pitch string representation is malformed.

    """
    note_re = _note_parser.fullmatch(nstr)

    if note_re is None:
        raise ValueError("Pitch string representation is malformed.")

    n = note_re[1].lower()
    m = note_re[2].lower() or ''
    o_str = note_re[3] or ''
    
    s = [x for x in tv.MS if x.ln == n][0]
    
    d = s.d
    
    m_key = [key for key,strs in tv.AC.items() if m in strs.values()][0]
    
    c = s.c + m_key
    
    o = _octave_reader((d,c), o_str, octave_context)

    if o is not None:
        return (d, c, o)
    return (d, c)


_note_parser = re.compile('([a-gA-G])\s*([^-\d\s\'\,]*)\s*(-?[0-9\'\,]*)')


def _octave_reader(note_tuple, octave_str, octave_context=None):
    """Returns the correct octave, given a tonal tuple and an octave string 
    and, optionally, an octave context.

    In the case of integer and Lilypond absolute octave inputs,
    this function simply returns the value from octave_str.
    In the case of Lilypond relative octave designations, 
    this function first finds the tonal_nearest_instance
    and then looks at octave_str to determine the correct octave.

    Parameters
    ----------

    note_tuple : tuple
        A two-value (octaveless) tonal tuple.
    
    octave_str : str
        The portion of nstr (from the above functions) which specifies the octave.
        This will be a string representation of an integer,
        some number of (''')s or (,,,)s,
        or an empty string.

    octave_context : tonal object with octave
        Used for Lilypond relative octave notation,
        this is the previous note (as a TonalVector or tuple)
        in a Lilypond parsing context.
    """

 
    # if int(octave) works, return the int
    # - if int(octave works) and octave_context is provided throw error

    try:
        octave_int = int(octave_str)
    except:
        pass
    else:
        if octave_context is not None:
            if octave_context.lower() != 'c4':
                raise TypeError("An integer octave designation does not need an octave context.")
            else: # context is c4
                return octave_int - 4
        return octave_int


    # if octave designation is empty
    #  - if octave context is present, this is lilypond relative
    #  - if octave context is not present, return None
    #     - if COULD be ly relative, but the ly parser will have to figure that out

    # if octave designation is '... or ,... 
    #  - if no context, ly absolute --- octave = len
    #  - if context, ly relative - octave = nearest +/- len

    if octave_str == '':
        if octave_context is None:
            return None

    octave_set = set(octave_str)
        
    if octave_str != '' and octave_set.isdisjoint(set(["'",","])):
        raise ValueError("Octave designation is malformed.")

    tmp_octave_val = len(octave_str)

    if octave_set == set([","]):
        tmp_octave_val = -tmp_octave_val

    if octave_context is None:
        return tmp_octave_val

    context_octave = ta.tonal_nearest_instance(octave_context, note_tuple)[2]
    octave_int = context_octave + tmp_octave_val

    return octave_int



if __name__ == "__main__":
    import doctest
    doctest.testmod()