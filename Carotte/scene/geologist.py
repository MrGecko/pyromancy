__author__ = 'Gecko'
from pyromancy.core.actor.Actor import Actor
from pyromancy.standard.actor.visual.sprite_actor import SpriteActor


class Geologist(Actor):
    TEXTURES = {
        "common": "media.terrain.clay",
        "bottom": "media.terrain.clay_empty.50",
        "top": "media.terrain.clay.light"
    }

    def __init__(self, scene):
        super(Geologist, self).__init__("geologist")
        self.__scene = scene
        self.__create_sprite = scene.root.find("sprite_factory").create_extended_zsprite

    @property
    def __hexamap(self):
        return self.__scene.root.find("hexamap")

    @property
    def __hexagrid(self):
        return self.__scene.root.find("hexagrid")

    def initialize(self):
        hexagrid = self.__hexagrid
        if hexagrid:
            for cell in hexagrid.get_active_children():
                self.identify(cell)

    def identify(self, cell):
        symbol = "common"
        __hexamap = self.__hexamap
        lvl = __hexamap.heightmap[cell.x + cell.y * __hexamap.map_width]
        if cell.z >= __hexamap.thickness:
            if lvl >= __hexamap.map_depth * 0.55:
                symbol = "top"
        elif lvl <= __hexamap.map_depth * 0.25:
            symbol = "bottom"

        new_sprite = self.__create_sprite(
            symbol=Geologist.TEXTURES[symbol],
            layer="hexamap",
        )

        x, y = __hexamap.iso_to_screenspace_coords(cell.x, cell.y, cell.z)
        z = cell.z * __hexamap.map_height - cell.y * 2 + (cell.x % 2 != 0)

        new_sprite.x = x
        new_sprite.y = y
        new_sprite.z = z

        cell.add_child(SpriteActor("sprite[%i,%i,%i]" % (x, y, z), new_sprite))