import math

from utils.method_dispatch import methoddispatch
from functools import singledispatch

"""
:dfn:`Quality` is a characteristic of an :term:`interval`
that specifies the exact :term:`magnitude`.

.. meta:: iq

In the :term:`Diatonic Major Scale`,
all intervals are either
:iq:`perfect`  (:i:`1`, :i:`4`, :i:`5`, :i:`8`)
or
:iq:`major` (:i:`2`, :i:`3`, :i:`6`, :i:`7`).

When either type of interval is augmented by one half-step,
the quality is :iq`augmented`.
When a :iq:`major` interval is diminished, the quality is minor;
whereas,
when a :iq:`perfect` interval is diminished, the quality is :iq`diminished`.
A :iq:`major` interval has to be diminished by two half steps,
passing through :iq:`minor`,
before becoming a :iq:`diminished` interval.

Consequently,
if we wish to map qualities to numbers
so that we can easily move from one to another,
we must recognized that there is not one single meaning of :iq:`augmented: or :iq:`diminished`.
That is, (:iq:`augmented` - 1) might be :iq:`perfect` or :iq:`major.
Therefore, there are two meanings of :iq:`augmented`.
And (:iq:`dminished` + 1) might be :iq:`perfect` or :iq:`minor`.
Therefore, there two meanings of :iq:`diminished`.

To represent these relationships
in a way that lends itself easily to
arithmetic tranformation,
we can map them onto a short number line:

"""


q_vals = {
- 2.5 : 'dbl_dimished-from_maj_min',
- 2   : 'dbl_diminished-from_perfect',
- 1.5 : 'diminished-from_maj_min',
- 1   : 'diminished-from_perfect',
- 0.5 : 'minor',
  0   : 'perfect',
  0.5 : 'major',
  1   : 'augmented-from_perfect',
  1.5 : 'augmented-from_maj_min',
  2   : 'dbl_augmented-from_perfect',
  2.5 : 'dbl_augmented-from_maj_min'
}

"""

..  devnote:

    This may cause a problem with quarter tones.
    I have a hunch they could be represented with composite numbers:
    (x + 0.5j)


"""

class IntervalQuality:


    qualities = {}

    def __init__(self, name, rel_number):
        self.name = name
        self.__rel_number = rel_number
        self.chromatic_modifier = self._chromatic_modifier()
        self.qualities[self.__rel_number] = self

    def _chromatic_modifier(self):
        """Returns a signed integer indicating
           the change in chromatic value from
           the interval of the same number
           in the diatonic major scale."""

        return math.floor(self.__rel_number)


    # Arithmetic operations

    def augment(self, halfsteps=1):
        aug_number = self.__rel_number + halfsteps
        return self.qualities[aug_number]

    def diminish(self, halfsteps=1):
        return self.augment(-halfsteps)

    def __add__(self, halfsteps):
        return self.augment(halfsteps)

    def __sub__(self, halfsteps):
        return self.__add__(-halfsteps)


    # String representations

    def abbr(self):
        return " ".join([wrd[:3] for wrd in str(self).split()])

    def __str__(self):
        return " ".join(self.name.split("-")[0].split("_"))

    def __repr__(self):
        return self.name



# Instantiate the Interval Qualities
for number, name in q_vals.items():
    IntervalQuality(name, number)


if __name__ == "__main__":
    print(IntervalQuality.qualities)
    import doctest
    doctest.testmod()
