from fractions import Fraction as Frac 

class TimeLength(Frac):
    """
    "Abstract" class, representing a length of musical time. 
    
    Primary purpose is modifying Fraction's arithmetic to:
     - return the proper type (not fractions)
    """
    # reimplement arithmetic to return correct class

    def __add__(self, x):
        return self.__class__(Frac(self) + Frac(x))
        
    def __radd__(self, x):
        return self.__add__(x)

    def __sub__(self, x):
        return self.__class__(Frac(self) - Frac(x))

    def __rsub__(self, x):
        return self.__sub__(x)

    def __mul__(self, x):
        return self.__class__(Frac(self) * x) 

    def __rmul__(self, x):
        return self.__mul__(x)
