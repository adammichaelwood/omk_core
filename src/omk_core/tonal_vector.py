from dotmap import DotMap

import tonal_arithmetic as ta

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
        TonalVector((2, 3, 1)) # E♭ 1 | NotImplemented
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
        """
        return TonalVector(ta.tonal_diff(self, x))

    def __abs__(self):
        return ta.tonal_abs(self)

    def __int__(self):
        return ta.tonal_int(self)

    def __gt__(self, x):
        return int(self) > int(x)

    def __lt__(self, x):
        return int(self) < int(x)

    def inversion(self, x=(0,0)):
        return TonalVector(ta.tonal_invert(self, x))

    # __eq__ not needed -- will be evaluated as a tuple




    ### Represent as a note ###

    class Note():
        
        def __init__(self, vector):
            self._v = vector


        # letter name
        @property
        def _ln(self):
            return self._v._Q.ln.upper()

        # how sharp or flat
        @property
        def _modifier_value(self): 
            return  self._v.c - self._v._Q.c

        @property
        def _modifier(self):
            return AC[self._modifier_value]

        def _unicode(self, octave_modifier=0):
            ustr = self._ln

            if self._modifier_value:
                ustr = "".join([ustr, self._modifier.u])

            if self._v._has_octave:
                ustr = " ".join([ustr, str(self._v.o + octave_modifier)])
            
            return ustr

        @property
        def unicode(self):
            return self._unicode()

        @property
        def unicode_C4(self):
            return self._unicode(octave_modifier=4)

        def _ascii(self, octave_modifier=0):
            astr = self._ln

            if self._modifier_value:
                astr = "".join([astr, self._modifier.a])

            if self._v._has_octave:
                astr = " ".join([astr, str(self._v.o + octave_modifier)])
            
            return astr
            
        @property
        def ascii(self):
            return self._ascii()

        @property
        def ascii_C4(self):
            return self._ascii(octave_modifier=4)

        @property
        def ly(self, show_octave=False):
            lystr = self._ln

            if self._modifier_value:
                lystr = "".join([lystr, self._modifier.ly])

            if self._v._has_octave and show_octave:
                lystr = " ".join([lystr, str(self._v.o)])
            
            return lystr

        @property
        def verbose(self):
            return " ".join([self._ln, self._modifier.v]).upper()

    
    class Interval():

        def __init__(self, vector):
            self._v = vector

        @property
        def unicode(self):
            return "NotImplemented"

if __name__ == "__main__":
    import doctest
    doctest.testmod()