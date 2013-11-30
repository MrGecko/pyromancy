__author__ = 'Gecko'



class Carotte(object):

    def __init__(self, sprite_factory, batch, size):
        self.__batch = batch
        self.__create_extended_sprite = sprite_factory.create_extended_sprite

    def get_cell_sprite(self, x, y, z, layer):

        new_sprite = self.__create_extended_sprite(
            symbol="media.terrain.clay",
            layer=layer,
            batch=self.__batch
        )
        return new_sprite


    def get_carotte_from_coord_list(self, cell_data):
        sprites = []
        i = 0
        for x, y, z, layer in cell_data:
            #ex: if cell_data[i+1] is None
            #       new_sprite = "media.terrain.clay.shadowed"
            #
            new_sprite = self.__create_extended_sprite(
                symbol="media.terrain.clay",
                layer=layer,
                batch=self.__batch
            )
            sprites.append(new_sprite)
            i += 1
        return sprites

