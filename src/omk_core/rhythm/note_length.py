from fractions import Fraction as Frac
import math

from . import time_length as tl

class NoteLength(tl.TimeLength):
    """
    >>> NoteLength(1,4) # Quarter Note
    NoteLength(1, 4)

    >>> NoteLength('1/4') # Quarter Note
    NoteLength(1, 4)
    """
    #def __new__(cls, numerator, denominator=None, nominal_value=None):
    #    return super().__new__(cls, numerator, denominator)

    #def __init__(self, numerator, denominator=None, nominal_value=None):
    #    self.nominal_value = nominal_value

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
        >>> undot(dhn)
        (NoteLength(1, 2), 1)

        >>> ddqn = NoteLength(1, 4).dot(2)
        >>> undot(ddqn)
        (NoteLength(1, 4), 2)

        >>> undot(NoteLength(1,8))
        (NoteLength(1, 8), 0)
        """
        num = self.numerator
        den = self.denominator
    
        dots = int(math.log2(num + 1)) - 1
        base = NoteLength(num+1, den) * Frac(1,2)
    
        return base, dots

    def untuple(self):
        if math.log2(self).is_integer(): # if is power of 2
            return self
    
        primes = [3,5,7,11,13]
        for p in primes:
            if math.log2(self.denominator/p).is_integer(): # if is power of 2
                break
                
        return self.__class__(int(self.numerator), int((p-1)*self.denominator/p)), p

    # util methods

    def __repr__(self):
        return "NoteLength({}, {})".format(self.numerator, self.denominator)

    # Constructors

    @classmethod
    def TupletMember(cls, notated_length="1/4", divisions=3, length=1):
        """
        Returns a NoteLength representing a single note in a tuple.
        Default return a quarter note triplet member.

        Parameters
        ----------

        notated_length : any type castable to NoteLength
            The notated length of a single division of the tuplet.

        divisions : int
            The number of divisions of the total tuplet length.

            The actual length of the total tuplet is
            one less than the number of divisions times the notated_length.
            For example, the total value of a quarter note triplet
            is equal to two quarter notes.

        length : int
            The length of the TupletMember,
            as measured in tuplet divisions.
            For example, in a quarter note triplet notated as
            3[half_note, quarter_note], the half note has a length of 2.
        """
        notated_length = cls(notated_length)
        numerator = notated_length * (divisions - 1)
        return cls((numerator * length), divisions) # , (notated_length * length))

    