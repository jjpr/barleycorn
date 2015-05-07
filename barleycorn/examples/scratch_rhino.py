__author__ = 'jjpr'

import sys
sys.path.append('/Users/jjpr/Development/workspace-pycharm-community-3.4.1/barleycorn')
sys.path.append('/Users/jjpr/Downloads/sourceforge/cgkit/light')

from scratch import *
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

if __name__=="__main__":
  print __file__

  # expt(xRS01)
  expt(xRAll01)


