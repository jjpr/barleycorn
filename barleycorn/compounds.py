import barleycorn

class Compound(barleycorn.Component):
  def __init__(self, **kwargs):
    barleycorn.Component.__init__(self, **kwargs)
  
class Boolean(Compound):
  def __init__(self, first, second, **kwargs):
    Compound.__init__(self, **kwargs)
    self.first = first
    self.second = second

class BooleanUnion(Boolean):
  def __init__(self, first, second, **kwargs):
    Boolean.__init__(self, first, second, **kwargs)

class BooleanIntersection(Boolean):
  def __init__(self, first, second, **kwargs):
    Boolean.__init__(self, first, second, **kwargs)

class BooleanSubtraction(Boolean):
  def __init__(self, first, second, **kwargs):
    Boolean.__init__(self, first, second, **kwargs)

