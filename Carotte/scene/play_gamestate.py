from pyglet.window import key

from pyromancy.core.gamestate.scenestate import SceneState


__author__ = 'Gecko'


class PlayGameState(SceneState):

    def __init__(self, scene):
        super(PlayGameState, self).__init__(scene, 5)

    def process_keyboard(self, handler, dt):
        self.process_camera(handler, dt)
        if handler[key.T]:
            print "hello, i'm the PlayGameState scene state (dt: %s)" % dt

    def process_camera(self, handler, dt):
        mvt_step = 800
        camera_dx = 0
        camera_dy = 0
        if handler[key.D]:
            camera_dx = 1
        if handler[key.A] or handler[key.Q]:
            camera_dx = -1
        if handler[key.S]:
            camera_dy = -1
        if handler[key.W] or handler[key.Z]:
            camera_dy = 1

        if handler[key.SPACE]:
            # self.scene.root.find("ship").send(PositionActor.MOVE, {"dx": 10, "dy": 5})
            hexamap = self.scene.root.find("hexamap")
            hexamap.gen_grid()


        if handler[key.H]:
            # self.scene.root.find("ship_weapon").send(PositionActor.MOVE, {"dx": 10, "dy": 5})
            pass

        camera_dx = camera_dx * mvt_step * dt
        camera_dy = camera_dy * mvt_step * dt

        camera = self.scene.root.find("main_camera")
        camera.target.x += camera_dx
        camera.target.y += camera_dy

    def clean_up(self):
        for obj in self.scene.root.find("game_objects").get_children():
            del obj
        print "Goodbye !"