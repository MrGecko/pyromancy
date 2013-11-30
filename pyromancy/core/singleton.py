

class Singleton: 
    """Singleton
    
       a simple Singleton class decorator
    """
    # on @ decoration
    def __init__(self, aClass):         
        self.__aClass = aClass
        self.__instance = None
        
    # on instance creation
    def __call__(self, *args, **kargs):
        if self.__instance is None:
            self.__instance = self.__aClass(*args, **kargs)

        return self.__instance
