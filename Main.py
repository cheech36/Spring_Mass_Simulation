from __future__ import division
from visual import *

class SpringMassSystem:
    def __init__(self, k, m, origin = vector(0,0,0), axis = vector(1,0,0)):
        self.k = k
        self.m = m
        self.origin = origin ## Fixed end of spring
        self.L_eq = 5
        self.axis = norm(axis)
        self.r_eq = self.origin + self.L_eq * self.axis
        self.r    = vector(self.r_eq)
        self.s = 0
        self.body = sphere(pos = self.r, radius = 2, color = color.red)
        self.v = vector(0,0,0)

    def recalc_v(self, dt):
        dv = -self.k/self.m * self.s
        self.v += dv
        return self.v

    def recalc_r(self, dt):
        dr = self.v * dt
        self.r += dr
        return self.r

    def render(self):
        self.body.pos = self.r

    def stretch(self, stretch):
        self.s = stretch * self.axis
        self.r += self.s

    def recalc_stretch(self):
        displacement = self.r - self.r_eq
        self.s = displacement

class enviornment:
    def __init__(self, time_resolution = .01):
        self.scene1 = display(x=0, y=0, width=1200, height = 600)
        self.scene1.autoscale = False
        self.scene1.title = 'Spring Mass Oscillator'
        self.scene1.range = (30,10,5)
        self.dt = time_resolution


    def run(self, system):
        while true:
            rate(100)
            system.recalc_v(self.dt)
            system.recalc_r(self.dt)
            system.recalc_stretch()
            system.render()



system1 = SpringMassSystem(5,10)
system1.stretch(2)
env1    = enviornment()
env1.run(system1)
