from pyromancy.core.actor.ActorGroup import ActorGroup
from pyromancy.standard.actor.level.terrain.heightmap import create_2d_texture_random as make_perlin
from pyromancy.standard.actor.level.Cell import Cell
from pyromancy.standard.actor.level.HexaGrid import HexaGrid


__author__ = 'Gecko'


class HexaMap(ActorGroup):
    def __init__(self, scene, (w, h, d, thickness), (cell_w, cell_h, edge_len)):
        super(HexaMap, self).__init__("hexamap")

        self.__scene = scene
        self.__create_extended_sprite = self.__scene.root.find("sprite_factory").create_extended_zsprite

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
    def heightmap(self):
        return self.__heightmap

    @property
    def map_depth(self):
        return self.__map_depth

    @property
    def map_width(self):
        return self.__map_width

    @property
    def map_height(self):
        return self.__map_height

    @property
    def thickness(self):
        return self.__thickness

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

        # create the cells
        grid = []
        for x in range(0, w):
            for y in range(0, h):
                d_range = range(0, self.__thickness)
                d_range += range(self.__thickness, self.__thickness + self.__heightmap[x + y * w], 1)
                # a vertical stack of cells
                carotte = []
                for z in d_range:
                    new_name = HexaMap.make_cell_name(x, y, z)
                    new_cell = Cell(new_name, x, y, z, None)
                    carotte.append(new_cell)
                grid.extend(carotte)

        hexagrid = HexaGrid(grid)
        self.add_child(hexagrid)

    def iso_to_screenspace_coords(self, x, y, z):
        # horizontal coord
        x2 = x * self.__t
        #vertical coord with a shift for the odd columns
        k = y * self.__q + (self.__edge_length - 1) * z
        y2 = k if (x % 2 == 0) else k - self.__q * 0.5

        return x2, y2

    def screenpace_to_iso_coords(self, x, y):

        x2 = 0
        y2 = 0
        z2 = 0

        return x2, y2, z2

    def add_cell(self, x, y, z):
        new_name = HexaMap.make_cell_name(x, y, z)
        hexagrid = self.get_child("hexagrid")
        cell = hexagrid.get_child(new_name)
        if cell is None:
            new_name = HexaMap.make_cell_name(x, y, z)
            cell = Cell(new_name, x, y, z, None)
            hexagrid.add_child(cell)
        return cell

    @staticmethod
    def make_cell_name(x, y, z):
        return "cell[%i,%i,%i]" % (x, y, z)
