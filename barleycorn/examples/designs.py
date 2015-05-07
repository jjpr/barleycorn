__author__ = 'jjpr'

from math import pi, acos
import barleycorn

class RockerStand01(barleycorn.Wrapper):
  def __init__(self, clearance_radius_inner=20.0, wall_thickness=1.0, **kwargs):
    self.clearance_radius_inner = clearance_radius_inner
    self.wall_thickness = wall_thickness

    barleycorn.Wrapper.__init__(self, self.makeMe(), **kwargs)

  def makeMe(self):
    tet_angle = acos(-1.0/3.0)
    tet_dihedral_angle = acos(1.0/3.0)
    leg_angle = (pi-tet_angle)/2.0

    self.bowl_radius_inner = self.clearance_radius_inner + (self.wall_thickness * 2.0)
    self.bowl_radius_outer = self.bowl_radius_inner + self.wall_thickness
    foot_radius = self.wall_thickness * 4.0
    leg_length = self.bowl_radius_outer * 2.0

    sph_bowl_outer = barleycorn.primitives.Sphere(self.bowl_radius_outer)
    cyl_bowl_outer = barleycorn.primitives.Cylinder(self.bowl_radius_outer*1.001, self.bowl_radius_outer*1.001)
    cyl_bowl_outer = cyl_bowl_outer.translateZ(-cyl_bowl_outer.height)
    sph_bowl_inner = barleycorn.primitives.Sphere(self.bowl_radius_inner)

    cyl_leg_01 = barleycorn.primitives.Cylinder(self.wall_thickness, leg_length)
    sph_foot_01 = barleycorn.primitives.Sphere(foot_radius)
    cyl_brace_01 = barleycorn.primitives.Cylinder(self.wall_thickness, leg_length)
    cyl_brace_01 = cyl_brace_01.rotateY(-pi/3.0).rotateZ(-tet_dihedral_angle/2.0)

    leg_foot_brace_01 = cyl_leg_01.bU(sph_foot_01).bU(cyl_brace_01)
    leg_foot_brace_01 = leg_foot_brace_01.translateZ(-cyl_leg_01.height).rotateY(-leg_angle)

    leg_foot_brace_02 = leg_foot_brace_01.rotateZ(2.0*pi/3.0)
    leg_foot_brace_03 = leg_foot_brace_02.rotateZ(2.0*pi/3.0)

    legs = leg_foot_brace_01.bU(leg_foot_brace_02).bU(leg_foot_brace_03)

    self.rim_radius_major = (self.bowl_radius_outer + self.bowl_radius_inner) / 2.0
    tor_rim = barleycorn.primitives.Torus(self.rim_radius_major, self.wall_thickness)
    con_rim_divot = barleycorn.primitives.Cone(self.wall_thickness * 2.0, self.wall_thickness *2.0)
    con_rim_divot_pos = con_rim_divot.translateY(self.rim_radius_major)
    con_rim_divot_neg = con_rim_divot.translateY(-self.rim_radius_major)

    base = cyl_bowl_outer.bI(sph_bowl_outer).bU(legs).bS(sph_bowl_inner)

    stand = base.bU(tor_rim).bS(con_rim_divot_pos).bS(con_rim_divot_neg)

    return stand

class RockerMiddle01(barleycorn.Wrapper):
  def __init__(self, clearance_radius_outer=20.0, stand_rim_radius_major=22.5, wall_thickness=1.0, **kwargs):
    self.clearance_radius_outer = clearance_radius_outer
    self.stand_rim_radius_major = stand_rim_radius_major
    self.wall_thickness = wall_thickness

    barleycorn.Wrapper.__init__(self, self.makeMe(), **kwargs)

  def makeMe(self):
    self.bowl_radius_outer = self.clearance_radius_outer - (self.wall_thickness * 2.0)
    self.bowl_radius_inner = self.bowl_radius_outer - self.wall_thickness
    rim_radius_major = (self.bowl_radius_outer + self.bowl_radius_inner) / 2.0
    pivot_arm_offset = self.wall_thickness * 3.0
    pivot_arm_length = self.stand_rim_radius_major - rim_radius_major

    sph_bowl_outer = barleycorn.primitives.Sphere(self.bowl_radius_outer)
    cyl_bowl_outer = barleycorn.primitives.Cylinder(self.bowl_radius_outer*1.001, self.bowl_radius_outer*1.001)
    cyl_bowl_outer = cyl_bowl_outer.translateZ(-cyl_bowl_outer.height)
    sph_bowl_inner = barleycorn.primitives.Sphere(self.bowl_radius_inner)

    tor_rim = barleycorn.primitives.Torus(rim_radius_major, self.wall_thickness)
    con_rim_divot = barleycorn.primitives.Cone(self.wall_thickness * 2.0, self.wall_thickness *2.0)
    con_rim_divot_pos = con_rim_divot.translateX(rim_radius_major)
    con_rim_divot_neg = con_rim_divot.translateX(-rim_radius_major)

    con_pivot = barleycorn.primitives.Cone(self.wall_thickness, pivot_arm_offset)
    cyl_pivot_arm = barleycorn.primitives.Cylinder(self.wall_thickness * 1.001, pivot_arm_length + (self.wall_thickness * 2.0))
    cyl_pivot_arm = cyl_pivot_arm.rotateX(pi/2.0).translateY(con_pivot.radius).translateZ(con_pivot.height)
    cyl_pivot_riser = barleycorn.primitives.Cylinder(self.wall_thickness, con_pivot.height)
    cyl_pivot_riser = cyl_pivot_riser.translateY(-pivot_arm_length)

    pivot = con_pivot.bU(cyl_pivot_arm).bU(cyl_pivot_riser)
    pivot_pos = pivot.translateY(self.stand_rim_radius_major)
    pivot_neg = pivot_pos.rotateZ(pi)

    body = cyl_bowl_outer.bI(sph_bowl_outer).bS(sph_bowl_inner).bU(tor_rim)

    middle = body.bS(con_rim_divot_pos).bS(con_rim_divot_neg).bU(pivot_pos).bU(pivot_neg)

    return middle
