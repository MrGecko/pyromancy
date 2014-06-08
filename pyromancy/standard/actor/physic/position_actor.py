from pyromancy.core.actor.Actor import Actor
from pyromancy.core.actor.ActorGroup import ActorGroup

__author__ = 'Gecko'


class PositionActor(ActorGroup):

    MOVE_TO = "MOVE_TO"
    MOVE = "MOVE"
    IDLE = "IDLE"
    REFRESH = "REFRESH"

    def __init__(self, x, y, z=0, relative_actor=None):
        super(PositionActor, self).__init__("position")
        self.send(Actor.ACTOR_ENABLED)
        self.register(PositionActor.MOVE_TO, self.__move_to)
        self.register(PositionActor.MOVE, self.__move)
        self.register(PositionActor.REFRESH, self.__refresh)
        self.__x = 0
        self.__y = 0
        self.__z = 0
        self.__relative_actor = relative_actor
        self.send(PositionActor.MOVE, {"dx": x, "dy": y, "dz": z})

    @property
    def x(self):
        return self.__x
    @property
    def y(self):
        return self.__y

    @property
    def z(self):
        return self.__z

    def __move_to(self, sender, kargs):
        if sender is not None:
            dx = kargs["x"] - self.__x
            dy = kargs["y"] - self.__y
            dz = kargs["z"] - self.__z
            if dx != 0 or dy != 0 or dz != 0:
                sender.send(PositionActor.MOVE, {"dx": dx, "dy": dy, "dz": dz})
                # else:
                #    sender.send(PositionActor.IDLE, {})

        return False

    def __move(self, sender, kargs):
        if self.__relative_actor is not None:
            rel_pos = self.__relative_actor.get_child("position")
            if rel_pos is not None:
                self.__x = rel_pos.x + kargs["dx"]
                self.__y = rel_pos.y + kargs["dy"]
                self.__z = rel_pos.z + kargs["dz"]
            else:
                self.__x += kargs["dx"]
                self.__y += kargs["dy"]
                self.__z += kargs["dz"]
        else:
            self.__x += kargs["dx"]
            self.__y += kargs["dy"]
            self.__z += kargs["dz"]
        return True

    def __refresh(self, sender, kargs):
        if sender is not None:
            sender.send(PositionActor.MOVE_TO, {"x": self.__x, "y": self.__y, "z": self.__z})
        return True
