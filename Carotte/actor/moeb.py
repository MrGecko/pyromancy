__author__ = 'MrGecko'

from pyromancy.core.actor.ActorGroup import ActorGroup


class Moeb(ActorGroup):
    def __init__(self, name, children):
        super(Moeb, self).__init__(name, children)


        # TODO: make a VelocityActor

