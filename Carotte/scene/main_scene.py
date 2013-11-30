from pyromancy.core.scene.scene import Scene
from init_gamestate import InitGameState
from play_gamestate import PlayGameState

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
        group_manager.add_group("background", -1)
        group_manager.add_group("hud.button")

        self.load_resources()
        self.egg = egg

        self.push(InitGameState, self)
        self.push(PlayGameState, self)

    def load_resources(self):
        self.root.find("resource_manager").add_font("media/fonts/Geo/Geo-Regular.ttf")

        load_image = self.root.find("sprite_factory").load_image
        load_image("media.ui.economy-button", "media/ui/economy-button.png", options={"nbtile_width": 3})
        load_image("media.playerunit.light.sparrow.Rebel", "media/playerunits/rebel-sparrow/light-ship.png")
        load_image("media.terrain.clay", "media/terrain/clayhex.png")

