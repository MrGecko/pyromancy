from pyglet.gl import glTranslatef

from pyromancy.core.actor.ActorGroup import ActorGroup


__author__ = 'MrGecko'

from pyromancy.core.actor.Actor import Actor
from pyromancy.standard.actor.physic.position_actor import PositionActor


class MeshActor(ActorGroup):
    SHOW = "SHOW"
    HIDE = "HIDE"

    def __init__(self, name, mesh, position):
        super(MeshActor, self).__init__(name, [position, ])

        self.__mesh = mesh
        self.__mesh.set_transform(self.__transform)

        self.register(PositionActor.MOVE, self.__move)
        self.register(PositionActor.MOVE_TO, self.__move_to)
        # self.register(Actor.ACTOR_ADDED, self.__object_added)

        self.send(Actor.ACTOR_ENABLED)

    @property
    def mesh(self):
        return self.__mesh

    def __transform(self):
        pos = self.get_child("position")
        glTranslatef(pos.x, pos.y, pos.z)
        print self.name, pos.x, pos.y, pos.z

    def __move(self, sender, kargs):
        # self.__sprite.set_relative_position(kargs["dx"], kargs["dy"], kargs["dz"])
        return True

    def __move_to(self, sender, kargs):
        # self.__sprite.set_absolute_position(kargs["x"], kargs["y"], kargs["z"])
        return True

    def __object_added(self, sender, kargs):
        self.parent.send(PositionActor.REFRESH)


