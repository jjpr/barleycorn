__author__ = 'jjpr'

import sys

from barleycorn.examples.scratch import *


_tk = None
_top = sys.modules["__main__"]
if "FreeCAD" in dir(_top) and _top.FreeCAD.ConfigGet("ExeName")=="FreeCAD":
  print "importing barleycorn.toolkits.toolkitFreeCAD"
  import barleycorn.toolkits.toolkitFreeCAD
  _tk = barleycorn.toolkits.toolkitFreeCAD.getToolkitFreeCAD()

def expt(func, export=False):
  '''
  expt() is a method which simplifies experimenting in FreeCAD's Python console.
  try this:
  <open a new document>
  import sys
  sys.path.append(<path to barleycorn>)
  sys.path.append(<path to cgkit light>)
  import scratch_freecad as sc
  sc.expt(sc.xRS01)

  @param func: a function which takes a reference to the toolkit and returns a list of barleycorn.Component
  @param export:  whether to export an STL file
  '''
  stuff = func(_tk)

  _tk.clean()
  _tk.show(stuff)
  _tk.look()
  if export:
    # _tk.exportSTL(stuff, _out_prefix)
    raise NotImplementedError()
  return stuff

