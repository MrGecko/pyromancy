"""
Camera tracks a position, orientation and zoom level, and applies openGL
transforms so that subsequent renders are drawn at the correct place, size
and orientation on screen
"""

from __future__ import division
from math import sin, cos

from pyglet.gl import (
    glLoadIdentity, glMatrixMode, gluLookAt, glOrtho,
    GL_MODELVIEW, GL_PROJECTION,
)

from pyromancy.core.actor.ActorGroup import ActorGroup


class Target(ActorGroup):

    def __init__(self, camera):
        super(Target, self).__init__("target")
        self.x, self.y = camera.x, camera.y
        self.scale = camera.scale
        self.angle = camera.angle
        self._target_object = None
        self._offset = (0, 0)
        self._hlock = False
        self._vlock = False

    def follow_gameobject(self, obj, hlock, vlock, offset):
        self._target_object = obj
        self._offset = offset
        self._hlock = hlock
        self._vlock = vlock

    def update(self, dt):
        if self._target_object is not None:
            pos = self._target_object.get_component("position")
            if not self._hlock:
                self.x = pos.x + self._offset[0]
            if not self._vlock:
                self.y = pos.y + self._offset[1]


class Camera(ActorGroup):

    def __init__(self, name, position=(0, 0), scale=1, angle=0, friction=1.0):
        super(Camera, self).__init__(name)
        self.x, self.y = position
        self.scale = scale
        self.angle = angle
        self.friction = friction
        self.target = Target(self)
        self.add_child(self.target)
        self.near_plane = 0.5
        self.far_plane = 10000

    def zoom(self, factor):
        self.target.scale *= factor

    def zoom_to(self, zoom):
        self.target.scale = zoom
        
    def pan(self, length, angle):
        self.target.x += length * sin(angle + self.angle)
        self.target.y += length * cos(angle + self.angle)

    def tilt(self, angle):
        self.target.angle += angle

    def update(self, dt):
        super(Camera, self).update(dt)
        self.x += (self.target.x - self.x) * self.friction
        self.y += (self.target.y - self.y) * self.friction
        self.scale += (self.target.scale - self.scale) * self.friction
        self.angle += (self.target.angle - self.angle) * self.friction


    def focus(self, width=1, height=1):
        """Set projection and modelview matrices ready for rendering"""
        if height <= 0:
            height = 1
        if width <= 0:
            width = 1

        # Set projection matrix suitable for 2D rendering"
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        aspect = width / float(height)
        # gluOrtho2D(-self.scale * aspect, +self.scale * aspect, -self.scale, +self.scale)
        glOrtho(-self.scale * aspect, +self.scale * aspect, -self.scale, +self.scale, self.near_plane, self.far_plane)

        # Set modelview matrix to move, scale & rotate to camera position"
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(
            int(self.x), int(self.y), +1.0,
            int(self.x), int(self.y), -1.0,
            sin(self.angle), cos(self.angle), 0.0)


    def hud_mode(self, width, height):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, width, 0, height, self.near_plane, self.far_plane)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def follow_gameobject(self, obj, hlock=False, vlock=False, offset=(0, 0)):
        self.target.follow_gameobject(obj, hlock, vlock, offset)
