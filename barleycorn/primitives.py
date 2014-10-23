import barleycorn
    
class Primitive(barleycorn.Component):
  def __init__(self, **kwargs):
    barleycorn.Component.__init__(self, **kwargs)
    
class Special(Primitive):
  """a superclass for any shape that can be described in a particular toolkit 
  but which is not supported by barleycorn.primitives"""
  def __init__(self, **kwargs):
    Primitive.__init__(self, **kwargs)
    
class Cone(Primitive):
  """a circular cone around the positive z axis with its apex at the origin"""
  def __init__(self, radius, height, **kwargs):
    Primitive.__init__(self, **kwargs)
    self.radius = radius
    self.height = height

class Torus(Primitive):
  """a torus centered at the origin with the z axis as its major axis"""
  def __init__(self, radiusMajor, radiusMinor, **kwargs):
    Primitive.__init__(self, **kwargs)
    self.radiusMajor = radiusMajor
    self.radiusMinor = radiusMinor

class Box(Primitive):
  """a rectangular solid with one corner at the origin extended along the positive x y and z axes"""
  def __init__(self, dimX, dimY, dimZ, **kwargs):
    Primitive.__init__(self, **kwargs)
    self.dimX = dimX
    self.dimY = dimY
    self.dimZ = dimZ
  
class Cylinder(Primitive):
  """a cylinder with its axis beginning at the origin and extending along the positive z axis"""
  def __init__(self, radius, height, **kwargs):
    Primitive.__init__(self, **kwargs)
    self.radius = radius
    self.height = height

class Wedge(Primitive):
  """an arc of a cylinder with its axis beginning at the origin and extending along the positive z axis
  and its angle beginning at the positive x axis and rotating toward the positive y axis; angle is in degrees"""
  def __init__(self, radius, height, angle, **kwargs):
    Primitive.__init__(self, **kwargs)
    self.radius = radius
    self.height = height
    self.angle = angle

class Sphere(Primitive):
  """a sphere with its center at the origin"""
  def __init__(self, radius, **kwargs):
    Primitive.__init__(self, **kwargs)
    self.radius = radius


