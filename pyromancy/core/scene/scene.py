"""
Created on 9 avr. 2012

@author: Gecko
"""
import pyglet

from pyromancy.core.actor.ActorGroup import ActorGroup
from pyromancy.core.gamestate.manager import StateManager
from pyromancy.core.mesh.mesh_factory import MeshFactory
from pyromancy.core.rendering.batch_manager import BatchManager
from pyromancy.core.rendering.group_manager import GroupManager
from pyromancy.core.resource.resource_manager import ResourceManager
from pyromancy.core.sprite.spritefactory import SpriteFactory


class Scene(StateManager):
    
    def __init__(self):
        super(Scene, self).__init__()
        self.__fps_clock = pyglet.clock.ClockDisplay()
        self.__show_fps = False
        self.__root = ActorGroup("root")
        self.__root.add_child(GroupManager("group_manager"))
        self.__root.add_child(SpriteFactory("sprite_factory", self))
        self.__root.add_child(MeshFactory("mesh_factory", self))
        self.__root.add_child(ResourceManager("resource_manager"))
        self.__root.add_child(BatchManager("batch_manager"))
        self.__root.add_child(BatchManager("hud_batch_manager"))
        self.__root.add_child(ActorGroup("game_objects"))
        self.__root.add_child(ActorGroup("hud"))

    @property
    def root(self):
        return self.__root

    def on_mouse_press(self, x, y, button, modifiers):
        if not self.empty:
            self.current.on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        if not self.empty:
            self.current.on_mouse_release(x, y, button, modifiers)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if not self.empty:
            self.current.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        if not self.empty:
            self.current.on_mouse_motion(x, y, dx, dy)
            
    def process_keyboard(self, handler, dt):
        if not self.empty:
            self.current.process_keyboard(handler, dt)

    def draw(self):
        if not self.empty:
            self.current.draw()

    def draw_head_display(self):
        if self.__show_fps:
            self.__fps_clock.draw()
        if not self.empty:
            self.current.draw_head_display()
            
    def update(self, dt):
        super(Scene, self).update(dt)
        self.__root.update(dt)

    def start(self):
        pass

