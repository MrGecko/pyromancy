from core.actor.ActorGroup import ActorGroup
from pyromancy.standard.actor.level.terrain.heightmap import create_2d_texture_random as make_perlin
from pyromancy.standard.actor.level.Cell import Cell
from standard.actor.level.HexaGrid import HexaGrid


__author__ = 'Gecko'


class HexaMap(ActorGroup):
    TEXTURES = {
        "common": "media.terrain.clay",
        "top": "media.terrain.clay.light"
    }

    def __init__(self, sprite_factory, cell_batch, (w, h, d, thickness), (cell_w, cell_h, edge_len)):
        super(HexaMap, self).__init__("hexamap")

        self.__cell_batch = cell_batch
        self.__create_extended_sprite = sprite_factory.create_extended_sprite

        self.__cell_width = cell_w
        self.__cell_height = cell_h

        self.__t = edge_len + (cell_w - edge_len - 2) * 0.5
        self.__q = cell_h - edge_len
        self.__edge_length = edge_len

        self.__map_width = w if w % 2 != 0 else w + 1
        self.__map_height = h if h % 2 != 0 else h + 1
        self.__map_depth = d
        self.__thickness = thickness

        self.__heightmap = []

    @property
    def cell_width(self):
        return self.__cell_width

    @property
    def cell_height(self):
        return self.__cell_height

    @property
    def height_in_pixels(self):
        return self.__cell_height * self.__map_height

    @property
    def width_in_pixels(self):
        return self.__cell_height * self.__map_width

    def get_six_neighborhood_names(self, x, y, z):
        return [
            HexaMap.make_cell_name(x - 1, y, z),
            HexaMap.make_cell_name(x, y - 1, z),
            HexaMap.make_cell_name(x + 1, y, z),
            HexaMap.make_cell_name(x + 1, y + 1, z),
            HexaMap.make_cell_name(x, y + 1, z),
            HexaMap.make_cell_name(x - 1, y + 1, z)
        ]

    def get_eight_neighborhood_names(self, x, y, z):
        names = self.get_six_neighborhood_names(x, y, z)
        names.extend([HexaMap.make_cell_name(x, y, z - 1),
                      HexaMap.make_cell_name(x, y, z + 1)])
        return names

    def get_neighborhood(self, names):
        hexagrid = self.get_child("hexagrid")
        return [n for n in [hexagrid.get_child(name) for name in names] if n is not None]


    def get_six_neighborhood(self, x, y, z):
        names = self.get_six_neighborhood_names(x, y, z)
        return self.get_neighborhood(names)


    def get_eight_neighborhood(self, x, y, z):
        names = self.get_eight_neighborhood_names(x, y, z)
        return self.get_neighborhood(names)

    def gen_grid(self, seed=1.0 / 20):
        heightmap_seed, heightmap = make_perlin(self.__map_width, self.__map_height, self.__map_depth, seed)
        self.__heightmap = heightmap

        w, h, d = self.__map_width - 1, self.__map_height - 1, self.__map_depth - 1

        # generate the cell coords
        #create the upper part of the map (the upper diagonal starts from the upper left corner)
        #d_range = range(0, d, 1)
        layer = 0
        coords = [(0, h)]
        ly = [0]
        for x in range(2, w + 2, 2):
            lx = range(x, -1, -1)

            ly.append(ly[-1])
            ly.append(ly[-1] + 1)

            layer += 1
            for i in range(0, len(lx)):
                cy = h - ly[i]
                if cy >= 0:
                    coords.append((lx[i], cy))

        #create the second part (the lower diagonal) of the map
        #it starts from the upper right corner
        q = 0
        for n in range(h, 0, -1):
            x = 0
            layer += 1
            for i in range(1, n + 1):
                coords.append((w - x, h - i - q))
                if w - x - 1 <= 0:
                    break
                coords.append((w - x - 1, h - i - q))
                x += 2
            q += 1

        #create the cells
        grid = []
        for cx, cy in coords:
            d_range = range(0, self.__thickness)
            d_range += range(self.__thickness, self.__thickness + self.__heightmap[cx + cy * w], 1)
            #a vertical stack of cells
            carotte = [self.__create_cell(cx, cy, z) for z in d_range]
            grid.extend(carotte)

        hexagrid = HexaGrid(grid)
        self.add_child(hexagrid)

    def __iso_to_screenspace_coords(self, x, y, z):
        #horizontal coord
        x2 = x * self.__t
        #vertical coord with a shift for the odd columns
        k = y * self.__q + (self.__edge_length - 1) * z
        y2 = k if (x % 2 == 0) else k - self.__q * 0.5

        return x2, y2

    def __create_cell(self, x, y, z, layer=None):
        new_name = HexaMap.make_cell_name(x, y, z)
        iso = self.__iso_to_screenspace_coords(x, y, z)
        if layer is None:
            layer = "map.layer.carotte[%i,%i]" % (x, y)
        sprite = self.__get_cell_sprite(x, y, z, layer)
        sprite.x = iso[0]
        sprite.y = iso[1]
        cell = Cell(new_name, x, y, z, sprite)
        return cell

    def add_cell(self, x, y, z):
        new_name = HexaMap.make_cell_name(x, y, z)
        cell = self.get_child("hexagrid").get_child(new_name)
        if cell is None:
            cell = self.__create_cell(x, y, z)

            self.get_child("hexagrid").add_child(cell)
        return cell


    @staticmethod
    def make_cell_name(x, y, z):
        return "cell[%i,%i,%i]" % (x, y, z)

    def __get_cell_sprite(self, x, y, z, layer):
        # TODO:a nettoyer, utiliser un defaultdict
        symbol = "common"
        if z >= self.__thickness:
            lvl = self.__heightmap[x + y * self.__map_width]
            if lvl >= self.__map_depth * 0.55:
                symbol = "top"

        new_sprite = self.__create_extended_sprite(
            symbol=HexaMap.TEXTURES[symbol],
            layer=layer,
            batch=self.__cell_batch
        )
        return new_sprite

