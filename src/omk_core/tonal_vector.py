from dotmap import DotMap

import tonal_arithmetic as ta
import interval_quality as iq

# "M_ajor Scale"
MS = [
    # diatonic value, chromatic value, interval quality (0 or 0.5), letter name, solfege list, function, diszonance
    {'d':0, 'c':0,  'q':0,   'in': 'unison',  'ln':"c", 'sf':['do'],  'f': 'tonic',        'z': 0},
    {'d':1, 'c':2,  'q':0.5, 'in': 'second',  'ln':"d", 'sf':['re'],  'f': 'subtonic',     'z': 2},
    {'d':2, 'c':4,  'q':0.5, 'in': 'third',   'ln':"e", 'sf':['mi'],  'f': 'mediant',      'z': 1},
    {'d':3, 'c':5,  'q':0,   'in': 'fourth',  'ln':"f", 'sf':['fa'],  'f': 'subdominant',  'z': 2},
    {'d':4, 'c':7,  'q':0,   'in': 'fifth',   'ln':"g", 'sf':['sol'], 'f': 'dominant',     'z': 0},
    {'d':5, 'c':9,  'q':0.5, 'in': 'sixth',   'ln':"a", 'sf':['la'],  'f': 'submediant',   'z': 1},
    {'d':6, 'c':11, 'q':0.5, 'in': 'seventh', 'ln':"b", 'sf':['ti'],  'f': 'leading tone', 'z': 3}
]

MS = [DotMap(x) for x in MS]

# Accidentals
AC = {
    # halfsteps : verbose, unicode, ascii, ly
    -2 : {'v': 'double flat', 'u':'𝄫', 'a':'bb', 'ly':'isis' },
    -1 : {'v': 'flat', 'u':'♭', 'a':'b', 'ly':'is'},
     0 : {'v': 'natural', 'u':'♮', 'a':'', 'ly':''},
     1 : {'v': 'sharp', 'u':'♯', 'a':'#', 'ly':'es'},
     2 : {'v': 'double sharp', 'u':'𝄪', 'a':'##', 'ly':'eses'},
}

AC = {i:DotMap(x) for i,x in AC.items()}


class TonalVector(tuple):
    
    def __new__(cls, tp):
        return super(TonalVector, cls).__new__(TonalVector, tp)
        
    def __init__(self, tp):

        self.d = self[0] # diatonic value
        self.c = self[1] # chromatic value
        self._Q = MS[self.d] # Q for source # rename?
        self.note = self.Note(self)
        self.interval = self.Interval(self)

        # if a third value (octave) supplied
        try:
            self.o = self[2]
            self._has_octave = True
        except IndexError:
            self.o = None
            self._has_octave = False

    ### Util ###

    def __repr__(self):
        """
        >>> TonalVector((0,0))
        TonalVector((0, 0))

        >>> TonalVector((2,4,1))
        TonalVector((2, 4, 1))
        """
        return "TonalVector({})".format(repr(tuple(self)))

    def __str__(self):
        """
        >>> print(TonalVector((0,1)))
        TonalVector((0, 1)) # C♯ | NotImplemented

        >>> print(TonalVector((2,3,1)))
        TonalVector((2, 3, 1)) # E♭1 | NotImplemented
        """
        return "{} # {} | {}".format(repr(self), self.note.unicode, self.interval.unicode)

    ### Tonal Arithmetic ###

    def __add__(self, x):
        """
        >>> TonalVector((0,1)) + TonalVector((1,1))
        TonalVector((1, 2))

        >>> TonalVector((6,11,1)) + TonalVector((1,1))
        TonalVector((0, 0, 2))
        """
        return TonalVector(ta.tonal_sum(self, x))

    def __sub__(self, x):
        """
        >>> TonalVector((0,1)) - TonalVector((1,1))
        TonalVector((6, 0))

        >>> TonalVector((6,11,1)) - TonalVector((1,1))
        TonalVector((5, 10, 1))

        >>> abs(TonalVector((6,11,1)) - TonalVector((1,1,0))) == abs(TonalVector((1,1,0)) - TonalVector((6,11,1)))
        True
        """
        return TonalVector(ta.tonal_diff(self, x))

    def distance(self, x):
        """Returns the smallest difference 
        return TonalVector(ta.tonal_abs_diff(self, x))

        >>> TonalVector((0,0,0)).distance(TonalVector((4,7,0)))
        TonalVector((4, 7, 0))

        >>> TonalVector((4,7,0)).distance(TonalVector((0,0,0)))
        TonalVector((4, 7, 0))

        >>> TonalVector((0,0)).distance(TonalVector((4,7)))
        TonalVector((3, 5))
        """
        return TonalVector(ta.tonal_abs_diff(self, x))

    def nearest_instance(self, x):
        """Returns a Tonal Vector that has the same pitch class or interval type as x,
        closest to self.

        Examples
        --------

        >>> TonalVector((0,0)).nearest_instance(TonalVector((1,1,-3)))
        TonalVector((1, 1))

        >>> TonalVector((0,0)).nearest_instance(TonalVector((6,11,3)))
        TonalVector((6, 11))

        >>> TonalVector((0,0,0)).nearest_instance(TonalVector((1,1,-3)))
        TonalVector((1, 1, 0))

        >>> TonalVector((0,0,0)).nearest_instance(TonalVector((6,11,3)))
        TonalVector((6, 11, -1))
        """

        return TonalVector(ta.tonal_nearest_instance(self,x))


    def __abs__(self):
        """
        >>> abs(TonalVector((0,0,-1)))
        12

        >>> abs(TonalVector((0,0,1)))
        12
        """
        return ta.tonal_abs(self)

    def __int__(self):
        """
        >>> int(TonalVector((0,0,-1)))
        -12

        >>> int(TonalVector((0,0,1)))
        12
        """
        return ta.tonal_int(self)

    def __gt__(self, x):
        """
        >>> TonalVector((1,1,0)) > TonalVector((0,0,0))
        True

        >>> TonalVector((2,4,1)) > (3,5,1)
        False

        >>> TonalVector((3,6,1)) > 6
        True
        """
        try:
            return int(self) > int(x)
        except TypeError:
            return int(self) > ta.tonal_int(x)

    def __lt__(self, x):
        """
        >>> TonalVector((1,1,0)) < TonalVector((0,0,0))
        False

        >>> TonalVector((2,4,1)) < (3,5,1)
        True

        >>> TonalVector((3,6,1)) < 6
        False
        """
        try:
            return int(self) < int(x)
        except TypeError:
            return int(self) < ta.tonal_int(x)

    def inversion(self, x=(0,0)):
        """
        >>> TonalVector((2,4)).inversion() # Maj3 --> min6
        TonalVector((5, 8))

        >>> TonalVector((5,8)).inversion() # min6 --> Maj3
        TonalVector((2, 4))

        >>> TonalVector((3,6)).inversion() # Aug4 --> dim5 (tritone)
        TonalVector((4, 6))

        >>> TonalVector((0,1,0)).inversion((0,0,0)) # augment unison --> diminished octave
        TonalVector((0, 11, 0))
        """
        return TonalVector(ta.tonal_invert(self, x))

    def __eq__(self, x):
        """
        >>> TonalVector((0,1,0)) == (0,1,0)
        True

        >>> TonalVector((0,1)) == TonalVector((1,1))
        False

        >>> TonalVector((0,1)) == 1
        True

        >>> int(TonalVector((0,1))) == int(TonalVector((1,1)))
        True
        """
        if type(self) == type(x):
            return tuple(self) == tuple(x)
        return tuple(self) == x or int(self) == x




    ### Represent as a note ###

    class Note():
        
        def __init__(self, vector):
            self._v = vector


        # letter name
        @property
        def _ln(self):
            """The letter name (without sharps or flats) of the note.
            
            Examples
            --------

            >>> TonalVector((0,0)).note._ln
            'C'

            >>> TonalVector((0,1)).note._ln
            'C'
            """
            return self._v._Q.ln.upper()

        # how sharp or flat
        @property
        def _modifier_value(self):
            """A number representing the distance in halfsteps between the named note
            and the natural version of the named note.

            >>> TonalVector((0,1)).note._modifier_value # C sharp
            1

            >>> TonalVector((4,6,1)).note._modifier_value # G flat
            -1
            """

            return  self._v.c - self._v._Q.c

        @property
        def _modifier(self):
            """A dict of info about how to represent the modifier (sharp, flat, natural).

            >>> TonalVector((0,0)).note._modifier == {'v': 'natural', 'u':'♮', 'a':'', 'ly':''}
            True
            """
            return AC[self._modifier_value]

        def _unicode(self, octave_modifier=0):
            """Returns a human readable representation of the note, with Unicode modifiers (♯, ♭).
            The octave_modifier can be used to set the octave designation for middle C.
            (In OMK, middle C == C0. In MIDI etc., middle C == C4).

            Examples
            --------

            >>> TonalVector((0,1)).note._unicode()
            'C♯'

            >>> TonalVector((1,1,0)).note._unicode(4)
            'D♭4'
            """
            ustr = self._ln

            if self._modifier_value:
                ustr = "".join([ustr, self._modifier.u])

            if self._v._has_octave:
                ustr = "".join([ustr, str(self._v.o + octave_modifier)])
            
            return ustr

        @property
        def unicode(self):
            """A human readable representation of the note, with Unicode modifiers (♯, ♭).
            If the note has an octave designation, middle C == C0.

            Examples
            --------

            >>> TonalVector((0,1)).note.unicode
            'C♯'

            >>> TonalVector((1,1,0)).note.unicode
            'D♭0'
            """
            return self._unicode()

        @property
        def unicode_C4(self):
            """A human readable representation of the note, with Unicode modifiers (♯, ♭).
            If the note has an octave designation, middle C == C4.

            Examples
            --------

            >>> TonalVector((0,1)).note.unicode_C4
            'C♯'

            >>> TonalVector((1,1,0)).note.unicode_C4
            'D♭4'
            """
            return self._unicode(octave_modifier=4)

        def _ascii(self, octave_modifier=0):
            """Returns a human readable representation of the note, with ascii modifiers (#, b).
            The octave_modifier can be used to set the octave designation for middle C.
            (In OMK, middle C == C0. In MIDI etc., middle C == C4).

            Examples
            --------

            >>> TonalVector((0,1)).note._ascii()
            'C#'

            >>> TonalVector((1,1,0)).note._ascii(4)
            'Db4'
            """
            astr = self._ln

            if self._modifier_value:
                astr = "".join([astr, self._modifier.a])

            if self._v._has_octave:
                astr = "".join([astr, str(self._v.o + octave_modifier)])
            
            return astr
            
        @property
        def ascii(self):
            """A human readable representation of the note, with Ascii modifiers (#, b).
            If the note has an octave designation, middle C == C0.

            Examples
            --------

            >>> TonalVector((0,1)).note.ascii
            'C#'

            >>> TonalVector((1,1,0)).note.ascii
            'Db0'
            """
            return self._ascii()

        @property
        def ascii_C4(self):
            """A human readable representation of the note, with Ascii modifiers (#, b).
            If the note has an octave designation, middle C == C4.

            Examples
            --------

            >>> TonalVector((0,1)).note.ascii_C4
            'C#'

            >>> TonalVector((1,1,0)).note.ascii_C4
            'Db4'
            """
            return self._ascii(octave_modifier=4)

        @property
        def ly_chroma(self):
            """The Lilypond representation of the note name, 
            without an octave designation.

            Examples
            --------

            >>> TonalVector((0,1)).note.ly_chroma # C sharp
            'ces'

            >>> TonalVector((6,10,1)).note.ly_chroma # B flat, with an octave designation
            'bis'
            """

            return "".join([self._ln.lower(), self._modifier.ly])

        @property
        def ly_abs8ve(self):
            """The Lilypond representation of the note name,
            with an absolute octave designation. 
            (see: http://lilypond.org/doc/v2.18/Documentation/learning/absolute-note-names)

            Examples
            --------

            >>> TonalVector((0,0,1)).note.ly_abs8ve # C above middle C
            "c'"

            >>> TonalVector((6,10,-1)).note.ly_abs8ve # B flat below middle C
            'bis,'

            >>> TonalVector((3,6,0)).note.ly_abs8ve # F sharp in octave of middle c
            'fes'

            >>> TonalVector((3,6)).note.ly_abs8ve # F sharp, no octave designation
            'fes'

            >>> TonalVector((1,1,4)).note.ly_abs8ve # D flat, 4 octaves above middle c
            "dis''''"

            >>> TonalVector((1,1,-4)).note.ly_abs8ve # D flat, 4 octaves below middle c
            'dis,,,,'
            """

            if not self._v._has_octave:
                return self.ly_chroma

            if self._v.o < 0:
                ostr = ","
            else:
                ostr = "'"

            return "".join([self.ly_chroma, ostr*abs(self._v.o)])


        def ly_rel8ve(self, prev=None):
            """Returns the Lilypond representation of the note name,
            with a relative octave designation, based on the previous note.

            >>> TonalVector((3,5,0)).note.ly_rel8ve(TonalVector((0,0,0)))
            'f'

            >>> TonalVector((4,7,0)).note.ly_rel8ve(TonalVector((0,0,0)))
            "g'"

            >>> TonalVector((3,5,-1)).note.ly_rel8ve(TonalVector((0,0,0)))
            'f,'

            >>> TonalVector((4,7,-1)).note.ly_rel8ve(TonalVector((0,0,0)))
            'g'
            """
            if prev == None:
                return self.ly_abs8ve

            if self._v.distance(prev).d <= 3:
                return self.ly_chroma

            closer_chroma = prev.nearest_instance(self._v)

            octave_distance = self._v.o - closer_chroma.o

            if octave_distance < 0:
                ostr = ","
            else:
                ostr = "'"

            return "".join([self.ly_chroma, ostr*abs(octave_distance)]) 


        @property
        def verbose(self):
            """
            >>> TonalVector((0,0)).note.verbose
            'C'
            
            >>> TonalVector((0,1)).note.verbose
            'Csharp'

            >>> TonalVector((0,1,1)).note.verbose
            'Csharp1'

            """ 
            if self._v.o == None:
                o = ""
            else:
                o = str(self._v.o)

            if self._modifier_value == 0:
                mod_text = ""
            else:
                mod_text = self._modifier.v

            return "".join([self._ln, mod_text, o])

        def __repr__(self):
            """
            >>> TonalVector((0, 0, 0)).note
            TonalVector((0, 0, 0)).note
            """
            return "".join([self._v.__repr__(), ".note"])

        def __str__(self):
            """
            >>> str(TonalVector((0, 0, 0)).note)
            'C0 | (0, 0, 0)'
            """
            return "".join([self.unicode, " | ", str(tuple(self._v))])

    
    class Interval():

        def __init__(self, vector):
            self._v = vector
            # self.quality = iq._get_quality(vector)

        @property
        def unicode(self):
            return "NotImplemented"

        


if __name__ == "__main__":
    import doctest
    doctest.testmod()