from random import randint as rdi

from pyromancy.core.gamestate.scenestate import SceneState
from pyromancy.standard.actor.level.HexaMap import HexaMap
from pyromancy.standard.actor.visual.sprite_actor import SpriteActor
from pyromancy.standard.actor.physic.position_actor import PositionActor
from pyromancy.core.actor.ActorGroup import ActorGroup
from Carotte.scene.geologist import Geologist


__author__ = 'Gecko'


class InitGameState(SceneState):

    def __init__(self, scene):
        super(InitGameState, self).__init__(scene)
        self.__game_objects = self.scene.root.find("game_objects")
        self.__sprite_factory = self.scene.root.find("sprite_factory")

        self.init_map()
        self.init_actors()

    def init_actors(self):
        # ship_sprite = self.__sprite_factory.create_extended_sprite(
        #    "media.playerunit.light.sparrow.Rebel", layer="game_objects", batch=self.batch_manager.current_batch
        #)
        #ship_actor = ActorGroup("ship", [PositionActor(500, 400), SpriteActor("rebel01", ship_sprite)])
        #
        #ship_weapon_sprite = self.__sprite_factory.create_extended_sprite(
        #    "media.playerunit.light.sparrow.Rebel", layer="game_objects", batch=self.batch_manager.current_batch
        #)
        #ship_weapon = ActorGroup("ship_weapon",
        #                         [PositionActor(20, 10, ship_actor), SpriteActor("rebel02", ship_weapon_sprite)])
        #ship_actor.add_child(ship_weapon)
        #self.__game_objects.add_child(ship_actor)
        moebs = ActorGroup("moebs")
        for i in range(0, 200):
            moeb_sprite = self.__sprite_factory.create_extended_zsprite(
                "media.character.moeb",
                layer="moebs",
                batch=self.batch_manager.current_batch,
                start_frame=0
            )
            moeb_sprite.set_animation([1, 2, 3, 4], 0.18)

            moeb_actor = ActorGroup("moeb%i" % i, [PositionActor(rdi(200, 2000), rdi(100, 1000), 100),
                                                   SpriteActor("moeb_sprite%i" % i, moeb_sprite)])

            moebs.add_child(moeb_actor)
        self.__game_objects.add_child(moebs)

    def init_map(self):
        # create the hexamap
        hexamap = HexaMap(self.scene, (51, 31, 4, 1), (59, 59, 25))
        self.scene.root.find("game_objects").add_child(hexamap)
        hexamap.gen_grid()

        # initialiaze geology
        self.scene.root.add_child(Geologist(self.scene))
        geologist = self.scene.root.find("geologist")
        geologist.initialize()
        geologist.pprint_minerals()

        #initialize camera position
        camera = self.scene.root.find("main_camera")
        camera.target.x = hexamap.width_in_pixels / 3 + hexamap.cell_width / 2
        camera.target.y = hexamap.height_in_pixels / 3 + hexamap.cell_height / 2





