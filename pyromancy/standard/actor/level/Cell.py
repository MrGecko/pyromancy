__author__ = 'Gecko'



class Cell(object):
    
    def __init__(self, x, y, z, sprite):
        #super(Cell, self).__init__(name)
        self.__x = x
        self.__y = y
        self.__z = z
        self.__data = {"mat": "clay"}
        self.__sprite = sprite

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def z(self):
        return self.__z

    @property
    def data(self):
        return self.__data