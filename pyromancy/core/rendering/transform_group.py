__author__ = 'MrGecko'

import pyglet
from pyglet.gl import glLoadIdentity


class TransformGroup(pyglet.graphics.Group):
    def __init__(self, parent, transform):
        super(TransformGroup, self).__init__(parent=parent)
        self.__transform = transform

    def set_state(self):
        glLoadIdentity()
        self.__transform()

    def unset_state(self):
        glLoadIdentity()

