from fractions import Fraction as Frac 

class TimeLength(Frac):
    """
    "Abstract" class, representing a length of musical time. 
    
    Primary purpose is modifying Fraction's arithmetic to:
     - return the proper type (not fractions)
     - carry a nominal value around (a false timelength used for notation)
    """



    # reimplement arithmetic to return NoteLengths

    def __add__(self, x):
        #try:
        #    nominal_value = self.nominal_value + x.nominal_value
        #except (TypeError, AttributeError):
        #    nominal_value = None
        return self.__class__(Frac(self) + Frac(x))#, nominal_value=nominal_value)
        

    def __radd__(self, x):
        return self.__add__(x)

    def __sub__(self, x):
        #try:
        #    nominal_value = self.nominal_value - x.nominal_value
        #except (TypeError, AttributeError):
        #    nominal_value = None
        return self.__class__(Frac(self) - Frac(x))#, nominal_value=nominal_value)

    def __rsub__(self, x):
        return self.__sub__(x)

    def __mul__(self, x):
        # if isinstance(self.nominal_value, type(self)):
        #    nominal_value = self.nominal_value * x
        # else:
        #    nominal_value = None
        return self.__class__(Frac(self) * x) #, nominal_value=nominal_value)

    def __rmul__(self, x):
        return self.__mul__(x)
