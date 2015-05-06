__author__ = 'jjpr'

import sys
from scratch import *

sys.path.append('/Users/jjpr/Downloads/sourceforge/cgkit/light')

import barleycorn.toolkits.toolkitRhino

_tk = barleycorn.toolkits.toolkitRhino.getToolkitRhino()

def expt(func, export=False):
  '''
  scratch.expt is a method which simplifies experimenting with Rhino Python.

  @param func: a function that takes a toolkit and returns a list of Barleycorn Components
  @param export: whether to export STL files
  '''
  stuff = func(_tk)

  _tk.clean()
  _tk.show(stuff)
  _tk.look()
  if export:
    raise NotImplementedError()
    # _tk.exportSTL(stuff, _out_prefix)
  return stuff

expt(xRS01)
