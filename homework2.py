############################################################
# HOMEWORK 2
#
# Team members: Duncan Hall, Griffin
#
# Emails:
#   duncan.hall@students.olin.edu
#   griffin.tschurwald@students.olin.edu
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

    def __str__ (self):
        return "EInteger({})".format(self._integer)

    def eval (self,prim_dict,fun_dict):
        return VInteger(self._integer)

    def substitute (self,id,new_e):
        return self


class EBoolean (Exp):
    # Boolean literal

    def __init__ (self,b):
        self._boolean = b

    def __str__ (self):
        return "EBoolean({})".format(self._boolean)

    def eval (self,prim_dict,fun_dict):
        return VBoolean(self._boolean)

    def substitute (self,id,new_e):
        return self

class ECall (Exp):
    """

    >>> ECall("+1", [EInteger(100)]).eval(INITIAL_PRIM_DICT,FUN_DICT).value
    101
    >>> ECall("+1", [EPrimCall("+",[EInteger(100),EInteger(200)])]).eval(INITIAL_PRIM_DICT,FUN_DICT).value
    301
    >>> ECall("+1", [ECall("+1", [EInteger(100)])]).eval(INITIAL_PRIM_DICT,FUN_DICT).value
    102
    >>> ECall("=",[EInteger(1),EInteger(2)]).eval(INITIAL_PRIM_DICT,FUN_DICT).value
    False
    >>> ECall("=",[EInteger(1),EInteger(1)]).eval(INITIAL_PRIM_DICT,FUN_DICT).value
    True
    >>> ECall("sum_from_to",[EInteger(0),EInteger(10)]).eval(INITIAL_PRIM_DICT,FUN_DICT).value
    55
    """

    def __init__(self, name, es):
        self._name = name
        self._exps = es

    def __str__ (self):
        return "ECall({},[{}])".format(self._name,",".join([ str(e) for e in self._exps]))

    def eval (self,prim_dict, fun_dict):
        vs = [ e.eval(prim_dict,fun_dict) for e in self._exps ]
        if self._name in prim_dict:
            return apply(prim_dict[self._name],vs)
        elif self._name in fun_dict:
            # 
            return ELet(
                [
                    (fun_dict[self._name]["params"][i], self._exps[i])
                    for i in range(len(self._exps))
                ],
                fun_dict[self._name]["body"]).eval(prim_dict, fun_dict)

            apply(fun_dict[self._name],vs)
        else:
            raise Exception("function {} not defined".format(self._name))

    def substitute (self,id,new_e):
        new_es = [ e.substitute(id,new_e) for e in self._exps]
        return ECall(self._name,new_es)


class EPrimCall (Exp):

    def __init__ (self,name,es):
        self._name = name
        self._exps = es

    def __str__ (self):
        return "EPrimCall({},[{}])".format(self._name,",".join([ str(e) for e in self._exps]))

    def eval (self,prim_dict,fun_dict):
        vs = [ e.eval(prim_dict,fun_dict) for e in self._exps ]
        if self._name in prim_dict:
            return apply(prim_dict[self._name],vs)
        elif self._name in fun_dict:
            return apply(fun_dict[self._name],vs)
        else:
            raise Exception("function {} not defined".format(self._name))

    def substitute (self,id,new_e):
        new_es = [ e.substitute(id,new_e) for e in self._exps]
        return EPrimCall(self._name,new_es)


class EIf (Exp):
    # Conditional expression

    def __init__ (self,e1,e2,e3):
        self._cond = e1
        self._then = e2
        self._else = e3

    def __str__ (self):
        return "EIf({},{},{})".format(self._cond,self._then,self._else)

    def eval (self,prim_dict,fun_dict):
        v = self._cond.eval(prim_dict,fun_dict)
        if v.type != "boolean":
            raise Exception ("Runtime error: condition not a Boolean")
        if v.value:
            return self._then.eval(prim_dict,fun_dict)
        else:
            return self._else.eval(prim_dict,fun_dict)

    def substitute (self,id,new_e):
        return EIf(self._cond.substitute(id,new_e),
                   self._then.substitute(id,new_e),
                   self._else.substitute(id,new_e))


class ELet (Exp):
    # local binding
    """
    >>> ELet([("a",EInteger(99))],EId("a")).eval(INITIAL_PRIM_DICT).value
    99
    >>> ELet([("a",EInteger(99)),("b",EInteger(66))],EId("a")).eval(INITIAL_PRIM_DICT).value
    99
    >>> ELet([("a",EInteger(99)),("b",EInteger(66))],EId("b")).eval(INITIAL_PRIM_DICT).value
    66
    >>> ELet([("a",EInteger(99))],ELet([("a",EInteger(66)),("b",EId("a"))],EId("a"))).eval(INITIAL_PRIM_DICT).value
    66
    >>> ELet([("a",EInteger(99))],ELet([("a",EInteger(66)),("b",EId("a"))],EId("b"))).eval(INITIAL_PRIM_DICT).value
    99
    >>> ELet([("a",EInteger(5)),("b",EInteger(20))],ELet([("a",EId("b")),("b",EId("a"))],EPrimCall("-",[EId("a"),EId("b")]))).eval(INITIAL_PRIM_DICT).value
    15
    """

    def __init__ (self, subs, e):
        self._e = e # e2
        self._ids = [sub[0] for sub in subs]
        self._exps = [sub[1] for sub in subs] # e1

    def __str__ (self):
        return "ELet({},{},{})".format(self._id.__str__(),self._e1.__str__(),self._e2.__str__())

    def eval (self,prim_dict,fun_dict):
        for i, id in enumerate(self._ids):
            self._e = self._e.substitute(id,self._exps[i])
        return self._e.eval(prim_dict,fun_dict)

    def substitute (self,id,new_e):
        if id in self._ids:  
            return ELet(
                    [(self._ids[i], self._exps[i].substitute(id, new_e))
                        for i in range(len(self._ids))
                    ],
                    self._e
                   )
            # return ELet(self._id,
                        # self._e1.substitute(id,new_e),
                        # self._e2)

        return ELet(
                [(self._ids[i], self._exps[i].substitute(id, new_e))
                    for i in range(len(self._ids))
                ],
                self._e.substitute(id, new_e)
               )
            
        # return ELet(self._id,
                    # self._e1.substitute(id,new_e),
                    # self._e2.substitute(id,new_e))

class ELetS(Exp):
    """
    >>> ELetS([("a",EInteger(99))],EId("a")).eval(INITIAL_PRIM_DICT).value
    99
    >>> ELetS([("a",EInteger(99)),("b",EInteger(66))],EId("a")).eval(INITIAL_PRIM_DICT).value
    99
    >>> ELetS([("a",EInteger(99)),("b",EInteger(66))],EId("b")).eval(INITIAL_PRIM_DICT).value
    66
    >>> ELet([("a",EInteger(99))],ELetS([("a",EInteger(66)),("b",EId("a"))],EId("a"))).eval(INITIAL_PRIM_DICT).value
    66
    >>> ELet([("a",EInteger(99))],ELetS([("a",EInteger(66)),("b",EId("a"))],EId("b"))).eval(INITIAL_PRIM_DICT).value
    66
    >>> ELetS([("a",EInteger(5)),("b",EInteger(20))],ELetS([("a",EId("b")),("b",EId("a"))],EPrimCall("-",[EId("a"),EId("b")]))).eval(INITIAL_PRIM_DICT).value
    0
"""

    def __init__ (self, subs, e):
        self._ids = [subs[0][0]]
        self._exps = [subs[0][1]]

        if len(subs) > 1:
            self._e = ELetS(subs[1:], e)
        else:
            self._e = e # e2

    def __str__ (self):
        return "ELet({},{},{})".format(self._id.__str__(),self._e1.__str__(),self._e2.__str__())

    def eval (self,prim_dict,fun_dict):
        for i, id in enumerate(self._ids):
            self._e = self._e.substitute(id,self._exps[i])
        return self._e.eval(prim_dict,fun_dict)

    def substitute (self,id,new_e):
        if id in self._ids:
            return ELetS(
                    [(self._ids[i], self._exps[i].substitute(id, new_e))
                        for i in range(len(self._ids))
                    ],
                    self._e
                   )

        return ELetS(
                [(self._ids[i], self._exps[i].substitute(id, new_e))
                    for i in range(len(self._ids))
                ],
                self._e.substitute(id, new_e)
               )


class ELetV (Exp):
    """
    >>> ELetV("a",EInteger(10),EId("a")).eval(INITIAL_PRIM_DICT).value
    10
    >>> ELetV("a",EInteger(10),ELetV("b",EInteger(20),EId("a"))).eval(INITIAL_PRIM_DICT).value
    10
    >>> ELetV("a",EInteger(10), ELetV("a",EInteger(20),EId("a"))).eval(INITIAL_PRIM_DICT).value
    20
    >>> ELetV("a",EPrimCall("+",[EInteger(10),EInteger(20)]),ELetV("b",EInteger(20),EId("a"))).eval(INITIAL_PRIM_DICT).value
    30
    >>> ELetV("a",EPrimCall("+",[EInteger(10),EInteger(20)]),ELetV("b",EInteger(20),EPrimCall("*",[EId("a"),EId("a")]))).eval(INITIAL_PRIM_DICT).value
    900
    """
    def __init__ (self, id, e1, e2):
        self._e = e2 # e2
        # lazy
        self._ids = [id] # [sub[0] for sub in subs]
        self._exps = [e1] #[sub[1] for sub in subs] # e1

    def __str__ (self):
        return "ELet({},{},{})".format(self._id.__str__(),self._e1.__str__(),self._e2.__str__())

    def eval (self,prim_dict,fun_dict):
        for i, id in enumerate(self._ids):
            self._e = self._e.substitute(id, EInteger(self._exps[i].eval(prim_dict).value))
        return self._e.eval(prim_dict,fun_dict)

    def substitute (self,id,new_e):
        if id in self._ids:  
            return ELet(
                    [(self._ids[i], self._exps[i].substitute(id, new_e))
                        for i in range(len(self._ids))
                    ],
                    self._e
                   )
            # return ELet(self._id,
                        # self._e1.substitute(id,new_e),
                        # self._e2)

        return ELet(
                [(self._ids[i], self._exps[i].substitute(id, new_e))
                    for i in range(len(self._ids))
                ],
                self._e.substitute(id, new_e)
               )


class EId (Exp):
    # identifier

    def __init__ (self,id):
        self._id = id

    def __str__ (self):
        return "EId({})".format(self._id)

    def eval (self,prim_dict,fun_dict):
        raise Exception("Runtime error: unknown identifier {}".format(self._id))

    def substitute (self,id,new_e):
        if id == self._id:
            return new_e
        return self


    
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





# Primitive operations

def oper_plus (v1,v2): 
    if v1.type == "integer" and v2.type == "integer":
        return VInteger(v1.value + v2.value)
    raise Exception ("Runtime error: trying to add non-numbers")

def oper_minus (v1,v2):
    if v1.type == "integer" and v2.type == "integer":
        return VInteger(v1.value - v2.value)
    raise Exception ("Runtime error: trying to add non-numbers")

def oper_times (v1,v2):
    if v1.type == "integer" and v2.type == "integer":
        return VInteger(v1.value * v2.value)
    raise Exception ("Runtime error: trying to add non-numbers")
def oper_zero (v1):
    if v1.type == "integer":
        return VBoolean(v1.value==0)
    raise Exception ("Runtime error: type error in zero?")

# Initial primitives dictionary

INITIAL_PRIM_DICT = {
    "+": oper_plus,
    "*": oper_times,
    "-": oper_minus,
    "zero?": oper_zero
}

FUN_DICT = {
      "square": {"params":["x"],
                 "body":EPrimCall("*",[EId("x"),EId("x")])},
      "=": {"params":["x","y"],
            "body":EPrimCall("zero?",[EPrimCall("-",[EId("x"),EId("y")])])},
      "+1": {"params":["x"],
             "body":EPrimCall("+",[EId("x"),EInteger(1)])},
      "sum_from_to": {"params":["s","e"],
                      "body":EIf(ECall("=",[EId("s"),EId("e")]),
                                 EId("s"),
                                 EPrimCall("+",[EId("s"),
                                                ECall("sum_from_to",[ECall("+1",[EId("s")]),
                                                                     EId("e")])]))}
     }


# for testing file
if __name__ == "__main__":
    import doctest
    doctest.run_docstring_examples(ECall, globals(), verbose=True)
