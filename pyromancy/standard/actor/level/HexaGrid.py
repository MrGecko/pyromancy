__author__ = 'Gecko'

from pyromancy.core.actor.ActorGroup import ActorGroup


class HexaGrid(ActorGroup):
    def __init__(self, cells):
        super(HexaGrid, self).__init__("hexagrid")

        self.add_children(cells)
