from fractions import Fraction as Frac
import itertools
import math

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
        num = self.numerator
        den = self.denominator
    
        dots = int(math.log2(num + 1)) - 1
        base = NoteLength(num+1, den) * Frac(1,2)
    
        return base, dots

    def untuple(self):
        """
        >>> NoteLength(1, 3).untuple()
        (NoteLength(1, 2), 3)

        >>> NoteLength(1, 6).untuple()
        (NoteLength(1, 4), 3)

        >>> NoteLength.TupletMember(NoteLength(1,4), 7).untuple()
        (NoteLength(1, 4), 7)

        >>> NoteLength(1, 4).untuple()
        (NoteLength(1, 4), 0)
        """
        if math.log2(self).is_integer(): # if is power of 2
            return (self, None)
    
        for tt in ((x*2)+1 for x in itertools.count()):
            if math.log2(self.denominator/tt).is_integer(): # if is power of 2
                break
                
        return self.__class__(int(self.numerator), int((2 ** math.floor(math.log2(tt)))*self.denominator/tt)), tt

    # util methods

    def __repr__(self):
        if self.numerator == 1 and math.log2(self.denominator).is_integer():
            return "NoteLength({}, {})".format(self.numerator, self.denominator)

        if not math.log2(self.denominator).is_integer(): # tuplet
            untuple_note, tuplet_divs = self.untuple()
            return "NoteLength.TupletMember({}, {})".format(
                untuple_note.__repr__(),
                tuplet_divs.__repr__()
                )

        # is dotted but isn't tuplet
        undot_note, dots = self.undot()
        return "{}.dot({})".format(undot_note.__repr__(), dots.__repr__())




        


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
        numerator = notated_length * (2 ** math.floor(math.log2(divisions)))
        return cls((numerator * length), divisions) # , (notated_length * length))

    