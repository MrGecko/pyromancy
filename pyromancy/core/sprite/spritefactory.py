from pyromancy.core.actor.Actor import Actor

from pyromancy.core.sprite.exsprite import ExSprite, ZExSprite


class SpriteFactory(Actor):
        
    def __init__(self, name, scene):
        super(SpriteFactory, self).__init__(name)
        self.__scene = scene
        self.__symbols = {}
        #self.__sprites = {}
        #self.reset()
        self.__group_manager = self.__scene.root.find("group_manager")

    def reset(self):
        self.__symbols = {}

    def load_image(self, name, filename, options=None):
        if not options:
            options = {}
        if name not in self.__symbols:
            self.__symbols[name] = self.__scene.root.find("resource_manager").load_image(filename, options)
        return self.__symbols[name]

    def create_extended_sprite(self, symbol, **kargs):
        return self.create_sprite(ExSprite, symbol, **kargs)

    def create_extended_zsprite(self, symbol, **kargs):
        return self.create_sprite(ZExSprite, symbol, **kargs)

    def create_sprite(self, sprite_impl, symbol, **kargs):

        if isinstance(symbol, basestring):
            #if symbol in self.__sprites:
            #    return self.__sprites[symbol]
            if symbol not in self.__symbols:
                print "[Warning SpriteFactory] symbol '%s' does not exist" % symbol
                return None
            tileset = self.__symbols[symbol]
        else:
            tileset = symbol

        if not "layer" in kargs:
            raise KeyError("[Error SpriteFactory] You should provide a layer name for this sprite")

        kargs["group"] = self.__group_manager.add_group(kargs["layer"])
        del kargs["layer"]

        if not "batch" in kargs or kargs["batch"] is None:
            raise ValueError("[Error SpriteFactory] You should provide a valid value for the 'Batch' argument")

        new_sprite = sprite_impl(tileset, **kargs)
        #self.__sprites[symbol] = new_sprite
        return new_sprite
        









