__author__ = 'jjpr'

import sys
import datetime
import json
sys.path.append('/Users/jjpr/Development/workspace-pycharm-community-3.4.1/barleycorn')
sys.path.append('/Users/jjpr/Downloads/sourceforge/cgkit/light')

from scratch import *
import barleycorn.util
import barleycorn.examples.designs as designs
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

  # _tk.clean()
  _tk.show(stuff)
  _tk.look()
  if export:
    raise NotImplementedError()
    # _tk.exportSTL(stuff, _out_prefix)
  return stuff

def summarize_tree(tree, param_list):
    tree.getForToolkit(_tk).resolve()
    tree_params = {key: getattr(tree, key, "blank") for key in param_list}
    return {"params": tree_params, "tree": tree.summary}

def dated_file(prefix, extension):
    return open(prefix + "_" + datetime.datetime.now().isoformat() + "." + extension, mode='w')

def dump_json(jsonable, prefix):
    dump = json.dumps(jsonable, indent=2)
    f = dated_file(prefix, "json")
    f.write(dump)
    f.close()

tree_iter_params_test = {"for_reals": [False]}

tree_iter_params_single = {}

tree_iter_params_01 = {
    "radius_fraction": [0.7, 0.6, 0.5],
    "base_radius": [2.0],
    "terminal_radius": [0.5, 0.75],
    "density": [4, 5]
}

tree_iter_params_02 = {
    "base_height": [15.0, 10.0, 7.5],
    "height_fraction": [0.5, 0.75, 0.9],
    "bend": [30, 45, 60]
}

tree_iter_params_03 = {
    "base_height": [10.0],
    "height_fraction": [0.5],
    "bend": [45],
    "density": [4, 3, 2]
}

tree_iter_params_04 = {
    "base_height": [10.0],
    "height_fraction": [0.5],
    "bend": [45],
    "density": [4]
}

def curry_params(func, params):
    def curried(tk):
        return func(params, tk)
    return curried

def xTreeIter(params, tk):
  trees = barleycorn.util.iterate_and_stack(params, designs_rhino.Tree, 100)
  dump_json([summarize_tree(tree, params.keys()) for tree in trees], "tree_summary")
  return trees

def xTreeIterTest(params, tk):
  params_test = dict(params, **tree_iter_params_test)
  trees = xTreeIter(params_test, tk)
  return trees

def xRT01(tk):
  return [xRAll01(tk)[-1]]

def xRAll01(tk):
  stand = designs.RockerStand01()
  middle = designs.RockerMiddle01(stand.clearance_radius_inner, stand.rim_radius_major, stand.wall_thickness)
  center = designs_rhino.RockerTree01(middle)
  return [stand, middle, center]


if __name__=="__main__":
  print __file__

  # expt(curry_params(xTreeIterTest, tree_iter_params_single))
  # expt(curry_params(xTreeIter, tree_iter_params_single))
  # expt(curry_params(xTreeIterTest, tree_iter_params_01))
  # expt(curry_params(xTreeIter, tree_iter_params_01))
  # expt(curry_params(xTreeIterTest, tree_iter_params_02))
  # expt(curry_params(xTreeIter, tree_iter_params_02))
  # expt(curry_params(xTreeIter, tree_iter_params_03))
  # expt(curry_params(xTreeIter, tree_iter_params_04))
  # expt(xRT01)
  expt(xRAll01)
  
  