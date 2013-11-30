#from pyromancy.core.singleton import Singleton

__author__ = 'Gecko'

from pyromancy.core.event.event import Event


class EventPool(object):

    __POOL_SIZE = 50
    __POOL = []

    I = 0

    def __init__(self):
        self.__expend()

    @classmethod
    def __expend(cls):
        cls.__POOL.extend([Event for i in range(cls.__POOL_SIZE)])
        cls.__POOL_SIZE *= 2

    @classmethod
    def get_event(cls, sender, message, kargs):
        if len(cls.__POOL) <= 0.25*cls.__POOL_SIZE:
            cls.__expend()
        new_event = cls.__POOL.pop()
        new_event.sender = sender
        new_event.message = message
        new_event.nb_token = 0
        new_event.arguments = kargs
        return new_event

    @classmethod
    def free_event(cls, e):
        e.sender = None
        e.message = "NULL"
        e.arguments = {}
        e.nb_token = 0
        #print "event is freed"
        cls.__POOL.append(e)

    @classmethod
    def get_usage(cls):
        return len(cls.__POOL)
