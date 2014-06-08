from pyromancy.core.actor.Actor import Actor
from pyromancy.standard.rect import Rect

__author__ = 'MrGecko'


class CollisionNineRect(Actor):
    def __init__(self, name, bottomleft, bottomright, topright, topleft):
        super(CollisionNineRect, self).__init__(name)

        self.__bottomleft = Rect(*bottomleft)
        self.__bottomright = Rect(*bottomright)
        self.__topright = Rect(*topright)
        self.__topleft = Rect(*topleft)

        self.__midbottom = Rect(self.__bottomleft.right,
                                self.__bottomleft.bottom,
                                self.__bottomright.left - self.__bottomleft.right,
                                self.bottomleft.height)

        self.__midleft = Rect(self.__bottomleft.left,
                              self.__bottomleft.top,
                              self.__bottomleft.width,
                              self.__topleft.bottom - self.__bottomleft.top)

        self.__midcenter = Rect(self.__bottomleft.right,
                                self.__bottomleft.top,
                                self.__bottomright.left - self.__bottomleft.right,
                                self.__topleft.bottom - self.__bottomleft.top)

        self.__midright = Rect(self.__midcenter.width,
                               self.__midcenter.bottom,
                               self.__bottomright.right - self.__midcenter.right,
                               self.__topright.bottom - self.__bottomright.top)

        self.__midtop = Rect(self.__bottomleft.bottomright,
                             self.__midcenter.top,
                             self.__topright.left - self.__topleft.right,
                             self.__topright.top - self.__midcenter.top)

    @property
    def bottomleft(self):
        return self.__bottomleft

    @property
    def bottomright(self):
        return self.__bottomright

    @property
    def topright(self):
        return self.__topright

    @property
    def topleft(self):
        return self.__topleft


    @property
    def midbottom(self):
        return self.__midbottom

    @property
    def midleft(self):
        return self.__midleft

    @property
    def midcenter(self):
        return self.__midcenter

    @property
    def midright(self):
        return self.__midright

    @property
    def midtop(self):
        return self.__midtop