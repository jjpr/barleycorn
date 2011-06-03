class Toolkit(object):
  def __init__(self, name=None, supportedPrimitives=[], supportedOperations=[]):
    self.name = name
    self.supportedPrimitives = supportedPrimitives
    self.supportedOperations = supportedOperations
    
  def makeItSo(self, component):
    pass
    
class ForToolkit(object):
  def __init__(self, component, toolkit):
    self.toolkit = toolkit
    self.component = component
    
class Component(object):
  def __init__(self, name, type, location, rotation):
    self.name = name
    self.type = type
    self.location = location
    self.rotation = rotation
    self.forToolkits = {}

class simpleRotation(object):
  def __init__(self, axisX, axisY, axisZ, angle, locX=0, locY=0, locZ=0):
    self.axisX = axisX
    self.axisY = axisY
    self.axisZ = axisZ
    self.angle = angle
    self.locX = locX
    self.locY = locY
    self.locZ = locZ
  
