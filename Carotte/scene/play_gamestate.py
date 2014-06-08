from random import choice

from pyglet.window import key

from pyromancy.core.gamestate.scenestate import SceneState
from pyromancy.standard.actor.physic.position_actor import PositionActor

__author__ = 'Gecko'


class PlayGameState(SceneState):
    def __init__(self, scene, lock=0.5):
        super(PlayGameState, self).__init__(scene, lock)

    def process_keyboard(self, handler, dt):
        self.process_camera(handler, dt)

        if handler[key.SPACE]:
            hexamap = self.scene.root.find("hexamap")
            if hexamap:
                hexamap.gen_grid()
                self.scene.root.find("geologist").initialize()

        if handler[key.H]:
            hexamap = self.scene.root.find("hexamap")
            if hexamap:
                random_cell = choice(hexamap.get_child("hexagrid").get_active_children())
                # print random_cell,
                new_cell = hexamap.add_cell(random_cell.x, random_cell.y, random_cell.z + 1)
                self.scene.root.find("geologist").identify(new_cell)
                print new_cell

        if handler[key.E]:
            hexamap = self.scene.root.find("hexamap")
            if hexamap:
                hexagrid = hexamap.get_child("hexagrid")
                random_cell = choice(hexagrid.get_active_children())
                neighborhood = hexamap.get_eight_neighborhood(random_cell.x, random_cell.y, random_cell.z)
                print "random cell: %s" % random_cell
                print "neighborhood: ", neighborhood

        if handler[key.F]:
            moeb = self.scene.root.find("moeb")
            moeb.send(PositionActor.MOVE_TO, {"x": 50, "y": 50})

        dx = 0
        dy = 0
        if handler[key.RIGHT]:
            dx += 1.0
        if handler[key.LEFT]:
            dx += -1.0
        if handler[key.UP]:
            dy += 1.0
        if handler[key.DOWN]:
            dy += -1.0

        if dx != 0 or dy != 0:
            moeb = self.scene.root.find("moeb")
            hexamap = self.scene.root.find("hexamap")
            moeb.send(PositionActor.MOVE, {"dx": dx, "dy": dy})
            hexamap.get_obj_layer(moeb)

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

        camera_dx = camera_dx * mvt_step * dt
        camera_dy = camera_dy * mvt_step * dt

        camera = self.scene.root.find("main_camera")
        if camera:
            camera.target.x += camera_dx
            camera.target.y += camera_dy

    def update(self, dt):
        super(PlayGameState, self).update(dt)

        # moebs = self.scene.root.find("moebs").get_active_children()
        #hexamap = self.scene.root.find("hexamap")
        #for moeb in moebs:
        #    moeb.send(PositionActor.MOVE, {"dx": 0.18, "dy": 0.04})
        #    pos = moeb.get_child("position")
        #    cell = hexamap.get_cell_from_screenspace_coords(pos.x, pos.y, pos.z)
        #    if cell:
        #        test = hexamap.get_obj_layer(moeb)
        #        new_z = cell.get_child("sprite").sprite.z
        #        pos.send(PositionActor.MOVE_TO, {"z": new_z})

        if not self.locked:
            self.scene.next_step()
