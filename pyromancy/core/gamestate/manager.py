


class StateManager(object):
    def __init__(self):
        self._states = []

    @property
    def states(self):
        return self._states
    
    @property
    def empty(self):
        return not self._states
    
    def update(self, *args, **kargs):
        if not self.empty:
            if not self.current.paused:
                self.current.update(*args, **kargs)
            
    @property
    def current(self):
        if self.empty:
            return None
        else:
            return self._states[-1]
               
    def push(self, state, *args, **kargs):
        if not self.empty:
            if not self.current.locked:
                self.current.pause()
                #the top item is not locked, push is allowed
                new_state = state(*args, **kargs)
                self._states.append(new_state)
            else:
                return False
        else:
            #the stack is empty: push is allowed
            self._states.append(state(*args, **kargs))        
        return True
    
    def pop(self):
        if not self.empty:
            #the top item is not locked, removing it is allowed
            if not self.current.locked:
                self.current.clean_up()
                self._states.pop()
                if not self.empty:
                    self.current.resume()
                return True
            else:
                #print "cant pop :", self.states[-1], "is locked"
                return False
        else:
            return True
    
    def set(self, state, *args, **kargs):
        if self.pop():
            return self.push(state, *args, **kargs)
        else:
            return False
            
    def pause(self, *args, **kargs):
        if not self.empty:
            self.current.pause(*args, **kargs)
        
    def resume(self, *args, **kargs):
        if not self.empty:
            self.current.resume(*args, **kargs)
    
    def __str__(self, *args, **kargs):
        return "->".join([s.name for s in self._states])
