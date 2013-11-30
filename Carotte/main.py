import pyglet
from pyromancy.core.egg import Egg
from scene.main_scene import MainScene


__author__ = 'Gecko'




class Application(Egg):
    def __init__(self):
        super(Application, self).__init__(960, 600)
        self.background_color = (8 / 255.0, 8 / 255.0, 8 / 255.0, 255)

        scene = MainScene(self)
        self.register_scene(scene)
        scene.start()


if __name__ == '__main__':
    application = Application()
    #cProfile.run('application = Application()', 'restats')
    #p = pstats.Stats('restats')
    #p.sort_stats('cumulative').print_stats(15)

    pyglet.app.run()
    #cProfile.run('pyglet.app.run()', 'restats')
    #p = pstats.Stats('restats')
    #p.sort_stats('time').print_stats(15)
