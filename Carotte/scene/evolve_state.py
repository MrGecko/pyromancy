from Carotte.scene.play_gamestate import PlayGameState
from pyromancy.standard.actor.physic.position_actor import PositionActor

__author__ = 'Gecko'

from random import choice


class EvolveGameState(PlayGameState):
    def __init__(self, scene):
        super(EvolveGameState, self).__init__(scene, 0)
        hexamap = self.scene.root.find("hexamap")
        if hexamap:
            random_cell = choice(hexamap.get_child("hexagrid").get_active_children())
            neighborhood = hexamap.get_eight_neighborhood(random_cell.x, random_cell.y, random_cell.z)
            # print "random cell: %s" % random_cell
            # print "neighborhood: ", neighborhood

        self.scene.root.find("ship").send(PositionActor.MOVE, {"dx": 10, "dy": 5})



