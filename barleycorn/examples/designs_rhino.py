__author__ = 'jjpr'

from barleycorn.toolkits.toolkitRhino import SpecialRhino
import barleycorn
import barleycorn.examples.designs as designs
import rhinoscriptsyntax as rs
import random

class Tree(SpecialRhino):
  def __init__(self, base_radius=4.0, terminal_radius=0.5, height=100.0, density=5, fraction=0.5, angle=60, **kwargs):
    self.base_radius = base_radius
    self.terminal_radius = terminal_radius
    self.height = height
    self.density = density
    self.fraction = fraction
    self.angle = angle
    SpecialRhino.__init__(self, **kwargs)

  def geometry(self):
    return self.tree_gen(self.base_radius, self.height)

  def tree_gen(self, radius, height):
    sub_radius = radius * self.fraction
    if radius < self.terminal_radius:
      return self.leaf_gen(sub_radius)
    else:
      trunk = [self.twig_gen(radius, sub_radius, height)]
      sub_angle_z = 0
      for i in range(self.density):
        sub_height = height * (self.fraction ** (i+1))
        sub_angle_y = self.angle * (self.fraction ** i)
        sub_angle_z += self.angle - (random.random() * self.angle / 2.0)
        sub = self.tree_gen(sub_radius, sub_height)
        sub = rs.RotateObjects(sub, (0,0,0), sub_angle_y, (0,1,0))
        sub = rs.RotateObjects(sub, (0,0,0), sub_angle_z, (0,0,1))
        sub = rs.MoveObjects(sub, (0,0,height - sub_height))
        try:
          trunk = rs.BooleanUnion(trunk+sub) or trunk
        except Exception as e:
          print e
      return trunk

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
    base = rs.AddCircle(rs.WorldXYPlane(), base_radius)
    top = rs.MoveObject(rs.AddCircle(rs.WorldXYPlane(), top_radius), (0.0, 0.0, height))
    srf = rs.AddLoftSrf([base, top])
    cap0 = rs.AddPlanarSrf([base])
    cap1 = rs.AddPlanarSrf([top])
    return rs.JoinSurfaces([srf, cap0, cap1])

  def bend(self):
    return 44

class RockerTree01(barleycorn.Wrapper):
  def __init__(self, middle, **kwargs):
    self.middle = middle
    barleycorn.Wrapper.__init__(self, self.makeMe(), **kwargs)

  def makeMe(self):
    base = designs.RockerCenter01(self.middle.clearance_radius_inner, self.middle.rim_radius_major, self.middle.wall_thickness)
    tree = Tree()
    return base.bU(tree)




