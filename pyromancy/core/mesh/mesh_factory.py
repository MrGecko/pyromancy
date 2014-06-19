from pyromancy.core.mesh.mesh import Mesh

__author__ = 'MrGecko'

from pyromancy.core.actor.Actor import Actor


class MeshFactory(Actor):
    def __init__(self, name, scene):
        super(MeshFactory, self).__init__(name)
        self.__scene = scene
        self.__symbols = {}
        # self.reset()
        self.__group_manager = self.__scene.root.find("group_manager")

    def reset(self):
        self.__symbols = {}

    def load_mesh_data(self, name, data, options=None):
        if not options:
            options = {}
        if name not in self.__symbols:
            self.__symbols[name] = data
        return self.__symbols[name]


    def create_mesh(self, symbol, **kargs):

        if isinstance(symbol, basestring):
            if symbol not in self.__symbols:
                raise "[Warning MeshFactory] symbol '%s' does not exist" % symbol

        kargs = self.__symbols[symbol]

        # if not "layer" in kargs:
        #  raise KeyError("[Error MeshFactory] You should provide a layer name for this mesh")

        #kargs["group"] = self.__group_manager.add_group(kargs["layer"])
        #del kargs["layer"]

        if not "batch" in kargs or kargs["batch"] is None:
            current_batch = self.__scene.root.find("batch_manager").current_batch
            kargs["batch"] = current_batch

        #vertex_count, mode, batch, group, *data
        new_mesh = Mesh(**kargs)

        return new_mesh











