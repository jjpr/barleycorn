# this is a skeleton, based on the FreeCAD class.  I'm working my way through it,
#  adapting it to the Rhino API
import datetime
import os
import barleycorn
import barleycorn.primitives
import barleycorn.compounds
import rhinoscript
import Rhino
import rhinoscriptsyntax as rs
import scriptcontext

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
    self.guid = None
    
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
    return self
  
  def resolveWrapper(self):
    self.guid = self.component.component.getForToolkit(self.toolkit).resolve().guid
    return self
  
  def resolveTransformation(self):
    matrix = self.makeMatrix(self.component.transformation)
    self.guid = rs.TransformObject(self.component.component.getForToolkit(self.toolkit).resolve().guid, matrix, True)
    return self

  def resolveCone(self):
    self.brep = rhinoscript.surface.AddCone(rs.WorldXYPlane(), self.component.height, self.component.radius)
    return self
  
  def resolveCylinder(self):
    self.brep = rhinoscript.surface.AddCylinder(rs.WorldXYPlane(), self.component.height, self.component.radius)
    return self
  
  def resolveBox(self):
    (x, y, z) = (self.component.dimX, self.component.dimY, self.component.dimY)
    verts = ((0.0, 0.0, 0.0), (x, 0.0, 0.0), (x, y, 0.0), (0.0, y, 0.0), (0.0, 0.0, z), (x, 0.0, z), (x, y, z), (0.0, y, z))
    self.guid = rs.AddBox(verts)
    return self
  
  def resolveTorus(self):
    self.guid = rs.AddTorus(rs.WorldXYPlane(),self.component.radiusMajor, self.component.radiusMinor)
    return self
  
  def resolveSphere(self):
    self.guid = rs.AddSphere(rs.WorldXYPlane(), self.component.radius)
    return self
            
  def resolveBooleanUnion(self):
    first = self.component.first.getForToolkit(self.toolkit).resolve().guid
    second = self.component.second.getForToolkit(self.toolkit).resolve().guid
    [self.guid] = rs.BooleanUnion([first, second], delete_input=False)
    return self

  def resolveBooleanIntersection(self):
    first = self.component.first.getForToolkit(self.toolkit).resolve().guid
    second = self.component.second.getForToolkit(self.toolkit).resolve().guid
    [self.guid] = rs.BooleanIntersection([first], [second], delete_input=False)
    return self

  def resolveBooleanSubtraction(self):
    first = self.component.first.getForToolkit(self.toolkit).resolve().guid
    second = self.component.second.getForToolkit(self.toolkit).resolve().guid
    [self.guid] = rs.BooleanDifference([first], [second], delete_input=False)
    return self
  
  def makeMatrix(self, transformation):
    # """takes a cgkit.cgtypes.mat4, returns a list of lists"""
    # return transformation.toList(rowmajor=True)
    #Does a pyrr Matrix44 just appear to be a list of lists?
    return transformation

class ToolkitRhino(barleycorn.Toolkit):
  def __init__(self):
    self.App = Rhino.RhinoApp
    barleycorn.Toolkit.__init__(self, "Rhino "+str(rs.ExeVersion())+"."+str(rs.ExeServiceRelease()), ForToolkitRhino)
  
  def show(self, components):
    keeper_guids = [component.getForToolkit(self).resolve().guid for component in components]
    for rhino_object in scriptcontext.doc.Objects:
      if not any(rhino_object.Equals(guid) for guid in keeper_guids):
        rs.DeleteObject(rhino_object)
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
    for rhino_object in scriptcontext.doc.Objects:
      rs.DeleteObject(rhino_object)

  def look(self, components=None):
    if components:
      rs.ZoomBoundingBox(rs.BoundingBox())

class SpecialRhino(barleycorn.primitives.Special):
  """a Rhino-specific implementation of primitives.Special"""
  def __init__(self, toolkit, **kwargs):
    barleycorn.primitives.Special.__init__(self, **kwargs)
    ftk = self.getForToolkit(toolkit)
    ftk.guid = self.geometry()
    ftk.resolved = True
  
  def geometry(self): #this is where the FreCAD-specific code goes
    raise NotImplementedError()

