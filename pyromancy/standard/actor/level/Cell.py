from core.actor.ActorGroup import ActorGroup
from standard.actor.visual.sprite_actor import SpriteActor

__author__ = 'Gecko'


class Cell(ActorGroup):
    def __init__(self, name, x, y, z, sprite):
        super(Cell, self).__init__(name=name)
        self.x = x
        self.y = y
        self.z = z
        self.data = {"mat": "clay"}  # dummy data
        self.add_child(SpriteActor("%s.sprite" % self.name, sprite))

    def __repr__(self):
        return self.name
