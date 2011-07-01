import cgkit.cgtypes

class Toolkit(object):
  """a Toolkit represents a particular application or library for 3D modeling, CAD, etc."""
  def __init__(self, name, forToolkitClass, supportedPrimitives=[], supportedOperations=[]):
    self.name = name
    self.forToolkitClass = forToolkitClass
    self.supportedPrimitives = supportedPrimitives
    self.supportedOperations = supportedOperations
    
class ForToolkit(object):
  """a ForToolkit object allows a Toolkit to store information and code 
  specific to the relationship between itself and a Component"""
  def __init__(self, component, toolkit):
    self.toolkit = toolkit
    self.component = component
    
class Component(object):
  """a Component represents any information manipulated by a 3D modeling or CAD program.  
  a Component's forToolkits attribute is a dictionary mapping any Toolkit that operates
  on the Component to a ForToolkit object which holds information and code specific to the 
  relationship between the Toolkit and the Component"""
  def __init__(self, name, type):
    self.name = name
    self.type = type
    self.forToolkits = {}
    
  def getForToolkit(self, toolkit):
    if not toolkit in self.forToolkits:
      self.forToolkits[toolkit] = toolkit.forToolkitClass(self, toolkit)
    return self.forToolkits[toolkit]
  
  def transform(self, transformation, name=None, type=None):
    return Transformation(self, transformation, name, type)

  def rotateX(self, angle, name=None, type=None):
    """angle is in radians"""
    trans = cgkit.cgtypes.mat4.rotation(angle, cgkit.cgtypes.vec3(1,0,0))
    return self.transform(trans, name, type)

  def rotateY(self, angle, name=None, type=None):
    """angle is in radians"""
    trans = cgkit.cgtypes.mat4.rotation(angle, cgkit.cgtypes.vec3(0,1,0))
    return self.transform(trans, name, type)

  def rotateZ(self, angle, name=None, type=None):
    """angle is in radians"""
    trans = cgkit.cgtypes.mat4.rotation(angle, cgkit.cgtypes.vec3(0,0,1))
    return self.transform(trans, name, type)

  def translateX(self, distance, name=None, type=None):
    """angle is in radians"""
    trans = cgkit.cgtypes.mat4.translation(cgkit.cgtypes.vec3(distance,0,0))
    return self.transform(trans, name, type)

  def translateY(self, distance, name=None, type=None):
    """angle is in radians"""
    trans = cgkit.cgtypes.mat4.translation(cgkit.cgtypes.vec3(0,distance,0))
    return self.transform(trans, name, type)

  def translateZ(self, distance, name=None, type=None):
    """angle is in radians"""
    trans = cgkit.cgtypes.mat4.translation(cgkit.cgtypes.vec3(0,0,distance))
    return self.transform(trans, name, type)
  
  def bU(self, second, name=None, type=None):
    return barleycorn.compounds.BooleanUnion(self, second, name, type)

  def bI(self, second, name=None, type=None):
    return barleycorn.compounds.BooleanIntersection(self, second, name, type)

  def bS(self, second, name=None, type=None):
    return barleycorn.compounds.BooleanSubtraction(self, second, name, type)

class Transformation(Component):
  def __init__(self, component, transformation, name=None, type=None):
    Component.__init__(self, name, type)
    self.component = component
    self.transformation = transformation
  
  def __getattr__(self, attrname):
    result = getattr(self.component, attrname)
    if isinstance(result, cgkit.cgtypes.vec3):
      return result*self.transformation
    return result

class Wrapper(Component):
  def __init__(self, component, name=None, type=None):
    Component.__init__(self, name, type)
    self.component = component

  def __getattr__(self, attrname):
    return getattr(self.component, attrname)

class simpleRotation(object):
  """angle is in degrees for now"""
  def __init__(self, axisX, axisY, axisZ, angle, locX=0.0, locY=0.0, locZ=0.0):
    self.axisX = axisX
    self.axisY = axisY
    self.axisZ = axisZ
    self.angle = angle
    self.locX = locX
    self.locY = locY
    self.locZ = locZ
  
import barleycorn.compounds

