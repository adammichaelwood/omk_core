from fractions import Fraction as Frac 

class TimeSignature(Frac):
    """
    The length of musical time in one measure.
    """

    def __new__(cls, numerator, denominator=None, groupings=None):

        return super().__new__(cls, numerator, denominator)

    def __init__(self, numerator, denominator=None, groupings=None):
        if denominator is None:
            self._n = self.numerator
            self._d = self.denominator
        else:
            self._n = numerator
            self._d = denominator

        self.groupings = groupings
        # self._multiplier = int(denominator/self.denominator)

        self._str = "{}/{}".format(
            str(self._n), 
            str(self._d)
            )

  
    def __add__(self, x):
        frac_sum = Frac(self) + Frac(x)
        
        try:
            x_d = x._d
        except AttributeError:
            x_d = 0

        den = max([self._d, x_d, frac_sum.denominator])

        m = Frac(den, frac_sum.denominator)
        num = frac_sum.numerator * m
        return self.__class__(num, den)

    def __radd__(self, x):
        return self.__add__(x)

    def __sub__(self, x):
        return self.__add__(-x)

    def __rsub__(self, x):
        return self.__class__((-self).__add__(x))

    def __mul__(self, x):
        frac_prod = Frac(self) * Frac(x)
        
        try:
            x_d = x._d
        except AttributeError:
            x_d = 0

        den = max([self._d, x_d, frac_prod.denominator])

        m = Frac(den, frac_prod.denominator)
        num = frac_prod.numerator * m
        return self.__class__(num, den)

    def __rmul__(self, x):
        return self.__mul__(x)

    def __truediv__(self, x):
        return self.__mul__(Frac(1,x))

