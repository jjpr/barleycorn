__author__ = 'jjpr'

from barleycorn.toolkits.toolkitRhino import SpecialRhino
import barleycorn
import barleycorn.examples.designs as designs
import rhinoscriptsyntax as rs
import random

class Tree(SpecialRhino):
  def __init__(self, base_radius=4.0, terminal_radius=0.5, density=5, **kwargs):
    self.base_radius = base_radius
    self.terminal_radius = terminal_radius
    self.density = density
    SpecialRhino.__init__(self, **kwargs)

  def geometry(self):
    return self.tree_gen(self.base_radius, self.base_radius * 40.0)

  def tree_gen(self, radius, height):
    if radius < self.terminal_radius:
      return self.leaf_gen(radius)
    else:
      trunk = [self.twig_gen(radius, height)]
      reduction = 0.7
      sub_radius = radius * reduction
      sub_height = height * reduction
      sub_num = random.randint(1, self.density)
      tip = self.tree_gen(sub_radius, sub_height)
      tip = rs.MoveObjects(tip, (0,0,sub_height))
      trunk = rs.BooleanUnion(trunk+tip) or trunk
      for i in range(sub_num):
        sub = self.tree_gen(sub_radius, sub_height)
        sub = rs.RotateObjects(sub, (0,0,0), self.bend(), (0,1,0))
        sub = rs.RotateObjects(sub, (0,0,0), random.random()*360.0, (0,0,1))
        sub = rs.MoveObjects(sub, (0,0,random.random()*height*0.4+height*0.5))
        trunk = rs.BooleanUnion(trunk+sub) or trunk
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


  def twig_gen(self, radius, height):
    base = rs.AddCircle(rs.WorldXYPlane(), radius)
    mid_01 = rs.MoveObject(rs.AddCircle(rs.WorldXYPlane(), radius * 0.85), (0.0, 0.0, height * 0.45))
    mid_02 = rs.MoveObject(rs.AddCircle(rs.WorldXYPlane(), radius * 0.40), (0.0, 0.0, height * 0.9))
    end = (0.0, 0.0, height)
    srf = rs.AddLoftSrf([base, mid_01, mid_02], end=end)
    cap = rs.AddPlanarSrf([base])
    return rs.JoinSurfaces([srf, cap])

  def bend(self):
    return 90 * (-(2.0/(self.density + 2.0))+1.0)

class RockerTree01(barleycorn.Wrapper):
  def __init__(self, middle, **kwargs):
    self.middle = middle
    barleycorn.Wrapper.__init__(self, self.makeMe(), **kwargs)

  def makeMe(self):
    base = designs.RockerCenter01(self.middle.clearance_radius_inner, self.middle.rim_radius_major, self.middle.wall_thickness)
    tree = Tree()
    return base.bU(tree)




