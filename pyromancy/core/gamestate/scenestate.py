from pyromancy.core.gamestate.state import TimeLockedState


class SceneState(TimeLockedState):
    def __init__(self, scene, lock=0):
        super(SceneState, self).__init__(lock)
        self.__scene = scene
        self.__hud_batches = []
        self.__batch_manager = self.__scene.root.find("batch_manager")
        self.__hud_batch_manager = self.__scene.root.find("hud_batch_manager")

    @property
    def scene(self):
        return self.__scene


    @property
    def batch_manager(self):
        return self.__batch_manager

    @property
    def hud_batch_manager(self):
        return self.__hud_batch_manager

    def draw(self):
        for batch in self.__batch_manager.batches:
            batch.draw()
            pass

    def draw_head_display(self):
        for batch in self.__hud_batch_manager.batches:
            batch.draw()

    def update(self, dt):
        super(SceneState, self).update(dt)

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    def on_mouse_release(self, x, y, button, modifiers):
        pass

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass

    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def process_keyboard(self, handler, dt):
        pass


