__author__ = 'MrGecko'

"""
Graphics group which transforms its members according to simple translation/rotation operations
"""

import pyglet

push = pyglet.gl.glPushMatrix
pop = pyglet.gl.glPopMatrix
translate = pyglet.gl.glTranslatef
rotate = pyglet.gl.glRotatef


class TransformGroup(pyglet.graphics.Group):
    def __init__(self, x=0, y=0, r=0, order=0, **kwargs):
        super(TransformGroup, self).__init__(**kwargs)
        self.order = order
        self.x = x
        self.y = y
        self.r = r

    def set_state(self):
        push()
        print self, self.x
        if self.x or self.y:
            translate(self.x, self.y, 0)
        if self.r:
            rotate(self.r, 0, 0, 1)

    def unset_state(self):
        pop()

    def __cmp__(self, other):
        if isinstance(other, TransformGroup):
            for v in (cmp(self.order, other.order), cmp(self.x, other.x), cmp(self.y, other.y), cmp(self.r, other.r)):
                if v != 0:
                    return v
        return -1

        # def __str__(self):
        #    return "TransformGroup(x=%0.2f, y=%0.2f, r=%0.2f, order=%d)" % (self.x, self.y, self.r, self.order)

        #def __repr__(self):
        #    return "TransformGroup(x=%0.2f, y=%0.2f, r=%0.2f, order=%d)" % (self.x, self.y, self.r, self.order)
