from pyromancy.core.actor.ActorGroup import ActorGroup
from pyromancy.core.rendering.transform_group import TransformGroup

__author__ = 'MrGecko'


class Mesh(ActorGroup):
    def __init__(self, vertex_count, mode, batch, faces, data, position, group=None):
        super(Mesh, self).__init__("mesh")
        self.__batch = batch
        self.__mode = mode
        self.__group = group
        self.__vertex_list = None
        self.add_child(position)

        self.__vertex_list = batch.add_indexed(vertex_count, mode,
                                               TransformGroup(x=position.x, y=position.x, r=0, order=position.z,
                                                              parent=group),
                                               faces, *data)


    @property
    def vertex_list(self):
        return self.__vertex_list

    def __del__(self):
        self.__vertex_list.delete()
