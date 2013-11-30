from random import randint as rdi

from Carotte.terrain.Carotte import Carotte
from pyromancy.core.actor.ActorGroup import ActorGroup
from pyromancy.standard.actor.level.Cell import Cell
from pyromancy.standard.actor.physic.position_actor import PositionActor


__author__ = 'Gecko'


class HexaMap(ActorGroup):

    def __init__(self, sprite_factory, cell_batch, (w, h, d), (cell_w, cell_h, edge_len), (x, y)=(0, 0)):
        super(HexaMap, self).__init__("hexamap")
        self.add_child(PositionActor(x, y))

        self.__t = edge_len + (cell_w - edge_len - 2) * 0.5
        self.__q = cell_h - edge_len
        self.__edge_length = edge_len

        self.__carotte = Carotte(sprite_factory, cell_batch, size=d)

        self.__grid = self.gen_grid(w-1, h-1, d)

    def gen_grid(self, w, h, d):
        #generate the cell coords
        #create the upper part of the map (the upper diagonal starts from the upper left corner)
        d_range = range(0, d, 1)
        layer = 0
        coords = [(0, h, layer)]
        ly = [0]
        for x in range(2, w+2, 2):
            lx = range(x, -1, -1)

            ly.append(ly[-1])
            ly.append(ly[-1] + 1)

            layer += 1
            for i in range(0, len(lx)):
                cy = h - ly[i]
                if cy >= 0:
                    coords.append((lx[i], cy, layer))

        #create the second part (the lower diagonal) of the map
        #it starts from the upper right corner
        q = 0
        for n in range(h, 0, -1):
            x = 0
            layer += 1
            for i in range(1, n+1):
                coords.append((w - x, h - i - q, layer))
                if w - x - 1 <= 0:
                    break
                coords.append((w - x - 1, h - i - q, layer))
                x += 2
            q += 1

        #create the cells
        grid = []
        for cx, cy, layer in coords:
            d_range = range(1, rdi(8, 9), 1)
            carotte = [self.__create_cell_from_carotte(self.__carotte, cx, cy, z, layer) for z in d_range]
            grid.extend(carotte)

        return grid

    def __get_cell_iso_coords(self, x, y, z):
        #horizontal coord
        x2 = x * self.__t
        #vertical coord with a shift for the odd columns
        k = y * self.__q + (self.__edge_length - 1) * z
        y2 = k if (x % 2 == 0) else k - self.__q * 0.5
        #position offset for the map itself
        pos = self.get_child("position")
        return pos.x + x2, pos.y + y2


    def __create_cell_from_carotte(self, carotte, x, y, z, layer):

        iso = self.__get_cell_iso_coords(x, y, z)

        sprite = carotte.get_cell_sprite(x, y, z, layer)
        sprite.x = iso[0]
        sprite.y = iso[1]

        new_cell = Cell(x, y, z, sprite)

        #new_cell.add_children([
        #    PositionActor(iso[0], iso[1], relative_actor=self),
        #    SpriteActor("sprite", sprite)
        #])

        return new_cell

