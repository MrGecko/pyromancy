from pyromancy.standard.actor.level.terrain.heightmap import create_2d_texture_random as make_perlin
from pyromancy.core.actor.ActorGroup import ActorGroup
from pyromancy.standard.actor.level.Cell import Cell
from pyromancy.standard.actor.physic.position_actor import PositionActor


__author__ = 'Gecko'


class HexaMap(ActorGroup):
    TEXTURES = {
        "common": "media.terrain.clay",
        "top": "media.terrain.clay.light"
    }

    def __init__(self, sprite_factory, cell_batch, (w, h, d, thickness), (cell_w, cell_h, edge_len), (x, y)=(0, 0)):
        super(HexaMap, self).__init__("hexamap")
        self.add_child(PositionActor(x, y))
        self.__pos = self.get_child("position")

        self.__cell_batch = cell_batch
        self.__create_extended_sprite = sprite_factory.create_extended_sprite

        self.__t = edge_len + (cell_w - edge_len - 2) * 0.5
        self.__q = cell_h - edge_len
        self.__edge_length = edge_len

        self.__map_width = w if w % 2 != 0 else w + 1
        self.__map_height = h if h % 2 != 0 else h + 1
        self.__map_depth = d
        self.__thickness = thickness

        heightmap_seed, heightmap = make_perlin(self.__map_width, self.__map_height, self.__map_depth, 1.0 / 20)

        self.__heightmap = heightmap

        self.__texture_maps = []
        self.__texture_maps.append((heightmap_seed, heightmap))

        #finally generate the map
        self.__grid = self.gen_grid(self.__map_width - 1, self.__map_height - 1, self.__map_depth)

    def gen_grid(self, w, h, d):
        # generate the cell coords
        #create the upper part of the map (the upper diagonal starts from the upper left corner)
        #d_range = range(0, d, 1)
        layer = 0
        coords = [(0, h, layer)]
        ly = [0]
        for x in range(2, w + 2, 2):
            lx = range(x, -1, -1)

            ly.append(ly[-1])
            ly.append(ly[-1] + 1)

            layer += 1
            for i in range(0, len(lx)):
                cy = h - ly[i]
                if cy >= 0:
                    coords.append((lx[i], cy, "map.layer%i" % layer))

        #create the second part (the lower diagonal) of the map
        #it starts from the upper right corner
        q = 0
        for n in range(h, 0, -1):
            x = 0
            layer += 1
            for i in range(1, n + 1):
                coords.append((w - x, h - i - q, "map.layer%i" % layer))
                if w - x - 1 <= 0:
                    break
                coords.append((w - x - 1, h - i - q, "map.layer%i" % layer))
                x += 2
            q += 1

        #create the cells
        grid = []
        for cx, cy, layer in coords:
            d_range = range(1, self.__thickness)
            d_range += range(self.__thickness, self.__thickness + self.__heightmap[cx + cy * w], 1)
            carotte = [self.__create_cell(cx, cy, z, layer) for z in d_range]
            grid.extend(carotte)

        return grid

    def __iso_to_screenspace_coords(self, x, y, z):
        # horizontal coord
        x2 = x * self.__t
        #vertical coord with a shift for the odd columns
        k = y * self.__q + (self.__edge_length - 1) * z
        y2 = k if (x % 2 == 0) else k - self.__q * 0.5
        #position offset for the map itself

        return self.__pos.x + x2, self.__pos.y + y2

    def __create_cell(self, x, y, z, layer):
        iso = self.__iso_to_screenspace_coords(x, y, z)
        sprite = self.__get_cell_sprite(x, y, z, layer)
        sprite.x = iso[0]
        sprite.y = iso[1]
        return Cell(x, y, z, sprite)

    def __get_cell_sprite(self, x, y, z, layer):
        # TODO:a nettoyer, utiliser un defaultdict
        symbol = "common"
        if z >= self.__thickness:
            lvl = self.__texture_maps[-1][1][x + y * self.__map_width]
            if lvl >= self.__map_depth * 0.55:
                symbol = "top"

        new_sprite = self.__create_extended_sprite(
            symbol=HexaMap.TEXTURES[symbol],
            layer=layer,
            batch=self.__cell_batch
        )
        return new_sprite