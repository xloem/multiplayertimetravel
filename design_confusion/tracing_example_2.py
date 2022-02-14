import numpy as np
import operator as op
from typing import Any

# this is a somewhat mid-general approach
# i was thinking it might be fun next to label add and mul as expanding and distributing over each other
# then implementation of a flattening interpretation could be simpler
# and avenues might be opened a little toward flattening through other analogous ops

class OpExpr:
    def __init__(self, op, *operands):
        self.op = op
        self.children = operands
    def __getattr__(self, attr):
        # give nonexisting attrs a None value
        return None
    def __getitem__(self, idx):
        return self.children[idx]
    def __add__(left, right):
        return OpExpr(op.add, left, right)
    def __radd__(right, left):
        return self.__add__(left)
    def __instancecheck__(self, cls):
        if issubclass(cls, Interpretation):
            return cls.test(self)
        else:
            return super().__instancecheck__(self, cls)
    def as(self, interpretation):
        return interpretation.form(self)
    #def be(self, interpretation)
    #    form = interpretation.form(self)
    #    self.op = form.op
    #    self.children = form.children
    #    return self

class Interpretation:
    def __new__(cls, obj, *params):
        if len(params) == 0:
            try:
                return cls.form(obj)
            except:
                return None
        else:
            return cls.new(obj, *params)
    def new(*params):
        raise NotImplementedError()
    def form(obj):
        raise NotImplementedError()
    @classmethod
    def test(cls, obj):
        try:
            return cls.form(obj) is not None
        except:
            return False

def _Reordered(*order):
    class Reordered(Interpretation):
        def form(expr):
            return OpExpr(expr.op, [expr[idx] for idx in order])
    Reordered.__name__ += '_' + '_'.join(str(idx) for idx in order)
    return Reordered
Reordered10 = _Reordered(1, 0)

# this class not presently used
def _OpChildTypes(op, *classes):
    class OpChildTypes(Interpretation):
        def new(*objs):
            return OpChildTypes.form(OpExpr(op, *objs))
        def form(expr):
            assert expr.op is op
            for child, cls in zip(expr.children, classes):
                if cls is not Any:
                   assert isinstance(child, cls)
            return expr
    OpChildTypes.__name__ = '_' + '_'.join(cls.__name__ for cls in classes)
    return OpChildTypes

def _Op(op):
    return _OpChildTypes(op)
Add = _Op(op.add)
Mul = _Op(op.mul)

# this adds nearness of expression properties.
# each operator has properties like commutivity
# that together provide for the distributed law
## a quick thing is that multiplication distributeds over and factors with addition
## so a*(b + c) == a*b + a*c
## there could be a rule added specifying this, or a property or label on them

def MulAddExpanded(form

def _CoeffObj(coeff_form, obj_form):
    # mul is important here
    # we can have any number of operands, and each one could be a linear combination, needing foil
    # however: the interpreter always produces pairs
    # we could also use e.g. sympy
    ## given we must do foil anyway
    ## a flattening operation makes sense
    ## which expands mul into a single sum
    CoeffObj = _OpChildTypes(op.mul, coeff_form, obj_form)
    ObjCoeff = _OpChildTypes(op.mul, obj_form, coeff_form)
    class CoeffObjNormative(CoeffObj):
        def form(expr):
            obj = obj_form(expr)
            if obj is not None:
                return CoeffObj(coeff_form(1), obj)
            return CoeffObj(expr) or Reordered10(ObjCoeff(expr))
    return CoeffObjNormative

def _LinearCombination(coeff_form, obj_form):
    CoeffObj = _CoeffObj(coeff_form, obj_form)
    class LinearCombination(Add):
        def form(expr):
            addands = []
            if Add.test(expr):
                for addand in expr.children:
                    addands.extend(LinearCombination(addand))
            else:
                coefflinear = CoeffLinearCombination(expr)
                if coefflinear is not None:

                coeffobj = CoeffObj(expr)
                if coeffobj is None:
                    coeffobj = CoeffLinear
                assert item is not None
                addands.append(item)
            return Add(*addands)
    CoeffLinearCombination = _CoeffObj(coeff_form, LinearCombination)
    return LinearCombination

class Scalar(OpExpr):
    def __init__(self, value):
        super().__init__(None, value)
    def range(self)
        return np.array((self[0], self[0]))

class Distribution(OpExpr):
    pass

class UniformDistribution(Distribution):
    def __init__(self, low, high):
        super().__init__(UniformDistribution, low, high)
    def range(self):
        return np.array(self.children)
    def sample(self, low=(), high=(), shape=None):
        low = np.max(low, self[0])
        high = np.min(high, self[1])
        return np.random.uniform(low, high, size=shape)

class LinearCombination(Interpretation):
    def form(expr):
        if Add.test(expr):
        else:
            item = CoefficientScalar(expr)
            assert item is not None
            addands = item

##### below would be a specialisation of a linear combination or expanded sum

class UniformDistributionLinearCombination:
    def __init__(self, opexpr):
        self.opexpr = opexpr
    def children(self):
        # recursive
        for child in self.opexpr.children:
            if isinstance(child, Scalar):
                child = OpExpr(op.mul, 1, child)
            elif isinstance(child, OpExpr

##### these comments below are likely just cognitive coping

# so now we have an analysis class/function
# that may form if conditions
# the space of generalisation into operator uses seems unreasonably large
# it would roughly involve adding a property to operator classes that would facilitate
# flattening.
# these properties exist, things like commutability

# the end goal is to show a structure where more work could be applied to form a distribution algebra
# given the scale of work handling properties, it makes sense to have the sum class
#there is some merit around new approach, more reusable for the later expansion
#so far.
#basically our working memory shrinks as we cope with further inhibition. the judgement is hard.


### this developed into CoeffObj
class ScaledValue(SumsToUniformDistributionSum):
    def __init__(self, value, scale):
        if not isinstance(value, SumsToUniformDistributionSum):

        self.value = value
        self.scale = scale
    def range(self):
        return self.value.range() * self.scale

class UniformDistributionSum(SumsToUniformDistributionSum):
    def __init__(self, dists...):
        self.children = [
                dist if isinstance(dist,SumsToUniformDistributionSum) else Scalar(dist)
                for dist in dists
        ]
        self.all_children = None
    def range(self):
        low, high = self.children[0].range()
        for child in self.children[1:]:
            sublow, subhigh = child.range()
            low += sublow
            high += subhigh
        return low, high
    def _heuristic_widest(self):
        max = 0
        maxobj = None
        for child in self.children:
            if type(child) is UniformDistribution:

    def heuristic_sample(self):
        # first we have a list of sampleable distributions and values that can fill them

        # we simplify by sampling from all but the one with highest range


class UniformDistributionLinearCombination(SumsToUniformDistributionLinearCombination):
    def __init__(self, scale_dists...):
        self.children = [
                dist if isinstance(dist,SumsToUniformDistributionLinearCombination) else Scalar(dist)
                for scale, dist in dists
        ]
        self.all_children = None
    def range(self):
        low, high = self.children[0].range()
        for child in self.children[1:]:
            sublow, subhigh = child.range()
            low += sublow
            high += subhigh
        return low, high
    def _heuristic_widest(self):
        max = 0
        maxobj = None
        for child in self.children:
            if type(child) is UniformDistribution:

    def heuristic_sample(self):
        # first we have a list of sampleable distributions and values that can fill them

        # we simplify by sampling from all but the one with highest range
