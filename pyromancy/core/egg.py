import pyglet
from pyglet.window import Window, key
from pyglet.gl import glClearColor
from pyglet.gl import glTexParameteri, GL_TEXTURE_MAG_FILTER, GL_TEXTURE_2D, GL_NEAREST, GL_TEXTURE_MIN_FILTER

from pyromancy.core.scene.camera import Camera


class Egg(object):
    def __init__(self, width, height):
        # display initializations
        self.__window = Window(width, height, vsync=True)
        self.__background_color = (0, 0, 0, 1.0)
        # self._fps_display = pyglet.clock.ClockDisplay()
        self.__key_state_handler = key.KeyStateHandler()
        self.__scene = None
        self.__window.event(self.on_draw)
        self.__window.push_handlers(self.__key_state_handler)
        self.__camera = None
        #schedule regular updates
        pyglet.clock.schedule_interval(self.update, 1 / 100.0)

    @property
    def window(self):
        return self.__window

    @property
    def background_color(self):
        return self.__background_color

    @background_color.setter
    def background_color(self, value):
        self.__background_color = value

    def register_scene(self, scene):
        self.__scene = scene
        self.__camera = Camera("main_camera", (0, 0), self.__window.height / 2.)
        self.__scene.root.add_child(self.__camera)
        self.__camera.target.x = self.__window.width / 2.
        self.__camera.target.y = self.__window.height / 2.
        self.__window.event(self.__scene.on_mouse_press)
        self.__window.event(self.__scene.on_mouse_release)
        self.__window.event(self.__scene.on_mouse_drag)
        self.__window.event(self.__scene.on_mouse_motion)


    def on_draw(self):
        self.__window.clear()
        glClearColor(*self.__background_color)
        if self.__scene is not None:
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

            # draw batches
            self.__camera.focus(self.__window.width, self.__window.height)
            self.__scene.draw()
            # draw specific batches for the hud
            self.__camera.hud_mode(self.__window.width, self.__window.height)
            self.__scene.draw_head_display()

    def update(self, dt):
        if self.__scene is not None:
            self.__scene.update(dt)
            self.__scene.process_keyboard(self.__key_state_handler, dt)
            self.__camera.update(dt)



