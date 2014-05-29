from core.actor.ActorGroup import ActorGroup

__author__ = 'Gecko'


class Cell(ActorGroup):
    
    def __init__(self, x, y, z, sprite):
        super(Cell, self).__init__(name="cell[%i,%i,%i]" % (x, y, z))
        self.x = x
        self.y = y
        self.z = z
        self.data = {"mat": "clay"}  # dummy data
        self.__sprite = sprite

        # @property
        #def x(self):
        #    return self.__x
        #
        #@property
        #def y(self):
        #    return self.__y
        #
        #@property
        #def z(self):
        #    return self.__z
        #
        #@property
        #def data(self):
        #    return self.__data