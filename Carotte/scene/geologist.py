from collections import defaultdict
from pprint import pprint

__author__ = 'Gecko'
from pyromancy.core.actor.Actor import Actor
from pyromancy.standard.actor.visual.sprite_actor import SpriteActor


class Geologist(Actor):
    MINERALS = {
        "mud": 1,
        "clay": 2,
        "granite": 3,
        "iron": 4,
        "salt": 5,
    }

    TEXTURES = defaultdict(
        lambda: "media.terrain.clay",
        [
            ("normal_clay", "media.terrain.clay"),
            ("dark_clay", "media.terrain.clay_empty.50"),
            ("light_clay", "media.terrain.clay.light")
        ]
    )

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


    def __identify_data(self, x, y, z):
        __hexamap = self.__hexamap

        # material
        mat = "normal_clay"
        lvl = __hexamap.heightmap[x + y * __hexamap.map_width]
        if z >= __hexamap.thickness:
            if lvl >= __hexamap.map_depth * 0.55:
                mat = "light_clay"
        elif lvl <= __hexamap.map_depth * 0.25:
            mat = "dark_clay"

        # minerals
        minerals = {"clay"}
        neighbors = __hexamap.get_eight_neighborhood(x, y, z)

        lclay = 0
        nclay = 0
        dclay = 0
        for n in neighbors:
            if n.data["material"] == "light_clay":
                lclay += 1
            elif n.data["material"] == "normal_clay":
                nclay += 1
            elif n.data["material"] == "dark_clay":
                dclay += 1

        if mat == "light_clay" and nclay >= 2:
            minerals.update({"clay", "mud"})
        if mat == "dark_clay" and dclay >= 3:
            minerals.update({"granite", "clay"})
        if mat == "dark_clay" and nclay >= 5:
            minerals.update({"iron", "clay"})
        if mat == "dark_clay" and lclay >= 2:
            minerals.update({"iron", "granite", "mud"})
        if mat == "light_clay" and lclay >= 2:
            minerals.update({"salt"})

        #data dict
        data = {
            "material": mat,
            "minerals": minerals,
        }
        return data

    def identify(self, cell):
        __hexamap = self.__hexamap

        x, y, z = cell.x, cell.y, cell.z

        cell.data.update(self.__identify_data(x, y, z))

        new_sprite = self.__create_sprite(
            symbol=Geologist.TEXTURES[cell.data["material"]],
            layer="hexamap",
        )

        # associate a sprite actor to the cell
        sprite_x, sprite_y = __hexamap.iso_to_screenspace_coords(x, y, z)
        sprite_z = z * __hexamap.map_height - y * 2 + (x % 2 != 0)

        new_sprite.x = sprite_x
        new_sprite.y = sprite_y
        new_sprite.z = sprite_z

        cell.add_child(SpriteActor("sprite[%i,%i,%i]" % (sprite_x, sprite_y, sprite_z), new_sprite))


    def pprint_minerals(self):
        minerals = {}
        for cell in self.__hexagrid.get_active_children():
            for m in cell.data["minerals"]:
                pass
                if m not in minerals:
                    minerals[m] = 0
                else:
                    minerals[m] += 1

        pprint(minerals)
