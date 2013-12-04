__author__ = 'Gecko'



class Carotte(object):

    TEXTURES = {
        "common": "media.terrain.clay",
        "top": "media.terrain.clay.light"
    }


    def __init__(self, w, h, d, thickness, sprite_factory, batch, texture_maps):
        self.__batch = batch
        self.__create_extended_sprite = sprite_factory.create_extended_sprite
        self.__texture_maps = texture_maps
        self.__w = w
        self.__h = h
        self.__d = d
        self.__thickness = thickness

    def get_cell_sprite(self, x, y, z, layer):
        #TODO:a nettoyer
        symbol = "common"
        if z >= self.__thickness:
            lvl = self.__texture_maps[-1][1][x + y*self.__w]
            if lvl >= self.__d * 0.55:
                symbol = "top"

        new_sprite = self.__create_extended_sprite(
            symbol=Carotte.TEXTURES[symbol],
            layer=layer,
            batch=self.__batch
        )
        return new_sprite


    #def get_carotte_from_coord_list(self, cell_data):
    #    sprites = []
    #    i = 0
    #    for x, y, z, layer in cell_data:
    #        #ex: if cell_data[i+1] is None
    #        #       new_sprite = "media.terrain.clay.shadowed"
    #        #
    #        new_sprite = self.__create_extended_sprite(
    #            symbol="media.terrain.clay",
    #            layer=layer,
    #            batch=self.__batch
    #        )
    #        sprites.append(new_sprite)
    #        i += 1
    #    return sprites

