############################################################
# HOMEWORK 1
#
# Team members: Duncan Hall, Jordan Van Duyne
#
# Emails: duncan.hall@students.olin.edu, jordan.vanduyne@students.olin.edu
#
# Remarks:
#




#
# Expressions
#

class Exp (object):
    pass


class EInteger (Exp):
    # Integer literal

    def __init__ (self,i):
        self._integer = i

    def __repr__ (self):
        return "EInteger({})".format(self._integer)

    def eval (self):
        return VInteger(self._integer)


class EBoolean (Exp):
    # Boolean literal

    def __init__ (self,b):
        self._boolean = b

    def __repr__ (self):
        return "EBoolean({})".format(self._boolean)

    def eval (self):
        return VBoolean(self._boolean)

class EVector (Exp):
    """
    >>> EVector([]).eval().length
    0
    >>> EVector([EInteger(10),EInteger(20),EInteger(30)]).eval().length
    3
    >>> EVector([EInteger(10),EInteger(20),EInteger(30)]).eval().get(0).value
    10
    >>> EVector([EInteger(10),EInteger(20),EInteger(30)]).eval().get(1).value
    20
    >>> EVector([EInteger(10),EInteger(20),EInteger(30)]).eval().get(2).value
    30
    >>> EVector([EPlus(EInteger(1),EInteger(2)),EInteger(0)]).eval().length
    2
    >>> EVector([EPlus(EInteger(1),EInteger(2)),EInteger(0)]).eval().get(0).value
    3
    >>> EVector([EPlus(EInteger(1),EInteger(2)),EInteger(0)]).eval().get(1).value
    0
    >>> EVector([EBoolean(True),EAnd(EBoolean(True),EBoolean(False))]).eval().length
    2
    >>> EVector([EBoolean(True),EAnd(EBoolean(True),EBoolean(False))]).eval().get(0).value
    True
    >>> EVector([EBoolean(True),EAnd(EBoolean(True),EBoolean(False))]).eval().get(1).value
    False
    >>> v1 = EVector([EInteger(2),EInteger(3)])
    >>> v2 = EVector([EInteger(33),EInteger(66)])

    >>> ETimes(v1,v2).eval().value
    264
    >>> ETimes(v1,EPlus(v2,v2)).eval().value
    528
    >>> ETimes(v1,EMinus(v2,v2)).eval().value
    0
    """
    # Vector of expressions

    def __init__ (self, es):
        self._es = es

    def __repr__ (self):
        return "EVector({})".format(self._es)

    def eval (self):
        return VVector([e.eval() for e in self._es])


class EPlus (Exp):
    """
    >>> def pair (v): return (v.get(0).value,v.get(1).value)

    >>> v1 = EVector([EInteger(2),EInteger(3)])
    >>> v2 = EVector([EInteger(33),EInteger(66)])

    >>> pair(EPlus(v1,v2).eval())
    (35, 69)
    >>> pair(EMinus(v1,v2).eval())
    (-31, -63)

    >>> b1 = EVector([EBoolean(True),EBoolean(False)])
    >>> b2 = EVector([EBoolean(False),EBoolean(False)])

   """
    # Addition operation

    def __init__ (self,e1,e2):
        self._exp1 = e1
        self._exp2 = e2

    def __repr__ (self):
        return "EPlus({},{})".format(self._exp1,self._exp2)

    def eval (self):
        v1 = self._exp1.eval()
        v2 = self._exp2.eval()
        if v1.type == "integer" and v2.type == "integer":
            return VInteger(v1.value + v2.value)
        if v1.type == "integer" and v2.type == "vector":
            return VVector([VInteger(v1.value + v2.get(n).value) for n in range(v2.length)])
        if v1.type == "vector" and v2.type == "integer":
            return VVector([VInteger(v1.get(n).value + v2.value) for n in range(v1.length)])
        if v1.type == "vector" and v2.type == "vector":
            if v1.length != v2.length:
                raise Exception ("Runtime error: trying to add vectors of different lengths")
            else:
                return VVector([VInteger(v1.get(n).value + v2.get(n).value) for n in range(v1.length)])

        if v1.type == "rational" and v2.type == "integer":
            return VRational(
                    v1.numer + v2.value * v1.denom,
                    v1.denom
                    )
        if v1.type == "integer" and v2.type == "rational":
            return VRational(
                    v2.numer + v1.value * v2.denom,
                    v2.denom
                    )
        if v1.type == "rational" and v2.type == "rational":
            return VRational(
                    v1.numer * v2.denom + v2.numer * v1.denom,
                    v1.denom * v2.denom
                    )
        raise Exception ("Runtime error: trying to add non-numbers")


class EMinus (Exp):
    # Subtraction operation

    def __init__ (self,e1,e2):
        self._exp1 = e1
        self._exp2 = e2

    def __repr__ (self):
        return "EMinus({},{})".format(self._exp1,self._exp2)

    def eval (self):
        v1 = self._exp1.eval()
        v2 = self._exp2.eval()
        if v1.type == "integer" and v2.type == "integer":
            return VInteger(v1.value - v2.value)
        if v1.type == "integer" and v2.type == "vector":
            return VVector([VInteger(v1.value - v2.get(i).value) for n in range(v2.length)])
        if v1.type == "vector" and v2.type == "integer":
            return VVector([VInteger(v1.get(i).value - v2.value) for n in range(v1.length)])
        if v1.type == "vector" and v2.type == "vector":
            if v1.length != v2.length:
                raise Exception ("Runtime error: trying to subtract vectors of different lengths")
            else:
                return VVector([VInteger(v1.get(n).value - v2.get(n).value) for n in range(v1.length)])

        if v1.type == "rational" and v2.type == "integer":
            return VRational(
                    v1.numer - v2.value * v1.denom,
                    v1.denom
                    )
        if v1.type == "integer" and v2.type == "rational":
            return VRational(
                    v1.value * v2.denom - v2.numer,
                    v2.denom
                    )
        if v1.type == "rational" and v2.type == "rational":
            return VRational(
                    v1.numer * v2.denom - v2.numer * v1.denom,
                    v1.denom * v2.denom
                    )
        raise Exception ("Runtime error: trying to subtract non-numbers")


class ETimes (Exp):
    """
    >>> v1 = EVector([EInteger(2),EInteger(3)])
    >>> v2 = EVector([EInteger(33),EInteger(66)])

    >>> ETimes(v1,v2).eval().value
    264
    >>> ETimes(v1,EPlus(v2,v2)).eval().value
    528
    >>> ETimes(v1,EMinus(v2,v2)).eval().value
    0
    """
    # Multiplication operation

    def __init__ (self,e1,e2):
        self._exp1 = e1
        self._exp2 = e2

    def __repr__ (self):
        return "ETimes({},{})".format(self._exp1,self._exp2)

    def eval (self):
        v1 = self._exp1.eval()
        v2 = self._exp2.eval()
        if v1.type == "integer" and v2.type == "integer":
            return VInteger(v1.value * v2.value)
        if v1.type == "integer" and v2.type == "vector":
            return VVector([VInteger(v1.value * v2.get(i).value) for i in range(v2.length)])
        if v1.type == "vector" and v2.type == "integer":
            return VVector([VInteger(v1.get(i).value * v2.value) for i in range(v1.length)])
        if v1.type == "vector" and v2.type == "vector":
            if v1.length != v2.length:
                raise Exception ("Runtime error: multiplying vectors of differing dimensions")
            return VInteger(sum([v1.get(i).value * v2.get(i).value for i in range(v1.length)]))
        if v1.type == "integer" and v2.type == "rational":
            return VRational(v1.value * v2.numer, v2.denom)
        if v1.type == "rational" and v2.type == "integer":
            return VRational(v1.numer * v2.value, v1.denom)
        if v1.type == "rational" and v2.type == "rational":
            return VRational(v1.numer * v2.numer, v1.denom * v2.denom)
        raise Exception ("Runtime error: trying to multiply non-numbers")

class EDiv (Exp):
    # Division operation

    def __init__ (self, e1, e2):
        self._exp1 = e1
        self._exp2 = e2

    def __repr__ (self):
        return "EDiv({},{})".format(self._exp1,self._exp2)

    def eval (self):
        v1 = self._exp1.eval()
        v2 = self._exp2.eval()

        if v1.type == "integer" and v2.type == "integer":
            return VRational(v1.value, v2.value)
        if v1.type == "rational" and v2.type == "integer":
            return ETimes(self._exp1, EDiv(EInteger(1), EInteger(v2.value))).eval()
        if (v1.type == "integer" or v1.type == "rational") and v2.type == "rational":
            return ETimes(self._exp1, EDiv(EInteger(v2.denom), EInteger(v2.numer))).eval()
        raise Exception ("Runtime error: trying to divide non-numbers")

class EIf (Exp):
    # Conditional expression

    def __init__ (self,e1,e2,e3):
        self._cond = e1
        self._then = e2
        self._else = e3

    def __repr__ (self):
        return "EIf({},{},{})".format(self._cond,self._then,self._else)

    def eval (self):
        v = self._cond.eval()
        if v.type != "boolean":
            raise Exception ("Runtime error: condition not a Boolean")
        if v.value:
            return self._then.eval()
        else:
            return self._else.eval()

class EIsZero(Exp):
    """
    >>> EIsZero(EInteger(0)).eval().value
    True
    >>> EIsZero(EInteger(1)).eval().value
    False
    >>> EIsZero(EInteger(9)).eval().value
    False
    >>> EIsZero(EInteger(-1)).eval().value
    False
    >>> EIsZero(EPlus(EInteger(1),EInteger(1))).eval().value
    False
    >>> EIsZero(EMinus(EInteger(1),EInteger(1))).eval().value
    True
    """
    def __init__ (self, e):
        self._e = e

    def __repr__ (self):
        return "EIsZero({})".format(self._e)

    def eval (self):
        v = self._e.eval()
        if v.type != "integer":
            raise Exception ("Runtime error: expression not an integer")
        if v.value == 0:
            return VBoolean(True)
        else:
            return VBoolean(False)

class EAnd(Exp):
    """
    >>> tt = EBoolean(True)
    >>> ff = EBoolean(False)

    >>> EAnd(tt,tt).eval().value
    True
    >>> EAnd(tt,ff).eval().value
    False
    >>> EAnd(ff,tt).eval().value
    False
    >>> EAnd(ff,ff).eval().value
    False
    >>> EAnd(EOr(tt,ff),EOr(ff,tt)).eval().value
    True
    >>> EAnd(EOr(tt,ff),EOr(ff,ff)).eval().value
    False
    >>> EAnd(tt,ENot(tt)).eval().value
    False
    >>> EAnd(tt,ENot(ENot(tt))).eval().value
    True
    """
    def __init__ (self, e1, e2):
        self._e1 = e1
        self._e2 = e2

    def __repr__ (self):
        return "EAnd({},{})".format(self._e1, self._e2)

    def eval (self):
        v1 = self._e1.eval()
        v2 = self._e2.eval()

        if v1.type == "boolean" and v2.type == "boolean":
            if not v1.value:
                return VBoolean(False)
            else:
                return VBoolean(v2.value)
        if v1.type == "vector" and v2.type == "boolean":
            return VVector([EAnd(v1.get(i), v2) for i in range(v1.length)])
        if v1.type == "boolean" and v2.type == "vector":
            return VVector([EAnd(v1, v2.get(i)) for i in range(v2.length)])
        if v1.type == "vector" and v2.type == "vector":
            if v1.length != v2.length:
                raise Exception ("Runtime error: trying to AND two vectors of different lengths")
            return VVector([EAnd(v1.get(n), v2.get(n)).eval for n in range(v1.length)])

               
        raise Exception ("Runtime error: conditions are not both Boolean")

class EOr (Exp):
    """
    >>> tt = EBoolean(True)
    >>> ff = EBoolean(False)
    >>> EOr(tt,tt).eval().value
    True
    >>> EOr(tt,ff).eval().value
    True
    >>> EOr(ff,tt).eval().value
    True
    >>> EOr(ff,ff).eval().value
    False
    """
    # Or expression

    def __init__ (self, e1, e2):
        self._e1 = e1
        self._e2 = e2

    def __repr__(self):
        return "EOr({}, {})".format(self._e1, self._e1)

    def eval (self):
        v1 = self._e1.eval()
        v2 = self._e2.eval()

        if v1.type == "boolean" and v2.type == "boolean":
            if v1.value:
                return VBoolean(True)
            else:
                return VBoolean(v2.value)
        if v1.type == "vector" and v2.type == "boolean":
            return VVector([EOr(v1.get(i), v2) for i in range(v1.length)])
        if v1.type == "boolean" and v2.type == "vector":
            return VVector([EOr(v1, v2.get(i)) for i in range(v2.length)])
        if v1.type == "vector" and v2.type == "vector":
            if v1.length != v2.length:
                raise Exception ("Runtime error: trying to AND two vectors of different lengths")
            return VVector([EOr(v1.get(n), v2.get(n)).eval for n in range(v1.length)])


        raise Exception ("Runtime error: OR argument not a Boolean")

class ENot (Exp):
    """
    >>> tt = EBoolean(True)
    >>> ff = EBoolean(False)
    >>> ENot(tt).eval().value
    False
    >>> ENot(ff).eval().value
    True
    """
    # Not expression

    def __init__ (self, e):
        self._e = e

    def __repr__ (self):
        return "ENot({})".format(self._e)

    def eval (self):
        v = self._e.eval()

        if v.type == "boolean":
            return VBoolean(not v.value)
        if v.type == "vector":
            return VVector([ENot(EBoolean(v.get(i))).eval() for i in range(v.length)])

        raise Exception ("Runtime error: NOT argument is non Boolean")

#
# Values
#

class Value (object):
    pass


class VInteger (Value):
    # Value representation of integers
    def __init__ (self,i):
        self.value = i
        self.type = "integer"

class VBoolean (Value):
    # Value representation of Booleans
    def __init__ (self,b):
        self.value = b
        self.type = "boolean"

class VVector (Value):
    """
    >>> VVector([]).length
    0
    >>> VVector([VInteger(10),VInteger(20),VInteger(30)]).length
    3
    >>> VVector([VInteger(10),VInteger(20),VInteger(30)]).get(0).value
    10
    >>> VVector([VInteger(10),VInteger(20),VInteger(30)]).get(1).value
    20
    >>> VVector([VInteger(10),VInteger(20),VInteger(30)]).get(2).value
    30
    """
    # Value representation of vectors
    def __init__ (self, v):
        self._v = v
        self.length = len(v)
        self.type = "vector"

    def get (self, n):
        if n >= self.length:
            raise Exception ("Runtime error: there is no {} element of the vector".format(str(n)))
        else:
            return self._v[n]

class VRational (Value):
    """
    >>> VRational(1,3).numer
    1
    >>> VRational(1,3).denom
    3
    >>> VRational(2,3).numer
    2
    >>> VRational(2,3).denom
    3

    >>> def rat (v): return "{}/{}".format(v.numer,v.denom)

    >>> rat(EDiv(EInteger(1),EInteger(2)).eval())
    '1/2'
    >>> rat(EDiv(EInteger(2),EInteger(3)).eval())
    '2/3'
    >>> rat(EDiv(EDiv(EInteger(2),EInteger(3)),EInteger(4)).eval())
    '1/6'
    >>> rat(EDiv(EInteger(2),EDiv(EInteger(3),EInteger(4))).eval())
    '8/3'

    >>> def rat (v): return "{}/{}".format(v.numer,v.denom)

    >>> half = EDiv(EInteger(1),EInteger(2))
    >>> third = EDiv(EInteger(1),EInteger(3))

    >>> rat(EPlus(half,third).eval())
    '5/6'
    >>> rat(EPlus(half,EInteger(1)).eval())
    '3/2'
    >>> rat(EMinus(half,third).eval())
    '1/6'
    >>> rat(EMinus(half,EInteger(1)).eval())
    '-1/2'
    >>> rat(ETimes(half,third).eval())
    '1/6'
    >>> rat(ETimes(half,EInteger(1)).eval())
    '1/2'
    """
    # Value representation of rational numbers
    def __init__ (self, n, d):
        self.numer = n
        self.denom = d
        self.type = "rational"

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    # doctest.run_docstring_examples(VRational, globals(), verbose=True)

