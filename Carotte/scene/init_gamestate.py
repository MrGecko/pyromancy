from pyromancy.core.actor.ActorGroup import ActorGroup
from pyromancy.core.gamestate.scenestate import SceneState
from pyromancy.standard.actor.physic.position_actor import PositionActor
from pyromancy.standard.actor.visual.sprite_actor import SpriteActor

from pyromancy.standard.actor.level.HexaMap import HexaMap

__author__ = 'Gecko'




class InitGameState(SceneState):

    def __init__(self, scene):
        super(InitGameState, self).__init__(scene, 0)
        self.__game_objects = self.scene.root.find("game_objects")
        self.__sprite_factory = self.scene.root.find("sprite_factory")
        self.init_map()
        self.init_actors()


    def init_actors(self):
        ship_sprite = self.__sprite_factory.create_extended_sprite(
            "media.playerunit.light.sparrow.Rebel", layer="ship", batch=self.batch_manager.current_batch

        )
        ship_actor = ActorGroup("ship", [PositionActor(500, 400), SpriteActor("rebel01", ship_sprite)])

        ship_weapon_sprite = self.__sprite_factory.create_extended_sprite(
            "media.playerunit.light.sparrow.Rebel", layer="ship", batch=self.batch_manager.current_batch
        )
        ship_weapon = ActorGroup("ship_weapon", [PositionActor(20, 10, ship_actor), SpriteActor("rebel02", ship_weapon_sprite)])
        ship_actor.add_child(ship_weapon)

        self.__game_objects.add_child(ship_actor)


    def init_map(self):
        hexamap = HexaMap(self.__sprite_factory, self.batch_manager.current_batch, (61, 61, 5, 10), (59, 59, 25))
        self.__game_objects.add_child(hexamap)


    def pause(self):
        print "Init... done"


