# this is a skeleton, based on the FreeCAD class.  I'm working my way through it, 
# adapting it to the Blender API

# Parts of this may need to be fixed after the Blender 2.61 Matrix changes

import datetime
import os
from math import pi
import barleycorn
import barleycorn.primitives
import barleycorn.compounds
import bpy
import mathutils

_toolkitBlender = None

def getToolkitBlender():
  global _toolkitBlender
  if _toolkitBlender is None:
    _toolkitBlender = ToolkitBlender()
  return _toolkitBlender

class ForToolkitBlender(barleycorn.ForToolkit):
  def __init__(self, component, toolkit):
    barleycorn.ForToolkit.__init__(self, component, toolkit)
    self.resolved = False
    self.obrep = None
    
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
    self.obrep = self.component.component.getForToolkit(self.toolkit).resolve().obrep
    self.resolved = True
    return self
  
  def resolveTransformation(self):
    #TODO 
    old_obrep = self.component.component.getForToolkit(self.toolkit).resolve().obrep
    m = mathutils.Matrix()
    (m[0][0], m[0][1], m[0][2], m[0][3], m[1][0], m[1][1], m[1][2], m[1][3], 
     m[2][0], m[2][1], m[2][2], m[2][3], m[3][0], m[3][1], m[3][2], m[3][3]) = old_obrep.matrix_local
    new_mat = m * self.makeMatrix(self.component.transformation)
    self.obrep = old_obrep.copy()
    self.obrep.matrix_local = new_mat
    self.resolved = True
    return self    
  
  def resolveCone(self):
    result = bpy.ops.mesh.primitive_cone_add(radius=self.component.radius, depth=self.component.height, 
                                             rotation=(pi, 0.0, 0.0), location=(0.0, 0.0, self.component.height/2.0))
    if "FINISHED" in result:
      self.obrep = bpy.context.object
    self.resolved = True
    return self
  
  def resolveCylinder(self):
    result = bpy.ops.mesh.primitive_cylinder_add(radius=self.component.radius, depth=self.component.height, 
                                             location=(0.0, 0.0, self.component.height/2.0))
    if "FINISHED" in result:
      self.obrep = bpy.context.object
    self.resolved = True
    return self
  
  def resolveBox(self):
    (x, y, z) = (self.component.dimX, self.component.dimY, self.component.dimY)
    verts = ((0.0, 0.0, 0.0), (x, 0.0, 0.0), (0.0, y, 0.0), (0.0, 0.0, z), (0.0, y, z), (x, 0.0, z), (x, y, 0.0), (x, y, z))
    faces = ((0, 2, 6, 1), (0, 3, 4, 2), (0, 1, 5, 3), (3, 5, 7, 4), (1, 6, 7, 5), (2, 4, 7, 6))
    me = bpy.data.meshes.new(self.component.name + "_mesh")
    me.from_pydata(verts, [], faces)
    self.obrep = bpy.data.objects.new(self.component.name, me)
    bpy.context.scene.objects.link(self.obrep)
    me.update()
    self.resolved = True
    return self
  
  def resolveTorus(self):
    result = bpy.ops.mesh.primitive_torus_add(major_radius=self.component.radiusMajor, minor_radius=self.component.radiusMinor)
    if "FINISHED" in result:
      self.obrep = bpy.context.object
    self.resolved = True
    return self
  
  def resolveSphere(self):
    result = bpy.ops.mesh.primitive_ico_sphere_add(size=self.component.radius)
    if "FINISHED" in result:
      self.obrep = bpy.context.object
    self.resolved = True
    return self
      
  def resolveBoolean(self):
    ops = {barleycorn.compounds.BooleanUnion: "UNION", barleycorn.compounds.BooleanIntersection: "INTERSECTION", barleycorn.compounds.BooleanSubtraction: "DIFFERENCE"}
    op = ops[self.component.__class__]
    first = self.component.first.getForToolkit(self.toolkit).resolve().obrep.copy()
    second = self.component.second.getForToolkit(self.toolkit).resolve().obrep
    bpy.context.scene.objects.active = first
    result = bpy.ops.object.modifier_add(type='BOOLEAN')
    if "FINISHED" in result:
      self.obrep = first
      first.modifiers[0].object = second
      first.modifiers[0].operation = op
    else: 
      raise Exception("error adding Boolean modifier: "+str(result))
    self.resolved = True
    return self
    
  def makeMatrix(self, transformation):
    """takes a cgkit.cgtypes.mat4, returns Blender mathutils.Matrix"""
    m = mathutils.Matrix()
    (m[0][0], m[0][1], m[0][2], m[0][3], m[1][0], m[1][1], m[1][2], m[1][3], 
     m[2][0], m[2][1], m[2][2], m[2][3], m[3][0], m[3][1], m[3][2], m[3][3]) = transformation.toList(rowmajor=True)
    return m

class ToolkitBlender(barleycorn.Toolkit):
  def __init__(self):
    self.app = bpy.app
    barleycorn.Toolkit.__init__(self, self.app.binary_path, ForToolkitBlender)
  
  def exportSTL(self, components, prefix):
    dirName = datetime.datetime.now().isoformat()
    dirPath = os.path.join(prefix, dirName)
    os.mkdir(dirPath)
    for i, component in enumerate(components):
      topftk = component.getForToolkit(self).resolve()
      name = component.name
      if name == None:
        name = "component_"+str(i+1)
      bpy.context.scene.objects.active = topftk.obrep
      bpy.ops.export_mesh.stl(filepath=dirPath+name+".stl")
  
  def clean(self):
    for ob in self.App.ActiveDocument.Objects:
      self.App.ActiveDocument.removeObject(ob.Name)
      
  def look(self):
    self.App.Gui.SendMsgToActiveView("ViewFit")
    self.App.Gui.activeDocument().activeView().viewAxometric()
    
class SpecialBlender(barleycorn.primitives.Special):
  """a Blender-specific implementation of primitives.Special"""
  def __init__(self, toolkit, **kwargs):
    barleycorn.primitives.Special.__init__(self, **kwargs)
    ftk = self.getForToolkit(toolkit)
    ftk.obrep = self.geometry()
    ftk.resolved = True
  
  def geometry(self): #this is where the FreCAD-specific code goes
    raise NotImplementedError()

