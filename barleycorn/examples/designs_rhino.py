__author__ = 'jjpr'

from barleycorn.toolkits.toolkitRhino import SpecialRhino
import barleycorn
import barleycorn.examples.designs as designs
import rhinoscriptsyntax as rs
import random

class Tree(SpecialRhino):
  def __init__(self, base_radius=4.0, terminal_radius=0.25, height=40.0, density=7, fraction=0.75, angle=180, bend=45,
               **kwargs):
    self.base_radius = base_radius
    self.terminal_radius = terminal_radius
    self.height = height
    self.density = density
    self.fraction = fraction
    self.angle = angle
    self.leaf = None
    self.bend = bend
    SpecialRhino.__init__(self, **kwargs)

  def geometry(self):
    return self.tree_gen(self.base_radius, self.height)

  def tree_gen(self, radius, height):
    if radius < self.terminal_radius:
      return self.get_leaf(radius * self.fraction)
    else:
      trunk = [self.twig_gen(radius, radius, height)]
      sub_angle_y = self.bend
      sub_angle_z = (1.5 * self.angle) - (random.random() * self.angle)
      sub_radius = radius * self.fraction
      sub_height = height * self.fraction
      sub = self.tree_gen(sub_radius, sub_height)
      sub = rs.RotateObjects(sub, (0,0,0), sub_angle_y, (0,1,0))
      sub = rs.RotateObjects(sub, (0,0,0), sub_angle_z, (0,0,1))
      sub = rs.MoveObjects(sub, (0,0,height))
      center = rs.MoveObjects(self.tree_gen(sub_radius, sub_height), (0,0,height))
      # for i in range(self.density):
      #   sub_radius = radius * (self.fraction ** (i+1))
      #   sub_height = height * (self.fraction ** (i+1))
      #   sub_angle_y = self.bend * (self.fraction ** i)
      #   sub_angle_z += (1.5 * self.angle) - (random.random() * self.angle)
      #   sub = self.tree_gen(sub_radius, sub_height)
      #   sub = rs.RotateObjects(sub, (0,0,0), sub_angle_y, (0,1,0))
      #   sub = rs.RotateObjects(sub, (0,0,0), sub_angle_z, (0,0,1))
      #   sub = rs.MoveObjects(sub, (0,0,height - sub_height))
      #   # try:
      #   #   trunk = rs.BooleanUnion(trunk+sub) or trunk
      #   # except Exception as e:
      #   #   print e
      #   trunk = trunk + sub
      trunk = trunk + sub + center
      return trunk

  def get_leaf(self, radius):
    # if not self.leaf:
    #   self.leaf = self.leaf_gen(1.0)
    # return rs.ScaleObject(self.leaf, (0.0, 0.0, 0.0), [radius]*3, True)
    return []

  def leaf_gen(self, radius):
    radius_02 = 0.85 * radius
    edge_pts = [
      (0.0, radius, 0.0),
      (0.0, radius_02, 2.0 * radius),
      (- radius * 1.5, radius * 3.0, radius * 5.0),
      (- radius * 1.5, radius * 3.0, radius * 8.0),
      (0.0, radius / 2.0, radius * 12.0),
      (radius, 0.0, radius * 13.0)
    ]
    profile_pts_top = [[pt, (radius + pt[0], 0.0, pt[2]), (pt[0], -pt[1], pt[2])] for pt in edge_pts[:-1]]
    profile_pts_bottom = [[(pt[0], -pt[1], pt[2]), (-radius + pt[0], 0.0, pt[2]), pt] for pt in edge_pts[:-1]]

    crvs_top = [rs.AddCurve(pts) for pts in profile_pts_top]
    crvs_bottom = [rs.AddCurve(pts) for pts in profile_pts_bottom]

    profile_crvs = [rs.JoinCurves(crvs) for crvs in zip(crvs_top, crvs_bottom)]

    srf = rs.AddLoftSrf(profile_crvs, end=edge_pts[-1])

    cap = rs.AddPlanarSrf([profile_crvs[0]])

    return rs.JoinSurfaces([srf, cap])

  def twig_gen(self, base_radius, top_radius, height):
    return rs.AddCylinder(rs.WorldXYPlane(), height, base_radius)

class RockerTree01(barleycorn.Wrapper):
  def __init__(self, middle, **kwargs):
    self.middle = middle
    barleycorn.Wrapper.__init__(self, self.makeMe(), **kwargs)

  def makeMe(self):
    base = designs.RockerCenter01(self.middle.clearance_radius_inner, self.middle.rim_radius_major, self.middle.wall_thickness)
    tree = Tree()
    return base.bU(tree)




