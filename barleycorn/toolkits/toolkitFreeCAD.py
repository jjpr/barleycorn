import barleycorn
import barleycorn.primitives
import barleycorn.compounds
import FreeCAD
from FreeCAD import Part
from FreeCAD import Base
import datetime
import os

_toolkitFreeCAD = None

def getToolkitFreeCAD():
  global _toolkitFreeCAD
  if _toolkitFreeCAD is None:
    _toolkitFreeCAD = ToolkitFreeCAD()
  return _toolkitFreeCAD

class ForToolkitFreeCAD(barleycorn.ForToolkit):
  def __init__(self, component, toolkit):
    barleycorn.ForToolkit.__init__(self, component, toolkit)
    self.resolved = False
    self.partrep = None
    
  def resolve(self):
    if not self.resolved:
      if isinstance(self.component, barleycorn.Transformation):
        self.resolveTransformation()
      elif isinstance(self.component, barleycorn.primitives.Primitive):
        self.resolvePrimitive()
      elif isinstance(self.component, barleycorn.compounds.Compound):
        self.resolveCompound()
      else:
        raise Exception("can't resolve type: "+str(type(self.component)))
      self.resolved = True
    return self
  
  def resolvePrimitive(self):
    if isinstance(self.component, barleycorn.primitives.Cone):
      self.partrep = Part.makeCone(0, self.component.radius, self.component.height)
    elif isinstance(self.component, barleycorn.primitives.Cylinder):
      self.partrep = Part.makeCylinder(self.component.radius, self.component.height)
    elif isinstance(self.component, barleycorn.primitives.Box):
      self.partrep = Part.makeBox(self.component.dimX, self.component.dimY, self.component.dimZ)
    elif isinstance(self.component, barleycorn.primitives.Torus):
      self.partrep = Part.makeTorus(self.component.radiusMajor, self.component.radiusMinor)
    elif isinstance(self.component, barleycorn.primitives.Wedge):
      self.partrep = Part.makeCylinder(self.component.radius, self.component.height, 
      Base.Vector(0,0,0), Base.Vector(0,0,1), self.component.angle)
    elif isinstance(self.component, barleycorn.primitives.Sphere):
      self.partrep = Part.makeSphere(self.component.radius)
    else:
      raise Exception("unrecognized primitive: "+str(type(self.component)))
    return self
      
  def resolveCompound(self):
    if isinstance(self.component, barleycorn.compounds.Boolean):
      first = self.component.first.getForToolkit(self.toolkit).resolve().partrep
      second = self.component.second.getForToolkit(self.toolkit).resolve().partrep
      if isinstance(self.component, barleycorn.compounds.BooleanUnion):
        self.partrep = first.fuse(second)
      elif isinstance(self.component, barleycorn.compounds.BooleanIntersection):
        self.partrep = first.common(second)
      elif isinstance(self.component, barleycorn.compounds.BooleanSubtraction):
        self.partrep = first.cut(second)
      else:
        raise Exception("unrecognized Boolean operator")
    else:
      raise Exception("unrecognized operator")
    return self
  
  def resolveTransformation(self):
    partrep = self.component.component.getForToolkit(self.toolkit).resolve().partrep
    self.partrep = partrep.transformGeometry(self.makeMatrix(self.component.transformation))#ASSUMES that transformshape makes a new copy or that freecad allows reuse of shape
  
  def makeMatrix(self, transformation):
    """takes a cgkit.cgtypes.mat4, returns FreeCAD.Matrix"""
    m = Base.Matrix()
    (m.A11, m.A21, m.A31, m.A41, m.A12, m.A22, m.A32, m.A42, m.A13, m.A23, m.A33, m.A43, m.A14, m.A24, m.A34, m.A44) = transformation.toList()
    return m

class ToolkitFreeCAD(barleycorn.Toolkit):
  def __init__(self):
    self.App = FreeCAD
    barleycorn.Toolkit.__init__(self, self.App.ConfigGet("ExeName")+" "+self.App.ConfigGet("ExeVersion"), ForToolkitFreeCAD)
  
  def show(self, components):
    for component in components:
      topftk = component.getForToolkit(self).resolve()
      Part.show(topftk.partrep)
    return components
    
  def exportSTL(self, components, prefix):
    dirName = datetime.datetime.now().isoformat()
    dirPath = os.path.join(prefix, dirName)
    os.mkdir(dirPath)
    for i, component in enumerate(components):
      topftk = component.getForToolkit(self).resolve()
      name = component.name
      if name == None:
        name = "component_"+str(i+1)
      topftk.partrep.exportStl(os.path.join(dirPath, name+".stl"))
  
  def clean(self):
    for ob in self.App.ActiveDocument.Objects:
      self.App.ActiveDocument.removeObject(ob.Name)
      
  def look(self):
    self.App.Gui.SendMsgToActiveView("ViewFit")
    self.App.Gui.activeDocument().activeView().viewAxometric()
    
class SpecialFreeCAD(barleycorn.primitives.Special):
  """a FreeCAD-specific implementation of primitives.Special"""
  def __init__(self, toolkit, name=None, type=None):
    barleycorn.primitives.Special.__init__(self, name, type)
    ftk = self.getForToolkit(toolkit)
    ftk.partrep = self.geometry()
    ftk.resolved = True
  
  def geometry(self):
    raise NotImplementedError()

