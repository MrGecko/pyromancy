from core.actor.ActorGroup import ActorGroup
from standard.actor.visual.sprite_actor import SpriteActor

__author__ = 'Gecko'


class Cell(ActorGroup):
    
    def __init__(self, x, y, z, sprite):
        super(Cell, self).__init__(name="cell[%i,%i,%i]" % (x, y, z))
        self.x = x
        self.y = y
        self.z = z
        self.data = {"mat": "clay"}  # dummy data
        self.add_child(SpriteActor("%s.sprite" % self.name, sprite))
