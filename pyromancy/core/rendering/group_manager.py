import pyglet
from pyromancy.core.actor.Actor import Actor

__author__ = 'Gecko'


class GroupManager(Actor):

    #rendering layers
    __group = {}
    
    def __init__(self, name):
        super(GroupManager, self).__init__(name)

    @classmethod
    def get_group(cls, name):
        try:
            return cls.__group[name]
        except KeyError:
            print "[group manager] group '%s' does not exist" % name
            return None

    @classmethod
    def add_group(cls, name, explicit_order=None):
        if name not in cls.__group:
            if explicit_order is None:
                num = len(cls.__group.keys())
            else:
                _n = cls.get_group_name(explicit_order)
                if _n is not None:
                    raise IndexError("[group manager] cannot create a group with the index %i: it already exists (%s)"
                                     % (explicit_order, _n))
                else:
                    num = explicit_order

            cls.__group[name] = pyglet.graphics.OrderedGroup(num)
        return cls.__group[name]

    @classmethod
    def pprint(cls):
        print "[rendering] ordered groups:"
        for k, v in sorted(cls.__group.iteritems(), lambda a, b: cmp(a[1].order, b[1].order)):
            print "%s: %s" % (k, v)

    @classmethod
    def get_group_order(cls, name):
        try:
            return cls.__group[name].order
        except KeyError:
            raise KeyError("[group manager] group %s does not exist" % name)

    @classmethod
    def get_group_name(cls, order):
        order = int(order)
        for k, v in cls.__group.iteritems():
            if v.order == order:
                return k
        return None


