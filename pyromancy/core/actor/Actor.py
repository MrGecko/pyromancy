__author__ = 'Gecko'
from pyromancy.core.event.event_pool import EventPool


class Actor(object):

    ACTOR_ADDED = "ACTOR_ADDED"
    ACTOR_REMOVED = "ACTOR_REMOVED"
    ACTOR_ENABLED = "ACTOR_ENABLED"
    ACTOR_DISABLED = "ACTOR_DISABLED"

    def __init__(self, name):
        #super(Actor, self).__init__()
        self.__name = name
        self.__parent = None
        self._callbacks = {
            Actor.ACTOR_ADDED: self.__object_added,
            Actor.ACTOR_REMOVED: self.__object_removed,
            Actor.ACTOR_ENABLED: self.__object_enabled,
            Actor.ACTOR_DISABLED: self.__object_disabled,
        }

    def register(self, event_id, method):
        self._callbacks.update({event_id: method})

    def unregister(self, event_id):
        self._callbacks.pop(event_id)

    @property
    def name(self):
        return self.__name

    @property
    def parent(self):
        return self.__parent

    @parent.setter
    def parent(self, p):
        self.__parent = p

    def has_child(self, c_name):
        return False

    def is_child_active(self, c_name):
        return False

    def get_child(self, c_name):
        return None

    def get_active_children(self):
        return []

    def add_child(self, child):
        return False

    def add_children(self, children):
        pass

    def remove_child(self, c_name):
        return False

    def enable_child(self, c_name):
        return False

    def disable_child(self, c_name):
        return False

    def fire(self, event):
        #print self.name, " fired %s!" % event.message
        if event.message in self._callbacks:
            return self._callbacks[event.message](event.sender, event.arguments)
        else:
            return True

    def notify(self, event):
        #process the event at the actor level
        self.fire(event)
        if event.nb_token <= 0:
            EventPool.free_event(event)

    def send(self, message, arguments=None):
        if arguments is None:
            arguments = {}
        self.notify(EventPool.get_event(self, message, arguments))

    def update(self, dt):
        pass

    def find(self, name):
        if self.name == name:
            return self
        else:
            return None

    def __del__(self):
        self._callbacks = {}

    def __object_added(self, sender, kargs):
        pass

    def __object_removed(self, sender, kargs):
        pass

    def __object_enabled(self, sender, kargs):
        pass

    def __object_disabled(self, sender, kargs):
        pass





