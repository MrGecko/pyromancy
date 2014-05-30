from Carotte.scene.play_gamestate import PlayGameState

__author__ = 'Gecko'

from random import choice


class EvolveGameState(PlayGameState):
    def __init__(self, scene):
        super(EvolveGameState, self).__init__(scene, 2)
        hexamap = self.scene.root.find("hexamap")
        if hexamap:
            random_cell = choice(hexamap.get_child("hexagrid").get_active_children())
            neighborhood = hexamap.get_eight_neighborhood(random_cell.x, random_cell.y, random_cell.z)
            # print "random cell: %s" % random_cell
            # print "neighborhood: ", neighborhood


