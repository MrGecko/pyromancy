from pyromancy.core.rendering.transform_group import TransformGroup

__author__ = 'MrGecko'


class Mesh(object):
    def __init__(self, vertex_count, mode, batch, faces, data, group=None):
        self.__batch = batch
        self.__mode = mode
        self.__group = group
        self.__vertex_list = batch.add_indexed(vertex_count, mode, TransformGroup(group, lambda: None), faces, *data)


    @property
    def vertex_list(self):
        return self.__vertex_list

    def __del__(self):
        self.__vertex_list.delete()

    def set_transform(self, func):
        self.__batch.migrate(self.__vertex_list,
                             self.__mode,
                             TransformGroup(self.__group, func),
                             self.__batch)
