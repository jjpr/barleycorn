__author__ = 'jjpr'

from barleycorn.toolkits.toolkitRhino import SpecialRhino
import barleycorn
import barleycorn.util
import barleycorn.examples.designs as designs
import rhinoscriptsyntax as rs
import random
from math import log, floor

class Tree(SpecialRhino):
  def __init__(self, base_radius=1.0, terminal_radius=0.5, base_height=12.0, density=5, radius_fraction=0.79,
               height_fraction=0.75, minimum_wall_thickness=0.7, angle=180, bend=47, for_reals=True, **kwargs):
    self.base_radius = base_radius
    self.terminal_radius = terminal_radius
    self.base_height = base_height
    self.density = density
    self.radius_fraction = radius_fraction
    self.height_fraction = height_fraction
    self.minimum_wall_thickness = minimum_wall_thickness
    self.angle = angle
    self.leaf = None
    self.bend = bend
    self.for_reals = for_reals
    SpecialRhino.__init__(self, **kwargs)

  def geometry(self):
    result, summary = self.tree_gen(self.base_radius, self.base_height)
    self.summary = summary
    return result or [self.get_leaf()]

  def tree_gen(self, radius, height):
    result = []
    summary = []
    if radius < self.terminal_radius:
      if self.for_reals:
        result.append(self.get_leaf())
      summary.append("leaf")
    else:
      if self.for_reals:
        result.append(self.twig_gen(radius, radius, height))
      summary.append("twig " + str(radius) + " " + str(height))
      subs = []
      sub_radius = radius * self.radius_fraction
      sub_height = height * self.height_fraction
      sub_angle_y = self.bend
      for i in range(self.density):
        sub_angle_z = (i + (0.5 * random.random())) * (360 / self.density)
        sub, sub_summary = self.tree_gen(sub_radius, sub_height)
        if self.for_reals:
          sub = rs.RotateObjects(sub, (0,0,0), sub_angle_y, (0,1,0))
          sub = rs.RotateObjects(sub, (0,0,0), sub_angle_z, (0,0,1))
          sub = rs.MoveObjects(sub, (0,0,height))
        subs += sub
        summary.append(sub_summary)
      center, center_summary = self.tree_gen(sub_radius, sub_height)
      if self.for_reals:
        center = rs.MoveObjects(center, (0,0,height))
      result += subs + center
      summary.append(center_summary)
    return result, summary

  def get_leaf(self):
    if not self.leaf:
      self.leaf = self.leaf_gen(self.terminal_radius, self.minimum_wall_thickness)
    return rs.CopyObject(self.leaf)

  def leaf_gen(self, radius, thickness):
    edge_pts = [
      (0.0, radius, 0.0),
      (0.0, radius, 2.0 * radius),
      (- radius * 1.5, radius * 2.0, radius * 5.0),
      (- radius * 1.5, radius * 2.0, radius * 8.0),
      (0.0, radius / 2.0, radius * 12.0),
      (radius, 0.0, radius * 13.0)
    ]
    profile_pts_top = [[pt, ((0.5 * thickness) + pt[0], 0.0, pt[2]), (pt[0], -pt[1], pt[2])] for pt in edge_pts[:-1]]
    profile_pts_bottom = [[(pt[0], -pt[1], pt[2]), ((-0.5 * thickness) + pt[0], 0.0, pt[2]), pt] for pt in edge_pts[:-1]]

    crvs_top = [rs.AddCurve(pts) for pts in profile_pts_top]
    crvs_bottom = [rs.AddCurve(pts) for pts in profile_pts_bottom]

    profile_crvs = [rs.JoinCurves(crvs) for crvs in zip(crvs_top, crvs_bottom)]

    srf = rs.AddLoftSrf(profile_crvs, end=edge_pts[-1])

    cap = rs.AddPlanarSrf([profile_crvs[0]])

    result = rs.JoinSurfaces([srf, cap])

    return result

  def twig_gen(self, base_radius, top_radius, height):
    return rs.AddCylinder(rs.WorldXYPlane(), height, base_radius)

  def branchings(self):
    return floor(log(self.terminal_radius / self.base_radius, self.radius_fraction)) + 1

  def enumerate_branchings(self, params):
    return [dict(perm, branchings=self.branchings(**perm)) for perm in barleycorn.util.make_param_product(params)]

class RockerTree01(barleycorn.Wrapper):
  def __init__(self, middle, **kwargs):
    self.middle = middle
    barleycorn.Wrapper.__init__(self, self.makeMe(), **kwargs)

  def makeMe(self):
    base = designs.RockerCenter01(self.middle.clearance_radius_inner, self.middle.rim_radius_major, self.middle.wall_thickness)
    tree = Tree().translateZ(-base.wall_thickness)
    return barleycorn.compounds.Collection([base, tree])




