import time


class State(object):
    def __init__(self):
        self._lock = False
        self._pause = False
    
    def clean_up(self):
        pass
        
    def pause(self):
        self._pause = True
        
    def resume(self):
        self._pause = False
    
    def update(self, dt):
        pass
    
    @property
    def paused(self):
        return self._pause
    @property
    def locked(self):
        return self._lock

    def lock(self):
        self._lock = True

    def unlock(self):
        self._lock = False
        
    def __str__(self, *args, **kargs):
        return self.__class__.__name__



class TimeLockedState(State):
    def __init__(self, lock):
        super(TimeLockedState, self).__init__()
        self._waited = 0

        self._lock = lock != 0

        self._time_to_wait = lock
        self._start_time = time.time()

    @property
    def waited(self):
        return self._waited

    def update(self, dt):
        self._waited += dt
        # Is it time to unlock ?
        if self._waited > self._time_to_wait:
            self._lock = False
