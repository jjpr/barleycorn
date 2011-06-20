import barleycorn
from barleycorn import primitives
from barleycorn import compounds
from FreeCAD import Part
from FreeCAD import Base
import datetime
import os

class ForToolkitFreeCAD(barleycorn.ForToolkit):
  def __init__(self, component, toolkit):
    barleycorn.ForToolkit.__init__(self, component, toolkit)
    self.resolved = False
    self.partrep = None
    
  def resolve(self):
    if not self.resolved:
      if isinstance(self.component, primitives.Primitive):
        self.resolvePrimitive()
      elif isinstance(self.component, compounds.Compound):
        self.resolveCompound()
      else:
        raise Exception("can't resolve type: "+str(type(self.component)))
      if self.component.rotation != None:
        if isinstance(self.component.rotation, barleycorn.simpleRotation):
          self.partrep.rotate(
          Base.Vector(self.component.rotation.locX,self.component.rotation.locY,self.component.rotation.locZ),
          Base.Vector(self.component.rotation.axisX,self.component.rotation.axisY,self.component.rotation.axisZ),
          self.component.rotation.angle)
        else:
          raise Exception("can't handle rotation")
      if self.component.location != None:
        if isinstance(self.component.location, tuple) and len(self.component.location)==3:
          self.partrep.translate(Base.Vector(self.component.location[0],self.component.location[1],
          self.component.location[2]))
        else:
          raise Exception("can't handle location")
      self.resolved = True
    return self
  
  def resolvePrimitive(self):
    if isinstance(self.component, primitives.Cone):
      self.partrep = Part.makeCone(0, self.component.radius, self.component.height)
    elif isinstance(self.component, primitives.Cylinder):
      self.partrep = Part.makeCylinder(self.component.radius, self.component.height)
    elif isinstance(self.component, primitives.Box):
      self.partrep = Part.makeBox(self.component.dimX, self.component.dimY, self.component.dimZ)
    elif isinstance(self.component, primitives.Torus):
      self.partrep = Part.makeTorus(self.component.radiusMajor, self.component.radiusMinor)
    elif isinstance(self.component, primitives.Wedge):
      self.partrep = Part.makeCylinder(self.component.radius, self.component.height, 
      Base.Vector(0,0,0), Base.Vector(0,0,1), self.component.angle)
    elif isinstance(self.component, primitives.Sphere):
      self.partrep = Part.makeSphere(self.component.radius)
    else:
      raise Exception("unrecognized primitive: "+str(type(self.component)))
    return self
      
  def resolveCompound(self):
    for op in self.component.operands:
      if not self.toolkit in op.forToolkits:
        op.forToolkits[self.toolkit] = ForToolkitFreeCAD(op, self.toolkit)
    first = self.component.operands[0].forToolkits[self.toolkit].resolve()
    second = self.component.operands[1].forToolkits[self.toolkit].resolve()
    if isinstance(self.component.operator, compounds.boolUnion):
      self.partrep = first.partrep.fuse(second.partrep)
    elif isinstance(self.component.operator, compounds.boolIntersection):
      self.partrep = first.partrep.common(second.partrep)
    elif isinstance(self.component.operator, compounds.boolSubtraction):
      self.partrep = first.partrep.cut(second.partrep)
    else:
      raise Exception("unrecognized operator")
    return self

class ToolkitFreeCAD(barleycorn.Toolkit):
  def __init__(self):
    barleycorn.Toolkit.__init__(self, "FreeCAD 0.11")
  
  def makeItSo(self, components):
    for component in components:
      if not self in component.forToolkits:
        component.forToolkits[self] = ForToolkitFreeCAD(component, self)
      topftk = component.forToolkits[self].resolve()
      Part.show(topftk.partrep)
    return components
    
  def exportSTL(self, components, prefix):
    dirName = datetime.datetime.now().isoformat()
    dirPath = os.path.join(prefix, dirName)
    os.mkdir(dirPath)
    for i, component in enumerate(components):
      if not self in component.forToolkits:
        component.forToolkits[self] = ForToolkitFreeCAD(component, self)
      topftk = component.forToolkits[self].resolve()
      name = component.name
      if name == None:
        name = "component_"+str(i+1)
      topftk.partrep.exportStl(os.path.join(dirPath, name+".stl"))
    
