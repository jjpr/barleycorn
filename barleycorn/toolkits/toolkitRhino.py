# this is a skeleton, based on the FreeCAD class.  I'm working my way through it, 
# adapting it to the Rhino API
import datetime
import os
import barleycorn
import barleycorn.primitives
import barleycorn.compounds
import rhinoscript
import Rhino
import rhinoscriptsyntax as rs

_toolkitRhino = None

def getToolkitRhino():
  global _toolkitRhino
  if _toolkitRhino is None:
    _toolkitRhino = ToolkitRhino()
  return _toolkitRhino

class ForToolkitRhino(barleycorn.ForToolkit):
  def __init__(self, component, toolkit):
    barleycorn.ForToolkit.__init__(self, component, toolkit)
    self.resolved = False
    self.brep = None
    
  def resolve(self):
    # see http://peter-hoffmann.com/2010/extrinsic-visitor-pattern-python-inheritance.html
    if not self.resolved:
      meth = None
      for cls in self.component.__class__.__mro__:
        meth_name = 'resolve'+cls.__name__
        meth = getattr(self, meth_name, None)
        if meth:
          break
      if not meth:
        raise Exception("can't resolve type: "+str(type(self.component)))
      return meth()
  
  def resolveWrapper(self):
    self.brep = self.component.component.getForToolkit(self.toolkit).resolve().brep
  
  def resolveTransformation(self):
    self.brep = self.component.component.getForToolkit(self.toolkit).resolve().brep.Duplicate()
    self.brep.Transform(self.makeMatrix(self.component.transformation))
  
  def resolveCone(self):
    self.brep = rhinoscript.surface.AddCone(rhinoscript.plane.WorldXYPlane(), self.component.height, self.component.radius)
    return self
  
  def resolveCylinder(self):
    self.brep = rhinoscript.surface.AddCylinder(rhinoscript.plane.WorldXYPlane(), self.component.height, self.component.radius)
    return self
  
  def resolveBox(self):
    (x, y, z) = (self.component.dimX, self.component.dimY, self.component.dimY)
    verts = ((0.0, 0.0, 0.0), (x, 0.0, 0.0), (x, y, 0.0), (0.0, y, 0.0), (0.0, 0.0, z), (x, 0.0, z), (x, y, z), (0.0, y, z))
    self.brep = rhinoscript.surface.AddBox(verts)
    return self
  
  def resolveTorus(self):
    self.brep = rhinoscript.surface.AddTorus(self.component.radiusMajor, self.component.radiusMinor)
    return self
  
  def resolveSphere(self):
    self.brep = rhinoscript.surface.AddSphere(self.component.radius)
    return self
            
  def resolveBooleanUnion(self):
    first = self.component.first.getForToolkit(self.toolkit).resolve().brep
    second = self.component.second.getForToolkit(self.toolkit).resolve().brep
    [self.brep] = rs.BooleanUnion([first, second], delete_input=False)
    return self

  def resolveBooleanIntersection(self):
    first = self.component.first.getForToolkit(self.toolkit).resolve().brep
    second = self.component.second.getForToolkit(self.toolkit).resolve().brep
    [self.brep] = rs.BooleanIntersection([first], [second], delete_input=False)
    return self

  def resolveBooleanSubtraction(self):
    first = self.component.first.getForToolkit(self.toolkit).resolve().brep
    second = self.component.second.getForToolkit(self.toolkit).resolve().brep
    [self.brep] = rs.BooleanDifference([first], [second], delete_input=False)
    return self
  
  def makeMatrix(self, transformation):
    """takes a cgkit.cgtypes.mat4, returns Rhino.Geometry.Transform"""
    m = Rhino.Geometry.Transform(1.0)
    (m.M00, m.M01, m.M02, m.M03, m.M10, m.M11, m.M12, m.M13, m.M20, m.M21, m.M22, m.M23, m.M30, m.M31, m.M32, m.M33) = transformation.toList(rowmajor=True)
    return m

class ToolkitRhino(barleycorn.Toolkit):
  def __init__(self):
    self.App = Rhino.RhinoApp
    barleycorn.Toolkit.__init__(self, "Rhino "+str(self.App.ExeVersion)+"."+str(self.App.ExeServiceRelease), ForToolkitRhino)
  
  def show(self, components):
    for component in components:
      topftk = component.getForToolkit(self).resolve()
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
      topftk.brep.exportStl(os.path.join(dirPath, name+".stl"))
  
  def clean(self):
    for ob in self.App.ActiveDocument.Objects:
      self.App.ActiveDocument.removeObject(ob.Name)
      
  def look(self):
    self.App.Gui.SendMsgToActiveView("ViewFit")
    self.App.Gui.activeDocument().activeView().viewAxometric()
    
class SpecialRhino(barleycorn.primitives.Special):
  """a Rhino-specific implementation of primitives.Special"""
  def __init__(self, toolkit, **kwargs):
    barleycorn.primitives.Special.__init__(self, **kwargs)
    ftk = self.getForToolkit(toolkit)
    ftk.brep = self.geometry()
    ftk.resolved = True
  
  def geometry(self): #this is where the FreCAD-specific code goes
    raise NotImplementedError()

