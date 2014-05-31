from pyromancy.core.gamestate.scenestate import SceneState
from pyromancy.standard.actor.level.HexaMap import HexaMap
from pyromancy.standard.actor.visual.sprite_actor import SpriteActor
from pyromancy.standard.actor.physic.position_actor import PositionActor

from core.actor.ActorGroup import ActorGroup

__author__ = 'Gecko'


class InitGameState(SceneState):

    def __init__(self, scene):
        super(InitGameState, self).__init__(scene)
        self.__game_objects = self.scene.root.find("game_objects")
        self.__sprite_factory = self.scene.root.find("sprite_factory")
        self.init_actors()
        self.init_map()


    def init_actors(self):
        ship_sprite = self.__sprite_factory.create_extended_sprite(
            "media.playerunit.light.sparrow.Rebel", layer="game_objects", batch=self.batch_manager.current_batch
        )
        ship_actor = ActorGroup("ship", [PositionActor(500, 400), SpriteActor("rebel01", ship_sprite)])

        ship_weapon_sprite = self.__sprite_factory.create_extended_sprite(
            "media.playerunit.light.sparrow.Rebel", layer="game_objects", batch=self.batch_manager.current_batch
        )
        ship_weapon = ActorGroup("ship_weapon",
                                 [PositionActor(20, 10, ship_actor), SpriteActor("rebel02", ship_weapon_sprite)])
        ship_actor.add_child(ship_weapon)
        self.__game_objects.add_child(ship_actor)

    def init_map(self):
        hexamap = HexaMap(self.__sprite_factory, self.batch_manager.current_batch,
                          (100, 17, 5, 1), (59, 59, 25))

        self.scene.root.find("game_objects").add_child(hexamap)
        hexamap.gen_grid()

        camera = self.scene.root.find("main_camera")
        camera.target.x = hexamap.width_in_pixels / 3 + hexamap.cell_width / 2
        camera.target.y = hexamap.height_in_pixels / 3 + hexamap.cell_height / 2




