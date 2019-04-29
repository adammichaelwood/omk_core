from fractions import Fraction as Frac
import itertools
import math
import warnings

from ..utils.math import pow2_floor_frac, primes, is_pow2

class NoteLength(Frac):
    """
    >>> NoteLength(1,4) # Quarter Note
    NoteLength(1, 4)

    >>> NoteLength('1/4') # Quarter Note
    NoteLength(1, 4)
    """

    # reimplement arithmetic to return correct class

    def __add__(self, x):
        """
        >>> NoteLength(1, 4) + NoteLength(1, 4)
        NoteLength(1, 2)

        >>> NoteLength(1, 2) + Frac(1, 2)
        NoteLength(1, 1)

        >>> NoteLength(1, 8) + 0.25
        NoteLength(3, 8)
        """
        return self.__class__(Frac(self) + x)
        
    def __radd__(self, x):
        """
        >>> NoteLength(1, 4) + NoteLength(1, 4)
        NoteLength(1, 2)

        >>> Frac(1, 2) + NoteLength(1, 2)
        NoteLength(1, 1)

        >>> 0.25 + NoteLength(1, 8)
        NoteLength(3, 8)
        """
        return self.__add__(x)

    def __sub__(self, x):
        """
        >>> NoteLength(1, 4) - NoteLength(1, 8)
        NoteLength(1, 8)

        >>> NoteLength(1, 2) - Frac(1, 8)
        NoteLength(3, 8)

        >>> NoteLength(1, 2) - 0.25
        NoteLength(1, 4)
        """
        return self.__class__(self.__add__(-x))

    def __rsub__(self, x):
        """
        >>> Frac(1, 2) - NoteLength(1, 4)
        NoteLength(1, 4)

        >>> 0.25 - NoteLength(1, 16)
        NoteLength(3, 16)
        """
        return self.__class__((-self).__add__(x))

    def __mul__(self, x):
        """
        >>> NoteLength(1, 4) * 2
        NoteLength(1, 2)

        >>> NoteLength(1, 4) * 0.5
        NoteLength(1, 8)
        """
        return self.__class__(Frac(self) * x) 

    def __rmul__(self, x):
        """
        >>> 2 * NoteLength(1, 4)
        NoteLength(1, 2)

        >>> 0.5 * NoteLength(1, 4)
        NoteLength(1, 8)
        """
        return self.__mul__(x)



    # rhythmic methods

    def dot(self, dots=1):
        """
        >>> NoteLength(1, 4).dot()
        NoteLength(3, 8)
        """

        return sum([self*Frac(1,(2**n)) for n in range(0,dots+1)])

    # rendering to other systems, making sense

    def undot(self):
        """
        Returns a tuple of (base note, dots).

        Examples
        --------

        >>> dhn = NoteLength(1, 2).dot()
        >>> dhn.undot()
        (NoteLength(1, 2), 1)

        >>> ddqn = NoteLength(1, 4).dot(2)
        >>> ddqn.undot()
        (NoteLength(1, 4), 2)

        >>> NoteLength(1,8).undot()
        (NoteLength(1, 8), 0)
        """
        base_note = NoteLength(pow2_floor_frac(self))
        dotted_value = base_note
        dots = 0
        while dotted_value != self:
            dots += 1
            dotted_value = base_note.dot(dots)
        return self.__class__(base_note), dots

    def untuple(self):
        """
        >>> NoteLength(1, 3).untuple()
        (NoteLength(1, 2), 3)

        >>> NoteLength(1, 6).untuple()
        (NoteLength(1, 4), 3)

        >>> NoteLength.TupletMember(NoteLength(1,4), 7).untuple()
        (NoteLength(1, 4), 7)

        >>> NoteLength(1, 4).untuple()
        (NoteLength(1, 4), None)
        """
        if is_pow2(self.denominator):
            return (self, None)

        for tt in primes(3):
            total_length = self * tt
            nominal_length = total_length / pow2_floor_frac(tt)
            if is_pow2(nominal_length.denominator):
                return self.__class__(nominal_length), tt

    # util methods

    def _plain_repr(self):
        return "NoteLength({}, {})".format(self.numerator, self.denominator)

    def __repr__(self):
        if is_pow2(self.denominator): 
            return self._plain_repr()
        
        untup_base, untup_tt = self.untuple()
        if untup_tt is not None: # tuplet
            untuple_note, tuplet_divs = self.untuple()
            return "NoteLength.TupletMember({}, {})".format(
                untup_base.__repr__(),
                untup_tt.__repr__()
                )

        # is dotted but isn't tuplet
        undot_note, dots = self.undot()
        return "{}.dot({})".format(undot_note.__repr__(), dots.__repr__())


        


    # Constructors

    @classmethod
    def TupletMember(cls, nominal_length="1/4", tuplet_type=3, units=1):
        """
        Returns a NoteLength representing a single note in a tuple.
        Default return a quarter note triplet member.

        Parameters
        ----------

        nominal_length : any type castable to NoteLength
            The notated length of a single division of the tuplet.

        tuplet_type : int
            The number of divisions of the total tuplet length.

            The actual length of the total tuplet is
            nominal_length times the nearest power of two below tuplet_type.
            For example:
            - the total value of a quarter note triplet
            is equal to two quarter notes.
            - the total value of an eigth note septuplet (7-part)
            is equal to four eighth notes.


        units : number
            The length of the TupletMember,
            as measured in tuplet divisions.
            For example, in a quarter note triplet notated as
            3[half_note, quarter_note], the half note has a length of 2.
        """
        if not is_pow2(nominal_length):
            warnings.warn("Making tuplets from dotted notes may fail unexpectedly.", RhythmWarning)

        nl = cls(nominal_length * units)

        total_length = nl * pow2_floor_frac(tuplet_type)
        member_length = total_length/tuplet_type
        return cls(member_length)

class RhythmWarning(UserWarning):
    pass
warnings.simplefilter('always', RhythmWarning)
    