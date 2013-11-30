# coding=utf-8


import pyglet
from pyglet.gl import *
from pyglet.image import TextureGrid, ImageGrid
from pyromancy.core.actor.Actor import Actor


class ResourceManager(Actor):
    
    __independant_tilesets = {}
    __fonts = {}
    
    def __init__(self, name):
        super(ResourceManager, self).__init__(name)

    @classmethod
    def load_tileset(cls, tileset):
        filename = tileset["image"]
        if not filename in cls.__independant_tilesets:
            try:
                img = pyglet.resource.image(filename)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
            except IOError:
                print "[resource manager error] unable to load image '%s'" % filename
                return None

            img.anchor_x = 0
            img.anchor_y = 0

            if "nbtile_width" in tileset:
                tilewidth = img.width / tileset["nbtile_width"]
                #assert tilewidth >= 1
            elif "tilewidth" in tileset:
                tilewidth = tileset["tilewidth"]
            else:
                tilewidth = img.width

            if "nbtile_height" in tileset:
                tileheight = img.height / tileset["nbtile_height"]
                #assert tileheight >= 1
            elif "tileheight" in tileset:
                tileheight = tileset["tileheight"]
            else:
                tileheight = img.height

            rx = img.width / tilewidth
            ry = img.height / tileheight

            img_grid = ImageGrid(img, ry, rx)
            for _img in img_grid:
                _img.anchor_x = 0
                _img.anchor_y = 0
                tileset["frames"] = TextureGrid(img_grid)

            tileset["tilewidth"] = tilewidth
            tileset["tileheight"] = tileheight
            cls.__independant_tilesets[filename] = tileset

        return cls.__independant_tilesets[filename]

    #make a light tileset from the picture
    @staticmethod
    def load_image(filename, options=None):
        if not options:
            options = {}
        data = {"image": filename}

        for k, v in options.items():
            data[k] = v

        return ResourceManager.load_tileset(data)

    @staticmethod
    def add_font(filename):
        pyglet.resource.add_font(filename)

    @classmethod
    def load_font(cls, **kargs):
        cls.__fonts[kargs["name"]] = pyglet.font.load(**kargs)
        return cls.__fonts[kargs["name"]]



