__author__ = 'Gecko'


class Event(dict):
    def __init__(self, sender=None, msg=None, kargs=None):
        super(Event, self).__init__()
        self["sender"] = sender
        self["message"] = msg
        if kargs is None:
            kargs = {}
        self["arguments"] = kargs
        self["nb_token"] = 0

    @property
    def sender(self):
        return self["sender"]

    @sender.setter
    def sender(self, v):
        self["sender"] = v

    @property
    def message(self):
        return self["message"]

    @message.setter
    def message(self, v):
        self["message"] = v

    @property
    def arguments(self):
        return self["arguments"]

    @arguments.setter
    def arguments(self, v):
        self["arguments"] = v

    @property
    def nb_token(self):
        return self["nb_token"]

    @nb_token.setter
    def nb_token(self, v):
        self["nb_token"] = v