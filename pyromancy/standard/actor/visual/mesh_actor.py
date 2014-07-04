from pyromancy.core.actor.ActorGroup import ActorGroup


__author__ = 'MrGecko'

from pyromancy.core.actor.Actor import Actor
from pyromancy.standard.actor.physic.position_actor import PositionActor


class MeshActor(ActorGroup):
    SHOW = "SHOW"
    HIDE = "HIDE"

    def __init__(self, name, mesh):
        super(MeshActor, self).__init__(name, [mesh, ])

        self.register(PositionActor.MOVE, self.__move)
        self.register(PositionActor.MOVE_TO, self.__move_to)
        # self.register(Actor.ACTOR_ADDED, self.__object_added)

        self.send(Actor.ACTOR_ENABLED)

    def __move(self, sender, kargs):
        # self.__sprite.set_relative_position(kargs["dx"], kargs["dy"], kargs["dz"])
        return True

    def __move_to(self, sender, kargs):
        # self.__sprite.set_absolute_position(kargs["x"], kargs["y"], kargs["z"])
        return True

    def __object_added(self, sender, kargs):
        self.parent.send(PositionActor.REFRESH)


