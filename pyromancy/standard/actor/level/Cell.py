from pyromancy.core.actor.ActorGroup import ActorGroup


__author__ = 'Gecko'


class Cell(ActorGroup):
    def __init__(self, name, x, y, z):
        super(Cell, self).__init__(name=name)
        self.x = x
        self.y = y
        self.z = z
        self.data = {
            "material": "normal_clay",
            "minerals": {}
        }  # dummy data

    def has_mineral(self, name):
        return name in [self.data["minerals"]]

    def __repr__(self):
        return self.name
