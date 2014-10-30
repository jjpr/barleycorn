# import cgkit.cgtypes
import pyrr
import datetime
# other imports at end to avoid circularity problems

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
  def __init__(self, **kwargs):
    self.name = kwargs.get("name", self.__class__.__name__+"_"+str(datetime.datetime.now().microsecond))
    self.forToolkits = {}
    
  def getForToolkit(self, toolkit):
    if not toolkit in self.forToolkits:
      self.forToolkits[toolkit] = toolkit.forToolkitClass(self, toolkit)
    return self.forToolkits[toolkit]
  
  def transform(self, transformation, **kwargs):
    return Transformation(self, transformation, **kwargs)

  def rotateX(self, angle, **kwargs):
    """angle is in radians"""
    # trans = cgkit.cgtypes.mat4.rotation(angle, cgkit.cgtypes.vec3(1,0,0))
    trans = pyrr.Matrix44.from_x_rotation(angle)
    return self.transform(trans, **kwargs)

  def rotateY(self, angle, **kwargs):
    """angle is in radians"""
    # trans = cgkit.cgtypes.mat4.rotation(angle, cgkit.cgtypes.vec3(0,1,0))
    trans = pyrr.Matrix44.from_y_rotation(angle)
    return self.transform(trans, **kwargs)

  def rotateZ(self, angle, **kwargs):
    """angle is in radians"""
    # trans = cgkit.cgtypes.mat4.rotation(angle, cgkit.cgtypes.vec3(0,0,1))
    trans = pyrr.Matrix44.from_z_rotation(angle)
    return self.transform(trans, **kwargs)

  def translateX(self, distance, **kwargs):
    """angle is in radians"""
    # trans = cgkit.cgtypes.mat4.translation(cgkit.cgtypes.vec3(distance,0,0))
    trans = pyrr.Matrix44.from_translation(pyrr.Vector3([distance, 0.0, 0.0]))
    return self.transform(trans, **kwargs)

  def translateY(self, distance, **kwargs):
    """angle is in radians"""
    # trans = cgkit.cgtypes.mat4.translation(cgkit.cgtypes.vec3(0,distance,0))
    trans = pyrr.Matrix44.from_translation(pyrr.Vector3([0.0, distance, 0.0]))
    return self.transform(trans, **kwargs)

  def translateZ(self, distance, **kwargs):
    """angle is in radians"""
    # trans = cgkit.cgtypes.mat4.translation(cgkit.cgtypes.vec3(0,0,distance))
    trans = pyrr.Matrix44.from_translation(pyrr.Vector3([0.0, 0.0, distance]))
    return self.transform(trans, **kwargs)
  
  def bU(self, second, **kwargs):
    return barleycorn.compounds.BooleanUnion(self, second, **kwargs)

  def bI(self, second, **kwargs):
    return barleycorn.compounds.BooleanIntersection(self, second, **kwargs)

  def bS(self, second, **kwargs):
    return barleycorn.compounds.BooleanSubtraction(self, second, **kwargs)

class Transformation(Component):
  def __init__(self, component, transformation, **kwargs):
    Component.__init__(self, **kwargs)
    self.component = component
    self.transformation = transformation
  
  def __getattr__(self, attrname):
    result = getattr(self.component, attrname)
    if isinstance(result, pyrr.Vector3):
      return result*self.transformation
    return result

class Wrapper(Component):
  def __init__(self, component, **kwargs):
    Component.__init__(self, **kwargs)
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
import barleycorn.primitives
import barleycorn.toolkits

