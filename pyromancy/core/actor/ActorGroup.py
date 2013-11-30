from pyromancy.core.actor.Actor import Actor

__author__ = 'Gecko'
from pyromancy.core.event.event_pool import EventPool


class ActorGroup(Actor):

    def __init__(self, name, children=None):
        super(ActorGroup, self).__init__(name)
        self.__actives = dict()
        self.__inactives = dict()
        if children is not None:
            self.add_children(children)

    def has_child(self, c_name):
        return c_name in self.__actives or c_name in self.__inactives

    def is_child_active(self, c_name):
        return c_name in self.__actives

    def get_child(self, c_name):
        if self.is_child_active(c_name):
            return self.__actives[c_name]
        else:
            return None

    def get_active_children(self):
        return self.__actives.values()

    def add_child(self, child):
        c_name = child.name
        if c_name in self.__actives or c_name in self.__inactives:
            self.remove_child(c_name)
        self.__actives[c_name] = child
        child.parent = self
        child.send(ActorGroup.ACTOR_ADDED)
        return True

    def add_children(self, children):
        for child in children:
            self.add_child(child)

    def remove_child(self, c_name):
        if c_name in self.__actives:
            self.__actives[c_name].notify(EventPool.get_event(self, ActorGroup.ACTOR_REMOVED, {}))
            self.__actives[c_name].__del__()
            self.__actives[c_name] = None
            del self.__actives[c_name]
            return True
        elif c_name in self.__inactives:
            self.__inactives[c_name].notify(EventPool.get_event(self, ActorGroup.ACTOR_REMOVED, {}))
            self.__inactives[c_name].__del__()
            self.__inactives[c_name] = None
            del self.__inactives[c_name]
            return True
        else:
            return False

    def enable_child(self, c_name):
        if c_name in self.__inactives:
            self.__actives[c_name] = self.__inactives[c_name]
            self.__actives[c_name].notify(EventPool.get_event(self, ActorGroup.ACTOR_ENABLED, {}))
            self.__inactives.pop(c_name)
            return True
        else:
            return False

    def disable_child(self, c_name):
        if c_name in self.__actives:
            self.__actives[c_name].disable()
            self.__inactives[c_name].notify(EventPool.get_event(self, ActorGroup.ACTOR_DISABLED, {}))
            self.__actives.pop(c_name)
            return True
        else:
            return False

    def fire(self, event):
        if event.message in self._callbacks:
            return self._callbacks[event.message](event.sender, event.arguments)
        else:
            return True

    def notify(self, event):
        #give tokens to the actor to keep the event alive
        #while notifying its children
        event.nb_token += 1
        #process the event at the actor level
        if self.fire(event):
            #notify the children
            for child in self.__actives.values():
                child.notify(event)
        #get the tokens back and try to free the event
        #if it's not used anymore
        event.nb_token -= 1
        if event.nb_token <= 0:
            EventPool.free_event(event)

    def send(self, message, arguments=None):
        if arguments is None:
            arguments = {}
        self.notify(EventPool.get_event(self, message, arguments))

    def update(self, dt):
        super(ActorGroup, self).update(dt)
        for child in self.__actives.values():
            child.update(dt)

    def find(self, name):
        if self.name == name:
            return self
        else:
            found = None
            for child in self.__actives.values():
                found = child.find(name)
                if found is not None:
                    break

            return found

    def __del__(self):
        for k, v in self.__actives.iteritems():
            v.__del__()
        for k, v in self.__inactives.iteritems():
            v.__del__()
        self.__actives = dict()
        self.__inactives = dict()
        self._callbacks = {}




