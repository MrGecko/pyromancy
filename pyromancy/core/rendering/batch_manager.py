import pyglet
from pyromancy.core.actor.Actor import Actor
#from pyromancy.core.actor.ActorGroup import ActorGroup

__author__ = 'Gecko'


class BatchManager(Actor):

    def __init__(self, name):
        super(BatchManager, self).__init__(name)
        self.__batch = {}
        self.__current_batch_name = None

    @property
    def batches(self):
        return self.__batch.values()

    @property
    def current_batch(self):
        return self.__batch[self.__current_batch_name]

    @property
    def current_batch_name(self):
        if self.__current_batch_name is None:
            raise KeyError("[batch manager] you need to add then select a batch")
        return self.__current_batch_name

    def add_batch(self, name):
        if name not in self.__batch.keys():
            self.__batch[name] = pyglet.graphics.Batch()
            return True
        else:
            return False

    def select_batch(self, name):
        if name in self.__batch.keys():
            self.__current_batch_name = name
            return True
        else:
            print "[batch manager] graphic batch '%s' does not exist" % name
            return False

    def get_batch(self, name):
        if name in self.__batch.keys():
            return self.__batch[name]
        else:
            print "[batch manager] graphic batch '%s' does not exist" % name
            return self.__batch["main"]

    def pprint(self):
        print "[rendering] batches:"
        for k in self.__batch.keys():
            print k
