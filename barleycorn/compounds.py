from barleycorn import Component

class Compound(Component):
  def __init__(self, operator, operands, name=None, type=None, location=None, rotation=None):
    Component.__init__(self, name, type, location, rotation)
    self.operator = operator
    self.operands = operands

class Operator(object):
  pass
  
class boolUnion(Operator):
  pass

class boolIntersection(Operator):
  pass

class boolSubtraction(Operator):
  pass

