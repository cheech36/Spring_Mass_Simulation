from __future__ import division
from visual import *
from visual.graph import *
import threading
import time
## Currently give error
## Need to move animation to primary thread
## For more details see: https://groups.google.com/forum/#!topic/vpython-users/TsDyBN9AKHU


class SpringMassSystem:
    def __init__(self, k, m, origin = vector(0,0,0), axis = vector(1,0,0)):
        self.t = 0
        self.k = k
        self.m = m
        self.damping = 0
        self.origin = origin ## Fixed end of spring
        self.L_eq = 5
        self.axis = norm(axis)
        self.r_eq = self.origin + self.L_eq * self.axis
        self.r    = vector(self.r_eq)
        self.s = 0
        self.body = sphere(pos = vector(self.r), radius = 2, color = color.red)
        self.v = vector(0,0,0)

        self.spring = helix(pos = origin, axis  = vector(self.axis - self.origin) * self.L_eq
                            , radius = 1, thickness = .25)
        self.mount = box(length=1, height=5, width=5)
        self.mount.axis = vector(self.axis)
        self.mount.pos = origin - self.axis * self.mount.length/2
        self.mount.color = color.blue

        self.f1 = gcurve(color = color.cyan)


    def recalc_v(self, dt):
        dv = -self.k/self.m * self.s - self.damping * self.v.mag * norm(self.s)
        self.v += dv
        return self.v

    def recalc_r(self, dt):
        dr = self.v * dt
        self.r += dr
        return self.r

    def render(self):
        self.body.pos = self.r
        self.spring.axis = self.r - self.origin

    def stretch(self, stretch):
        self.s = stretch * self.axis
        self.r += self.s

    def recalc_stretch(self):
        displacement = self.r - self.r_eq
        self.s = displacement
        return self.s

    def set_springLength(self, length):
        self.L_eq = length
        self.r_eq = self.origin + self.L_eq * self.axis
        self.r = vector(self.r_eq)
        self.body.pos = vector(self.r)
        self.spring.axis  = self.r - self.origin

    def set_dampingConst(self, b):
        self.damping = b/self.m

    def graph(self,t,y):
        self.f1.plot(pos=(t,y))


class systemThread (threading.Thread):
    def __init__(self, threadID,  mgr):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.mgr = mgr

    def run(self):
        while true:
            self.mgr.recalc()
            time.sleep(.01)

class enviornment:
    def __init__(self, time_resolution = .01):
        self.scene1 = display(x=0, y=0, width=1200, height = 600)
        self.scene1.autoscale = False
        self.scene1.title = 'Spring Mass Oscillator'
        self.scene1.range = (30,10,5)
        self.dt = time_resolution

    def go(self, mgr):
        while true:
            rate(100)
            mgr.render()

class systemManager:
    def __init__(self, flags = 'none', resolution = .02):
        self.systemList = list()
        self.dt = resolution
        self.nSystems = 0
        self.flags = flags


    def addSystem(self, oscillator):
        self.systemList.append(oscillator)
        ++self.nSystems

    def recalc(self):
        for s in self.systemList:
            s.recalc_v(self.dt)
            s.recalc_r(self.dt).y
            y = s.recalc_stretch().y
            if self.flags == 'graph' and s.t <= 50:
                s.t += self.dt
                s.f1.plot(pos=(s.t,y))

    def render(self):
        for s in self.systemList:
            s.render()

system1 = SpringMassSystem(3,10, vector(0,0,0), vector(0,-1,0))
system1.set_springLength(20)
system1.set_dampingConst( .4 )
system1.stretch(8)
system1.body.color = color.cyan

system2 = SpringMassSystem(10,10, vector(10,0,0), vector(0,-1,0))
system2.set_springLength(20)
system2.set_dampingConst( .8 )
system2.stretch(8)
system2.f1.dot_color = color.red

mgr_th1 = systemManager('graph')
mgr_th2 = systemManager('graph')

mgr_th1.addSystem(system1)
mgr_th2.addSystem(system2)

systemThread1 = systemThread(1,  mgr_th1)
systemThread2 = systemThread(2,  mgr_th2)

systemThread1.start()
systemThread2.start()

mgr_graphics = systemManager()
mgr_graphics.addSystem(system1)
mgr_graphics.addSystem(system2)

env1    = enviornment()
env1.go(mgr_graphics)

