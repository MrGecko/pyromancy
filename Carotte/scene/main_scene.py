from pyromancy.core.scene.scene import Scene
from init_gamestate import InitGameState
from play_gamestate import PlayGameState
from Carotte.scene.evolve_state import EvolveGameState

__author__ = 'Gecko'


class MainScene(Scene):
    def __init__(self, egg):
        super(MainScene, self).__init__()
        batch_manager = self.root.find("batch_manager")

        batch_manager.add_batch("main")
        batch_manager.select_batch("main")

        hud_batch_manager = self.root.find("hud_batch_manager")
        hud_batch_manager.add_batch("main")
        hud_batch_manager.select_batch("main")

        group_manager = self.root.find("group_manager")
        group_manager.add_group("hexamap")
        group_manager.add_group("game_objects")

        self.load_resources()
        self.egg = egg
        # group_manager.pprint()

    def start(self):
        self.push(InitGameState, self)
        self.push(PlayGameState, self)

    def next_step(self):
        if isinstance(self.current, EvolveGameState):
            self.set(PlayGameState, self)
        elif isinstance(self.current, PlayGameState):
            self.set(EvolveGameState, self)

    def load_resources(self):
        # self.root.find("resource_manager").add_font("media/fonts/Geo/Geo-Regular.ttf")

        load_image = self.root.find("sprite_factory").load_image
        # load_image("media.ui.economy-button", "media/ui/economy-button.png", options={"nbtile_width": 3})
        load_image("media.playerunit.light.sparrow.Rebel", "media/playerunits/rebel-sparrow/light-ship.png")

        load_image("media.terrain.clay_empty.50", "media/terrain/clayhex_empty_50.png")
        load_image("media.terrain.clay", "media/terrain/clayhex.png")
        load_image("media.terrain.clay.light", "media/terrain/clayhex_light.png")


