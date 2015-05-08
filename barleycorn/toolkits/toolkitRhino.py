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
    self.guids = []
    
  def resolve(self):
    # see http://peter-hoffmann.com/2010/extrinsic-visitor-pattern-python-inheritance.html
    result = self
    if not self.resolved:
      meth = None
      for cls in self.component.__class__.__mro__:
        meth_name = 'resolve'+cls.__name__
        meth = getattr(self, meth_name, None)
        if meth:
          break
      if not meth:
        raise Exception("can't resolve type: "+str(type(self.component)))
      result = meth()
      self.resolved = True
    print self.component.__class__.__name__
    for g in self.guids:
      print str(g)
    return result
  
  def resolveWrapper(self):
    self.guids += self.component.component.getForToolkit(self.toolkit).resolve().guids
    return self
  
  def resolveTransformation(self):
    matrix = self.makeMatrix(self.component.transformation)
    self.guids += rs.TransformObjects(self.component.component.getForToolkit(self.toolkit).resolve().guids, matrix, True)
    return self

  def resolveSpecial(self):
    self.guids += self.component.geometry()
    return self

  def resolveCone(self):
    self.guids += [rhinoscript.surface.AddCone(rs.WorldXYPlane(), self.component.height, self.component.radius)]
    return self
  
  def resolveCylinder(self):
    self.guids += [rhinoscript.surface.AddCylinder(rs.WorldXYPlane(), self.component.height, self.component.radius)]
    return self
  
  def resolveBox(self):
    (x, y, z) = (self.component.dimX, self.component.dimY, self.component.dimY)
    verts = ((0.0, 0.0, 0.0), (x, 0.0, 0.0), (x, y, 0.0), (0.0, y, 0.0), (0.0, 0.0, z), (x, 0.0, z), (x, y, z), (0.0, y, z))
    self.guids += [rs.AddBox(verts)]
    return self
  
  def resolveTorus(self):
    self.guids += [rs.AddTorus(rs.WorldXYPlane(),self.component.radiusMajor, self.component.radiusMinor)]
    return self
  
  def resolveSphere(self):
    self.guids += [rs.AddSphere(rs.WorldXYPlane(), self.component.radius)]
    return self
            
  def resolveBooleanUnion(self):
    first = self.component.first.getForToolkit(self.toolkit).resolve().guids
    second = self.component.second.getForToolkit(self.toolkit).resolve().guids
    self.guids += rs.BooleanUnion(first + second, delete_input=False)
    return self

  def resolveBooleanIntersection(self):
    first = self.component.first.getForToolkit(self.toolkit).resolve().guids
    second = self.component.second.getForToolkit(self.toolkit).resolve().guids
    self.guids += rs.BooleanIntersection(first, second, delete_input=False)
    return self

  def resolveBooleanSubtraction(self):
    first = self.component.first.getForToolkit(self.toolkit).resolve().guids
    second = self.component.second.getForToolkit(self.toolkit).resolve().guids
    result = rs.BooleanDifference(first, second, delete_input=False)
    if not result:
      raise Exception
    self.guids += result
    print "Subtraction: "
    print "first: " + str(first)
    print "second: " + str(second)
    print "result: " + str(result)
    return self
  
  def makeMatrix(self, transformation):
    """takes a cgkit.cgtypes.mat4, returns a list of lists"""
    (A11, A21, A31, A41, A12, A22, A32, A42, A13, A23, A33, A43, A14, A24, A34, A44) = transformation.toList()
    return [[A11, A12, A13, A14], [A21, A22, A23, A24], [A31, A32, A33, A34], [A41, A42, A43, A44]]

class ToolkitRhino(barleycorn.Toolkit):
  def __init__(self):
    self.App = Rhino.RhinoApp
    barleycorn.Toolkit.__init__(self, "Rhino "+str(rs.ExeVersion())+"."+str(rs.ExeServiceRelease()), ForToolkitRhino)
  
  def show(self, components):
    keeper_guid_strings = [str(item) for component in components for item in component.getForToolkit(self).resolve().guids]
    for keeper_guid_string in keeper_guid_strings:
      print "keeper guid: " + keeper_guid_string
    for rhino_object in scriptcontext.doc.Objects:
      doc_guid_string = str(rhino_object.Id)
      print "doc guid: " + doc_guid_string
      if doc_guid_string not in keeper_guid_strings:
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
      for guid in topftk.guids:
        guid.exportStl(os.path.join(dirPath, name+".stl"))
  
  def clean(self):
    for rhino_object in scriptcontext.doc.Objects:
      rs.DeleteObject(rhino_object)

  def look(self, components=None):
    if components:
      rs.ZoomBoundingBox(rs.BoundingBox())

class SpecialRhino(barleycorn.primitives.Special):
  """a Rhino-specific implementation of primitives.Special"""
  def __init__(self, **kwargs):
    barleycorn.primitives.Special.__init__(self, **kwargs)

  def geometry(self): #this is where the Rhino-specific code goes
    raise NotImplementedError()

