from pyromancy.core.actor.Actor import Actor

__author__ = 'MrGecko'


class Mesh(Actor):
    def __init__(self, vertex_count, mode, batch, faces, data, group=None):
        super(Mesh, self).__init__(name="mesh")
        self.__vertex_list = batch.add_indexed(vertex_count, mode, group, faces, *data)

    @property
    def vertex_list(self):
        return self.__vertex_list

    def __del__(self):
        self.__vertex_list.delete()
        super(Mesh, self).__del__()

