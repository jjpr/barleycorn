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

class bU(Compound):
  def __init__(self, first, second):
    Compound.__init__(self, boolUnion(), [first, second])
    
class bI(Compound):
  def __init__(self, first, second):
    Compound.__init__(self, boolIntersection(), [first, second])
    
class bS(Compound):
  def __init__(self, first, second):
    Compound.__init__(self, boolSubtraction(), [first, second])
    
