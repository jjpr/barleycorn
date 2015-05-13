__author__ = 'jjpr'

from math import pi, acos, cos, sin, atan, degrees, sqrt, e, ceil

def make_param_product(params, param_product=None, my_dict=None):
  if param_product is None:
    param_product = []
  if my_dict is None:
    my_dict = {}
  if params:
    new_params = params.copy()
    param, vals = new_params.popitem()
    for val in vals:
      new_dict = my_dict.copy()
      new_dict[param] = val
      make_param_product(new_params, param_product, new_dict)
  else:
      param_product.append(my_dict)
  return param_product

def stack_coords(n, i, offset=1):
  root = n**(1./3.)
  base = int(ceil(root))
  x = i%base
  y = (i//base)%base
  z = ((i//base)//base)%base
  return (x*offset, y*offset, z*offset)

def iterate_and_stack(params, component_class, spacing):
  param_product = make_param_product(params)
  results = []
  for i, permutation in enumerate(param_product):
    print permutation
    coords = stack_coords(len(param_product), i, spacing)
    print coords
    single = component_class(**permutation).translate(coords)
    results.append(single)
  return results

def cartesian(rho, theta, phi):
  x = rho * sin(theta) * cos(phi)
  y = rho * sin(theta) * sin(phi)
  z = rho * cos(theta)
  return (x,y,z)

sum_of_squares = lambda vec: sum(x**2 for x in vec)

vec_len = lambda vec : sqrt(sum_of_squares(vec))

def spherical(x, y, z):
  rho = vec_len((x, y, z))
  theta = acos(z/vec_len((x, y, z)))
  phi = atan(y/x)
  return (rho, theta, phi)




