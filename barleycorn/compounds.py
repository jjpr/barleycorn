import barleycorn

class Compound(barleycorn.Component):
  def __init__(self, name=None, type=None):
    barleycorn.Component.__init__(self, name, type)
  
class Boolean(Compound):
  def __init__(self, first, second, name=None, type=None):
    Compound.__init__(self, name, type)
    self.first = first
    self.second = second

class BooleanUnion(Boolean):
  def __init__(self, first, second, name=None, type=None):
    Boolean.__init__(self, first, second, name, type)

class BooleanIntersection(Boolean):
  def __init__(self, first, second, name=None, type=None):
    Boolean.__init__(self, first, second, name, type)

class BooleanSubtraction(Boolean):
  def __init__(self, first, second, name=None, type=None):
    Boolean.__init__(self, first, second, name, type)

