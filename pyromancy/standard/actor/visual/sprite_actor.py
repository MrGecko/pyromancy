from pyromancy.core.actor.Actor import Actor
from pyromancy.standard.actor.physic.position_actor import PositionActor

__author__ = 'Gecko'


class SpriteActor(Actor):
    SHOW = "SHOW"
    HIDE = "HIDE"

    def __init__(self, name, sprite):
        super(SpriteActor, self).__init__(name)
        assert sprite is not None
        self.__sprite = sprite
        self.register(PositionActor.MOVE, self.__move)
        self.register(PositionActor.MOVE_TO, self.__move_to)
        self.register(Actor.ACTOR_ADDED, self.__object_added)

        self.send(Actor.ACTOR_ENABLED)

    @property
    def sprite(self):
        return self.__sprite

    def __move(self, sender, kargs):
        self.__sprite.set_relative_position(kargs["dx"], kargs["dy"])
        return True

    def __move_to(self, sender, kargs):
        self.__sprite.set_absolute_position(kargs["x"], kargs["y"])
        return True

    def __object_enabled(self, sender, arguments):
        self.parent.send(SpriteActor.SHOW)

    def __object_disabled(self, sender, kargs):
        self.parent.send(SpriteActor.HIDE)

    def __object_added(self, sender, kargs):
        self.parent.send(PositionActor.REFRESH)
