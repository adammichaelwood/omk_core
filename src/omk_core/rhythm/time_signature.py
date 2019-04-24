from fractions import Fraction as Frac 

# from . import time_length as tl

class TimeSignature(Frac):
    """
    The length of musical time in one measure.
    """

    def __new__(cls, numerator, denominator):

        return super().__new__(cls, numerator, denominator)

    def __init__(self, numerator, denominator):
        self._n = numerator
        self._d = denominator
        self._multiplier = int(denominator/self.denominator)

        self._str = "{}/{}".format(
            str(self.numerator*self._multiplier), 
            str(self.denominator*self._multiplier)
            )

  
    def __add__(self, x):
        frac_sum = Frac(self) + Frac(x)
        
        try:
            den = max([self._d, x._d, frac_sum.denominator])
        except NameError:
            den = self._d

        m = den / frac_sum.denominator
        num = int(frac_sum.numerator * m)
        return self.__class__(num, den)


