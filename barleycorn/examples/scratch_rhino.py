__author__ = 'jjpr'

import sys
import datetime
import json
sys.path.append('/Users/jjpr/Development/workspace-pycharm-community-3.4.1/barleycorn')
sys.path.append('/Users/jjpr/Downloads/sourceforge/cgkit/light')

from scratch import *
import barleycorn.util
import barleycorn.examples.designs_rhino as designs_rhino
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

def xTree(tk):
  tree = designs_rhino.Tree()
  print tree
  return [tree]

def xTreeIter(tk):
  params = {
    "fraction": [0.6, 0.5],
    "angle": [180, 120],
    "bend": [30, 45, 60]
  }
  return barleycorn.util.iterate_and_stack(params, designs_rhino.Tree, 200)

def xTreeSummary():
  params = {
    "fraction": [0.6, 0.5],
    "for_reals": [False]
  }
  f = open("tree_test_" + datetime.datetime.now().isoformat() + ".json", mode='w')
  results = barleycorn.util.iterate_and_stack(params, designs_rhino.Tree, 200)
  summary = []
  for result in results:
    result.getForToolkit(_tk).resolve()
    tree_params = {key: getattr(result, key, "blank") for key in params.keys()}
    summary.append({"params": tree_params, "tree": result.summary})
  dump = json.dumps(summary, indent=2)
  f.write(dump)
  f.close()

if __name__=="__main__":
  print __file__

  # expt(xRS01)
  # expt(xRAll01)
  # expt(xTree)
  expt(xTreeIter)
  # xTreeSummary()
  
  
  